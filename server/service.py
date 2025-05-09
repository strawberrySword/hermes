from model.model import get_recommendations
import repository.articles as articles


def recommend(user_id, start=0, end=10):
    recommendations = get_recommendations(user_id, end)
    return articles.find_many(recommendations)
