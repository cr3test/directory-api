build: docker_test

heroku_deploy:
	heroku container:push web

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

DJANGO_MIGRATE := python manage.py migrate
FLAKE8 := flake8 . --exclude=migrations
PYTEST := pytest . --cov=. $(pytest_args)
COLLECT_STATIC := python manage.py collectstatic --noinput

test:
	$(DJANGO_MIGRATE) && $(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST)

DJANGO_WEBSERVER := \
	python manage.py migrate; \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose rm -f && docker-compose pull
DOCKER_COMPOSE_CREATE_ENVS := python env_writer.py env.json env-postgres.json

docker_run:
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose up --build

DOCKER_SET_DEBUG_ENV_VARS := \
	export DIRECTORY_PORT=8000; \
	export DIRECTORY_DEBUG=true; \
	export DIRECTORY_SECRET_KEY=debug; \
	export DIRECTORY_UI_SECRET=debug; \
	export DIRECTORY_POSTGRES_USER=debug; \
	export DIRECTORY_POSTGRES_PASSWORD=debug; \
	export DIRECTORY_POSTGRES_DB=directory_api_debug; \
    export DIRECTORY_SQS_ENROLMENT_QUEUE_NAME=debug; \
    export DIRECTORY_SQS_INVALID_ENROLMENT_QUEUE_NAME=debug; \
	export DIRECTORY_DATABASE_URL=postgres://debug:debug@postgres:5432/directory_api_debug

DOCKER_REMOVE_ALL_DIRECTORY_API := \
	docker ps -a | \
	grep -e directoryapi_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all_directory_api:
	$(DOCKER_REMOVE_ALL_DIRECTORY_API)

docker_debug: docker_remove_all_directory_api
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	docker-compose pull && \
	docker-compose build && \
	docker-compose run -d --no-deps queue_worker && \
	docker-compose run --service-ports webserver make django_webserver

docker_webserver_bash:
	docker exec -it directoryapi_webserver_1 sh

docker_queue_worker_bash:
	docker exec -it directoryapi_queue_worker_1 sh

docker_psql:
	docker-compose run postgres psql -h postgres -U debug

DOCKER_SET_DEBUG_AWS_ACCESS_ENVS := \
	export DIRECTORY_AWS_ACCESS_KEY_ID=test; \
	export DIRECTORY_AWS_SECRET_ACCESS_KEY=test

docker_test_requirements:
	pip install -r requirements_test.txt --src /usr/local/src

docker_test: docker_remove_all_directory_api
	$(DOCKER_SET_DEBUG_AWS_ACCESS_ENVS) && \
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose build && \
	docker-compose run webserver make docker_test_requirements test

docker_test_circleci: docker_test
	bash -c "if [[ $? != 0 ]]; then exit 1; fi"

DEBUG_SET_ENV_VARS := \
	export SECRET_KEY=debug; \
	export PORT=8000; \
	export DEBUG=true; \
	export DB_NAME=directory_api_debug; \
	export DB_USER=debug; \
	export DB_PASSWORD=debug

debug_webserver:
	 $(DEBUG_SET_ENV_VARS); $(DJANGO_WEBSERVER);

debug_queue_worker:
	$(DEBUG_SET_ENV_VARS); ./manage.py queue_worker

DEBUG_CREATE_DB := \
	psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$$DB_NAME'" | \
	grep -q 1 || psql -U postgres -c "CREATE DATABASE $$DB_NAME"; \
	psql -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname = '$$DB_USER'" | \
	grep -q 1 || echo "CREATE USER $$DB_USER WITH PASSWORD '$$DB_PASSWORD'; GRANT ALL PRIVILEGES ON DATABASE \"$$DB_NAME\" to $$DB_USER; ALTER USER $$DB_USER CREATEDB" | psql -U postgres

debug_db:
	$(DEBUG_SET_ENV_VARS) && $(DEBUG_CREATE_DB)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(FLAKE8) && $(PYTEST)

debug: test_requirements debug_db debug_test


.PHONY: build docker_run_test clean test_requirements docker_run docker_debug docker_webserver_bash docker_queue_worker_bash docker_psql docker_test debug_webserver debug_queue_worker debug_db debug_test debug
