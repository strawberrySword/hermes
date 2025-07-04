import datetime
from bson import ObjectId
from flask import jsonify
from article_recommender.model import load_model, recommend_topk_from_embeddings, recommend_topk_from_titles
import articles.repository as repository
import interactions.service as interactions_service
import interactions.repository as interactions_repository
import torch


model = load_model()


def recommend(user_id, topic, page_size):
    interaction_data = interactions_repository.get_user_interaction_data(
        user_id)
    stale_articles = interaction_data["stale_articles"]
    viewed_articles_ids = interaction_data["viewed_articles"]

    if not viewed_articles_ids:
        return jsonify(get_some_articles())

    candidates = repository.find_fresh(stale_articles, topic)
    if not candidates:
        return jsonify([])

    viewed_articles_ids = [ObjectId(article['article_id'])
                           for article in viewed_articles_ids]

    viewed_articles = repository.find_many(viewed_articles_ids)

    _scores, recommended_articles_id = recommend_topk_from_embeddings(
        model=model,
        history_titles=[article['title'] for article in viewed_articles],
        candidate_emb=torch.tensor(
            [article['embeddings'] for article in candidates]),
        topk=page_size,
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    )

    interactions_service.record_many_recommended(
        user_id=user_id,
        article_ids=[candidates[i]['id'] for i in recommended_articles_id])

    res = [candidates[i] for i in recommended_articles_id]
    return jsonify(res)


def get_top_topics(user_id):
    return repository.get_top_topics(user_id)


def get_some_articles():
    return repository.get_random(10)


def get_random_article():
    return repository.get_random(1)[0]
