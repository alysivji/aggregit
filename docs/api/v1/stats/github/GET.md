# Get All Movies

Get stats for user from Github.

**URL** : `/v1/stats/github/:github_id`

**URL Parameters** : `github_id=[str]`

**Method** : `GET`

**Auth required** : No

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

**Condition** : User stats successfully queried

**Code** : `200 OK`

**Sample Response**

```json
{
    "data": {
        "languages_used": [
            "c++",
            "jupyter notebook",
            "vim script",
            "ruby",
            "smarty",
            "css",
            "python",
            "makefile",
            "shell",
            "javascript",
            "mako",
            "c",
            "batchfile",
            "powershell",
            "html"
        ],
        "repo_topics": [
            "scraping",
            "mongodb",
            "reddit",
            "scrapy"
        ],
        "stars_given": 318,
        "stars_recieved": 32,
        "total_account_size": 293440, // in kilobytes
        "total_commits_to_non_forked": 564,
        "total_follower_count": 56,
        "total_following_count": 28,
        "total_forked_repos": 13,
        "total_open_issues": 4,
        "total_original_repos": 39,
        "total_watcher_count": 10
    },
    "error": null
}
```

## Error Responses

**Condition** : If `github_id` is not a user on Github.

**Code** : `404 NOT FOUND`

**Content**

```json
{
    "data": null,
    "error": "Github ID not found"
}
```
