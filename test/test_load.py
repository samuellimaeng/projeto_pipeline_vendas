# test/test_load.py
import pandas as pd
import pytest
from unittest.mock import MagicMock
from src import load


def test_load_data_dataframe_vazio_lanca_erro():
    df_vazio = pd.DataFrame()

    with pytest.raises(ValueError):
        load.load_data(df_vazio)


def test_load_data_chama_to_sql_com_parametros_corretos(monkeypatch):
    df = pd.DataFrame({'id': [1, 2], 'produto': ['Mouse', 'Teclado']})

    mock_engine = MagicMock()
    monkeypatch.setattr(load, 'get_engine', lambda: mock_engine)

    mock_to_sql = MagicMock()
    monkeypatch.setattr(pd.DataFrame, 'to_sql', mock_to_sql)

    load.load_data(df, table_name='tabela_teste')

    mock_to_sql.assert_called_once_with(
        'tabela_teste', mock_engine, if_exists='replace', index=False
    )


def test_load_data_fecha_conexao_mesmo_com_erro(monkeypatch):
    df = pd.DataFrame({'id': [1]})

    mock_engine = MagicMock()
    monkeypatch.setattr(load, 'get_engine', lambda: mock_engine)

    def to_sql_com_erro(*args, **kwargs):
        raise Exception('Erro simulado de conexão')

    monkeypatch.setattr(pd.DataFrame, 'to_sql', to_sql_com_erro)

    with pytest.raises(Exception):
        load.load_data(df)

    mock_engine.dispose.assert_called_once()


def test_get_engine_cria_engine_com_configuracao_correta(monkeypatch):
    monkeypatch.setattr(load, 'DB_CONFIG', {
        'user': 'usuario_teste',
        'password': 'senha_teste',
        'host': 'localhost',
        'port': 5432,
        'database': 'banco_teste',
    })

    engine = load.get_engine()

    assert engine.url.username == 'usuario_teste'
    assert engine.url.host == 'localhost'
    assert engine.url.database == 'banco_teste'