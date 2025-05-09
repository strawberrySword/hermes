from flask import Flask, request, jsonify
import service
from __main__ import app

@app.route('/articles/<user_id>', methods=['GET'])
def get_articles(user_id):
    return jsonify(service.recommend(user_id))