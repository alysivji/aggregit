"""
Fetch stats from Bitbucket API

This API provides reponses with links that do not require as much
parsing as Github.

BitBucket public API has generous rate limits so do not need keys
"""

import logging
from typing import Any, Dict, List, NamedTuple

import requests

# Configuration
logger = logging.getLogger(__name__)

_HEADERS = {
    'User-Agent': 'Aggregit',
}


class Response(NamedTuple):
    """
    Holds required information from response
    """
    json: Dict[str, Any]


##################
# Helper Functions
##################

def _bitbucket_api_get(endpoint: str):
    """
    Only function that uses requests to hit the API
    """
    r = requests.get(endpoint, headers=_HEADERS)
    # TODO: would be good to have r.raise_for_status() in production
    return Response(r.json())


def _get_all_items(endpoint: str):
    """
    Handle BitBucket API Pagination
    """
    all_items = []

    url = endpoint  # first page
    while True:
        resp = _bitbucket_api_get(url)

        all_items.extend(resp.json['values'])

        if 'next' in resp.json:
            url = resp.json['next']
        else:
            return all_items


def _get_size(endpoint: str):
    """
    For endpoints that give results size in metadata as part of a JSON reponse
    """
    resp = _bitbucket_api_get(endpoint)
    return resp.json['size']


##########################
# Fetch from BitBucket API
##########################

# TODO: Use async requests to speed up response time
# discuss "Make it work. Make it right. Make it fast" during Code Review

def fetch_user_data(username):
    """
    Username can be either a team account or an individual account
    """
    user_data_endpoint = f'https://api.bitbucket.org/2.0/users/{username}'
    resp = _bitbucket_api_get(user_data_endpoint)

    if resp.json['type'] == 'error':
        team_data_endpoint = f'https://api.bitbucket.org/2.0/teams/{username}'
        resp = _bitbucket_api_get(team_data_endpoint)

    return resp.json


def fetch_num_watchers(endpoints: List[str]):
    total_watchers = 0

    for endpoint in endpoints:
        total_watchers += _get_size(endpoint)

    return total_watchers


def fetch_all_open_issues(endpoints: List[str]):
    all_issues = []
    for endpoint in endpoints:
        issues = _get_all_items(endpoint)
        all_issues.extend(issues)

    open_issues = [issue for issue in all_issues
                   if issue['state'] in ['new', 'open']]

    return open_issues


def fetch_all_commits(endpoints: List[str]):
    all_commits = []
    for endpoint in endpoints:
        commits = _get_all_items(endpoint)
        all_commits.extend(commits)

    return all_commits


####################
# Main Functionality
####################

# TODO: Could refactor Stats into Class. Create BitbucketStats subclass

def repo_stats(username: str):
    user = fetch_user_data(username)

    if 'error' in user:
        logging.error('Bitbucket account not found')
        return {'error': 'Bitbucket account not found'}

    followers_endpoint = user['links']['followers']['href']
    num_followers = _get_size(followers_endpoint)

    following_endpoint = user['links']['following']['href']
    num_following = _get_size(following_endpoint)

    all_repos_endpoint = user['links']['repositories']['href']
    all_repos = _get_all_items(all_repos_endpoint)

    # Calculate stats based on data fetched from all_repos
    original = [repo for repo in all_repos if 'parent' not in repo]
    num_original = len(original)

    forked = [repo for repo in all_repos if 'parent' in repo]
    num_forked = len(forked)

    size_of_account = sum([repo['size'] for repo in all_repos])  # kilobytes

    languages_used = [repo['language'].lower()
                      for repo in all_repos
                      if repo['language'] != '']
    languages_used = list(set(languages_used))

    # Fetch data from other endpoints and calculate stats
    watcher_endpoints = [repo['links']['watchers']['href']
                         for repo in all_repos]
    num_watchers = fetch_num_watchers(watcher_endpoints)

    # This is not like Github's issues
    issues_endpoints = [repo['links']['issues']['href']
                        for repo in all_repos
                        if repo['has_issues'] is True]
    open_issues = fetch_all_open_issues(issues_endpoints)
    num_open_issues = len(open_issues)

    commit_endpoints = [repo['links']['commits']['href']
                        for repo in all_repos
                        if 'parent' not in repo]
    all_commits_in_original_repos = fetch_all_commits(commit_endpoints)
    num_commits = len(all_commits_in_original_repos)

    # Gather stats to send back
    stats = {
        'total_original_repos': num_original,
        'total_forked_repos': num_forked,
        'total_watcher_count': num_watchers,
        'total_follower_count': num_followers,
        "total_following_count": num_following,
        'stars_recieved': 0,  # bitbucket is not very social
        'stars_given': 0,  # bitbucket is not very social
        'total_open_issues': num_open_issues,
        'total_commits_to_non_forked': num_commits,
        'total_account_size': size_of_account,
        'languages_used': languages_used,
        'repo_topics': [],  # could not find in API
    }
    return stats
