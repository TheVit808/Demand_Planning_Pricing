# Trilha B — Resultados de previsão

## Objetivo

Comparar baseline sazonal, regressão, árvore e modelo temporal sem vazamento temporal.

## Partições

| Partição | Data inicial | Data final | Linhas |
|---|---|---|---:|
| Train |  |  |  |
| Validation |  |  |  |
| Test |  |  |  |

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
| Baseline sazonal 7d |  |  |  |  |
| Ridge |  |  |  |  |
| Random Forest |  |  |  |  |
| Exponential Smoothing |  |  |  |  |

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