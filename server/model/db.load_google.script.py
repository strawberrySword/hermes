# this script will read the users
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

import dateutil.relativedelta as rd

import os
import json

# load the environment variables from the .env file
load_dotenv()
# get the database URL from the environment variables
MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client["hermes"]
user_collection = db["users"]
articles_collection = db["articles"]
likes_collection = db["likes"]


def filter_by_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(subset=["date"])
    df = df[df["date"].apply(lambda d: d.year == year)]
    return df


def load_articles():
    """
    Load articles from .csv and load to db.
    """
    articles = pd.read_csv("data/google_news_2025.csv")

    articles.drop(columns=['category'],
                  axis=1, inplace=True)
    articles.drop(columns=['language'],
                  axis=1, inplace=True)
    articles['date'] = pd.to_datetime(articles['date'])
    articles['date'] = articles['date'].apply(
        lambda x: x + rd.relativedelta(months=5))
    articles = articles[articles["image"].notna() & (
        articles["image"].str.strip() != "")]

    # Convert the DataFrame to a list of dictionaries
    articles_dict = articles.to_dict(orient="records")
    print(articles_dict[0])  # print the first article
    # Insert the articles into the MongoDB collection
    articles_collection.insert_many(articles_dict)


if __name__ == "__main__":
    # load_users()
    # load_action_history()
    load_articles()
