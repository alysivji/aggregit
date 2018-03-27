from collections import abc

from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_args

from app import app
import app.adapters.bitbucket as bitbucket
import app.adapters.github as github

API_PREFIX = '/v1/stats'


##################
# Helper Functions
##################

# TODO figure out how to return responses from helper functions
# Read thru Flask docs or maybe a plugin simplifies creating REST APIs

def get_stats(service, func, username):
    """
    Get stats from service. Return 404 if user does not exist

    NOTE: this function is not plugged in, just here to show that I know what
    I need to refactor

    Parameters
    ----------
    service : str
        Service to poll
    func : function
        Service function that returns stats
    username : str
        Username to get stats for

    Returns
    -------
    dict
        Stats from service for user that exists
    """
    stats = func(username)

    output = {
        'data': None,
        'error': None,
    }

    if 'error' in stats:
        output['error'] = f'{service} ID not found'
        return jsonify(output), 404

    return output


###########
# Endpoints
###########

# TODO: Middleware to format output
# Falcon had a great framework, will need to explore Flask extensions
# Maybe FlaskRestful simplifies life?

@app.route(f'{API_PREFIX}/github/<username>')
@use_args({'username': fields.Str(location='view_args')})
def github_stats(args, **kwargs):
    stats = github.repo_stats(args['username'])

    output = {
        'data': None,
        'error': None,
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
        'data': None,
        'error': None,
    }

    if 'error' in stats:
        output['error'] = "BitBucket ID not found"
        return jsonify(output), 404

    output['data'] = stats
    return jsonify(output)


# TODO webargs is returning HTML versus JSON for 422s
# The webargs falcon plugin always returned JSON for 422s
# Investigate how to return JSON with 422s in Flask

combined_schema = {
    'github': fields.Str(location='query', required=True),
    'bitbucket': fields.Str(location='query', required=True),
}


@app.route(f'{API_PREFIX}/combined')
@use_args(combined_schema)
def aggregate_stats(args, **kwargs):
    output = {
        'data': None,
        'error': None,
    }

    github_username = args['github']
    github_stats = github.repo_stats(github_username)

    if 'error' in github_stats:
        output['error'] = "Github ID not found"
        return jsonify(output), 404

    bitbucket_username = args['bitbucket']
    bitbucket_stats = bitbucket.repo_stats(bitbucket_username)

    if 'error' in bitbucket_stats:
        output['error'] = "BitBucket ID not found"
        return jsonify(output), 404

    # Combine dictionaries
    agg_stats = {}
    for key in github_stats.keys():
        intermediate_result = github_stats[key] + bitbucket_stats[key]

        # make sure we only keep distinct items in the list
        if isinstance(intermediate_result, abc.Sequence):
            intermediate_result = list(set(intermediate_result))

        agg_stats[key] = intermediate_result

    output['data'] = agg_stats
    return jsonify(output)
