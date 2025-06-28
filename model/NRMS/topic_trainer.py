# %%
# setup
import os
import wandb
import torch
import torch.nn as nn
from nrms import NRMS
from typing import List, Dict
from torch.optim.adamw import AdamW
from tqdm import tqdm
import math
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizerFast, get_linear_schedule_with_warmup
from data import load_and_tokenize_news, load_behaviors, MindDataset, mind_collate_fn

# %% [markdown]
# # Setup dataloader

# %%
BASE_DATA_DIR = './data/MIND_'


MAX_TITLE_LEN = 100   # each headline → exactly MAX_TITLE_LEN tokens (truncated/padded)
MAX_HISTORY  = 50     # each user’s clicked history → exactly MAX_HISTORY articles
BACTH_SIZE = 6


tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
PAD_ID = tokenizer.pad_token_id

train_news_dict = load_and_tokenize_news(BASE_DATA_DIR+'train/news.tsv', tokenizer, MAX_TITLE_LEN, include_topics=True)
train_samples   = load_behaviors(BASE_DATA_DIR+'train/behaviors.tsv', train_news_dict, MAX_HISTORY, include_topics=True)

val_news_dict = load_and_tokenize_news(BASE_DATA_DIR+'val/news.tsv', tokenizer, MAX_TITLE_LEN, include_topics=True)
val_samples   = load_behaviors(BASE_DATA_DIR+'val/behaviors.tsv', val_news_dict, MAX_HISTORY, include_topics=True)


train_dataset = MindDataset(train_samples, include_topics=True)
val_dataset = MindDataset(val_samples, include_topics=True)

train_dl = DataLoader(
    train_dataset,
    batch_size=BACTH_SIZE,
    shuffle=True,
    collate_fn= lambda x: mind_collate_fn(x, include_topics=True)
)

valid_dl = DataLoader(
    val_dataset,
    batch_size=BACTH_SIZE,
    shuffle=True,
    collate_fn= lambda x: mind_collate_fn(x, include_topics=True)
)

# %% [markdown]
# # Define model

# %%
model = NRMS(
    vocab_size=tokenizer.vocab_size,
    d_embed_word = 128,
    d_embed_news = 256,
    n_heads_news = 8,
    n_heads_user = 8,
    d_mlp_news = 512,
    d_mlp_user = 512,
    news_layers = 1,
    user_layers = 1,
    dropout = 0.1,
    pad_max_len = MAX_TITLE_LEN,
)

# %%
f'{sum(p.numel() for p in model.parameters()): ,}'

# %% [markdown]
# # Train loop

