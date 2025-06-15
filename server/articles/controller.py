from flask import Flask, request, jsonify
import articles.service as service
from articles.service import recommend, get_seen, get_liked, like_article as like
from __main__ import app

PAGE_SIZE = 10


@app.route('/api/articles/matrix-factorization/<user_id>/<page>', methods=['GET'])
def get_articles(user_id, page):
    res = jsonify({
        'data': recommend(user_id, start=int(page) * PAGE_SIZE, end=(int(page) + 1) * PAGE_SIZE),
        'previousPage': max(int(page) - 1, 0),
        'nextCursor': int(page) + 1
    })
    return res


@app.route('/api/articles/history/<user_id>/<page>', methods=['GET'])
def get_seen_articles(user_id, page):
    res = jsonify({
        'data': get_seen(user_id, start=int(page) * PAGE_SIZE, end=(int(page) + 1) * PAGE_SIZE),
        'previousPage': max(int(page) - 1, 0),
        'nextCursor': int(page) + 1
    })
    return res


@app.route('/api/articles/like/<article_id>/<user_id>', methods=['GET'])
def find_liked_article(article_id, user_id):
    article = get_liked(article_id, user_id)
    if not article:
        return jsonify({'message': 'Article not found'}), 404
    return jsonify(article), 200


@app.route('/api/articles/like/<article_id>/<user_id>', methods=['POST'])
def like_article(article_id, user_id):
    article = like(article_id, user_id)
    if not article:
        return jsonify({'message': 'Article not found'}), 404
    return jsonify(article), 200


@app.route('/api/articles/like/<article_id>/<user_id>', methods=['DELETE'])
def delete_like(article_id, user_id):
    service.delete_like(article_id, user_id)
    return "Unlike article successfully", 200
