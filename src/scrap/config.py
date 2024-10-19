import logging
import logging.config
import os
import sys
from pathlib import Path, PosixPath
from typing import Any

import yaml
from dotenv import load_dotenv


load_dotenv()


def load_yaml_config(filepath: PosixPath | str) -> dict:
    """Loads yaml file by `filepath` and returns content as a dict."""
    if not Path.is_file(filepath) or not os.access(filepath, os.R_OK):
        sys.exit(1)
    with Path.open(filepath) as config_file:
        return yaml.safe_load(config_file)


class SettingField:
    """Descriptor class for accessing environment variables.

    Attributes:
        var_name (str): The name of the environment variable to fetch.
        cast_to (type): The type to cast the environment variable to.
            Defaults to `str`.
        default (Any): The default value to return if the environment
            variable is not set.
    """

    def __init__(
        self,
        var_name: str,
        cast_to: type = str,
        default: Any = None,
    ) -> None:
        self.var_name = var_name
        self.type = cast_to
        self.default = default

    def __get__(self, instance, owner) -> Any:  # noqa: ANN001
        value = None
        if self.default is not None:
            value = os.environ.get(self.var_name, self.default)
        else:
            try:
                value = os.environ[self.var_name]
            except KeyError as e:
                msg = f"'{self.var_name}' environment variable should be set!"
                raise ValueError(msg) from e

        if self.type is bool:
            return value.lower() == "true"

        try:
            return self.type(value)
        except TypeError as e:
            msg = f"Cannot cast {value} to {self.type}!"
            raise TypeError(msg) from e


UUID_LEN = 36
MD5_LEN = 32
URL_MAX_LEN = 2083


class ProjectConfig:
    base_dir = Path(__file__).resolve().parent
    project_dir = base_dir.parent.parent
    categories_data_dir = project_dir / "data" / "categories"
    logging_config_path = base_dir / "logging.yml"


logging.config.dictConfig(load_yaml_config(ProjectConfig.logging_config_path))


class AppConfig:
    app_name = "ms"  # Marketplace Scraper
    logger_prefix = f"{app_name}."


class DBConfig:
    table_prefix = f"{AppConfig.app_name}_"
    url = SettingField("DATABASE_URL")


class SeleniumConfig:
    chrome_driver_path = SettingField(
        "CHROME_DRIVER_PATH",
        default="/usr/bin/chromedriver-128",
    )
    default_user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like "
        "Gecko) Chrome/119.0.6045.123 YaBrowser/23.9.1.962 Yowser/2.5 "
        "Safari/537.36"
    )


class OzonScraperConfig:
    domain = "https://www.ozon.ru/"
    short_category_url = domain + "category/{cat_id}"
