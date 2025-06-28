from flask import Flask, Response, abort, request, jsonify
import requests
import articles.service as service
from __main__ import app

from auth.service import auth_required

PAGE_SIZE = 10

@app.route('/api/articles', methods=['GET'])
@auth_required
def get_some_articles(user_email):
    return service.recommend(user_email), 200


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
