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
**SHAHAR FILL HERE**

- **React** — for ...
- **NiceGUI** — for ...
- ...

### Backend
**SHAHAR FILL HERE**

- **Flask** — for ...
- **FastAPI** — for ...
- ...

### Algorithmic

- **PyTorch** — We write, train, and evaluate the entire NRMS (candidate ranking) model in raw PyTorch. The NRMS model is defined in `model/NRMS/nrms.py` and leverages the user and news encoders which are defined in `model/modules/encoder.py`. We leverage PyTorch dataloaders to train the model, and the pre-processing/loading/collating pipeline is written in `model/NRMS/data/...`. The entire training pipeline (pre-process -> dataloaders -> define model -> train) is demonstrated in `model/NRMS/train.ipynb` as a notebook and in `model/NRMS/trainer.py` as a script.

- **HuggingFace 🤗** - We leverage the HuggingFace 🤗 pipeline feature to use a pretrained model (namely, `FacebookAI roberta large mnli`) to use zero-shot classification, in order to classify articles to topics.

- **Weights & Biases** - We make use of Weights&Biases to view our model's training curves/convergence plots, and to monitor the training of our model. Our plots are available [here](https://wandb.ai/the_magnivim/NRMS).

### Data Platforms
**SHAHAR FILL HERE**

- **MySQL** — for storing main user interactions...
- **Redis** — for caching models and user interactions...

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

Describe the main stages of your system development, major changes, and lessons learned.

Example:

- **Milestone 1:** Initial prototype with basic search and static recommendations.
- **Milestone 2:** Added collaborative filtering using PyTorch.
- **Milestone 3:** Integrated OpenAI model for better item embeddings.
- **Milestone 4:** Switched to Redis for faster caching.
- **Milestone 5:** Improved search engine ranking using TF-IDF.

&nbsp;<br>

## Open Issues, Limitations, and Future Work

- Currently we don't actually have a recent, updated news source, and we use past data which is being fed as we live 3 months into the past. This is of course a limitation which we have to overcome in the future, and acquire some up-to-date news source. A solution to this may be simply scraping different news websites.

- Another limitation is our scale; Our current model is small and thus pretty fast. Scaling up to more serious models/databases we will of course run into scaling challenges, such as latency.

- A major feature which we didn't quite implement in our product yet is diversity. A big future step would be implementing diversification of a user's feed, to show them the same news articles from different points of view, as mentioned in different news sources.

- Another big feature left for the future is fine-grained clustering of articles; We plan on implementing clustering of articles into fine-grained recent events. We then plan to work with those clusters rather then the big topics 

&nbsp;<br>

## Additional Comments

Any extra insights, difficulties, tricks, or interesting stories you want to share.