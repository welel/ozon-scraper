class LoaderError(Exception):
    """Base loader error"""


class SeleniumLoaderError(LoaderError):
    """Base selenium loader error."""


class ElementNotFound(SeleniumLoaderError):
    """HTML element isn't found."""
