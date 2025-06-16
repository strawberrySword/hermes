from fetcher.google_fetcher import GoogleNewsFetcher
from utils.insert_articles import insert_articles
import os
import time


CATEGORIES = [
    "world", "nation", "business", "technology",
    "entertainment", "sports", "science", "health"
]


def fetch_articles_by_category(api_key, categories, articles_per_category=10):
    """
    Fetches news articles for each specified category using GNews API.

    Args:
        api_key (str): GNews API key.
        categories (list of str): List of GNews-supported category keywords (e.g., 'business', 'technology').
        articles_per_category (int): Number of articles to fetch per category.

    Returns:
        list of dict: Combined list of all fetched and parsed articles.
    """
    all_articles = []
    for category in categories:
        print(f"\nFetching articles for category: {category}")
        fetcher = GoogleNewsFetcher(api_key=api_key, query=category, max_results=articles_per_category)
        articles = fetcher.fetch_articles()
        all_articles.extend(articles)
        time.sleep(1.5)
    return all_articles


def run_fetcher():
    api_key = os.getenv("GNEWS_API_KEY")
    if not api_key:
        raise ValueError("GNEWS_API_KEY not found in environment variables.")
    articles = fetch_articles_by_category(api_key, CATEGORIES, articles_per_category=10)
    insert_articles(articles)


if __name__ == "__main__":
    print("Hello World!")

