help:
	@echo 'Makefile for managing web application                        '
	@echo '                                                             '
	@echo 'Usage:                                                       '
	@echo ' make build      build images                                '
	@echo ' make up         creates containers and starts service       '
	@echo ' make start      starts service containers                   '
	@echo ' make stop       stops service containers                    '
	@echo ' make down       stops service and removes containers        '
	@echo '                                                             '
	@echo ' make migrate    run migrations                              '
	@echo ' make test       run tests                                   '
	@echo ' make test_cov   run tests with coverage.py                  '
	@echo ' make test_fast  run tests without migrations                '
	@echo ' make lint       run flake8 linter                           '
	@echo '                                                             '
	@echo ' make attach     attach to process inside service            '
	@echo ' make logs       see container logs                          '
	@echo ' make shell      connect to app container in new bash shell  '
	@echo ' make dbshell    connect to postgres inside db container     '
	@echo '                                                             '

build:
	docker-compose build

up:
	docker-compose up -d web

start:
	docker-compose start web

stop:
	docker-compose stop

down:
	docker-compose down

attach: ## Attach to web container
	docker attach $(docker-compose ps -q web)

logs:
	docker-compose logs -f web

shell: ## Shell into web container
	docker-compose exec -it web bash

dbshell: ## Shell into postgres process inside db container
	echo 'Need to add db'

migrate: up
	echo 'Need to add migrations'

test: migrate
	docker-compose exec web pytest

test_cov: migrate
	docker-compose exec web pytest --verbose --cov

test_cov_view: migrate
	docker-compose exec web pytest --cov --cov-report html && open ./htmlcov/index.html

test_fast: ## Can pass in parameters using p=''
	docker-compose exec web pytest $(p)

# Flake 8
# options: http://flake8.pycqa.org/en/latest/user/options.html
# codes: http://flake8.pycqa.org/en/latest/user/error-codes.html
lint: up
	docker-compose exec web flake8
