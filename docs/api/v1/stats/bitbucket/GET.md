# Get BitBucket Stats

Get stats for user from BitBucket.

**URL** : `/v1/stats/bitbucket/:bitbucket_id`

**URL Parameters** : `bitbucket_id=[str]`

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
            "python"
        ],
        "repo_topics": [],
        "stars_given": 0,
        "stars_recieved": 0,
        "total_account_size": 20822093, // in kilobytes
        "total_commits_to_non_forked": 11,
        "total_follower_count": 0,
        "total_following_count": 0,
        "total_forked_repos": 2,
        "total_open_issues": 2,
        "total_original_repos": 11,
        "total_watcher_count": 12
    },
    "error": null
}
```

## Error Responses

**Condition** : If `bitbucket_id` is not a user on BitBucket.

**Code** : `404 NOT FOUND`

**Content**

```json
{
    "data": null,
    "error": "BitBucket ID not found"
}
```
