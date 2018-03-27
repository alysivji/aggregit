# Get All Movies

Get combined stats from Github and BitBucket

**URL** : `/v1/stats/combined`

**Method** : `GET`

**Auth required** : No

**Permissions required** : None

**Data constraints** : `{}`

**Query Parameters**

|Name|Description|Field Type
|---|---|---|
|`github`|Github ID to pull stats for|Required
|`bitbucket`|BitBucket ID to pull stats for|Required

## Success Responses

**Condition** : User stats successfully queried

**Code** : `200 OK`

**Sample Response**

```json
{
    "data": {
        "languages_used": [
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
            "html",
            "c++"
        ],
        "repo_topics": [
            "scraping",
            "mongodb",
            "scrapy",
            "reddit"
        ],
        "stars_given": 318,
        "stars_recieved": 32,
        "total_account_size": 21115533, // in kilobytes
        "total_commits_to_non_forked": 575,
        "total_follower_count": 56,
        "total_following_count": 28,
        "total_forked_repos": 15,
        "total_open_issues": 6,
        "total_original_repos": 50,
        "total_watcher_count": 22
    },
    "error": null
}
```

## Error Responses

**Condition** : If `bitbucket` ID or `github` ID not found on either site.

**Code** : `404 NOT FOUND`

**Content**

```json
{
    "data": null,
    "error": "BitBucket ID not found"
}
```

**Condition** : If `bitbucket` ID or `github` ID is missing from query string

**Code** : `422 UNPROCESSABLE ENTITY`

**Content**

```json
{
    "data": null,
    "error": "BitBucket ID not found"
}
```
