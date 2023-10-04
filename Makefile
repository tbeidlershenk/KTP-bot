TAG = jlgingrich/ktp-qwerty

latest:
# Before building, make sure requirements are updated
	@.venv/bin/pip freeze > requirements.txt
	@docker compose build

up:
	docker compose build
	docker compose up

venv:
# Sets up a local venv with the project requirements
	@python3 -m venv .venv
	@.venv/bin/pip install -r requirements.txt

clean:
# Remove all docker images with the base tag
	@docker images -a | grep "${TAG}*" | awk '{print $$1 ":" $$2}' | xargs docker rmi