import pandas as pd
from db.mongo_client import collection
from pymongo.collection import Collection
from typing import Tuple
from utils.insert_articles import insert_articles
from langdetect import detect, LangDetectException


CSV_PATH = "data/google_news.csv"


def load_dataset(path: str) -> pd.DataFrame:
    """
    Load the news dataset from a csv FILE

    Args:
        path (str): Path to the CSV file

    Returns:
        pd.DataFrame: Loaded dataset.
    """

    try:
        df = pd.read_csv(path)
        print(f"Loaded dataset with {len(df)} records")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the file: {path}")
    except Exception as e:
        raise RuntimeError(f" Error loading dataset: {e}")


def connect_to_collection() -> Collection:
    """
    Get the MongoDB collection object.

    Returns:
        Collection: MongoDB collection to insert into.
    """
    return collection


def filter_missing_images(df: pd.DataFrame) -> pd.DataFrame:
    og_length = len(df)
    df_filtered = df[df["image"].notna() & (df["image"].str.strip() != "")]
    removed = og_length - len(df_filtered)
    print(f"Removed {removed} articles without images.")
    return df_filtered


def filter_by_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(subset=["date"])
    df = df[df["date"].apply(lambda d: d.year == year)]
    return df


def is_english(text):
    if not isinstance(text, str) or text.strip() == "":
        return False
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False


def split_by_date(df: pd.DataFrame, top_n: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_sorted = df.sort_values("date", ascending=False)
    return df_sorted.head(top_n), df_sorted.iloc[top_n:]


def add_category_col(df: pd.DataFrame):
    if "category" not in df.columns:
        df["category"] = ""
    return df


def preprocess_articles_for_db(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """
    Filter, sort, and select top articles for DB.
    Store the remainder to a CSV file.

    Args:
        df (pd.DataFrame): Raw article dataset.
        top_n (int): Number of articles to keep for DB.

    Returns:
        pd.DataFrame: Top N articles ready for DB insertion.
    """
    df = filter_missing_images(df)  # Only keep articles with images
    df = filter_by_year(df, 2025)   # Only keep articles from 2025
    df = df[df["title"].apply(is_english)]  # Only keep articles in English

    df = add_category_col(df)
    top_articles, remaining_articles = split_by_date(df, top_n)  # Split the top_n articles and the rest

    remaining_articles.to_csv("data/google_news_2025.csv", index=False)
    print(f"{len(top_articles)} articles prepared for DB.")
    print(f"{len(remaining_articles)} saved to data/google_news_2025.csv.")

    return top_articles


def format_articles_for_insertion(df: pd.DataFrame) -> list:
    """
    Convert a DataFrame of articles to a list of dicts formatted for MongoDB insertion.

    Args:
        df (pd.DataFrame): Articles with original field names.

    Returns:
        list: List of dicts matching MongoDB schema.
    """
    formatted = []
    for _, row in df.iterrows():
        article = {
            "url": row["url"],
            "title": row["title"],
            "source": row.get("publisher", ""),
            "publishedAt": row["date"],
            "image": row["image"],
            "category": row.get("category", ""),
            "keyword": row.get("keyword", ""),
            "country": row.get("country", ""),
            "language": row.get("language", "")
        }
        formatted.append(article)
    return formatted


def main():
    df = load_dataset(CSV_PATH)
    print("MongoDB connection established.")

    top_articles = preprocess_articles_for_db(df, top_n=50000)
    formatted_articles = format_articles_for_insertion(top_articles)
    insert_articles(formatted_articles)


if __name__ == "__main__":
    main()

