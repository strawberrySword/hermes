from flask import Flask, request, jsonify
from articles.service import get_all_articles
from __main__ import app

@app.route('/articles/<page>', methods=['GET'])
def get_articles(page):
    print(page)
    res = jsonify({
        'data': get_all_articles(),
        'previousPage': max(int(page) - 1, 0),
        'nextCursor': int(page) + 1
        })
    
    return res