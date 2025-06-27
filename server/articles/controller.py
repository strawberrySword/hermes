from flask import Flask, Response, abort, request, jsonify
import requests
import articles.service as service
from __main__ import app

from auth.service import auth_required

PAGE_SIZE = 10


@app.route('/api/articles/<page>', methods=['GET'])
def get_articles(user_id, page):
    res = jsonify({
        'data': service.recommend(user_id, start=int(page) * PAGE_SIZE, end=(int(page) + 1) * PAGE_SIZE),
        'previousPage': max(int(page) - 1, 0),
        'nextCursor': int(page) + 1
    })
    return res


@app.route('/api/articles', methods=['GET'])
@auth_required
def get_some_articles(current_user):
    print(f"Current user: {current_user}")
    return jsonify(service.get_some_articles()), 200


@app.route('/api/articles/history/<user_id>/<page>', methods=['GET'])
def get_seen_articles(user_id, page):
    res = jsonify({
        'data': service.get_seen(user_id, start=int(page) * PAGE_SIZE, end=(int(page) + 1) * PAGE_SIZE),
        'previousPage': max(int(page) - 1, 0),
        'nextCursor': int(page) + 1
    })
    return res


@app.route('/api/articles/like/<article_id>/<user_id>', methods=['GET'])
def find_liked_article(article_id, user_id):
    article = service.get_liked(article_id, user_id)
    if not article:
        return jsonify({'message': 'Article not found'}), 404
    return jsonify(article), 200


@app.route('/api/articles/like/<article_id>/<user_id>', methods=['POST'])
def like_article(article_id, user_id):
    article = service.like_article(article_id, user_id)
    if not article:
        return jsonify({'message': 'Article not found'}), 404
    return jsonify(article), 200


@app.route('/api/articles/like/<article_id>/<user_id>', methods=['DELETE'])
def delete_like(article_id, user_id):
    service.delete_like(article_id, user_id)
    return "Unlike article successfully", 200


@app.route('/api/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return abort(400, 'Missing "url" parameter')
    # Fetch the target URL
    resp = requests.get(url, stream=True)
    # Build a proxy response
    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    def generate():
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                yield chunk
    return Response(generate(), status=resp.status_code, headers=headers)
