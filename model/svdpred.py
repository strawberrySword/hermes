import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
from collections import defaultdict

def parse_behaviors(file_path):
    user_clicks = defaultdict(set)
    user_map = {}
    item_map = {}
    user_counter = 0
    item_counter = 0

    data, rows, cols = [], [], []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 5:
                continue

            _, user_id, _, history, impressions = parts
            if user_id not in user_map:
                user_map[user_id] = user_counter
                user_counter += 1
            u_idx = user_map[user_id]

            if history:
                for article_id in history.split():
                    if article_id not in item_map:
                        item_map[article_id] = item_counter
                        item_counter += 1
                    i_idx = item_map[article_id]
                    rows.append(u_idx)
                    cols.append(i_idx)
                    data.append(1)
                    user_clicks[user_id].add(article_id)

            for imp in impressions.split():
                article_id, label = imp.split('-')
                if article_id not in item_map:
                    item_map[article_id] = item_counter
                    item_counter += 1
                i_idx = item_map[article_id]
                rows.append(u_idx)
                cols.append(i_idx)
                data.append(int(label))
                if int(label) == 1:
                    user_clicks[user_id].add(article_id)

    interaction_matrix = csr_matrix((data, (rows, cols)), shape=(user_counter, item_counter))
    return interaction_matrix, user_map, item_map, user_clicks

def perform_svd_sparse(matrix, n_components=30):
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    user_factors = svd.fit_transform(matrix)
    item_factors = svd.components_.T
    return user_factors, item_factors

def recommend(user_id, user_factors, item_factors, user_map, item_map, reverse_item_map, user_clicks, num=5):
    if user_id not in user_map:
        raise ValueError(f"User {user_id} not found.")

    u_idx = user_map[user_id]
    user_vector = user_factors[u_idx]
    scores = np.dot(item_factors, user_vector)

    # Filter out already clicked items
    clicked = set(user_clicks.get(user_id, []))
    for i, item_id in enumerate(reverse_item_map):
        if item_id in clicked:
            scores[i] = -np.inf

    top_indices = np.argsort(scores)[-num:][::-1]
    recommendations = [reverse_item_map[i] for i in top_indices]
    return recommendations

# ------------------ MAIN ------------------

if __name__ == "__main__":
    behavior_path = "behaviorsS.tsv"  # Your path
    user_id = "U13740"               # Example user
    num_recommendations = 5

    matrix, user_map, item_map, user_clicks = parse_behaviors(behavior_path)
    reverse_item_map = [None] * len(item_map)
    for k, v in item_map.items():
        reverse_item_map[v] = k
    user_factors, item_factors = perform_svd_sparse(matrix)
    recommendations = recommend(user_id, user_factors, item_factors, user_map, item_map, reverse_item_map, user_clicks, num=num_recommendations)
    print(recommendations)