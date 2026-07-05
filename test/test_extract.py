import pandas as pd
import pytest
from src.extract import extract_data


def test_extract_arquivo_inexistente():
    with pytest.raises(FileNotFoundError):
        extract_data('caminho/que/nao/existe.csv')


def test_extract_arquivo_vazio(tmp_path):
    arquivo = tmp_path / "vazio.csv"
    arquivo.write_text("")  # cria um arquivo .csv totalmente vazio

    with pytest.raises(ValueError):
        extract_data(arquivo)


def test_extract_apenas_cabecalho(tmp_path):
    arquivo = tmp_path / "so_header.csv"
    arquivo.write_text("ID,Data,Produto\n")  # só cabeçalho, sem linhas de dado

    with pytest.raises(ValueError):
        extract_data(arquivo)


def test_extract_arquivo_valido(tmp_path):
    arquivo = tmp_path / "dados.csv"
    arquivo.write_text("ID,Produto\n1,Mouse\n2,Teclado\n")

    df = extract_data(arquivo)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['ID', 'Produto']