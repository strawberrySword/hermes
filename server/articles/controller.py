from flask import Flask, request, jsonify
from articles.service import recommend
from __main__ import app

PAGE_SIZE = 10


@app.route('/api/articles/<user_id>/<page>', methods=['GET'])
def get_articles(user_id, page):
    res = jsonify({
        'data': recommend(user_id, start=int(page) * PAGE_SIZE, end=(int(page) + 1) * PAGE_SIZE),
        'previousPage': max(int(page) - 1, 0),
        'nextCursor': int(page) + 1
    })
    return res
