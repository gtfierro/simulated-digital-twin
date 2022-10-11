TESTCASE=multizone_office_simple_air

.PHONY: build down run

build:
	 docker compose -f project1-boptest/docker-compose.yml -f docker-compose.yml build

down:
	 docker compose -f project1-boptest/docker-compose.yml -f docker-compose.yml down

run:
	docker compose -f project1-boptest/docker-compose.yml -f docker-compose.yml up -d
	docker compose -f project1-boptest/docker-compose.yml -f docker-compose.yml logs -f
