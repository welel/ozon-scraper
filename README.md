# Ozon Scraper

This project allows scraping data about products, review and review media from the Ozon website. Selenium is used for scraping, and PostgreSQL is used for data storage.


# 🛠️ Requirements

- Python 3.12+
- Docker & Docker Compose
- Chrome Browser
- [Chrome Driver](https://googlechromelabs.github.io/chrome-for-testing/) for your Chrome version


# 🏗️ Installation

- [Create virtual environment and activate it](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) and [install dependencies](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#using-requirements-files).

    ```bash
    python3.12 -m venv env
    source env/bin/activate
    pip install --upgrade pip && pip install -r requirements.txt
    ```

- Copy/rename `.env.dist` to `.env` and fill in the required data.

    ```bash
    cp .env.dist .env
    ```

- Build the Docker images for the project.

    ```bash
    docker build -t scraper-base -f contrib/docker/scraper/Dockerfile .
    docker compose -p ozon-scraper --env-file .env -f contrib/docker/docker-compose.yml build
    ```

- Start the Docker containers. This will initialize the database and run migrations.

    ```bash
    docker compose -p ozon-scraper --env-file .env -f contrib/docker/docker-compose.yml up -d
    ```

- Update the `DATABASE_URL` in the `.env` file to point to the database via the exposed port. Change the db host in to `localhost`.

- Export the environment variables to your shell session.

    ```bash
    source contrib/scripts/export_env.sh
    ```
- Use management commands (start with the `--help` flag to get more information about management commands).

    ```bash
    cd src/
    python -m scrap.manage --help
    ```

## Scraping Steps

> **Note:** Management commands are run from the `./src` directory.

1. **Load categories into the database.**

    The category data is located in the `./data/categories` folder. [More about the dataset](data/categories/README.md). To load the categories into the database, use the following management command. This command will populate the category and category meta tables.

    ```bash
    python -m scrap.manage load_ozon_categories_from_api_results
    ```

2. **Configure categories.**

    After loading, modify the `ms_scraper_ozon_category_meta` table using raw SQL queries or a database tool like [DBeaver](https://dbeaver.io/). Set the `is_parsing_enabled` column to `TRUE` and assign a `parsing_priority` (lower values are processed first) to the categories you want to scrape.

3. **Scrape category pages.**

    This command walks through category pages, collecting product data.

    ```bash
    python -m scrap.manage scrape_ozon_category_pages
    ```

4. **Scrape product reviews.**

    This command goes through the products and collects reviews and associated media.

    ```bash
    python -m scrap.manage scrape_ozon_product_reviews_from_state
    ```
