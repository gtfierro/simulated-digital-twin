TESTCASE=multizone_office_simple_air
build:
	 docker compose -f project1-boptest/docker-compose.yml -f docker-compose.yml build

run:
	docker compose -f project1-boptest/docker-compose.yml -f docker-compose.yml up -d
	docker compose -f project1-boptest/docker-compose.yml -f docker-compose.yml logs -f
