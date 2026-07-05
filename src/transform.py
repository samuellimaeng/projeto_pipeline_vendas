import logging 
import pandas as pd

logger = logging.getLogger(__name__)

def transform_data (df : pd.DataFrame) -> pd.DataFrame:

    """
    Cleans and standardizes the extracted data.

    Steps:
        1. Standardize column names.
        2. Remove duplicate rows.
        3. Convert data types (dates, numbers).
        4. Handle null values.
        5. Remove extra spaces from text columns.
        6. Check consistency between quantidade, preco_unitario and valor_total.

    Args:
        df: raw DataFrame coming from the extraction step.

    Returns:
        pd.DataFrame: the cleaned and standardized DataFrame.

    Raises:
        ValueError: if the input DataFrame is empty.
    """

    # -> Check if the DataFrame is empty
    if df.empty:
        msg = 'The Dataframe received from transformation is empty !'
        logger.error(msg)
        raise ValueError(msg)
    
    logger.info('Starting the transformation . . .')
    df = df.copy() # -> Avoids changing the original DataFrame

    # -> Standardize column names: lowercase, no spaces, no accents
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.normalize('NFKD')
        .str.encode('ascii', errors='ignore')
        .str.decode('utf-8')
        .str.replace(' ', '_')
    )
    logger.info('Columns standardized: %s', list(df.columns))

    # -> Remove duplicate rows
    duplicated_count = df.duplicated().sum()
    if duplicated_count > 0 :
        logger.warning('Found %s duplicated rows. Removing them.', duplicated_count)
        df = df.drop_duplicates()

    # -> Convert columns to the right data types
    df['data'] = pd.to_datetime(df['data'], errors = 'coerce', dayfirst=True)
    df['quantidade'] = pd.to_numeric(df['quantidade'], errors = 'coerce')
    df['valor_total'] = pd.to_numeric(df['valor_total'], errors = 'coerce')
    df['preco_unitario'] = pd.to_numeric(df['preco_unitario'], errors = 'coerce')

    # -> Handle null values (drop rows missing critical fields)
    null_counts = df.isnull().sum()
    if null_counts.any():
        logger.warning('Null values found:\n%s', null_counts[null_counts > 0])
        df = df.dropna(subset=['id', 'data', 'quantidade', 'preco_unitario'])
        logger.info('Rows with critical nulls removed. Remaining rows: %s', len(df))


    # -> Remove extra spaces from text columns
    text_columns = ['produto', 'regiao', 'vendedor']
    for col in text_columns:
        df[col] = df[col].str.strip()


    calculated_total = df['quantidade'] * df['preco_unitario']
    incosistent = ~calculated_total.round(2).eq(df['valor_total'].round(2))

    if(incosistent.any()):
        logger.warning(
            'Found %s rows where valor_total does not match quantidade * valor_unitario',
            incosistent.sum()
        )

    # -> Business rule decided here: recalculate instead of just warning,
    # -> to keep the data consistent.

    df.loc[incosistent, 'valor_total'] = calculated_total[incosistent].round(2)
    logger.info('Recalculated valor_total for inconsistent rows.')

    logger.info('Data transformation completed successfully.')
    logger.info('Rows: %s, colums: %s.', len(df), len(df.columns))

    return df