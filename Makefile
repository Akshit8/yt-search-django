init: 
	django-admin startproject core .

create-app:
	django-admin startapp $(name)

dev:
	docker-compose up -d

create-migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate

see-sql:
	python manage.py sql $(name) $(num)

run:
	python manage.py runserver