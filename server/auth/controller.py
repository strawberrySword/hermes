from flask import Flask, request, jsonify
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
