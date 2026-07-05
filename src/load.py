import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine  # -> used to connect to the database
from config import DB_CONFIG
from src.extract import extract_data
from src.transform import transform_data

logger = logging.getLogger(__name__)


def get_engine() -> Engine:
    """
    Creates and returns the connection engine for the Postgres database.

    Returns:
        Engine: a configured SQLAlchemy connection object.
    """
    connection_string = (
        f'postgresql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}'
        f'@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["database"]}'
    )
    return create_engine(connection_string)


def load_data(df: pd.DataFrame, table_name: str = 'raw_data') -> None:
    """
    Loads the processed DataFrame into a table in the Postgres database.

    Args:
        df: DataFrame with the data already processed and validated.
        table_name: name of the destination table in the database.

    Raises:
        ValueError: if the DataFrame is empty.
        Exception: if the connection or the write to the database fails.
    """

    if df.empty:
        msg = 'Cannot load an empty dataframe into the database.'
        logger.error(msg)
        raise ValueError(msg)

    engine = get_engine()

    try:
        logger.info('Connecting to the database and loading table "%s"...', table_name)

        df.to_sql(table_name, engine, if_exists='replace', index=False)

        logger.info('Table "%s" loaded successfully with %s rows.', table_name, len(df))

    except Exception:
        logger.error('Failed to load data into table "%s".', table_name, exc_info=True)
        raise

    finally:
        engine.dispose()


def run_pipeline() -> None:
    """Runs the full ETL pipeline: extract, transform and load."""
    df_raw = extract_data()
    df_processed = transform_data(df_raw)
    load_data(df_processed)
    logger.info('ETL pipeline completed successfully.')


if __name__ == '__main__':
    run_pipeline()