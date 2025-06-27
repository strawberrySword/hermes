import pandas as pd
import vowpalwabbit as vw
from collections import defaultdict
import math
import os

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
    
    def close(self):
        self.vw.finish()

# Usage
if __name__ == '__main__':
    ranker = MinimalVWRanker()
    users = ['U33207', 'U91836', 'U73700']  # Sample user IDs
    for user in users:
        print(f"User {user}: {ranker.get_recommendations(user,5)}")
    ranker.close()