# 🔄 Pipeline Vendas — ETL de Dados com Python & PostgreSQL

> Do CSV bruto a uma tabela limpa e confiável no banco de dados: um pipeline de ETL completo, construído do zero para aprender (e mostrar) como dados reais são tratados na prática.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-brightgreen)

---
**Estrutura de pastas do projeto** 

<img width="359" height="713" alt="estrutura_de_pastas" src="https://github.com/user-attachments/assets/ac292ce0-367a-4a40-9a63-155bc10625d3" />

---

**Pipeline em execução (Logs)**

<img width="1017" height="235" alt="pipeline_em_execucao" src="https://github.com/user-attachments/assets/96e076d5-8050-4224-9e87-4defd95e5e90" />

---

**Testes realizados (Pytest)**

<img width="1167" height="493" alt="teste_python" src="https://github.com/user-attachments/assets/bd1b2141-6662-4e9a-9926-8534646eac56" />

---

## 📌 Sobre o projeto

Este projeto simula um cenário comum no dia a dia de quem trabalha com dados: receber um arquivo CSV bruto, cheio de inconsistências, e transformá-lo em uma base confiável, pronta para análise.

O pipeline segue o modelo clássico de **ETL (Extract, Transform, Load)**, com cada etapa isolada em seu próprio módulo, tratamento de erros específico e logging em todas as fases — do jeito que um pipeline de produção deveria ser.




## ✨ O que o pipeline faz

- **Extração** — lê o CSV de origem, validando se o arquivo existe, se não está vazio e se pode ser corretamente interpretado.
- **Transformação**
  - Padroniza nomes de colunas (minúsculas, sem espaços, sem acentos)
  - Remove linhas duplicadas
  - Converte tipos de dados (datas e números)
  - Trata valores nulos em campos críticos
  - Remove espaços extras em colunas de texto
  - Valida a consistência entre `quantidade`, `preço_unitário` e `valor_total`, recalculando quando necessário
- **Carga** — grava os dados já tratados em uma tabela do PostgreSQL, usando SQLAlchemy.
- **Logging** — cada etapa registra o que está acontecendo, incluindo alertas de dados suspeitos (duplicados, nulos, inconsistências).

## 🗂️ Estrutura do projeto

```
pipeline_vendas/
├── data/                     # Arquivos CSV de entrada (raw)
├── logs/
│   └── pipeline.log           # Log gerado a cada execução do pipeline
├── src/
│   ├── extract.py             # Extração e validação do CSV
│   ├── transform.py           # Limpeza e padronização dos dados
│   ├── load.py                 # Conexão e carga no PostgreSQL
│   ├── logger.py               # Configuração do logging
│   └── main.py                 # Ponto de entrada do pipeline
├── test/
│   ├── test_extract.py         # Testes da etapa de extração
│   ├── test_load.py            # Testes da etapa de carga
│   └── test_transform.py       # Testes da etapa de transformação
├── config.py                  # Configurações de conexão (não versionado)
├── pytest.ini                  # Configuração dos testes
├── requirements.txt            # Dependências do projeto
└── README.md
```

## ⚙️ Tecnologias utilizadas

- **Python 3.11+**
- **Pandas** — manipulação e limpeza de dados
- **SQLAlchemy** — conexão com o banco de dados
- **PostgreSQL** — armazenamento dos dados processados
- **Logging** (biblioteca padrão) — rastreabilidade do pipeline

## 🚀 Como rodar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/samuellimaeng/projeto_pipeline_vendas.git
   cd projeto_pipeline_vendas
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure a conexão com o banco em `config.py` (use `config.example.py` como modelo):
   ```python
   DB_CONFIG = {
       "user": "seu_usuario",
       "password": "sua_senha",
       "host": "localhost",
       "port": "5432",
       "database": "nome_do_banco",
   }
   ```

4. Coloque o arquivo CSV de origem em `data/raw/`.

5. Execute o pipeline:
   ```bash
   python main.py
   ```

## ✅ Testes

O projeto conta com testes automatizados (pytest) para cada etapa do pipeline:

```bash
pytest
```

- `test_extract.py` — valida os cenários de leitura do CSV (arquivo inexistente, vazio, mal formatado)
- `test_transform.py` — valida a limpeza, padronização e as regras de consistência dos dados
- `test_load.py` — valida a carga dos dados no banco

## 🧠 Decisões técnicas

Alguns pontos que exigiram atenção durante o desenvolvimento:

- **Erros tratados de forma específica** (arquivo inexistente, vazio, mal formatado) em vez de um `except` genérico — facilita o diagnóstico de problemas.
- **Inconsistências entre `quantidade x preço_unitário` e `valor_total`** são recalculadas automaticamente, priorizando a consistência dos dados ao invés de apenas alertar.
- **Logging em cada etapa**, para que qualquer falha no pipeline possa ser rastreada até a origem.

## 📈 Próximos passos

- [ ] Criar um `Dockerfile` para facilitar a reprodução do ambiente
- [ ] Adicionar agendamento automático da execução (ex: Airflow ou cron)
- [ ] Aumentar a cobertura de testes (ex: casos extremos de inconsistência de dados)

---

📫 Projeto feito como parte da minha jornada de estudos em dados. Feedbacks são muito bem-vindos!
