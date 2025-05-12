# this script will read the users
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

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


def load_users():
    """
    Load users from .tsv and load to db.
    """
    users = pd.read_csv("data/behaviors.tsv", sep="\t")
    users = users.iloc[:, 1].unique().tolist()
    users_dict = [{"user_id": user} for user in users]

    user_collection.insert_many(users_dict)


def load_articles():
    """
    Load articles from .tsv and load to db.
    """
    articles = pd.read_csv("data/news.tsv", sep="\t")

    print(articles.iloc[:, 0].head())  # article_id
    print(articles.iloc[:, 1].head())  # genre
    print(articles.iloc[:, 2].head())  # topic
    print(articles.iloc[:, 3].head())  # title
    print(articles.iloc[:, 4].head())  # subtitle
    print(articles.iloc[:, 5].head())  # url

    articles = articles.iloc[:, 0:6]
    articles.columns = ["article_id", "genre",
                        "topic", "title", "subtitle", "url"]
    articles = articles.drop_duplicates(subset=["article_id"])
    articles = articles.reset_index(drop=True)
    articles = articles.where(pd.notnull(articles), "")

    # Convert the DataFrame to a list of dictionaries
    articles_dict = articles.to_dict(orient="records")
    print(articles_dict[0])  # print the first article
    # Insert the articles into the MongoDB collection
    articles_collection.insert_many(articles_dict)


def load_action_history():
    """
    Load action history from .tsv and load to db.
    """
    actions = pd.read_csv("data/behaviors.tsv", sep="\t")
    actions = actions.iloc[:, 1:4]
    actions.columns = ["user_id", "time_stamp", "article_id"]
    actions = actions.reset_index(drop=True)
    actions['article_id'] = actions['article_id'].str.split()
    actions = actions.explode('article_id').reset_index(drop=True)
    actions['time_stamp'] = pd.to_datetime(
        actions['time_stamp'], format='%m/%d/%Y %I:%M:%S %p')
    actions_dict = actions.to_dict(orient="records")

    print(len(actions_dict))  # print the number of actions``
    # likes_collection.insert_many(actions_dict)


if __name__ == "__main__":
    # load_users()
    # load_action_history()
    load_articles()
