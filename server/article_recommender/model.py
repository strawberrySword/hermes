from article_recommender.nrms import NRMS

from typing import List
import torch
from transformers import BertTokenizer

# Constants — make sure these match your training settings
MAX_HISTORY = 50
MAX_TITLE_LEN = 100
PAD_ID = 0  # [PAD] token for BERT

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")


def tokenize_titles(titles: List[str], max_len: int = MAX_TITLE_LEN) -> torch.Tensor:
    """
    Tokenizes and pads a list of article titles using BERT tokenizer.
    Returns: token_ids (N, max_len), padding_mask (N, max_len)
    """
    encodings = tokenizer(
        titles,
        padding="max_length",
        truncation=True,
        max_length=max_len,
        return_tensors="pt",
        return_attention_mask=True,
        add_special_tokens=False  # NRMS does not expect [CLS] or [SEP]
    )
    token_ids = encodings["input_ids"]       # (N, max_len)
    padding_mask = ~encodings["attention_mask"].bool()  # True = pad
    return token_ids, padding_mask


def recommend_topk_from_titles(
    model: torch.nn.Module,
    history_titles: List[str],
    candidate_titles: List[str],
    topk: int = 5,
    device: torch.device = torch.device("cpu")
):
    """
    Recommends top-k titles from a list of candidate article titles,
    given a user's clicked history (also as titles).

    Args:
        model:            Trained NRMS model.
        history_titles:   List of clicked article titles (strings).
        candidate_titles: List of candidate article titles (strings).
        topk:             Number of top articles to return.
        device:           Torch device to run the model on.

    Returns:
        List of top-k recommended article titles (strings).
    """
    model.to(device)
    model.eval()

    # 1. Tokenize history and candidates
    hist_tokens, hist_mask = tokenize_titles(
        history_titles, max_len=MAX_TITLE_LEN)
    cand_tokens, cand_mask = tokenize_titles(
        candidate_titles, max_len=MAX_TITLE_LEN)

    # 2. Pad history to MAX_HISTORY size
    num_hist = len(history_titles)
    if num_hist < MAX_HISTORY:
        pad_len = MAX_HISTORY - num_hist
        pad_tokens = torch.full((pad_len, MAX_TITLE_LEN),
                                PAD_ID, dtype=torch.long)
        pad_mask = torch.ones((pad_len, MAX_TITLE_LEN), dtype=torch.bool)
        hist_tokens = torch.cat([pad_tokens, hist_tokens], dim=0)
        hist_mask = torch.cat([pad_mask, hist_mask], dim=0)
    elif num_hist > MAX_HISTORY:
        hist_tokens = hist_tokens[-MAX_HISTORY:]
        hist_mask = hist_mask[-MAX_HISTORY:]

    # 3. Add batch dimension
    clicked_ids = hist_tokens.unsqueeze(0).to(
        device)    # (1, MAX_HISTORY, MAX_TITLE_LEN)
    clicked_mask = hist_mask.unsqueeze(0).to(
        device)     # (1, MAX_HISTORY, MAX_TITLE_LEN)
    cand_ids = cand_tokens.unsqueeze(0).to(
        device)       # (1, K, MAX_TITLE_LEN)
    cand_mask = cand_mask.unsqueeze(0).to(
        device)        # (1, K, MAX_TITLE_LEN)

    # 4. Forward pass
    with torch.no_grad():
        logits = model(clicked_ids, clicked_mask,
                       cand_ids, cand_mask)  # (1, K)

    scores = logits.squeeze(0)  # (K,)
    topk_vals, topk_idxs = torch.topk(scores, k=min(topk, scores.size(0)))

    return scores, topk_idxs.tolist()


CHECK_PATH = './article_recommender/checkpoints/checkpoint_epoch5.pt'


def load_model():
    model = NRMS(
        vocab_size=tokenizer.vocab_size,
        d_embed_word=128,
        d_embed_news=256,
        n_heads_news=8,
        n_heads_user=8,
        d_mlp_news=512,
        d_mlp_user=512,
        news_layers=1,
        user_layers=1,
        dropout=0.1,
        pad_max_len=MAX_TITLE_LEN,
    )

    model.load_state_dict(torch.load(
        CHECK_PATH, map_location="cpu", weights_only=True))
    return model
