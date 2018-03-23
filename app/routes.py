from flask import jsonify

from app import app

API_PREFIX = '/api/v1'


@app.route(f'{API_PREFIX}/')
@app.route(f'{API_PREFIX}/index')
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return jsonify(posts)
