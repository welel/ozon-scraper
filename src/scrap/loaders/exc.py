class LoaderError(Exception):
    """Base loader error"""


class SeleniumLoaderError(LoaderError):
    """Base selenium loader error."""


class ElementNotFound(SeleniumLoaderError):
    """HTML element isn't found."""

    def __init__(self, not_found_element: str) -> None:
        super().__init__(f"{not_found_element} element isn't found")
