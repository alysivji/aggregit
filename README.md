# Aggregit

This project will aggregate statistics from github and bitbucket.

## Setup Instructions

Requires Docker, Docker-Compose, Make.

1. Clone repo
1. Create [Github Personal Access Token](https://github.com/settings/tokens)
1. `export GITHUB_TOKEN='INSERT_TOKEN_HERE'`
1. `make build`
1. `make up`

App is live at `http://localhost:5000`

**API Endpoints**

```console
* GET http://localhost:5000/v1/stats/github/:github_id
* GET http://localhost:5000/v1/stats/bitbucket/:bitbucket_id
* GET http://localhost:5000/v1/stats/combined?github=github_id&bitbucket=bitbucket_id
```

## API Documentation

[Detailed documentation](docs/api/).

## Notes

### Asynchronous Requests

* This project would be a lot more efficient using async requests or task queues
* User Request needs to wait for `requests.get` calls to finish

### Tests

* `make test` to run
* Wrote a few tests
* Would write more tests following [this example](https://github.com/alysivji/aggregit/blob/master/tests/adapters/bitbucket_test.py#L16)
    * Mock requests
    * Have `.json` file in test directory
    * Make sure correct information is being returned

### Continuous Integration

* Hooked this up to my [drone](https://drone.io) instance

### Services

* Github API requires a Personal Access Token
* [BitBucket API limits](https://confluence.atlassian.com/bitbucket/rate-limits-668173227.html) are generous
* BitBucket isn't really a social platform, could not find a way to *star* a project

### Makefile Commands

```text
Makefile for managing the SivDev Microservice

Usage:
 make build      build images
 make up         creates containers and starts service
 make start      starts service containers
 make stop       stops service containers
 make down       stops service and removes containers

 make migrate    run migrations
 make test       run tests
 make test_cov   run tests with coverage.py
 make test_fast  run tests without migrations
 make lint       run flake8 lintery

 make attach     attach to process inside service
 make logs       see container logs
 make shell      connect to container in new bash shell
```
