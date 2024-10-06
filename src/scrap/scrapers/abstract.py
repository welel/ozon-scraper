import abc


class Scraper(abc.ABC):

    @abc.abstractmethod
    def run(self) -> None:
        """Starts scraping."""
