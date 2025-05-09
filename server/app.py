from flask import Flask
import db
app = Flask(__name__)

import controller

if __name__ == '__main__':
   app.run(port=5000, debug=True)