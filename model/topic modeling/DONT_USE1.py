from bertopic import BERTopic
from bertopic.dimensionality import BaseDimensionalityReduction
from bertopic.vectorizers import ClassTfidfTransformer
from umap import UMAP
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder


def load_news(path):
    df = pd.read_table(f"{path}/news.tsv", header=None)
    df.columns = ['news_id', 'category', 'subcategory', 'title', 'abstract', 'url', 'title_entities', 'abstract_entities']
    df['text'] = (df['title'].fillna('')).str.lower()
    return df[['text', 'category']]

# Load data
train_df = load_news("Mind_train")
val_df = load_news("Mind_val")[:1000]

# Label encoding
all_categories = pd.concat([train_df['category'], val_df['category']])
label_encoder = LabelEncoder()
label_encoder.fit(all_categories)

# Transform labels
train_df['label'] = label_encoder.transform(train_df['category'])
val_df['label'] = label_encoder.transform(val_df['category'])

X_train = train_df['text'].tolist()
X_test = val_df['text'].tolist()
y_train = train_df['label'].tolist()
y_test = val_df['label'].tolist()

# Initialize models
empty_dimensionality_model = BaseDimensionalityReduction()
clf_clustering = LogisticRegression()
ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)

# Create a fully supervised BERTopic instance
topic_model = BERTopic(
    umap_model=empty_dimensionality_model,
    hdbscan_model=clf_clustering,
    ctfidf_model=ctfidf_model
)

# Fit the model
topics, probs = topic_model.fit_transform(X_train, y=y_train)

print("Topic model fitted successfully!")
print(f"Number of topics found: {len(topic_model.get_topic_info())}")

# Map input `y` to topics
mappings = topic_model.topic_mapper_.get_mappings(True)
# Fix the mappings - use label_encoder.classes_ to get original category names
mappings = {value: label_encoder.classes_[key] for key, value in mappings.items() if key < len(label_encoder.classes_)}

df = topic_model.get_topic_info()
df["Class"] = df.Topic.map(mappings)
"""
print("\nTopic Information:")
print(df[['Topic', 'Count', 'Class']].head(10))"""

# Fixed function to extract topic features
def extract_topic_features(documents, topic_model):
    """
    Extract topic-based features for classification.
    Returns a matrix where each row represents a document and columns represent topic assignments.
    """
    topics, probabilities = topic_model.transform(documents)
    
    # Get all unique topics (excluding outlier topic -1)
    all_topics = sorted([t for t in topic_model.get_topics().keys() if t != -1])
    n_topics = len(all_topics)
    
    if n_topics == 0:
        raise ValueError("No valid topics found")
    
    # Create feature matrix
    features = np.zeros((len(documents), n_topics))
    
    # Handle case where probabilities is None (common in supervised BERTopic)
    if probabilities is None:
        print("Using binary topic assignment (probabilities not available)")
        # Use binary encoding: 1 for assigned topic, 0 for others
        for i, topic in enumerate(topics):
            if topic != -1 and topic in all_topics:
                topic_idx = all_topics.index(topic)
                features[i, topic_idx] = 1.0
    else:
        print("Using topic probabilities")
        # Use probability distributions
        for i, (topic, probs_dist) in enumerate(zip(topics, probabilities)):
            if topic != -1 and topic in all_topics:
                if probs_dist is not None and len(probs_dist) > 0:
                    # Use probability distribution
                    for j, prob in enumerate(probs_dist):
                        if j < n_topics:
                            features[i, j] = prob
                else:
                    # Fallback to binary encoding
                    topic_idx = all_topics.index(topic)
                    features[i, topic_idx] = 1.0
    
    return features

# Alternative approach: Use topic keywords as features
def extract_topic_keyword_features(documents, topic_model, max_features=100):
    """
    Extract features based on topic keywords using TF-IDF approach.
    """
    # Get all topic keywords
    all_keywords = []
    topics_dict = topic_model.get_topics()
    
    for topic_id in topics_dict:
        if topic_id != -1:  # Exclude outlier topic
            keywords = [word for word, score in topics_dict[topic_id][:10]]  # Top 10 words per topic
            all_keywords.extend(keywords)
    
    # Remove duplicates while preserving order
    unique_keywords = list(dict.fromkeys(all_keywords))
    
    # Create TF-IDF vectorizer with topic keywords as vocabulary
    vectorizer = CountVectorizer(
        vocabulary=unique_keywords[:max_features],
        lowercase=True,
        stop_words='english'
    )
    
    features = vectorizer.fit_transform(documents).toarray()
    return features

# Extract features for training and testing
print("\nExtracting topic features...")
result_train = extract_topic_features(X_train, topic_model)
result_test = extract_topic_features(X_test, topic_model)
print(f"Topic probability features shape - Train: {result_train.shape}, Test: {result_test.shape}")

# Train classifier on topic features
print("\nTraining classifier...")
clf = LogisticRegression(max_iter=1000, random_state=42)

# Check if we have valid features
if result_train.shape[1] == 0:
    print("Error: No features extracted. Using simple bag-of-words as fallback.")
    # Fallback to simple bag-of-words
    vectorizer = CountVectorizer(max_features=100, stop_words='english')
    result_train = vectorizer.fit_transform(X_train).toarray()
    result_test = vectorizer.transform(X_test).toarray()

clf.fit(result_train, y_train)

# Make predictions
print("Making predictions...")
y_pred = clf.predict(result_test)

# Evaluate
print("\nClassification Report:")
# Fix: Get unique labels present in y_test and y_pred to avoid mismatch
unique_labels = sorted(list(set(y_test + y_pred.tolist())))
target_names_filtered = [label_encoder.classes_[i] for i in unique_labels]

print(classification_report(y_test, y_pred, 
                          labels=unique_labels,
                          target_names=target_names_filtered))
"""# Additional evaluation metrics
from sklearn.metrics import accuracy_score, confusion_matrix
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")

# Show some example predictions
print("\nExample predictions:")
for i in range(min(5, len(X_test))):
    true_label = label_encoder.classes_[y_test[i]]
    pred_label = label_encoder.classes_[y_pred[i]]
    print(f"Text: {X_test[i][:100]}...")
    print(f"True: {true_label}, Predicted: {pred_label}")
    print("-" * 50)

# Show topic distribution
print(f"\nTopic distribution in training data:")
unique_topics, counts = np.unique(topics, return_counts=True)
for topic, count in zip(unique_topics, counts):
    topic_class = mappings.get(topic, "Unknown")
    print(f"Topic {topic} ({topic_class}): {count} documents")"""