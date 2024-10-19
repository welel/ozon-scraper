import abc
import logging
from collections.abc import Iterator
from typing import Any

from pydantic import BaseModel

from scrap.config import AppConfig


Data = dict[str, Any]
LoadedData = Data | list[Data]
ValidatedData = LoadedData | BaseModel | list[BaseModel]


class Loader(abc.ABC):
    """Abstract class for data loading.

    This abstract class defines the interface for loading data.
    Subclasses must implement the `_load` method to provide specific
    loading logic.

    Attributes:
        schema: An optional Pydantic schema for data validation
            and deserialization.

    """

    schema: BaseModel | None = None

    def __init__(self) -> None:
        self.logger = logging.getLogger(AppConfig.logger_prefix + __name__)
        self._shutdown_after_load = True

    def _init_next_page(self, data: ValidatedData) -> None:  # noqa: B027
        """Initializes loading for the next page of data.

        Subclasses can override this method to handle pagination.

        Args:
            data: The loaded data from the current page.
        """

    @abc.abstractmethod
    def _load(self) -> LoadedData | None:
        """Abstract method to load data.

        This method must be implemented by subclasses to provide
        the specific logic for loading data.

        Returns:
            The loaded data, or None a resource is empty.
        """

    def load(self) -> LoadedData | None:
        """Loads data.

        This method loads data using the `_load` method and then
        processes it using optional post-processing steps, such as
        schema validation and deserialization.

        Returns:
            The loaded and processed data, or None a resource is empty.
        """
        data = self._load()
        if not data:
            return None

        data = self._after_load(data)

        if self.schema:
            data = self.schema.model_validate(data)
            if hasattr(data, "root") and isinstance(data.root, list):
                data = data.root

        if self._shutdown_after_load:
            self._shutdown()

        return data

    def _stop_expr(self, data: ValidatedData) -> bool:
        """Checks an expression to determine whether to stop loading.

        Args:
            data: The loaded data.

        Returns:
            True if loading should stop, False otherwise.
        """
        return False

    def _after_load(self, data: ValidatedData) -> ValidatedData:
        """Process data after loading `_load`.

        Args:
            data: The loaded data.

        Returns:
            Proccessed loaded data.
        """
        return data

    def iload(self) -> Iterator[LoadedData]:
        """Returns iterator to load data.

        This method provides an iterator interface for loading data
        to implement paginated loading.

        Yields:
            The loaded and processed data.
        """
        self._shutdown_after_load = False
        while True:
            data = self.load()
            if data is None:
                break

            yield data

            if self._stop_expr(data):
                break

            self._init_next_page(data)
        self._shutdown()

    def _shutdown(self) -> None:  # noqa: B027
        """Shutdown operations after loading.

        Calls after single load call: loader.load()
        or on end of iteration loader.iload().
        """
