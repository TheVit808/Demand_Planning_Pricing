# Demand Planning & Pricing

Projeto de exploração analítica para **planejamento de demanda, preço, margem e rupturas de estoque**. A base sintética combina calendário, produto, região e observações diárias para analisar padrões de consumo, comparar métodos de previsão e simular cenários de pricing.

## Escopo técnico

- **Período:** 2024-01-01 a 2025-12-31;
- **Granularidade:** uma observação diária por produto e região;
- **Fato principal:** `fact_demand_pricing_daily`;
- **Dimensões:** `dim_date` (731 dias), `dim_product` (12 produtos) e `dim_region` (5 regiões);
- **Formato:** CSV e Parquet em `data/sample/`;
- **Observações:** 43.860 linhas na tabela fato;
- **Divisão temporal:** `train`, `validation` e `test` na coluna `dataset_split`.

A tabela fato reúne calendário e feriados, produto/categoria/classe ABC, região, promoção e desconto, preços de lista/bruto/líquido, custo, estoque disponível, unidades vendidas, receita, margem, indicadores de ruptura, vendas perdidas estimadas, lags, médias móveis, tendência e flags de anomalia.

## Fluxo analítico

```text
data/sample/*.csv|parquet
          ↓
Trilha A: EDA, sazonalidade, outliers e rupturas
          ↓
Trilha B: features temporais e previsão de demanda
          ↓
Trilha C: elasticidade exploratória e simulação de pricing
          ↓
reports/ e reports/figures/
```

- [`notebooks/01_trilha_a_exploracao.ipynb`](notebooks/01_trilha_a_exploracao.ipynb): exploração, sazonalidade, rupturas e baselines;
- [`notebooks/02_trilha_b_previsao.ipynb`](notebooks/02_trilha_b_previsao.ipynb): previsão sem vazamento temporal, avaliação segmentada e exportação das previsões;
- [`notebooks/03_trilha_c_pricing.ipynb`](notebooks/03_trilha_c_pricing.ipynb): elasticidade, cenários de preço/desconto, capacidade e sensibilidade.

## Partições e prevenção de vazamento

| Partição | Período | Linhas |
|---|---|---:|
| Train | 2024-01-01 a 2024-12-31 | 21.960 |
| Validation | 2025-01-01 a 2025-06-30 | 10.860 |
| Test | 2025-07-01 a 2025-12-31 | 11.040 |

As partições são estritamente temporais. As features da Trilha B utilizam calendário, preço, desconto, promoção, disponibilidade, produto, categoria, região, lags de 1/7 dias e médias móveis de 7/28 dias. O notebook inclui asserções para impedir o uso direto de `units_sold`, receita ou margem futuras como features.

## Resultados de previsão

A comparação de validação está registrada em [`reports/trilha_b/experiments.csv`](reports/trilha_b/experiments.csv):

| Modelo | WAPE | MAE | RMSE | Observações |
|---|---:|---:|---:|---:|
| Random Forest | 0,3079 | 0,2403 | 0,3501 | 10.860 |
| Baseline sazonal 7 dias | 0,3567 | 0,2785 | 0,5585 | 10.860 |
| Ridge | 0,4728 | 0,3690 | 0,5063 | 10.860 |
| Exponential Smoothing | 0,4990 | 0,3895 | 0,5450 | 10.860 |

Com base apenas na validação, o **Random Forest** foi selecionado para a avaliação final. No teste, após ajuste com treino + validação, obteve WAPE **0,3093**, MAE **0,2689** e RMSE **0,3717** em 11.040 observações. As previsões estão em [`reports/trilha_b/predictions_test.csv`](reports/trilha_b/predictions_test.csv) e `.parquet`.

Os resultados por produto estão em [`reports/trilha_b/metrics_by_product.csv`](reports/trilha_b/metrics_by_product.csv). O erro de validação é mais alto em produtos de baixa demanda, como P011 (WAPE 1,5148), P009 (0,9017) e P003 (0,6233), o que recomenda avaliar métricas e agregações segmentadas antes de usar o modelo operacionalmente.

## Pricing e elasticidade — Trilha C

A Trilha C usa apenas linhas sem anomalias conhecidas para estimar uma elasticidade exploratória em regressão log-log entre preço líquido e unidades vendidas. A elasticidade global registrada é **-0,1788**, com R² de **0,0898**; as estimativas por produto estão em [`reports/trilha_c/elasticity_by_product.csv`](reports/trilha_c/elasticity_by_product.csv). Quando a qualidade mínima não é atendida, a simulação utiliza elasticidade fallback de `-1,20`.

