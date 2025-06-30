# Hermes - Personalized News Feed

Hermes is a personalized news feed application that leverages machine learning to provide users with a customized news experience. It features a modern, responsive user interface and a robust backend that powers the recommendation engine.

## Features

- **Personalized News Feed:** Users receive a customized feed of articles based on their reading history and preferences.
- **Tinder-style Card Swiping:** A "Tinder for news" feature allows users to swipe through articles, providing a fun and engaging way to discover new content.
- **Topic-based Recommendations:** The application categorizes articles into topics and recommends content based on the user's preferred topics.
- **User Authentication:** Secure user authentication is implemented using JWT and Google OAuth.

## High-Level Implementation Details

The project is a full-stack application with the following core components:

- **Frontend:** The client-side is a single-page application built with **React** and **Vite**. It uses Material-UI for components and styling and communicates with the backend via a REST API.

- **Backend:** The server is a **Flask** application written in Python. It exposes a REST API for the frontend and handles user authentication, article recommendations, and database interactions.

- **Machine Learning Model:** The recommendation engine is powered by a custom-built model using **PyTorch**. The model is trained on the [MIND dataset](https://msnews.github.io/) and uses a combination of collaborative filtering and content-based filtering techniques to generate personalized recommendations.

- **Database:** **MongoDB** is used as the primary database to store user data, articles, and interaction data.

- **News Fetcher:** A separate Python script (`server/news_fetcher/fetch_pipeline.py`) is responsible for fetching and processing news articles from various sources. It can be run on a schedule to keep the content fresh.

## Recommendation Pipeline

The recommendation pipeline is designed to deliver relevant and personalized news articles to users. It consists of two main stages: candidate generation and ranking.

1.  **Candidate Generation & Filtering:** Initially, a large pool of articles is fetched from various news sources. When a user requests recommendations, a subset of these articles is selected as candidates. This selection is based on several factors, including:
    *   **User's Explicit Preferences:** Topics the user has shown interest in.
    *   **Implicit Feedback:** Articles the user has read, liked, or swiped on.
    *   **Recency:** Newer articles are prioritized to ensure the content is fresh.
    This filtering is done by querying the MongoDB database, which stores all articles and user interaction data.

2.  **Ranking Model:** Once the candidate articles are selected, they are ranked using a sophisticated recommendation model. The core of this model is an **NRMS (News Recommendation Model with a multi-head self-attention)** model, a state-of-the-art approach for news recommendation. The model analyzes the user's historical interactions and the content of the candidate articles to predict the likelihood of the user's interest. The articles are then sorted based on this prediction, and the top-ranked articles are presented to the user in their feed.

## Local Setup and Running the Project

To run the project locally, you will need to have the following installed:

- Python 3.x
- Node.js and npm
- MongoDB

**1. Clone the repository:**

```bash
git clone <repository-url>
cd hermes
```

**2. Set up the backend:**

- **Install Python dependencies:**
  ```bash
  pip install -r server/requirements.txt
  ```

- **Set up environment variables:**
  Create a `.env` file in the `server` directory and add the following:
  ```
  JWT_SECRET_KEY=super-secret
  GOOGLE_CLIENT_ID=<your-google-client-id>
  ```

- **Run the server:**
  ```bash
  python server/app.py
  ```
  The server will start on `http://localhost:5000`.

**3. Set up the frontend:**

- **Install Node.js dependencies:**
  ```bash`
  cd client
  npm install
  ```

- **Run the client:**
  ```bash
  npm run dev
  ```
  The client will be available at `http://localhost:5173`.

**4. Fetching News Articles:**

To populate the database with news articles, you can run the news fetcher script:

```bash
python server/news_fetcher/fetch_pipeline.py
```

This will fetch articles from the configured sources and store them in the MongoDB database. You can also set up a cron job to run this script periodically.
