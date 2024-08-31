import os
from typing import Any


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


UUID_LEN = 36
URL_MAX_LEN = 2083


class AppConfig:
    app_name = "mp"  # Marketplace Parser
    logger_prefix = f"{app_name}."


class DBConfig:
    table_prefix = f"{AppConfig.app_name}_"
    url = SettingField("DATABASE_URL")


class SeleniumConfig:
    chrome_driver_path = "/usr/bin/chromedriver-128"


class OzonParserConfig:
    domain = "https://www.ozon.ru/"
    short_cat_url = domain + "category/{cat_id}"
