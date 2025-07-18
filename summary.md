**You should change the content of this file. Please use all second-level headings.**

# Project Summary

## Datasets Used

- **Dataset 1** — MIND small, News recommendation, [Link](https://msnews.github.io/).
- **Dataset 2** — Google news dataset, News, Sadly no public link available.

Additional data-related information:

- We choose use the MIND small dataset rather than the entire MIND dataset to match our small model and low-resource project.
- We make use of the Google news dataset, which was bought by the university for the education and AI hackathon last month.
- We train our recommender systems on the MIND dataset, and then use the Google news dataset for the actual application, as a proof of concept for live news fettching and staying up-to-date.

&nbsp;<br>

## Technologies and Frameworks

### Frontend
- **React & Vite** — Our frontend is a Single Page Application (SPA) built with `React` and `TypeScript`, bundled with `Vite` for a fast development experience.
- **Routing** - We use `react-router` for client-side routing and navigation between different views.
- **UI Components** — We leverage `Material UI (MUI)` for a consistent and modern design system, providing a rich set of pre-built components.
- **State Management & Data Fetching** — We use `TanStack Query (React Query)` to manage server state, handle caching, and streamline data fetching from our backend API via `axios`.
- **Authentication** — User authentication is handled using `Auth0`, providing a secure and robust login system.

### Backend
- **Flask** — A lightweight Python web framework used to build our REST API. It handles routing, requests, and responses.
- **MongoDB** — We use MongoDB as our primary database, accessed via `PyMongo`. It stores user data, articles, and interaction history.
- **Authentication** — Our API is secured using JSON Web Tokens (JWTs). The server validates tokens to protect routes and authorize user actions.
- **Architecture** — The backend follows a layered architecture, separating concerns into controllers (handling HTTP requests), services (business logic), and repositories (data access).

### Algorithmic

- **PyTorch** — We write, train, and evaluate the entire NRMS (candidate ranking) model in raw PyTorch. The NRMS model is defined in `model/NRMS/nrms.py` and leverages the user and news encoders which are defined in `model/modules/encoder.py`. We leverage PyTorch dataloaders to train the model, and the pre-processing/loading/collating pipeline is written in `model/NRMS/data/...`. The entire training pipeline (pre-process -> dataloaders -> define model -> train) is demonstrated in `model/NRMS/train.ipynb` as a notebook and in `model/NRMS/trainer.py` as a script.

- **HuggingFace 🤗** - We leverage the HuggingFace 🤗 pipeline feature to use a pretrained model (namely, `FacebookAI roberta large mnli`) to use zero-shot classification, in order to classify articles to topics.

- **Weights & Biases** - We make use of Weights&Biases to view our model's training curves/convergence plots, and to monitor the training of our model. Our plots are available [here](https://wandb.ai/the_magnivim/NRMS).

### Data Platforms

- **MongoDB** — Our primary database for storing articles, user information, and interaction data. We use the `pymongo` library in our Python backend to interact with the database.

### AI

- **FacebookAI roberta large mnli** - An MNLI finetuned checkpoint of Facebook's RoBERTa model. Used in our project to classify the topic of a given article, conditioned on it's headline. Used in a zero shot classification pipeline using the celebrated `HuggingFace` package.

&nbsp;<br>

## Main Algorithms

A brief summary of the key algorithms and features developed:

- **Topic classification** - We run inference on a pretrained MNLI finetuned model to make zero-shot classification predictions, in order to classify articles' categories.
- **Content-Based (topic ranking)** - To rank the topics for a user's page. We use a counts-based approach, ranking by the frequence of the topic in the user's history.
- **Content-Based (NRMS)** - To rank the articles inside each category, conditioned on the user's history. This is done using the NRMS model.

&nbsp;<br>

## Development Environment

- **GitHub** - the way we synchronized code versions between our team members.
- **VSCode** - the IDE in which we wrote this project.

- **Claude 4 sonnet** - For emotional support and additional help with development 😅.

&nbsp;<br>

## Development Evolution

- **Milestone 1 (March-May 2025): Project Initialization and Core Model Development.** The project began with the initial repository setup in late March. The core of the application started to take shape in May with the establishment of the server structure and the first implementation of the Neural News Recommendation with Multi-Head Self-Attention (NRMS) model. This phase was defined by rapid prototyping and foundational work on the recommendation engine.

- **Milestone 2 (Late May - Early June 2025): NRMS Refinement and Training Infrastructure.** This period was dedicated to intensely developing and refining the NRMS model. Key advancements included building a robust training pipeline with a script-based trainer, implementing data loaders, and introducing critical training features like gradient clipping, a learning rate scheduler, and residual connections. The team established a systematic approach to model evaluation and checkpointing.

- **Milestone 3 (Mid-June 2025): News Fetching and Server Integration.** To ensure the content remained current, a news fetching pipeline was developed and integrated into the server. This marked a key transition from working with static datasets to handling live, incoming data, a critical step toward a real-world application.

- **Milestone 4 (Late June 2025): Topic Modeling and Advanced Classification.** The team introduced topic modeling to categorize articles. Initially, this was based on traditional methods, but it quickly evolved with the integration of a sophisticated zero-shot classification pipeline using a pre-trained model from HuggingFace 🤗. This allowed for dynamic and accurate topic assignment without the need for a custom-trained classifier.

- **Milestone 5 (Early July 2025): Performance Optimization and Finalization.** As the system matured, performance became a priority. A Redis caching layer was implemented to store and reuse article embeddings, significantly reducing latency. The database was streamlined for more efficient development and deployment. The final weeks were spent on documentation, code cleanup, and preparing the project for its final presentation.

&nbsp;<br>

## Open Issues, Limitations, and Future Work

- Currently we don't actually have a recent, updated news source, and we use past data which is being fed as we live 3 months into the past. This is of course a limitation which we have to overcome in the future, and acquire some up-to-date news source. A solution to this may be simply scraping different news websites.

- Another limitation is our scale; Our current model is small and thus pretty fast. Scaling up to more serious models/databases we will of course run into scaling challenges, such as latency.

- A major feature which we didn't quite implement in our product yet is diversity. A big future step would be implementing diversification of a user's feed, to show them the same news articles from different points of view, as mentioned in different news sources.

- Another big feature left for the future is fine-grained clustering of articles; We plan on implementing clustering of articles into fine-grained recent events. We then plan to work with those clusters rather then the big topics 

&nbsp;<br>
