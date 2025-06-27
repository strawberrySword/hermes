from ast import mod
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import MaximalMarginalRelevance
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np
import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif
import warnings
warnings.filterwarnings('ignore')
os.environ["TOKENIZERS_PARALLELISM"] = "false"
"""
Think about increasing the number of features, iter etc...
depending on the size of the final training set
"""

# Download required NLTK data
nltk.download('stopwords')

class Supervised_TM:
    def __init__(self, 
                 embedding_model_name='all-MiniLM-L6-v2',
                 use_gpu=False,
                 min_topic_size=18,
                 nr_topics='auto',
                 diversity=0.7,
                 random_state=52):
        
        self.random_state = random_state
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        # label encorder
        self.label_encoder = LabelEncoder()        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(
            embedding_model_name,
            device='cuda' if use_gpu else 'cpu'
        )
        
        #  UMAP for dimensionality reduction
        self.umap_model = UMAP(
            n_neighbors=15,
            n_components=5,
            min_dist=0.0,
            metric='cosine',
            low_memory=True,
            random_state=random_state
        )
        
        # HDBSCAN for clustering with probability support
        self.hdbscan_model = HDBSCAN(
            min_cluster_size=min_topic_size,
            metric='euclidean',
            cluster_selection_method='eom',
            prediction_data=True,
            min_samples=5
        )
        
        #  representation model
        self.representation_model = MaximalMarginalRelevance(diversity=diversity)
        
        # Custom vectorizer for better text processing
        self.vectorizer_model = CountVectorizer(
            max_features=500,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=2,
            max_df=0.95
        )
        
        #  C-TF-IDF
        self.ctfidf_model = ClassTfidfTransformer(
            reduce_frequent_words=True,
            bm25_weighting=True
        )
        
        # Initialize BERTopic
        self.topic_model = BERTopic(
            embedding_model=self.embedding_model,
            umap_model=self.umap_model,
            hdbscan_model=self.hdbscan_model,
            vectorizer_model=self.vectorizer_model,
            ctfidf_model=self.ctfidf_model,
            representation_model=self.representation_model,
            nr_topics=nr_topics,
            verbose=True
        )
        
        # Ensemble classifier for better performance
        self.classifier = self._create_ensemble_classifier()
        self.scaler = StandardScaler()
        
    def _create_ensemble_classifier(self):
        """Create an ensemble classifier for better accuracy."""
        classifiers = [
            ('lr', LogisticRegression(
                max_iter=1000, 
                random_state=self.random_state,
                class_weight='balanced'
            )),
            ('rf', RandomForestClassifier(
                n_estimators=100,
                random_state=self.random_state,
                class_weight='balanced',
                n_jobs=-1
            )),
            ('svm', SVC(
                probability=True,
                random_state=self.random_state,
                class_weight='balanced'
            ))
        ]
        
        return VotingClassifier(
            estimators=classifiers,
            voting='soft',
            n_jobs=-1
        )
    
    def extract__features(self, documents, is_training=True):
        """Extract multiple types of features for better classification."""
        print("Extracting  features...")
        
        # Ensure documents are strings
        documents = [str(doc) if doc is not None else '' for doc in documents]
        
        # 1.  topic-based features
        topics, probabilities = self.topic_model.transform(documents)
        topic_features = self._get_topic_features(topics, probabilities)
        
        # 2. Document-topic similarity features
        doc_topic_sim = self._compute_document_topic_similarities(documents)
        
        # 3. TF-IDF features
        if is_training:
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=500,
                ngram_range=(1, 2),
                stop_words='english',
                min_df=2,
                max_df=0.95
            )
            tfidf_features = self.tfidf_vectorizer.fit_transform(documents).toarray()
        else:
            tfidf_features = self.tfidf_vectorizer.transform(documents).toarray()
        
        # 4. Document embeddings (reduced dimensionality)
        print("Computing document embeddings...")
        embeddings = self.embedding_model.encode(documents, show_progress_bar=True)
        
        # Reduce embedding dimensionality for efficiency
        if is_training:
            self.embedding_reducer = TruncatedSVD(n_components=50, random_state=self.random_state)
            reduced_embeddings = self.embedding_reducer.fit_transform(embeddings)
        else:
            reduced_embeddings = self.embedding_reducer.transform(embeddings)
        
        # 5. Statistical features
        stat_features = self._extract_statistical_features(documents)
        
        # Combine all features
        combined_features = np.hstack([
            topic_features,
            doc_topic_sim,
            tfidf_features,
            reduced_embeddings,
            stat_features
        ])
        
        # Ensure all features are numeric and finite
        combined_features = np.nan_to_num(combined_features, nan=0.0, posinf=0.0, neginf=0.0)
        
        print(f"Combined feature shape: {combined_features.shape}")
        return combined_features
    
    def _compute_document_topic_similarities(self, documents):
        """Compute similarity between documents and topic centroids."""
        print("Computing document-topic similarities...")
        
        try:
            # Get document embeddings
            doc_embeddings = self.embedding_model.encode(documents)
            
            # Get topic centroids (representative embeddings)
            all_topics = sorted([t for t in self.topic_model.get_topics().keys() if t != -1])
            
            if not all_topics:
                return np.zeros((len(documents), 1))
                
            # Compute topic centroids using topic words
            topic_centroids = []
            for topic_id in all_topics:
                try:
                    # Get topic words and create representative text
                    topic_words = [word for word, score in self.topic_model.get_topic(topic_id)[:10]]
                    if topic_words:
                        topic_text = ' '.join(topic_words)
                        centroid = self.embedding_model.encode([topic_text])[0]
                        topic_centroids.append(centroid)
                    else:
                        # Create zero centroid as fallback
                        topic_centroids.append(np.zeros(doc_embeddings.shape[1]))
                except Exception as e:
                    print(f"Warning: Error processing topic {topic_id}: {e}")
                    # Create zero centroid as fallback
                    topic_centroids.append(np.zeros(doc_embeddings.shape[1]))
            
            if not topic_centroids:
                return np.zeros((len(documents), 1))
                
            topic_centroids = np.array(topic_centroids)
            
            # Compute cosine similarities
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(doc_embeddings, topic_centroids)
            
            print(f"Document-topic similarity features shape: {similarities.shape}")
            return similarities
            
        except Exception as e:
            print(f"Warning: Error in similarity computation: {e}")
            return np.zeros((len(documents), 1))
    
    def _get_topic_features(self, topics, probabilities):
        """Extract  topic-based features."""
        all_topics = sorted([t for t in self.topic_model.get_topics().keys() if t != -1])
        n_topics = max(len(all_topics), 1)  # Ensure at least 1 topic
        
        print(f"Found {n_topics} topics (excluding outliers)")
        
        # Create topic features
        features = np.zeros((len(topics), n_topics))
        print("Using topic probabilities")
        # Use actual probabilities
        for i, (topic, probs) in enumerate(zip(topics, probabilities)):
            if topic != -1 and probs is not None:
                try:
                    probs_array = np.array(probs)
                    if len(probs_array) >= n_topics:
                        features[i] = probs_array[:n_topics]
                    else:
                        # Fallback to binary if probabilities are incomplete
                        if topic in all_topics:
                            topic_idx = all_topics.index(topic)
                            features[i, topic_idx] = 1.0
                except:
                    # Fallback to binary encoding
                    if topic in all_topics:
                        topic_idx = all_topics.index(topic)
                        features[i, topic_idx] = 1.0
        
        print(f"Topic features shape: {features.shape}")
        return features
    
    def _extract_statistical_features(self, documents):
        """Extract statistical features from documents."""
        features = []
        for doc in documents:
            doc = str(doc) if doc is not None else ''
            words = doc.split()
            doc_features = [
                len(doc),  # Document length
                len(words),  # Word count
                len(set(words)) if words else 0,  # Unique word count
                doc.count('.'),  # Sentence count (approximate)
                doc.count('!') + doc.count('?'),  # Exclamation/question count
                np.mean([len(word) for word in words]) if words else 0,  # Average word length
            ]
            features.append(doc_features)
        
        features_array = np.array(features)
        # Ensure all features are finite
        features_array = np.nan_to_num(features_array, nan=0.0, posinf=0.0, neginf=0.0)
        return features_array
    
    def fit(self, documents, y_supervised):
        """Fit the supervised topic model."""
        print("Preprocessing documents...")
        
        # Ensure documents are strings
        documents = [str(doc) if doc is not None else '' for doc in documents]

        print("Fitting BERTopic model...")
        self.topic_model.fit(documents)
        print("Training supervised classifier...")
        # Extract  features
        features = self.extract__features(documents, is_training=True)
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Feature selection with appropriate scorer
        n_features = min(1000, features_scaled.shape[1])  # Limit features for efficiency
        self.feature_selector = SelectKBest(f_classif, k=n_features)
        
        features_selected = self.feature_selector.fit_transform(features_scaled, y_supervised)
            
        # Train ensemble classifier
        self.classifier.fit(features_selected, y_supervised)
        
        return self
    
    def predict(self, documents):
        """Predict topics and classes for new documents."""
        # Ensure documents are strings
        documents = [str(doc) if doc is not None else '' for doc in documents]
        
        results = {}
        try:
            # Extract features for prediction
            features = self.extract__features(documents, is_training=False)
            features_scaled = self.scaler.transform(features)
                
            if self.feature_selector is not None:
                features_selected = self.feature_selector.transform(features_scaled)
            else:
                features_selected = features_scaled
            
            # Predict classes
            class_predictions = self.classifier.predict(features_selected)
            
            results['class_predictions'] = class_predictions
        except Exception as e:
            print(f"Warning: Prediction failed: {e}")
            # Return default predictions
            results['class_predictions'] = np.zeros(len(documents), dtype=int)
        
        return results
    
    def evaluate(self, X_test, y_test):
        """Comprehensive evaluation."""
        try:
            predictions = self.predict(X_test)
            y_pred = predictions['class_predictions']
            
            accuracy = accuracy_score(y_test, y_pred)
            f1_weighted = f1_score(y_test, y_pred, average='weighted')
            f1_macro = f1_score(y_test, y_pred, average='macro')
            
            return {
                'accuracy': accuracy,
                'f1_weighted': f1_weighted,
                'f1_macro': f1_macro,
                'predictions': y_pred
            }
        except Exception as e:
            print(f"Error in evaluation: {e}")
            return {
                'accuracy': 0.0,
                'f1_weighted': 0.0,
                'f1_macro': 0.0,
                'predictions': np.zeros(len(y_test))
            }
    #news loading and preprocessing
    def load_news(self,path):
        """Load and preprocess news data."""
        df = pd.read_table(f"{path}/news.tsv", header=None)
        df.columns = ['news_id', 'category', 'subcategory', 'title', 'abstract', 'url', 'title_entities', 'abstract_entities']

        # Combine title and abstract for better context
        df['text'] = (df['title'].fillna('') + ' ' + df['abstract'].fillna('')).str.lower()
            
        return df[['text', 'category']].dropna()
    def init(self):
        """init"""
        print("Loading data...")
        #Remove the # to run on as a test
        train_df = self.load_news("Mind_train")#[:10000]
        val_df = self.load_news("Mind_val")#[:3000]

        print(f"Training samples: {len(train_df)}")
        print(f"Validation samples: {len(val_df)}")
        
        # Label encoding
        all_categories = pd.concat([train_df['category'], val_df['category']])
        self.label_encoder.fit(all_categories)
        
        train_df['label'] = self.label_encoder.transform(train_df['category'])
        val_df['label'] = self.label_encoder.transform(val_df['category'])
        
        X_train = train_df['text'].tolist()
        X_test = val_df['text'].tolist()
        y_train = train_df['label'].tolist()
        y_test = val_df['label'].tolist()
        
        print(f"Number of unique categories: {len(self.label_encoder.classes_)}")
        print(f"Categories: {self.label_encoder.classes_}")
        
        # Fit the model
        print("Training model...")
        self.fit(X_train, y_train)
        
        # Evaluate
        print("\nEvaluating model...")
        results = self.evaluate(X_test, y_test)
        
        print(f"\nPerformance Metrics:")
        print(f"Accuracy: {results['accuracy']:.4f}")
        print(f"F1 Weighted: {results['f1_weighted']:.4f}")
        print(f"F1 Macro: {results['f1_macro']:.4f}")
        
        # another classification report
        unique_labels = sorted(list(set(y_test + results['predictions'].tolist())))
        target_names_filtered = [self.label_encoder.classes_[i] for i in unique_labels]
            
        print("\nDetailed Classification Report:")
        print(classification_report(
            y_test, results['predictions'],
            labels=unique_labels,
            target_names=target_names_filtered,
            zero_division=0
        ))
        
        return self
    #User prediction for user usage
    def u_predict(self, documents):
        predictions = self.predict(documents)['class_predictions']
        return self.label_encoder.inverse_transform(predictions)
    
def main():
    #delete the comments in lines 382 383 
    # example
    model_example = Supervised_TM()
    model_example.init()
    example = "I Was An NBA Wife. Here's How It Affected My Mental Health.	I felt like I was a fraud, and being an NBA wife didn't help that. In fact, it nearly destroyed me."
    prediction= model_example.u_predict([example])
    print(prediction)
    return model_example

if __name__ == "__main__":
    model = main()