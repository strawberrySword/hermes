import db
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.update({
    "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "super-secret"),
    "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID")
})
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

import articles.controller
import auth.controller

if __name__ == '__main__':
    print("Starting the server...")
    app.run(port=5000, debug=True)
