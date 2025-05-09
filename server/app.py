from flask import Flask
from flask_cors import CORS

import db
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

import articles.controller
import auth.controller

if __name__ == '__main__':
   app.run(port=5000, debug=True)