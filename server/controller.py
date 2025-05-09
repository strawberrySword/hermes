from flask import Flask, request, jsonify
import service
from __main__ import app

PAGE_SIZE = 10


@app.route('/api/articles/<user_id>/<page>', methods=['GET'])
def get_articles(user_id, page):
    res = jsonify({
        'data': service.recommend(user_id, start=int(page) * PAGE_SIZE, end=(int(page) + 1) * PAGE_SIZE),
        'previousPage': max(int(page) - 1, 0),
        'nextCursor': int(page) + 1
    })
    return res


@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = service.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)


@app.route('/api/user/random', methods=['GET'])
def get_random_user():
    user = service.get_random_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)
