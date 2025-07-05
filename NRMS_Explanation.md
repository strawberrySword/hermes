
# NRMS Model Explained

## Introduction
The NRMS (Neural News Recommendation with Multi-Head Self-Attention) model is a sophisticated, content-based recommendation system designed to suggest news articles to users based on their past reading history. This document provides a detailed explanation of its architecture, how it works, and its specific implementation within this project.

## Core Concepts
The central idea of NRMS is to generate meaningful vector representations (embeddings) for both news articles and users. Recommendations are then made by identifying the articles with embeddings most similar to a user's embedding. This is accomplished using two primary components: a **News Encoder** and a **User Encoder**.

### 1. News Encoder
The News Encoder creates a vector representation for a single news article by analyzing its title.

- **Word Embeddings**: The process begins by converting each word in the article's title into a dense vector using a pre-trained embedding layer. This layer acts as a lookup table, mapping each word in the vocabulary to a unique vector.
- **Multi-Head Self-Attention**: The sequence of word embeddings is then processed by a multi-head self-attention mechanism. This allows the model to weigh the importance of each word in the title relative to the others, capturing the deep contextual meaning of the headline.
- **Additive Attention (Pooling)**: Finally, an additive attention layer aggregates the word-level information into a single, fixed-size vector representing the entire news article. This "news embedding" encapsulates the semantic essence of the article.

### 2. User Encoder
The User Encoder creates a vector representation for a user by analyzing their reading history.

- **News Embeddings as Input**: It takes the news embeddings of the articles the user has previously clicked on as its input.
- **Multi-Head Self-Attention**: Similar to the News Encoder, a multi-head self-attention mechanism is applied to the sequence of news embeddings. This enables the model to learn a user's interests by identifying which articles in their history are most indicative of their preferences. For instance, if a user frequently reads about finance, those articles will be weighted more heavily in their final user profile.
- **Additive Attention (Pooling)**: An additive attention layer then "pools" the contextualized news embeddings into a single "user embedding," which represents the user's overall interests.

### 3. Recommendation and Scoring
Once the user and candidate article embeddings are created, the recommendation process is straightforward:

1.  The model calculates the **dot product** between the user's embedding and the embedding of each candidate article.
2.  This calculation yields a relevance **score** for each candidate.
3.  The articles are ranked by these scores, and the highest-scoring ones are presented to the user as recommendations.

## Project Implementation

### Model Training (`/model/NRMS/`)

The training of the NRMS model is handled in the `/model/NRMS/` directory.

- **`nrms.py`**: This file defines the core `NRMS` model architecture, which integrates the `NewsEncoder` and `UserEncoder` modules (defined in `modules/encoder.py`). The `forward` method in this class executes the end-to-end process of converting input text to recommendation scores.
- **`trainer.py`**: This script orchestrates the model training process.
    - **Data Handling**: It loads and preprocesses the MIND dataset, which contains user browsing histories and news article data. The `MindDataset` class and `mind_collate_fn` function are responsible for tokenizing titles, padding sequences to a uniform length, and preparing batches for the model.
    - **Training Loop**: The `train` function implements the core training logic. It iterates over the dataset, computes the model's predictions, and calculates the `CrossEntropyLoss`. This loss function is ideal for ranking tasks, as it pushes the model to assign higher scores to articles the user actually clicked on. The model's weights are updated using the AdamW optimizer and a learning rate scheduler.
    - **Monitoring & Checkpointing**: Training progress, including loss and Mean Reciprocal Rank (MRR), is logged to Weights & Biases for visualization. Model checkpoints are saved periodically.

### Server-Side Inference (`/server/article_recommender/`)

The trained model is used to generate live recommendations in the server application. To optimize performance, article embeddings are pre-computed and cached.

- **`nrms.py`**: A copy of the model definition file is included here to reconstruct the model architecture during inference.
- **`model.py`**: This file contains the logic for using the trained model in a production setting.
    - **Embedding Caching**: Instead of computing article embeddings on-the-fly, a script (`calculate_embeddings.py`) is run periodically to process new articles. It uses the `NewsEncoder` part of the NRMS model to generate embeddings for article titles and stores them in the database.
    - **`load_model()`**: This function loads the pre-trained model weights from a saved checkpoint file (`checkpoint_epoch5.pt`).
    - **`recommend_topk_from_titles()`**: This is the main function for generating recommendations. It takes a user's reading history (as a list of titles) and a list of candidate articles. For the user's history, it generates user embedding on the fly. For candidate articles, it retrieves their pre-computed embeddings from the cache. It then calculates scores and returns the top-k recommended articles.

### End-to-End Flow

1.  **Offline Training**: The NRMS model is trained on the MIND dataset to learn how to represent user interests and article content.
2.  **Deployment**: The resulting trained model checkpoint is deployed with the server application.
3.  **Embedding Caching**: A background process periodically calculates embeddings for new articles and stores them in a cache (e.g., a database).
4.  **Online Inference**: When a user requests recommendations, the server:
    a. Retrieves the user's reading history.
    b. Gathers a list of candidate articles and fetches their pre-computed embeddings from the cache.
    c. Uses the loaded NRMS model's `UserEncoder` to compute the user's embedding from their history.
    d. Calculates the dot product between the user embedding and the cached candidate article embeddings to get scores.
    e. Returns the highest-ranked articles as personalized recommendations.
