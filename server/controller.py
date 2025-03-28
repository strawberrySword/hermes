from flask import Flask, request, jsonify
from __main__ import app

@app.route('/articles', methods=['GET'])
def get_articles():
    data = [
        {
            'id': 1,
            'title': 'Article 1',
            'content': 'This is article 1'
        },
        {
            'id': 2,
            'title': 'Article 2',
            'content': 'This is article 2'
        }
    ]
    
    return jsonify(data)