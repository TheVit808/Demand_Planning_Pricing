# Model Card — Dashboard Demand Planning & Pricing

## Objetivo

Conectar previsão de demanda, exceções operacionais e avaliação do modelo em uma camada de visualização.

## Fontes

- Tabela fato diária:
- Previsões da Trilha B:
- Cenários da Trilha C:
- Dimensões:

## Granularidade

Uma linha por produto, região e data na tabela diária.

## Partições temporais

- Treino:
- Validação:
- Teste:

## Modelo selecionado

- Nome:
- Critério de seleção:
- Split de seleção:
- Horizonte:

## Métricas

- WAPE:
- MAE:
- RMSE:
- Cobertura do intervalo:

## Features

- Lags;
- Médias móveis defasadas;
- Calendário;
- Produto/região;
- Preço/promoção;
- Disponibilidade.

## Exceções

- Ruptura;
- Subprevisão;
- Sobreprevisão;
- Anomalia de dados.

## Limitações

- Dados sintéticos;
- Relações de preço exploratórias;
- Intervalos sujeitos à metodologia disponível;
- Ausência de garantia de decisão comercial;
- Possível alteração de erro por segmento;
- Dependência da qualidade das fontes.

## Uso permitido

Exploração de portfólio, demonstração técnica, estudos de model validation, Power BI e analytics.

## Uso não permitido

Não usar como recomendação financeira, comercial, de estoque ou de preço em operação real sem validação, governança e aprovação dos responsáveis.