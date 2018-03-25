"""
Fetch stats from Github API
"""

from typing import Any, Dict, List, NamedTuple
import urllib

import requests

from app import app

# Configuration
_GITHUB_TOKEN = app.config['GITHUB_TOKEN']
_GITHUB_API_URL = 'https://api.github.com'
_HEADERS = {
    'User-Agent': 'Aggregit',
    'Authorization': f'token {_GITHUB_TOKEN}',
}


class Response(NamedTuple):
    """
    Holds required information from response
    """
    json: Dict[str, Any]
    headers: Dict[str, str]


##################
# Helper Functions
##################

def _extract_page_from_link_header(link):
    """
    Helper function to extract page
    """
    extracted_url = link.split('<')[1].split('>')[0]
    url_details = urllib.parse.urlparse(extracted_url)  # returns a namedtuple
    query_string = url_details.query
    params = urllib.parse.parse_qs(query_string)
    return int(params['page'][0])


_link = '<https://api.github.com/user/4369343/repos?type=all&page=2>; rel="last"'  # noqa
assert _extract_page_from_link_header(_link) == 2


def github_api_get(endpoint, *, params={}):
    """
    Given GitHub endpoint, returns JSON response and headers
    """
    # remove leading slash from endpoint if it is included
    if endpoint[0] == '/':
        endpoint = endpoint[1:]

    r = requests.get(f'{_GITHUB_API_URL}/{endpoint}',
                     headers=_HEADERS, params=params)

    return Response(r.json(), r.headers)


def get_all_items(endpoint):
    """
    Handle Github API pagination
    """
    all_items = []

    # get items from first page
    resp = github_api_get(endpoint, params={'type': 'all', 'page': 1})
    r_json = resp.json
    r_headers = resp.headers
    all_items.extend(r_json)

    # if multiple pages, fetch all items
    if r_headers.get('Link', None):
        for link in r_headers['Link'].split(', '):
            if 'rel="last"' in link:
                last_page = _extract_page_from_link_header(link)

        for page in range(2, last_page + 1):
            r_json, _ = github_api_get(endpoint,
                                       params={'type': 'all', 'page': page})

            all_items.extend(r_json)

    return all_items


#######################
# Fetch from Github API
#######################

# TODO: Can refactor into one function, but wanted to be explicit
# discuss during Code Review

# TODO: Use async requests to speed up response time
# discuss "Make it work. Make it right. Make it fast" during Code Review

def fetch_all_repos(username):
    all_repos_endpoint = f'users/{username}/repos'
    return get_all_items(all_repos_endpoint)


def fetch_all_followers(username):
    all_followers_endpoint = f'users/{username}/followers'
    return get_all_items(all_followers_endpoint)


def fetch_all_watchers(username):
    all_watchers_endpoint = f'users/{username}/subscriptions'
    return get_all_items(all_watchers_endpoint)


def fetch_all_starred_repos(username):
    starred_repos_endpoint = f'users/{username}/starred'
    return get_all_items(starred_repos_endpoint)


def fetch_all_open_issues(username):
    q = f'is:open+author:{username}+archived:false'
    r = requests.get(f'{_GITHUB_API_URL}/search/issues?q={q}')

    num_open_issues = r.json()['total_count']
    return num_open_issues


def fetch_all_commits(username, repos: List[str]):
    all_commits = []
    for repo in repos:
        repo_commits_endpoint = f'repos/{username}/{repo}/commits'
        repo_commits = get_all_items(repo_commits_endpoint)
        all_commits.extend(repo_commits)

    return all_commits


def fetch_all_languages(languages_endpoints: List[str]):
    """
    Endpoint has a different JSON response than others, so bespoke function
    """
    repo_languages = []
    for endpoint in languages_endpoints:
        r = requests.get(endpoint, headers=_HEADERS)
        repo_languages.extend(list(r.json().keys()))

    return list(set(repo_languages))


def fetch_all_topics(repo_endpoints: List[str]):
    """
    Beta feature so we require an additional header
    """
    topic_headers = dict(_HEADERS)
    topic_headers['Accept'] = 'application/vnd.github.mercy-preview+json'

    all_topics = []
    for endpoint in repo_endpoints:
        repo_topic_endpoint = f"{endpoint}/topics"
        r = requests.get(repo_topic_endpoint, headers=topic_headers)
        all_topics.extend(r.json()['names'])

    return list(set(all_topics))


####################
# Main Functionality
####################

# TODO: Refactor stats into Class where each attribute abstracts a fetch
# to the API for the specific site we want to poll
# Would be easy to refactor if I took the time to collect sample data for tests

def repo_stats(username: str):
    all_repos = fetch_all_repos(username)

    # User created repos
    original = [repo['name'] for repo in all_repos if repo['fork'] is False]
    num_original = len(original)

    # Forked repos
    forked = [repo['name'] for repo in all_repos if repo['fork'] is True]
    num_forked = len(forked)

    stars_recieved = sum([repo['stargazers_count'] for repo in all_repos])
    size_of_account = sum([repo['size'] for repo in all_repos])

    # Open Issues
    num_open_issues = fetch_all_open_issues(username)

    # commits
    all_commits_in_original_repos = fetch_all_commits(username, original)
    num_commits = len(all_commits_in_original_repos)

    # Fetch data from other endpoints
    followers = fetch_all_followers(username)
    num_followers = len(followers)

    watchers = fetch_all_watchers(username)
    num_watchers = len(watchers)

    starred_repos = fetch_all_starred_repos(username)
    num_stars_given = len(starred_repos)

    repo_language_endpoints = [repo['languages_url'] for repo in all_repos]
    languages_used = fetch_all_languages(repo_language_endpoints)

    repo_endpoints = [repo['url'] for repo in all_repos]
    repo_topics = fetch_all_topics(repo_endpoints)

    stats = {
        'total_original_repos': num_original,
        'total_forked_repos': num_forked,
        'total_watcher_count': num_watchers,
        'total_follower_count': num_followers,
        'stars_recieved': stars_recieved,
        'stars_given': num_stars_given,
        'total_open_issues': num_open_issues,
        'total_commits_to_non_forked': num_commits,
        'total_account_size': size_of_account,
        'languages_used': languages_used,
        'repo_topics': repo_topics
    }

    return stats
