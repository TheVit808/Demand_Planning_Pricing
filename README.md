# Demand Planning & Pricing

Projeto de exploração analítica para **planejamento de demanda, preço, margem e rupturas de estoque**. A base sintética combina calendário, produto, região e observações diárias para avaliar padrões de consumo e comparar baselines de previsão.

## Escopo técnico

- **Período:** 2024-01-01 a 2025-12-31;
- **Granularidade:** uma observação diária por produto e região;
- **Fato principal:** `fact_demand_pricing_daily`;
- **Dimensões:** `dim_date` (731 dias), `dim_product` (12 produtos) e `dim_region` (5 regiões);
- **Formato:** CSV e Parquet em `data/sample/`;
- **Observações:** 43.860 linhas na tabela fato;
- **Divisão analítica:** `train`, `validation` e `test` na coluna `dataset_split`.

A tabela fato reúne calendário e feriados, produto/categoria/classe ABC, região, promoção e desconto, preços de lista/bruto/líquido, custo, estoque disponível, unidades vendidas, receita, margem, indicadores de ruptura, vendas perdidas estimadas, lags, médias móveis, tendência e flags de anomalia.

## Fluxo de análise

```text
data/sample/*.csv|parquet
          ↓
notebooks/01_trilha_a_exploracao.ipynb
          ↓
EDA, sazonalidade, outliers, rupturas e baselines
          ↓
reports/ e reports/figures/
```

O notebook utiliza pandas, NumPy, Matplotlib, Seaborn e scikit-learn. Os relatórios derivados incluem sazonalidade mensal, volume por produto, métricas por produto/região, rupturas e uma figura de demanda móvel de 28 dias.

## Resultados de referência

Os baselines registrados em `reports/trilha_a_metricas_baseline.csv` foram avaliados sobre 11.040 observações:

| Modelo | WAPE | MAE | RMSE |
|---|---:|---:|---:|
| Naive 1 dia | 0,3573 | 0,3107 | 0,6039 |
| Sazonal 7 dias | 0,3505 | 0,3047 | 0,5975 |

O baseline sazonal de 7 dias apresenta melhora marginal sobre o naive de 1 dia. A demanda mensal é mais alta em novembro e dezembro, com 3.626 e 3.789 unidades, respectivamente; a taxa mensal de ruptura observada varia aproximadamente entre 2,5% e 3,7%.

## Execução local

Requisitos: Python 3.11+ e os pacotes definidos em `requirements.txt`.

```bash
python3 -m pip install -r requirements.txt
jupyter notebook notebooks/01_trilha_a_exploracao.ipynb
```

O notebook resolve a raiz do projeto a partir do diretório de execução, carrega `data/sample/fact_demand_pricing_daily.parquet` e grava/atualiza artefatos em `reports/`.

## Organização

```text
data/sample/              Dimensões e fato em CSV/Parquet
notebooks/                 Exploração da Trilha A
reports/                   Métricas, tabelas, resultados e figuras
reports/figures/           Visualizações exportadas
requirements.txt           Dependências Python
```

> **Estado atual:** o repositório contém a base sintética e a exploração/baseline da Trilha A. O relatório `reports/trilha_a_resultados.md` ainda possui campos de documentação não preenchidos, e as próximas etapas previstas são engenharia de atributos, modelos de previsão, intervalos de confiança e simulações de preço/desconto.
