# Modules Description

## User Interface (Client)

- **Technology**: React, TypeScript, Vite
- **Responsibilities**: Displays the user interface, handles user interactions, and communicates with the backend server to fetch articles and recommendations.
- **Interactions**: 
  - Calls backend APIs for user authentication, fetching articles, and getting recommendations.
  - Receives data from the backend to display in the UI.
  - We use `react-query` to handle api calls and client caching.
- **Source code**: [`/client/`](./client/)

## Backend Server (API Gateway)

- **Technology**: Python, Flask, Pymongo
- **Responsibilities**: Exposes the system's APIs, handles business logic, and orchestrates requests between the frontend client and the various backend services.
- **Interactions**: 
  - Handles all incoming requests from the client.
  - Interacts with the User & Content Management module to handle users, articles, and interactions.
  - Calls the Recommendation Engine to get personalized article recommendations.
- **Source code**: [`/server/`](./server/)

## Article Recommendation Engine

- **Technology**: pytorch
- **Responsibilities**: Recommends articles based on user's view hisotry.
- **Interactions**:
  - Receives a user's reading history from the Backend Server and a list of candidates.
  - Returns a ranked list of recommended articles to the Backend Server.
- **Training and Eval Code**: [`/model/nrms/`](./model/nrms/)
- **Inference Code**: [`/server/article_recommender/`](./server/article_recommender/)
- **Further Reading**: [`NRMS`](./NRMS_Explanation.md)

## Topic Modeling

- **Technology**: Python, RoBERTa (zero-shot classification)
- **Responsibilities**: Classifies articles into topics using a pre-trained RoBERTa model.
- **Interactions**: 
  - The model classifies news articles into a predefined set of topics.
- **Source code**: [`/model/topic_classifier.ipynb`](./model/topic_classifier.ipynb)

## Embedding Generation

- **Technology**: Python, PyTorch
- **Responsibilities**: Generates vector embeddings for news article titles using the trained NRMS News Encoder. These embeddings are cached for performance.
- **Interactions**: 
  - Reads article data from the database.
  - Uses the NRMS model to compute embeddings.
  - Stores the generated embeddings back into the database.
- **Source code**: [`/server/scripts/calculate_embeddings.py`](./server/scripts/calculate_embeddings.py)

## User and Content Management

- **Technology**: Python, MongoDB
- **Responsibilities**: Manages user accounts, stores user interaction data (clicks, reads), and manages the collection of news articles.
- **Interactions**: 
  - Provides user data for authentication and personalization.
  - Stores new articles and user interactions.
  - Accessed by the Backend Server to retrieve and store data.
- **Source code**:
  - Users: [`/server/auth/`](./server/auth/)
  - Articles: [`/server/articles/`](./server/articles/)
  - Interactions: [`/server/interactions/`](./server/interactions/)

## Data Ingestion Pipeline

- **Technology**: Python, Shell Scripts
- **Responsibilities**: Periodically fetches new news articles from external sources and ingests them into the system's database.
- **Interactions**: 
  - Runs on a schedule (e.g., cron job).
  - Fetches data from news APIs.
  - Inserts new articles into the database, which then get processed by the Embedding Generation module.
- **Source code**: [`/server/news_fetcher/`](./server/news_fetcher/)
