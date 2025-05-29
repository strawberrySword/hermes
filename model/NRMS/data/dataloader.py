import os
from typing import List, Dict
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizerFast

# --------------------------------------------------
# 5) MindDataset and collate_fn (with mask fix)
# --------------------------------------------------
class MindDataset(Dataset):
    """
    wraps the tokenized samples from load_behaviors() for PyTorch DataLoader.
    Each item returns:
      clicked_token_ids:   (N, L)   LongTensor
      clicked_token_mask:  (N, L)   BoolTensor
      candidate_token_ids: (Ki, L)  LongTensor
      candidate_token_mask:(Ki, L)  BoolTensor
      label:               scalar   int
    """
    def __init__(
        self,
        data: List[Dict],
        max_clicks: int = 50,
        max_title_len: int = 100,
        pad_id: int = 0  # usually 0, but can be set to tokenizer.pad_token_id
    ):
        self.data = data
        self.max_clicks = max_clicks
        self.max_title_len = max_title_len
        self.pad_id = pad_id

    def __len__(self):
        return len(self.data)

    def pad_and_mask(self, titles: List[List[int]]):
        """
        titles: List of token-ID lists, each length ≤ max_title_len.
        We create a (num_titles, max_title_len) tensor of token IDs,
        then build mask = (padded_ids != PAD_ID). That way, any PAD_ID
        remains False in mask.

        Returns:
          padded_ids: LongTensor (num_titles, max_title_len)
          mask:       BoolTensor (num_titles, max_title_len)
        """
        num_titles = len(titles)
        # 1) Fill with PAD_ID
        padded = torch.full(
            (num_titles, self.max_title_len),
            self.pad_id,
            dtype=torch.long
        )

        # 2) Copy real token lists into padded
        for i, token_list in enumerate(titles):
            length = min(len(token_list), self.max_title_len)
            if length > 0:
                padded[i, :length] = torch.tensor(token_list[:length], dtype=torch.long)

        
        mask = (padded == self.pad_id)
        return padded, mask

    def __getitem__(self, idx):
        sample = self.data[idx]

        # a) Padded/pool clicked history (always length = max_clicks)
        clicked_titles = sample["clicked_titles"][:self.max_clicks]
        clicked_ids, clicked_mask = self.pad_and_mask(clicked_titles)
        # clicked_ids:   shape (max_clicks, max_title_len)
        # clicked_mask:  shape (max_clicks, max_title_len)

        # b) Padded/pool candidates (Ki may vary)
        candidate_titles = sample["candidate_titles"]
        cand_ids, cand_mask = self.pad_and_mask(candidate_titles)
        # cand_ids:   shape (Ki, max_title_len)
        # cand_mask:  shape (Ki, max_title_len)

        label = sample["label"]

        return {
            "clicked_token_ids":   clicked_ids,   # (max_clicks, max_title_len)
            "clicked_token_mask":  clicked_mask,  # (max_clicks, max_title_len)
            "candidate_token_ids": cand_ids,      # (Ki, max_title_len)
            "candidate_token_mask": cand_mask,    # (Ki, max_title_len)
            "label":               label          # int
        }

def mind_collate_fn(batch):
    """
    Pads candidate lists (which may vary Ki per sample) up to K_max,
    then stacks everything into fixed‐shape tensors.

    Returns:
      clicked_ids:   (B, max_clicks, max_title_len)
      clicked_mask:  (B, max_clicks, max_title_len)
      cand_ids:      (B, K_max, max_title_len)
      cand_mask:     (B, K_max, max_title_len)
      labels:        (B,)  long
    """
    B = len(batch)
    N, L = batch[0]["clicked_token_ids"].shape  # = (max_clicks, max_title_len)

    # Find largest Ki in this batch
    Ks = [x["candidate_token_ids"].shape[0] for x in batch]
    K_max = max(Ks)

    # 1) Stack clicked IDs & masks (these are all shape (N, L))
    clicked_ids = torch.stack([x["clicked_token_ids"] for x in batch], dim=0)   # (B, N, L)
    clicked_mask = torch.stack([x["clicked_token_mask"] for x in batch], dim=0) # (B, N, L)

    # 2) Prepare padded candidate_ids and candidate_mask
    PAD_ID = 0
    cand_ids  = torch.full((B, K_max, L), PAD_ID, dtype=torch.long)  # (B, K_max, L)
    cand_mask = torch.zeros((B, K_max, L), dtype=torch.bool)        # (B, K_max, L)
    labels    = torch.zeros(B, dtype=torch.long)                    # (B,)

    for i, x in enumerate(batch):
        Ki = x["candidate_token_ids"].shape[0]
        cand_ids[i, :Ki, :]  = x["candidate_token_ids"]
        cand_mask[i, :Ki, :] = x["candidate_token_mask"]
        labels[i] = x["label"]

    return clicked_ids, clicked_mask, cand_ids, cand_mask, labels