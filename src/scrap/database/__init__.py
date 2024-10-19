from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, sessionmaker

from scrap.config import DBConfig


engine = create_engine(DBConfig.url)
_session = sessionmaker(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with _session() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
