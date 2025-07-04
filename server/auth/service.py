from functools import wraps
from flask import request, jsonify, current_app
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError
import auth.repository as repository


def auth_required(f):
    """
    Decorator that extracts and decodes JWT token from Authorization header.

    Expected header format: "Authorization: Bearer <token>"

    The decoded payload is passed to the decorated function as 'current_user' parameter.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'error': 'Authorization header is required'}), 401

        # Extract token from "Bearer <token>" format
        try:
            token_type, token = auth_header.split(' ', 1)
            if token_type.lower() != 'bearer':
                return jsonify({'error': 'Invalid authorization header format. Expected: Bearer <token>'}), 401
        except ValueError:
            return jsonify({'error': 'Invalid authorization header format. Expected: Bearer <token>'}), 401

        try:
            decoded_payload = jwt.decode(token, algorithms=["RS256"],  options={
                "verify_signature": False})

            find_or_create_user(decoded_payload)

        except ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except DecodeError:
            return jsonify({'error': 'Invalid token format'}), 401
        except InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': f'Token validation failed {e}'}), 500
        print(f"User {decoded_payload['email']} authenticated successfully")
        return f(user_email=decoded_payload['email'], *args, **kwargs)

    return decorated_function


def find_or_create_user(user_data: dict):
    """
    Find a user by their email, or create a new user if not found.
    """
    user_data = {key: user_data[key] for key in [
        "name", "given_name", "family_name", "nickname", "picture", "email"] if key in user_data}
    repository.upsert_one(user_data)
