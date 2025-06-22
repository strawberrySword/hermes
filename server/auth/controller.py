from flask import request, jsonify, g
from authlib.jose import jwt
from functools import wraps
from urllib.request import urlopen
from flask import request, jsonify
import auth.service as auth
from __main__ import app


@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = auth.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)


@app.route('/api/user/random', methods=['GET'])
def get_random_user():
    user = auth.get_random_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)


jwks = None


def get_jwks():
    global jwks
    if jwks is None:
        resp = urlopen(
            f'https://{app.config.get("AUTH0_DOMAIN")}/.well-known/jwks.json')
        jwks = resp.read()
    return jwks


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth = request.headers.get('Authorization', None)
        if auth:
            parts = auth.split()
            if parts[0].lower() == 'bearer':
                token = parts[1]
        if not token:
            return jsonify({"message": "Missing token"}), 401
        try:
            claims = jwt.decode(token, get_jwks(), claims_params={
                "aud": app.config.get("API_AUDIENCE"),
                "iss": f"https://{app.config.get("AUTH0_DOMAIN")}/"
            })
            claims.validate_exp()
        except Exception as e:
            return jsonify({"message": f"Invalid token: {str(e)}"}), 401
        g.user = claims
        return f(*args, **kwargs)
    return decorated


@app.route('/api/profile')
@requires_auth
def profile():
    claims = g.user
    sub = claims['sub']
    print(f"User claims: {claims}")
    print(f"User sub: {sub}")
    # user = User.query.filter_by(sub=sub).first()
    # if not user:
    #     user = User(
    #         sub=sub,
    #         email=claims.get('email'),
    #         name=claims.get('name'),
    #         picture=claims.get('picture')
    #     )
    #     db.session.add(user)
    #     db.session.commit()
    # return jsonify({
    #     "sub": sub,
    #     "email": user.email,
    #     "name": user.name,
    #     "picture": user.picture
    # })
