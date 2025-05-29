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
		clicked_token_ids: torch.LongTensor,     # (B, N, L)
		clicked_token_mask: torch.BoolTensor,    # (B, N, L)
		candidate_token_ids: torch.LongTensor,   # (B, K, L)
		candidate_token_mask: torch.BoolTensor   # (B, K, L)
		) -> torch.Tensor:                           # returns (B, K)


		B, N, L = clicked_token_ids.shape
		K = candidate_token_ids.size(1)

		# Embed articles of click history
		clicked_flat_ids = clicked_token_ids.view(B * N, L)      # (B*N, L)
		clicked_flat_mask = clicked_token_mask.view(B * N, L)    # (B*N, L)

		clicked_emb_flat = self.news_encoder(clicked_flat_ids, clicked_flat_mask)		
		clicked_news_emb = clicked_emb_flat.view(B, N, self.d_embed)      # (B, N, d_embed)


		# Embed article embeddings (lmfao attention again)
		clicked_slot_mask = clicked_token_mask.all(dim=2)  # (B, N)
	
		user_emb = self.user_encoder(clicked_news_emb, clicked_slot_mask)  # (B, d_embed)


		# Flatten and encode candidate news
		candidate_flat_ids = candidate_token_ids.view(B * K, L)
		candidate_flat_mask = candidate_token_mask.view(B * K, L)

		candidate_emb_flat = self.news_encoder(candidate_flat_ids, candidate_flat_mask)
		candidate_emb = candidate_emb_flat.view(B, K, self.d_embed)  # (B, K, d_embed)

		# Dot product: (B, K)
		scores = torch.bmm(candidate_emb, user_emb.unsqueeze(2)).squeeze(2)

		return scores  # logits (B, K)