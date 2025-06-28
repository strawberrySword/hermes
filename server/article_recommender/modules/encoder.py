import torch
import math
import torch.nn as nn
import torch.nn.functional as F

from article_recommender.modules import SinePositionalEncoding

class NewsEncoder(nn.Module):
    """
    Input: 
      - token_ids: LongTensor of shape (batch_size, seq_len)
      - mask (optional): BoolTensor of shape (batch_size, seq_len), where True indicates padding.
    Output:
      - news_embedding: FloatTensor of shape (batch_size, news_dim)
    """
    def __init__(
        self,
        vocab_size: int,
        d_embed: int = 768,           # e.g., 200‐d word embeddings
        d_embed_news = None,         # e.g., 200‐d news embeddings
        n_heads: int = 12,
        d_mlp: int = 3072,             # hidden dim in the Transformer FFN
        n_layers: int = 1,
        dropout: float = 0.1,
        pad_max_len: int = 5000       # max length for positional encoding (default is 5000)
    ):
        super().__init__()
        self.d_embed = d_embed
        self.d_embed_news = d_embed_news if d_embed_news is not None else self.d_embed

        self.word_embedding = nn.Embedding(vocab_size, d_embed)

        self.pos_encoding = SinePositionalEncoding(d_model=d_embed, max_len=pad_max_len)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_embed,
            nhead=n_heads,
            dim_feedforward=d_mlp,
            dropout=dropout,
            activation="gelu",
            batch_first=True  # we are using (batch, seq, dim)
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)

        self.postnet = nn.Sequential(
            nn.Linear(d_embed, d_mlp),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_mlp, d_embed_news)
        )


    def forward(self, token_ids: torch.LongTensor, mask: torch.BoolTensor):
        """
        token_ids: (batch_size, seq_len)
        mask: (batch_size, seq_len) where True=padding positions (to be masked out)
        """

        key_padding_mask = mask if mask is not None else None  # (batch_size, seq_len) boolean padding mask
        
        # Embed tokens and apply positional encoding
        x = self.word_embedding(token_ids)
        x = self.pos_encoding(x)

        # Transformer + resid        
        transformer_out = self.transformer_encoder(x, src_key_padding_mask=key_padding_mask) # (batch_size, seq_len, d_embed)
        x = x + transformer_out

        # Sum pool
        inv_mask = (~mask).unsqueeze(-1).float()  # 1 where token is real, 0 where pad
        x = torch.sum(x * inv_mask, dim=1)  # (batch_size, d_embed)
        
        # Postnet
        return self.postnet(x)  # (batch_size, d_embed_out)


class UserEncoder(nn.Module):
    """
    UserEncoder aggregates a sequence of clicked-news embeddings into a single user embedding.
    It applies:
      1) A TransformerEncoder over the sequence of news embeddings (shape: [B, N, E]).
      2) A token-wise MLP + residual + LayerNorm on the Transformer outputs.
      3) Sum-pooling across the N clicked-news slots (masking out padding slots).
      4) A second MLP + residual + LayerNorm on the pooled vector.

    Inputs:
      clicked_news_emb: FloatTensor of shape (B, N, E),
                        where B = batch size (number of users),
                              N = number of clicked-news slots per user,
                              E = embedding dimension of each news.
      click_mask:       BoolTensor of shape (B, N),
                        where True indicates that slot is padding (no actual click).

    Output:
      user_emb: FloatTensor of shape (B, E)
    """

    def __init__(
        self,
        d_embed: int = 768,  # news embedding dimension, will be used as user embedding dimension aswell
        n_heads: int = 12,
        d_mlp: int = 3072,
        n_layers: int = 1,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.d_embed = d_embed
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_embed,
            nhead=n_heads,
            dim_feedforward=d_mlp,
            dropout=dropout,
            activation="gelu",
            batch_first=True,  # expects input shape (batch, seq_len, d_embed)
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)


        self.postnet = nn.Sequential(
            nn.Linear(d_embed, d_mlp),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_mlp, d_embed),
        )

    def forward(self, clicked_news_emb: torch.Tensor, click_mask: torch.BoolTensor):
        """
        clicked_news_emb: FloatTensor of shape (B, N, E)
        click_mask:       BoolTensor of shape (B, N),
                          where True = padding slot to ignore.

        Returns:
          user_emb: FloatTensor of shape (B, E)
        """

        # Transformer + resid
        x = self.transformer(clicked_news_emb, src_key_padding_mask=click_mask)
        x = clicked_news_emb + x
        
        # Sum pool
        inv_mask = (~click_mask).unsqueeze(-1).float()  # shape: (B, N, 1)
        x = torch.sum(x * inv_mask, dim=1)         # shape: (B, E)

        
        return self.postnet(x)     # shape: (B, E)