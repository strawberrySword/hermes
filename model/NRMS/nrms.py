import torch
import math
import torch.nn as nn
import torch.nn.functional as F

from modules import NewsEncoder, UserEncoder


class NRMS(nn.Module):
    """
    Complete NRMS model that includes both NewsEncoder and UserEncoder internally.
    Forward pass:
      1) Flatten clicked-news (B, N, L) → (B*N, L), run through NewsEncoder → (B*N, L, E)
      2) Pool over L to get (B*N, E), reshape → (B, N, E) for user history
      3) Flatten candidate-news (B, K, L) → (B*K, L), run through NewsEncoder → (B*K, L, E)
      4) Pool over L to get (B*K, E), reshape → (B, K, E) for candidates
      5) Build click_slot_mask (B, N) from clicked_token_mask (B, N, L)
      6) Pass clicked-news embeddings + click_slot_mask to UserEncoder → (B, E)
      7) Dot-product between user_emb (B, E) and candidate_emb (B, K, E) → scores (B, K)
    """

    def __init__(
        self,
        vocab_size: int,
        d_embed: int = 768,
        n_heads: int = 12,
        d_mlp: int = 3072,
        news_layers: int = 1,
        user_layers: int = 1,
        dropout: float = 0.1,
        pad_max_len: int = 5000,
    ):
        """
        Args:
          vocab_size: size of token vocabulary
          d_embed:    embedding dimension for words and news/user vectors
          n_heads:    number of attention heads
          d_mlp:      hidden dimension in each postnet & Transformer FFN
          news_layers: number of Transformer layers in NewsEncoder
          user_layers: number of Transformer layers in UserEncoder
          dropout:    dropout probability
          pad_max_len: maximum sequence length for positional encoding
        """
        super().__init__()
        self.d_embed = d_embed

        
        self.news_encoder = NewsEncoder(
            vocab_size=vocab_size,
            d_embed=d_embed,
            n_heads=n_heads,
            d_mlp=d_mlp,
            n_layers=news_layers,
            dropout=dropout,
            pad_max_len=pad_max_len,
        )

        self.user_encoder = UserEncoder(
            d_embed=d_embed,
            n_heads=n_heads,
            d_mlp=d_mlp,
            n_layers=user_layers,
            dropout=dropout,
        )


    def forward(
        self,
        clicked_token_ids: torch.LongTensor,
        clicked_token_mask: torch.BoolTensor,
        all_doc_token_ids: torch.LongTensor,
        all_doc_token_mask: torch.BoolTensor,
    ) -> torch.Tensor:
        """
        clicked_token_ids:  (B, N, L)
        clicked_token_mask: (B, N, L)
        all_doc_token_ids:  (D, L)
        all_doc_token_mask: (D, L)

        Returns:
          scores: (B, D)
        """
        B, N, L = clicked_token_ids.shape
        D, L_check = all_doc_token_ids.shape

        
        # Embed all documents
        all_doc_emb = self.news_encoder(all_doc_token_ids, all_doc_token_mask) # (D, d_embed)
        
        
        # Embed articles of click history
        clicked_flat_ids = clicked_token_ids.view(B * N, L)      # (B*N, L)
        clicked_flat_mask = clicked_token_mask.view(B * N, L)    # (B*N, L)

        clicked_emb_flat = self.news_encoder(clicked_flat_ids, clicked_flat_mask)
        clicked_news_emb = clicked_emb_flat.view(B, N, self.d_embed)      # (B, N, d_embed)


        # Embed article embeddings (lmfao attention again)
        clicked_slot_mask = clicked_token_mask.all(dim=2)  # (B, N)

        user_emb = self.user_encoder(clicked_news_emb, clicked_slot_mask)  # (B, d_embed)


        # We take scores as softmax(dot(usr_embed, candidates))
        logits = torch.matmul(user_emb, all_doc_emb.t())  # (B, D)

        scores = F.softmax(logits, dim=1)  # (B, D), softmax over all documents

        return scores