import pandas as pd
import vowpalwabbit as vw
from collections import defaultdict
import math
import os
from sklearn.metrics import ndcg_score, accuracy_score
import numpy as np

class MinimalVWRanker:
    def __init__(self, data_path='./Mind_train'):
        self.vw = vw.Workspace('--quiet')  # Simple regression mode
        self.categories = []
        self.news_to_cat = []
        self.user_cats = defaultdict(lambda: defaultdict(float))
        self.load_data(data_path)
    
    def load_data(self, data_path):
        # Load and process MIND data
        news_df = pd.read_csv(os.path.join(data_path, 'news.tsv'), sep='\t', header=None,
                             names=['news_id', 'category', 'subcategory', 'title', 'abstract', 'url', 'title_entities', 'abstract_entities'])
        behaviors_df = pd.read_csv(os.path.join(data_path, 'behaviors.tsv'), sep='\t', header=None,
                                  names=['impression_id', 'user_id', 'time', 'history', 'impressions'])
        
        self.news_to_cat = dict(zip(news_df['news_id'], news_df['category']))
        self.categories = list(set(news_df['category'].dropna()))
        
        # Train on user interactions
        for _, row in behaviors_df.iterrows():
            user_id = row['user_id']
            
            # Count category interactions
            if pd.notna(row['history']):
                for news_id in row['history'].split():
                    if news_id in self.news_to_cat:
                        self.user_cats[user_id][self.news_to_cat[news_id]] += 1
            
            if pd.notna(row['impressions']):
                for imp in row['impressions'].split():
                    parts = imp.split('-')
                    if len(parts) == 2 and parts[1] == '1' and parts[0] in self.news_to_cat:
                        self.user_cats[user_id][self.news_to_cat[parts[0]]] += 1
                    if len(parts) == 2 and parts[1] == '0' and parts[0] in self.news_to_cat:
                        self.user_cats[user_id][self.news_to_cat[parts[0]]] += -0.1
        
        # Train VW model - simple regression format
        for user_id, cats in self.user_cats.items():
            for cat, count in cats.items():
                if cat in self.categories:
                    score = 1.0 / (1.0 + math.exp(-count + 5))                    
                    # Simple VW format: score | label |features
                    example = f"{score} |u user_{hash(user_id)} |c {cat.replace(' ', '_')}"
                    self.vw.learn(example)
    
    def get_recommendations(self, user_id, top_k=5):
        # Predict score for each category
        scores = []
        for cat in self.categories:
            example = f"|u user_{hash(user_id)} |c {cat.replace(' ', '_')}"
            score = self.vw.predict(example)
            scores.append((cat, score))
        
        ranked = sorted(scores, key=lambda x: x[1], reverse=True)
        return [cat for cat, _ in ranked[:top_k]]
    
    def update_bad(self, user_id, category):
        if category in self.categories:
            self.user_cats[user_id][self.news_to_cat[category]] += -0.15
            count = self.user_cats[user_id][self.news_to_cat[category]]
            score = 1.0 / (1.0 + math.exp(-count + 5)) 
            example = f"{score} |u user_{hash(user_id)} |c {category.replace(' ', '_')}"
            self.vw.learn(example)
    def update_good(self, user_id, category):
        if category in self.categories:
            self.user_cats[user_id][self.news_to_cat[category]] += 1
            count = self.user_cats[user_id][self.news_to_cat[category]]
            score = 1.0 / (1.0 + math.exp(-count + 5)) 
            example = f"{score} |u user_{hash(user_id)} |c {category.replace(' ', '_')}"
            self.vw.learn(example)
    def evaluate(self,test_data_path='./Mind_val',top_k=5):
        # Load test data
        test_news_df = pd.read_csv(os.path.join(test_data_path, 'news.tsv'), sep='\t', header=None,
                                  names=['news_id', 'category', 'subcategory', 'title', 'abstract', 'url', 'title_entities', 'abstract_entities'])
        test_behaviors_df = pd.read_csv(os.path.join(test_data_path, 'behaviors.tsv'), sep='\t', header=None,
                                       names=['impression_id', 'user_id', 'time', 'history', 'impressions'])
        
        test_news_to_cat = dict(zip(test_news_df['news_id'], test_news_df['category']))
        
        # Collect evaluation data
        all_predictions = []
        all_true_labels = []
        all_ndcg_scores = []
        hit_count = 0
        total_impressions = 0
        
        for _, row in test_behaviors_df.iterrows():
            user_id = row['user_id']
            
            if pd.notna(row['impressions']):
                # Get user's predicted category preferences
                predicted_cats = self.get_recommendations(user_id, top_k)
                
                # Extract true positive interactions from impressions
                clicked_categories = []
                impression_categories = []
                
                for imp in row['impressions'].split():
                    parts = imp.split('-')
                    if len(parts) == 2 and parts[0] in test_news_to_cat:
                        news_category = test_news_to_cat[parts[0]]
                        impression_categories.append(news_category)
                        
                        if parts[1] == '1':  # Clicked
                            clicked_categories.append(news_category)
                            total_impressions += 1
                
                # Calculate hit rate (if any predicted category matches clicked categories)
                if clicked_categories:
                    if any(cat in clicked_categories for cat in predicted_cats):
                        hit_count += 1
                    
                    # Prepare data for NDCG calculation
                    if impression_categories:
                        # Create relevance scores for categories in this impression
                        relevance_scores = []
                        predicted_scores = []
                        
                        unique_cats = list(set(impression_categories))
                        for cat in unique_cats:
                            relevance_scores.append(1.0 if cat in clicked_categories else 0.0)
                            
                            # Get prediction score for this category
                            example = f"|u user_{hash(user_id)} |c {cat.replace(' ', '_')}"
                            pred_score = self.vw.predict(example)
                            predicted_scores.append(pred_score)
                        
                        if len(relevance_scores) > 1 and sum(relevance_scores) > 0:
                            # Calculate NDCG for this impression
                            try:
                                ndcg = ndcg_score([relevance_scores], [predicted_scores], k=min(top_k, len(relevance_scores)))
                                all_ndcg_scores.append(ndcg)
                            except:
                                pass
                
                # Collect category-level predictions vs actual for overall accuracy
                for cat in self.categories:
                    example = f"|u user_{hash(user_id)} |c {cat.replace(' ', '_')}"
                    pred_score = self.vw.predict(example)
                    all_predictions.append(pred_score)
                    all_true_labels.append(1.0 if cat in clicked_categories else 0.0)
        
        # Calculate metrics
        metrics = {}
        
        # Hit Rate
        metrics['hit_rate'] = hit_count / total_impressions if total_impressions > 0 else 0.0
        
        # Average NDCG
        metrics['avg_ndcg'] = np.mean(all_ndcg_scores) if all_ndcg_scores else 0.0
        
        # Coverage (how many unique categories were recommended)
        all_recommended_cats = set()
        for _, row in test_behaviors_df.iterrows():
            user_id = row['user_id']
            recommended = self.get_recommendations(user_id, top_k)
            all_recommended_cats.update(recommended)
        
        metrics['category_coverage'] = len(all_recommended_cats) / len(self.categories)
        
        # Summary statistics
        metrics['total_test_users'] = len(test_behaviors_df)
        metrics['total_impressions'] = total_impressions
        metrics['total_categories'] = len(self.categories)
        
        print("\nEvaluation Metrics:")
        for metric, value in metrics.items():
            if isinstance(value, float):
                print(f"{metric}: {value:.4f}")
            else:
                print(f"{metric}: {value}")
    def add_new_user(self, user_id):
        """Add a new user with optional interaction history."""
        self.user_cats[user_id] = defaultdict(float)
        for category in self.categories:
            self.user_cats[user_id][category] = 0.1
        
        # Train model with new user data
        for category in self.categories:
            count = self.user_cats[user_id][category]
            if count != 0:
                score = 1.0 / (1.0 + math.exp(-count + 5))
                example = f"{score} |u user_{hash(user_id)} |c {category.replace(' ', '_')}"
                self.vw.learn(example)
    
    def close(self):
        self.vw.finish()

# Usage
if __name__ == '__main__':
    ranker = MinimalVWRanker()
    users = ['U33207', 'U91836', 'U73700']  # Sample user IDs
    for user in users:
        print(f"User {user}: {ranker.get_recommendations(user,5)}")
    ranker.evaluate()
    ranker.close()