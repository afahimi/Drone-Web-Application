## Build ##
build:
	docker-compose build --parallel

## Run ##
up:
	docker-compose up && tail -f /dev/null

## Cleanup ##
down:
	docker-compose down
