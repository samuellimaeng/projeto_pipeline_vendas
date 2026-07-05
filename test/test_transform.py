import pandas as pd
import pytest
from src.transform import transform_data

def test_remove_linhas_com_nulos_criticos():
    df = pd.DataFrame({
        'ID': [1, 2],
        'Data': ['01/01/2024', None],  # linha 2 tem data nula
        'Produto': ['Mouse', 'Teclado'],
        'Regiao': ['Sul', 'Norte'],
        'Vendedor': ['Ana', 'Bruno'],
        'Quantidade': [1, 2],
        'Preco Unitario': [50.0, 100.0],
        'Valor Total': [50.0, 200.0]
    })
    resultado = transform_data(df)
    assert len(resultado) == 1  # só sobrou 1 linha


def test_remove_espacos_em_colunas_de_texto():
    df = pd.DataFrame({
        'ID': [1],
        'Data': ['01/01/2024'],
        'Produto': ['Mouse '],
        'Regiao': [' Sul'],
        'Vendedor': ['Ana'],
        'Quantidade': [1],
        'Preco Unitario': [50.0],
        'Valor Total': [50.0]
    })
    resultado = transform_data(df)
    assert resultado['produto'].iloc[0] == 'Mouse'
    assert resultado['regiao'].iloc[0] == 'Sul'


def test_recalcula_valor_total_inconsistente():
    df = pd.DataFrame({
        'ID': [1],
        'Data': ['01/01/2024'],
        'Produto': ['Mouse'],
        'Regiao': ['Sul'],
        'Vendedor': ['Ana'],
        'Quantidade': [3],
        'Preco Unitario': [10.0],
        'Valor Total': [999.0]  # errado de propósito (deveria ser 30.0)
    })
    resultado = transform_data(df)
    assert resultado['valor_total'].iloc[0] == 30.0


def test_lanca_erro_se_dataframe_vazio():
    df_vazio = pd.DataFrame()
    with pytest.raises(ValueError):
        transform_data(df_vazio)