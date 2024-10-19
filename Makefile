build:
	docker build -t scraper-base -f contrib/docker/scraper/Dockerfile .
	docker compose -p ozon-scraper -f contrib/docker/docker-compose.yml build

up:
	docker compose -p ozon-scraper -f contrib/docker/docker-compose.yml up -d

down:
	docker compose -p ozon-scraper -f contrib/docker/docker-compose.yml down

install_linters:
	pip install ruff==0.7.0 mypy==1.12.0 mypy-extensions==1.0.0
