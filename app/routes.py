from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_args

from app import app
import app.adapters.bitbucket as bitbucket
import app.adapters.github as github

API_PREFIX = '/api/v1'


# TODO: Middleware to format output
# Falcon had a great framework, will need to explore Flask extensions
# Maybe FlaskRestful simplifies life?

@app.route(f'{API_PREFIX}/github/<username>')
@use_args({'username': fields.Str(location='view_args')})
def github_stats(args, **kwargs):
    stats = github.repo_stats(args['username'])

    output = {
        'error': None,
        'data': None,
    }

    if 'error' in stats:
        output['error'] = "Github ID not found"
        return jsonify(output), 404

    output['data'] = stats
    return jsonify(output)


@app.route(f'{API_PREFIX}/bitbucket/<username>')
@use_args({'username': fields.Str(location='view_args')})
def bitbucket_stats(args, **kwargs):
    stats = bitbucket.repo_stats(args['username'])

    output = {
        'error': None,
        'data': None,
    }

    if 'error' in stats:
        output['error'] = "BitBucket ID not found"
        return jsonify(output), 404

    return jsonify(stats)
