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
    if not os.path.isfile(filepath) or not os.access(filepath, os.R_OK):
        print(f"ERROR: config file '{filepath}' not eixsts or not readable\n")
        sys.exit(1)
    with open(filepath, "r") as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)


class SettingField:

    def __init__(
            self,
            var_name: str,
            cast_to: type = str,
            default: Any = None,
    ):
        self.var_name = var_name
        self.type = cast_to
        self.default = default

    def __get__(self, instance, owner):
        value = None
        if self.default is not None:
            value = os.environ.get(self.var_name, self.default)
        else:
            try:
                value = os.environ[self.var_name]
            except KeyError:
                raise ValueError(
                    f"'{self.var_name}' environment variable should be setted!"
                )

        if self.type == bool:
            return value.lower() == 'true'

        try:
            return self.type(value)
        except TypeError:
            raise TypeError(f"Cannot cast {value} to {self.type}!")


BASE_DIR = Path(__file__).resolve().parent

UUID_LEN = 36
MD5_LEN = 32
URL_MAX_LEN = 2083


logging_config_path = os.path.join(BASE_DIR, "logging.yml")
logging.config.dictConfig(load_yaml_config(logging_config_path))


class AppConfig:
    app_name = "mp"  # Marketplace Parser
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


class OzonParserConfig:
    domain = "https://www.ozon.ru/"
    short_category_url = domain + "category/{cat_id}"
