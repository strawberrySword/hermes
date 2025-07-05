# Hermes - Personalized News Feed

## About
Hermes is a personalized news feed application that leverages machine learning to provide users with a customized news experience. It features a modern, responsive user interface and a robust backend that powers the recommendation engine.

This project is developed for the *Recommender Systems Workshop* at Tel Aviv University.  
More information can be found on the [Workshop Website](https://courses.cs.tau.ac.il/recsys/).
## Features

- **Personalized News Feed:** Users receive a customized feed of articles based on their reading history and preferences.
- **Tinder-style Card Swiping:** A "Tinder for news" feature allows users to swipe through articles, providing a fun and engaging way to discover new content.
- **Topic-based Recommendations:** The application categorizes articles into topics and recommends content based on the user's preferred topics.
- **User Authentication:** Secure user authentication is implemented using JWT and Google OAuth.

## Documentation
You can find all the documentation in the following files:

- [Installation Guide](install.md)
- [Project Summary](summary.md)
- [Modules Description](modules.md)
- [NRMS walkthrough](NRMS_Explanation.md)

## High-Level Implementation Details

The project is a full-stack application with the following core components:

- **Frontend:** The client-side is a single-page application built with **React** and **Vite**. It uses Material-UI for components and styling and communicates with the backend via a REST API.

- **Backend:** The server is a **Flask** application written in Python. It exposes a REST API for the frontend and handles user authentication, article recommendations, and database interactions.

- **Machine Learning Model:** The recommendation engine is powered by a custom-built model using **PyTorch**. The model is trained on the [MIND dataset](https://msnews.github.io/) and uses a content-based filtering technique to generate personalized recommendations.

- **Database:** **MongoDB** is used as the primary database to store user data, articles, and interaction data.

- **News Fetcher:** A separate Python script (`server/news_fetcher/fetch_pipeline.py`) is responsible for fetching and processing news articles from various sources. It can be run on a schedule to keep the content fresh.

## Recommendation Pipeline

The recommendation pipeline is designed to deliver relevant and personalized news articles to users. It consists of two main stages: candidate generation and ranking.

1. **Candidate Generation & Filtering:** Initially, a large pool of articles is fetched from various news sources. When a user requests recommendations we get the most recent 1000 articles which are not `stale`.
A stale article is defined to be an article that satisfies at least one of those conditions:
  - Has been read by the user.
  - Has been recommended to the user in the last hour.

2.  **Ranking Model:** Once the candidate articles are selected, they are ranked using a sophisticated recommendation model. The core of this model is an **NRMS (News Recommendation Model with a multi-head self-attention)** model, a state-of-the-art approach for news recommendation. The model analyzes the user's historical interactions and the content of the candidate articles to predict the likelihood of the user's interest. The articles are then sorted based on this prediction, and the top-ranked articles are presented to the user in their feed.

### Authors
- Shahar Glam — shaharglame@gmail.com  
- Daniel Volkov — das.volkov@gmail.com  
- Gil Greenstein - gilgre2@gmail.com
- Aviv Bar-Or - avivbaror@mail.tau.ac.il