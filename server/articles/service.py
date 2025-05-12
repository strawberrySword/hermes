from model.model import get_recommendations
import articles.repository as repository

def recommend(user_id, start=0, end=10):
    recommendations = get_recommendations(user_id, end)
    return repository.find_many(recommendations[start:end])
