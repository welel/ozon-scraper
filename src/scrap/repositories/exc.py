from typing import Any


class RepositoryError(Exception):
    """Base repository error."""


class ObjectExists(RepositoryError):
    """Object exists in the reposity.

    Args:
        existing_pk (Any): Object with this PK is exists in the repo.
    """

    def __init__(self, *args, existing_pk: Any, **kwargs):
        if existing_pk is not None:
            super().__init__(
                f"Object with {existing_pk} pk is already exists."
            )
        else:
            super().__init__("Object is already exists.")


class ObjectNotExists(RepositoryError):
    """Object doesn't exist in the reposity.

    Args:
        missin_pk (Any): Object with this PK doesn't exist in the repo.
    """

    def __init__(self, *args, missin_pk: Any, **kwargs):
        if missin_pk is not None:
            super().__init__(
                f"Object with {missin_pk} pk doesn't exist."
            )
        else:
            super().__init__("Object doesn't exist.")
