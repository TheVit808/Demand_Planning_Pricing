# Trilha B — Resultados de previsão

## Objetivo

Comparar baseline sazonal, regressão, árvore e modelo temporal sem vazamento temporal.

## Partições

| Partição | Data inicial | Data final | Linhas |
|---|---|---|---:|
| Train |01/01/2024 | 31/12/2024 | 21.960 |
| Validation | 01/01/2025 | 30/06/2025 | 10.860 |
| Test | 01/07/2024 | 31/12/2025 | 11.040 |

## Features

- Lags de 1 e 7 dias;
- Médias móveis de 7 e 28 dias;
- Calendário;
- Preço e desconto;
- Promoção;
- Disponibilidade;
- Produto, categoria e região.

## Comparação na validação

| Modelo | WAPE | MAE | RMSE | Observações |
|---|---:|---:|---:|---:|
| Baseline sazonal 7d | 0,3567 | 0,2785 | 0,5585 | 10.860 |
| Ridge | 0,4728 | 0,3690 | 0,5063 | 10.860 |
| Random Forest | 0,3079 | 0,2403 | 0,3501 | 10.860 |
| Exponential Smoothing | 0,4990 | 0,3895 | 0,5450 | 10.860 |

## Avaliação por segmento

Descrever os produtos, regiões e categorias com maior erro.

## Vazamento temporal

Descrever como as partições e features foram protegidas contra informação futura.

## Modelo selecionado

Registrar a justificativa baseada na validação, não no teste.

## Limitações

- Dados sintéticos;
- Previsão inicial de um passo à frente;
- Estoque e promoções podem não estar disponíveis com a mesma antecedência na operação real;
- Elasticidade e relações de preço não devem ser interpretadas como causais.

## Próximos passos

- Implementar intervalos de previsão;
- Criar backtesting com janelas móveis;
- Avaliar horizontes de 7, 14 e 28 dias;
- Conectar previsões ao dashboard da Trilha D;
- Avançar para simulação de pricing da Trilha C.