.PHONY: help install run migrate seed test worker docker-build docker-up clean

help:
	@echo "WorkSphere Enterprise HRMS — Developer Commands"
	@echo "  make install     : Install Python dependencies"
	@echo "  make migrate     : Apply database migrations"
	@echo "  make seed        : Seed master demo dataset"
	@echo "  make run         : Start Django development server"
	@echo "  make test        : Run all automated test suites"
	@echo "  make worker      : Launch Celery async task worker"
	@echo "  make docker-up   : Launch Docker compose multi-container stack"

install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

seed:
	python manage.py seed_hrms_data

run:
	python main.py

test:
	python manage.py test

worker:
	celery -A worksphere worker -l info

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
