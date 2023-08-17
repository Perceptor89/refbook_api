run:
	docker-compose up --build

test:
	python manage.py test

lint:
	flake8 refbook

poetry-export:
	poetry export --without-hashes --format=requirements.txt > requirements.txt