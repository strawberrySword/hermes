import os
from typing import List, Dict
from xml.etree.ElementInclude import include
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizerFast
from .dataloader import MindDataset, mind_collate_fn


PAD_ID = 0

def load_and_tokenize_news(
        news_path: str,
        tokenizer: BertTokenizerFast,
        max_len: int,
        include_topics: bool = False
    ) -> Dict[str, List[int]]:
    """
    Parses MIND’s news.tsv to build news_dict: news_id → [WordPiece IDs].
    Truncate or keep at most max_len tokens. If a title is empty or missing,
    store [PAD_ID] so it becomes a single‐token “[PAD]”.
    """
    news_dict = {}
    with open(news_path, encoding="utf-8") as f:
        for line in f:
            cols = line.strip().split('\t')
            if len(cols) < 4:
                continue
            news_id = cols[0]
            title_text = cols[3]

            encoding = tokenizer(
                title_text,
                add_special_tokens=True,
                truncation=True,
                max_length=max_len,
                padding=False,
                return_attention_mask=False
            )
            input_ids = encoding["input_ids"]
            if len(input_ids) == 0:
                # If tokenizer for some reason returns [], we at least store one PAD
                input_ids = [PAD_ID]
            news_dict[news_id] = input_ids

            if include_topics:
                topic_text = cols[1]

                topic_encoding = tokenizer(
                    topic_text,
                    add_special_tokens=True,
                    truncation=True,
                    max_length=max_len,
                    padding=False,
                    return_attention_mask=False
                )
                topic_ids = topic_encoding["input_ids"]
                if len(topic_ids) == 0:
                    # If tokenizer for some reason returns [], we at least store one PAD
                    topic_ids = [PAD_ID]
                news_dict[f'{news_id}_topic'] = topic_ids


    return news_dict

# --------------------------------------------------
# 3) Function: load_behaviors(...)  ← fixed here
# --------------------------------------------------
def load_behaviors(
        behaviors_path: str,
        news_dict: Dict[str, List[int]],
        max_history: int,
        include_topics: bool = False
    ) -> List[Dict]:
    """
    Parses MIND’s behaviors.tsv into a list of samples.
    For missing history slots, we now append an empty list ([])
    so that pad_and_mask() can treat it as fully padded.
    """
    samples: List[Dict] = []
    with open(behaviors_path, encoding="utf-8") as f:
        for line in f:
            cols = line.strip().split('\t')
            if len(cols) < 5:
                continue

            history_field     = cols[3]  # e.g. "N123 N456 N789"
            candidates_field  = cols[4]  # e.g. "N321-0 N654-1 N987-0"
            history_nids      = history_field.split()
            candidate_items   = candidates_field.split()

            # 1) Build clicked_titles (keep last max_history IDs, pad front with [])
            history_nids = history_nids[-max_history:]
            clicked_titles: List[List[int]] = []
            for nid in history_nids:
                if nid in news_dict:
                    clicked_titles.append(news_dict[nid])
                else:
                    # If news id is missing, treat as single PAD to avoid crash
                    clicked_titles.append([PAD_ID])

            # Pad at front with empty lists for any missing slots
            pad_count = max_history - len(clicked_titles)
            if pad_count > 0:
                clicked_titles = [[]] * pad_count + clicked_titles
                # Now each of those first pad_count entries is [],
                # and pad_and_mask() will mark them as fully False in mask.

            # 2) Build candidate_titles and find the clicked index
            candidate_titles: List[List[int]] = []
            candidate_topics: List[List[int]] = []
            label_index = None
            for idx, item in enumerate(candidate_items):
                nid, lbl_str = item.split('-')
                lbl = int(lbl_str)
                if nid in news_dict:
                    candidate_titles.append(news_dict[nid])
                    if include_topics and f'{nid}_topic' in news_dict:
                        candidate_topics.append(news_dict[f'{nid}_topic'])
                else:
                    candidate_titles.append([PAD_ID])
                    if include_topics:
                        candidate_topics.append([PAD_ID])

                if lbl == 1 and label_index is None:
                    label_index = idx

            # If no clicked candidate, skip this line
            if label_index is None:
                continue

            if include_topics:
                samples.append({
                    "clicked_titles":   clicked_titles,       # List[List[int]] of length exactly max_history
                    "candidate_titles": candidate_titles,     # List[List[int]] (length Ki)
                    "candidate_topics": candidate_topics,   # List[List[int]] (length Ki) if include_topics=True
                    "label":            label_index           # int in [0, Ki-1]
                })
            else:
                samples.append({
                    "clicked_titles":   clicked_titles,       # List[List[int]] of length exactly max_history
                    "candidate_titles": candidate_titles,     # List[List[int]] (length Ki)
                    "label":            label_index           # int in [0, Ki-1]
                })

    return samples