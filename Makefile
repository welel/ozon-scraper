build:
	docker build -t scraper-base -f contrib/docker/scraper/Dockerfile .
	docker compose -p ozon-scraper --env-file=.env -f contrib/docker/docker-compose.yml build

up:
	docker compose -p ozon-scraper --env-file=.env -f contrib/docker/docker-compose.yml up -d

down: export_envs
	docker compose -p ozon-scraper --env-file=.env -f contrib/docker/docker-compose.yml down