A simulação opera na granularidade diária por produto/região e avalia **20 cenários** combinando:

- alteração de preço de `-20%` a `+20%`;
- desconto adicional de `0%`, `5%`, `10%` ou `20%`;
- limite geral configurado de alteração de preço de `-30%` a `+30%`;
- alerta para desconto profundo a partir de `35%`;
- demanda limitada pelo estoque disponível;
- risco de ruptura calculado por cenário.

Os principais artefatos são:

- [`reports/trilha_c/pricing_scenarios_summary.csv`](reports/trilha_c/pricing_scenarios_summary.csv): resumo agregado dos cenários;
- [`reports/trilha_c/pricing_review_table.csv`](reports/trilha_c/pricing_review_table.csv): tabela para revisão de decisão;
- [`reports/trilha_c/pricing_scenarios_by_product.csv`](reports/trilha_c/pricing_scenarios_by_product.csv): resultados por produto;
- [`reports/trilha_c/pricing_scenarios_detail.parquet`](reports/trilha_c/pricing_scenarios_detail.parquet): detalhe diário por cenário;
- [`reports/trilha_c/elasticity_sensitivity.csv`](reports/trilha_c/elasticity_sensitivity.csv): sensibilidade com multiplicadores de elasticidade `0,75`, `1,00` e `1,25`;
- [`reports/trilha_c/simulation_assumptions.json`](reports/trilha_c/simulation_assumptions.json): premissas serializadas.

No resumo atual, aumentos de preço de `+10%` a `+20%` sem desconto tendem a preservar risco de ruptura nulo e elevar margem; descontos maiores podem aumentar receita, mas reduzem margem e/ou elevam o risco de ruptura. A tabela de revisão considera aceitáveis cenários com risco de ruptura de até **20%** e desconto adicional inferior a `35%`.

> **Importante:** elasticidades e cenários são associativos e exploratórios, não estimativas causais nem recomendações comerciais. A simulação usa estoque simplificado, não modela lead time, pedidos em trânsito, concorrência ou preço de mercado. O notebook aplica limite de risco de 20% na revisão, enquanto `simulation_assumptions.json` registra `0,8`; esses parâmetros devem ser alinhados antes de qualquer uso operacional.

## Resultados exploratórios

Os baselines iniciais da Trilha A, em [`reports/trilha_a_metricas_baseline.csv`](reports/trilha_a_metricas_baseline.csv), foram avaliados sobre 11.040 observações:

| Modelo | WAPE | MAE | RMSE |
|---|---:|---:|---:|
| Naive 1 dia | 0,3573 | 0,3107 | 0,6039 |
| Sazonal 7 dias | 0,3505 | 0,3047 | 0,5975 |

A demanda mensal é mais alta em novembro e dezembro, com 3.626 e 3.789 unidades, respectivamente; a taxa mensal de ruptura observada varia aproximadamente entre 2,5% e 3,7%. Outros artefatos incluem sazonalidade, volume por produto, rupturas e a figura de demanda móvel de 28 dias em `reports/`.

## Execução local

Requisitos: Python 3.11+ e os pacotes definidos em `requirements.txt`, incluindo `statsmodels` para Exponential Smoothing.

```bash
python3 -m pip install -r requirements.txt
jupyter notebook notebooks/01_trilha_a_exploracao.ipynb
jupyter notebook notebooks/02_trilha_b_previsao.ipynb
jupyter notebook notebooks/03_trilha_c_pricing.ipynb
```

Os notebooks resolvem a raiz do projeto a partir do diretório de execução, carregam `data/sample/fact_demand_pricing_daily.parquet` e gravam/atualizam artefatos em `reports/`.

## Organização

```text
data/sample/              Dimensões e fato em CSV/Parquet
notebooks/                 Exploração, previsão e pricing (Trilhas A-C)
reports/                   Métricas, previsões, cenários e resultados
reports/trilha_b/          Experimentos e previsões de teste
reports/trilha_c/          Elasticidades, cenários e análises de sensibilidade
reports/figures/           Visualizações exportadas
requirements.txt           Dependências Python
```

> **Estado atual:** o repositório possui a base sintética e as Trilhas A, B e C implementadas em notebooks, com baselines, previsão, elasticidade exploratória e simulações exportadas. As próximas etapas são conectar pricing ao forecast, usar demanda prevista em vez de médias históricas, adicionar intervalos de previsão, backtesting com janelas móveis, estoque de segurança/lead time e validação das premissas com experimento ou teste controlado.
