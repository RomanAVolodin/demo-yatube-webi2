django-migrate:
	./manage.py migrate --fake movies 0001
	./manage.py migrate

start:
	./manage.py runserver

admin:
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123123 \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python manage.py createsuperuser --noinput || true


make-trans:
	django-admin makemessages -l ru -e py -e html -i venv
compile-trans:
	django-admin compilemessages --exclude venv