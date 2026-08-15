from airflow.exceptions import AirflowConfigException
from logging import getLogger
import os


log = getLogger(__name__)


def get_engine_url(
    db_database: str,
    db_username: str = os.getenv("MY_DB_USER"),
    db_password: str = os.getenv("MY_DB_PASSWORD"),
    db_hostname: str = os.getenv("MY_DB_HOST"),
    db_dialect: str = os.getenv("MY_DB_DIALECT"),
    db_driver: str = os.getenv("MY_DB_DRIVER"),
    db_port: str = os.getenv("MY_DB_PORT")
) -> str:
    """Builds a database engine URL."""

    args = locals()
    missing = [name for name, value in args.items() if value is None]
    if missing:
        raise AirflowConfigException(
            f"Missing variables to create database engine URL: {', '.join(missing)} ... "
            f"Please double check the config."
        )

    log.debug(f"Creating engine for database '{db_database}' ...")

    url = f"{db_dialect}+{db_driver}://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_database}"

    log.debug("Returning engine ...")

    return url