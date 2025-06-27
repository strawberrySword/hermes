import array
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load news data
def load_news(path):
    df = pd.read_table(f"{path}/news.tsv", header=None)
    df.columns = ['news_id', 'category', 'subcategory', 'title', 'abstract', 'url', 'title_entities', 'abstract_entities']
    
    #df['text'] = (df['title'].fillna(''))
    #should enable on the servers
    df['text'] = (df['title'].fillna('') + ' ' + df['abstract'].fillna('')).str.lower()
    return df[['text', 'category']]

train_df = load_news("Mind_train")
val_df = load_news("Mind_val")

# Label encoding
all_categories = pd.concat([train_df['category'], val_df['category']])
label_encoder = LabelEncoder()
label_encoder.fit(all_categories)

# Now transform separately
train_df['label'] = label_encoder.transform(train_df['category'])
val_df['label'] = label_encoder.transform(val_df['category'])

# Vectorize text with TF-IDF
vectorizer = TfidfVectorizer(max_features=20000)
vectorizer.fit(train_df['text'])
X_train = vectorizer.transform(train_df['text'])
X_val = vectorizer.transform(val_df['text'])
y_train = train_df['label']
y_val = val_df['label']
# Train classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# Evaluate
labels = np.arange(len(label_encoder.classes_))
y_pred = clf.predict(X_val)
print(classification_report(y_val, y_pred, labels=labels, target_names=label_encoder.classes_,zero_division=0))
