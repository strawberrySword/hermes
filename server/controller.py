from flask import Flask, request, jsonify
import service



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
