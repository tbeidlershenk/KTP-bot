build:
	@docker compose build

up: build
	docker compose up --force-recreate
