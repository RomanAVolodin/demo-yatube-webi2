.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: django-migrate
django-migrate: ## apply migrations
	./manage.py migrate

.PHONY: start
start: ## start dev server
	./manage.py runserver

.PHONY: admin
admin: ## create admin user
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123123 \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python manage.py createsuperuser --noinput || true


.PHONY: make-trans
make-trans: ## make translations
	django-admin makemessages -l ru -e py -e html -i venv

.PHONY: compile-trans
compile-trans: ## compile translations
	django-admin compilemessages --exclude venv