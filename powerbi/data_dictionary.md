# Data Dictionary — Camada de Dashboard

## dashboard_daily

| Coluna | Tipo Power BI | Descrição | Regra |
|---|---|---|---|
| date | Date | Data do registro | Uma data por produto-região |
| product_id | Text | Chave do produto | Filtro de produto |
| region_id | Text | Chave da região | Filtro de região |
| units_sold | Whole number | Demanda observada | Alvo histórico |
| prediction | Decimal number | Demanda prevista | Modelo da Trilha B |
| lower_bound | Decimal number | Limite inferior | Incerteza |
| upper_bound | Decimal number | Limite superior | Incerteza |
| forecast_horizon | Whole number | Horizonte | Filtro de horizonte |
| stockout_flag | True/False | Ruptura | Exceção operacional |
| revenue_brl | Decimal number | Receita | Soma em BRL |
| gross_margin_brl | Decimal number | Margem bruta | Soma em BRL |

## dashboard_exceptions

Descrever o contrato das exceções e a origem de cada regra.

## dashboard_model_metrics

Descrever WAPE, MAE, RMSE, cobertura e segmentação.

## dashboard_pricing_scenarios

Descrever preço, desconto, receita, margem e risco de ruptura.