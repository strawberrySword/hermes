from bson import ObjectId
from flask import jsonify
from article_recommender.model import load_model, recommend_topk_from_titles
import articles.repository as repository
import interactions.service as interactions_service
import interactions.repository as interactions_repository
import torch


model = load_model()


def recommend(user_id):
    stale_articles = interactions_repository.get_stale(user_id)
    if (not stale_articles):
        return jsonify(get_some_articles())
    candidates = repository.find_fresh(stale_articles)
    viewed_articles_ids = interactions_repository.get_viewed(user_id)
    viewed_articles_ids = [ObjectId(article['article_id'])
                           for article in viewed_articles_ids]
    print("before candidates", len(candidates))

    viewed_articles = repository.find_many(viewed_articles_ids)
    print("after candidates", len(viewed_articles))
    _scores, recommended_articles_id = recommend_topk_from_titles(
        model=model,
        history_titles=[article['title'] for article in viewed_articles],
        candidate_titles=[article['title'] for article in candidates],
        topk=10,
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    )

    interactions_service.record_many_recommended(
        user_id=user_id,
        article_ids=[candidates[i]['id'] for i in recommended_articles_id])

    res = [candidates[i] for i in recommended_articles_id]
    return jsonify(res)


def get_some_articles():
    return repository.get_random(10)
