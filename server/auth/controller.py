from flask import Flask, request, jsonify
from auth.service import hey
from __main__ import app

@app.route('/login/<page>', methods=['GET'])
def login(page):
    ...