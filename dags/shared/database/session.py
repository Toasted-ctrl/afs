from collections.abc import Generator
from contextlib import contextmanager
from logging import getLogger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import os


log = getLogger(__name__)


@contextmanager
def get_db_session(database: str) -> Generator[Session]:
    """Provides a transactional database session scope.
    Rolls back on exception, and always closes the session.
    Does not flush by default."""

    log.info(f"Creating session with database '{database}' ...")

    db_username = os.getenv("MY_DB_USER")
    db_password = os.getenv("MY_DB_PASSWORD")
    db_hostname = os.getenv("MY_DB_HOST")
    db_dialect = os.getenv("MY_DB_DIALECT")
    db_driver = os.getenv("MY_DB_DRIVER")
    db_port = os.getenv("MY_DB_PORT")

    url = f"{db_dialect}+{db_driver}://{db_username}:{db_password}@{db_hostname}:{db_port}/{database}"
    log.info(f"Created database engine url: {url[:20]} ...")

    engine = create_engine(url=url, echo=False)
    log.info("Created database engine ...")

    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )

    session = SessionLocal()
    log.info(f"Created database session with database '{database}', yielding ...")

    try:
        yield session
    except Exception:
        log.exception(f"Encountered an exception while interacting with database '{database}', rolling back changes ...")
        session.rollback()
        raise
    finally:
        session.close()
        log.info(f"Closed session with database '{database}' ...")
        engine.dispose()
        log.info(f"Disposed database engine ...")