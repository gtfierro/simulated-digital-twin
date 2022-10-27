include .env

.PHONY: build down run

build:
	 docker compose -f docker-compose.yml build

down:
	 docker compose -f docker-compose.yml down

up:
	docker compose -f docker-compose.yml up -d
	docker compose -f docker-compose.yml logs -f
