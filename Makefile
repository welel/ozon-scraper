build:
	docker build -t scraper-base -f contrib/docker/scraper/Dockerfile .
	docker compose -p ozon-scraper -f contrib/docker/docker-compose.yml build

up:
	docker compose -p ozon-scraper -f contrib/docker/docker-compose.yml up -d

down:
	docker compose -p ozon-scraper -f contrib/docker/docker-compose.yml down
