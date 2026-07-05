from pathlib import Path  # -> works with file paths
import pandas as pd  # -> library to handle tabular data
import logging  # -> library to log messages

logger = logging.getLogger(__name__)  # -> logger for this module


def extract_data(file_path: str | Path = 'data/raw/dados_projeto.csv') -> pd.DataFrame:
    """
    Reads a CSV file and returns its content as a DataFrame.

    Args:
        file_path: path to the CSV file.

    Returns:
        pd.DataFrame: the data loaded from the file.

    Raises:
        FileNotFoundError: if the file doesn't exist.
        ValueError: if the file is empty, can't be parsed, or ends up
            with no data after being read.
    """

    file_path = Path(file_path)

    logger.info('Starting data extraction from %s...', file_path)

    # Check if the file actually exists
    if not file_path.exists():
        msg = f'The file {file_path} does not exist. Please check the path and try again.'
        logger.error(msg)
        raise FileNotFoundError(msg)

    try:
        df = pd.read_csv(file_path)  # -> reads the file into a DataFrame

    # -> file exists but has no content
    except pd.errors.EmptyDataError:
        msg = f'The file {file_path} is empty. Please check the file content and try again.'
        logger.error(msg)
        raise ValueError(msg)

    # -> file content isn't a valid CSV
    except pd.errors.ParserError:
        msg = f'Error parsing the file {file_path}. Please check the file format and try again.'
        logger.error(msg)
        raise ValueError(msg)

    # Check if the DataFrame came out empty (e.g. only headers, no rows)
    if df.empty:
        msg = f'The dataframe from {file_path} is empty. Please check the file content and try again.'
        logger.error(msg)
        raise ValueError(msg)

    logger.info('Data extracted successfully from %s.', file_path)
    logger.info('Rows: %s, columns: %s.', len(df), len(df.columns))

    return df