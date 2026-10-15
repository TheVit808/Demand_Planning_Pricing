# Trilha A — Resultados da exploração

## Período e granularidade

- Período analisado: 01/01/2024 a 31/12/2025
- Granularidade: uma observação diária por produto e região
- Número de observações: 43.860 linhas na tabela fato

## Qualidade

- Duplicidades: 0
- Nulos: 0
- Reconciliação de receita:
- Reconciliação de margem:

## Sazonalidade

- Meses de maior demanda: Novembro - DezembroD
 Efeito de fim de semana:
- Efeito de feriados:
- Efeito promocional:

## Outliers

- Método utilizado: IQR
- Quantidade identificada: 915
- Anomalias conhecidas:
- Critério de tratamento:

## Rupturas

- Taxa geral:
- Produtos críticos: 15
- Regiões críticas:
- Vendas perdidas estimadas:

## Baseline

| Modelo | WAPE | MAE | RMSE |
|---|---:|---:|---:|
| Naive 1d | 0,3573 | 0,3107 | 0,6039 |
| Sazonal 7d | 0,3505 | 0,3047 | 0,5975 |

## Próximos passos

- Comparar regressão e árvore na Trilha B;
- Criar features de calendário e preço;
- Avaliar intervalos de previsão;
- Preparar simulações de preço e desconto;
- Publicar indicadores no Power BI.