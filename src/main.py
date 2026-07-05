from src.logger import setup_logger
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

def main():
    """Runs the ETL pipeline: extract, transform and load the data."""

    setup_logger()

    df_raw = extract_data()
    df_tratado = transform_data(df_raw)
    df_load = load_data(df_tratado)

    print(df_tratado.head())
    print(f'Pipeline executed successfully')


if __name__ == "__main__":
    main()