# %%
def train(
    model,
    train_dataloader,
    val_dataloader,
    epochs: int = 2,
    lr: float = 1e-4,
    device: str = "cuda",
    log_interval: int = 100,
    checkpoint_interval: int = 10000,
    project_name: str = "NRMS",
    save_path: str = "./checkpoints_topic/",
    smoothing_alpha: float = 0.8,  # EWMA smoothing factor
):
    """
    Trains `model` using train_dataloader, evaluates on val_dataloader each epoch,
    logs EWMA-smoothed loss + MRR + learning rate to W&B, and finally saves model parameters.
    """
    model.to(device)

    # Initialize W&B
    wandb.init(
        project=project_name,
        config={
            "epochs": epochs,
            "learning_rate": lr,
            "optimizer": "AdamW",
            "loss_fn": "CrossEntropyLoss",
            "metric": "MRR",
            "smoothing_alpha": smoothing_alpha,
            "target_labels": "Topics",
            
            "model_def": 	"""
							model = NRMS(
								vocab_size=tokenizer.vocab_size,
								d_embed_word = 128,
								d_embed_news = 256,
								n_heads_news = 8,
								n_heads_user = 8,
								d_mlp_news = 512,
								d_mlp_user = 512,
								news_layers = 1,
								user_layers = 1,
								dropout = 0.1,
								pad_max_len = MAX_TITLE_LEN,
							)"""                                  
        },
    )
    # Only log weight histograms (no gradients) to cut down on storage
    wandb.watch(model, log="parameters", log_freq=500)

    criterion = nn.CrossEntropyLoss(reduction='mean')
    optimizer = AdamW(
        model.parameters(),
        lr=lr,
        betas=(0.9, 0.999),
        eps=1e-8,
        weight_decay=1e-4
    )

    # === Scheduler Setup ===
    # total_steps = epochs * number_of_batches_per_epoch
    total_steps = epochs * len(train_dataloader)
    warmup_steps = int(0.1 * total_steps)  # 10% warmup

    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_steps
    )
    # =======================

    step = 0  # global batch index

    # Initialize EWMA trackers
    ewma_loss = None
    ewma_mrr = None

    for epoch in range(1, epochs + 1):
        ##### Training Phase #####
        model.train()
        total_train_loss = 0.0
        total_train_mrr = 0.0
        total_train_samples = 0

        for clicked_ids,clicked_mask, _, _, cand_topic_ids, cand_topic_mask, labels in tqdm(
            train_dataloader, desc=f"Epoch {epoch} [Train]"
        ):
            clicked_ids = clicked_ids.to(device)
            clicked_mask = clicked_mask.to(device)
            cand_ids = cand_topic_ids.to(device)
            cand_mask = cand_topic_mask.to(device)
            labels = labels.to(device)  # (B,)

            optimizer.zero_grad()

            # Forward pass → logits of shape (B, K)
            scores: torch.Tensor = model(
                clicked_ids, ~clicked_mask, cand_ids, cand_mask
            )  # (B, K)
            loss = criterion(scores, labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            scheduler.step()  # <-- step the scheduler immediately after optimizer

            # Compute batch MRR
            with torch.no_grad():
                batch_size = labels.size(0)
                batch_mrr = 0.0
                for i in range(batch_size):
                    true_idx = labels[i].item()
                    sorted_indices = scores[i].argsort(descending=True)
                    rank = (sorted_indices == true_idx).nonzero(as_tuple=False).item() + 1
                    batch_mrr += 1.0 / rank
                batch_mrr /= batch_size

            # Update EWMA for loss
            if ewma_loss is None:
                ewma_loss = loss.item()
            else:
                ewma_loss = smoothing_alpha * ewma_loss + (1.0 - smoothing_alpha) * loss.item()

            # Update EWMA for MRR
            if ewma_mrr is None:
                ewma_mrr = batch_mrr
            else:
                ewma_mrr = smoothing_alpha * ewma_mrr + (1.0 - smoothing_alpha) * batch_mrr

            # Accumulate totals (for printing at end of epoch)
            total_train_loss += loss.item() * batch_size
            total_train_mrr += batch_mrr * batch_size
            total_train_samples += batch_size

            # Log smoothed scalars (loss, MRR, lr) to W&B every log_interval steps
            if step % log_interval == 0:
                current_lr = scheduler.get_last_lr()[0]
                wandb.log(
                    {
                        "train/loss_EWMA": ewma_loss,
                        "train/MRR_EWMA": ewma_mrr,
                        "train/lr": current_lr,
                        "epoch": epoch,
                    },
                    step=step,
                )

            # Save checkpoint periodically
            if step % checkpoint_interval == 0 and step > 0:
                print(f"Saving checkpoint at step {step}...")
                checkpoint_path = save_path + f"checkpoint_epoch{epoch}_step{step}.pt"
                torch.save(model.state_dict(), checkpoint_path)
                print(f"Checkpoint saved to {checkpoint_path}")

            step += 1

        # End of epoch: compute raw averages
        avg_train_loss = total_train_loss / total_train_samples
        avg_train_mrr = total_train_mrr / total_train_samples
        print(
            f"Epoch {epoch:02d} | "
            f"Train Loss: {avg_train_loss:.4f}, Train MRR: {avg_train_mrr:.4f}"
        )

        ##### Validation Phase #####
        model.eval()
        total_val_loss = 0.0
        total_val_mrr = 0.0
        total_val_samples = 0

        with torch.no_grad():
            for clicked_ids,clicked_mask, _, _, cand_topic_ids, cand_topic_mask, labels in tqdm(
                val_dataloader, desc=f"Epoch {epoch} [Val]"
            ):
                clicked_ids = clicked_ids.to(device)
                clicked_mask = clicked_mask.to(device)
                cand_ids = cand_topic_ids.to(device)
                cand_mask = cand_topic_mask.to(device)
                labels = labels.to(device)

                scores = model(clicked_ids, ~clicked_mask, cand_ids, cand_mask)
                loss = criterion(scores, labels)

                batch_size = labels.size(0)
                batch_mrr = 0.0
                for i in range(batch_size):
                    true_idx = labels[i].item()
                    sorted_indices = scores[i].argsort(descending=True)
                    rank = (sorted_indices == true_idx).nonzero(as_tuple=False).item() + 1
                    batch_mrr += 1.0 / rank
                batch_mrr /= batch_size

                total_val_loss += loss.item() * batch_size
                total_val_mrr += batch_mrr * batch_size
                total_val_samples += batch_size

        avg_val_loss = total_val_loss / total_val_samples
        avg_val_mrr = total_val_mrr / total_val_samples
        print(
            f"Epoch {epoch:02d} | "
            f"Val Loss:   {avg_val_loss:.4f}, Val MRR:   {avg_val_mrr:.4f}"
        )

        # Log validation metrics to W&B once per epoch
        wandb.log(
            {
                "val/loss": avg_val_loss,
                "val/MRR": avg_val_mrr,
                "epoch": epoch,
            },
            step=step,
        )

        # Save model checkpoint at end of epoch
        print(f"Saving model parameters for epoch {epoch}...")
        checkpoint_path = save_path + f"checkpoint_epoch{epoch}.pt"
        torch.save(model.state_dict(), checkpoint_path)
        print(f"Checkpoint saved to {checkpoint_path}")

    # Finish the W&B run
    wandb.finish()


# %% [markdown]
# # Run training!

# %%
wandb.login()

# %%
train(
    model,
    train_dl,
    valid_dl,
    epochs=5,
    lr=1e-4,
    device="cuda" if torch.cuda.is_available() else "cpu",
    log_interval=100,
    checkpoint_interval=1000,
    project_name="NRMS",
    save_path="./checkpoints_topic/"
)


