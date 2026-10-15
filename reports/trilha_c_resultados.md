# Trilha C — Pricing Analytics

## Objetivo

Estimar elasticidade de forma exploratória e simular cenários de preço/desconto, receita, margem e risco de ruptura.

## Dados e período

- Fonte: fact_demand_pricing_daily.parquet
- Período-base: 01/01/2024 a 31/12/2025
- Granularidade:
- Produtos: 12
- Regiões: 5
- Linhas: 43,860

## Estimativa de elasticidade

| Nível | Elasticidade | R² | Observações | Qualidade |
|---|---:|---:|---:|---|
| Global | -0.17877665309197985 | 0.0897813852764986 |  |  |
| Produto |  |  |  |  |

Descrever a especificação log-log e os controles utilizados.

## Premissas da simulação

- Origem da elasticidade: elasticity_by_product
- Elasticidade fallback: quando houver qualidade mínima
- Limite de preço: -30% a 30%
- Limite de desconto: 35%
- Custo unitário:
- Regra de estoque:
- Limite de risco: 80%
- Tratamento de anomalias: Não aplicar.

## Cenários

| Cenário | Alteração de preço | Desconto adicional | Receita | Margem | Risco de ruptura |
|---|---:|---:|---:|---:|---:|
| P+20_D00	 | 0.2000 | 0.0000 | 1,182.5587 | 656.8525 | 0.0000 |
| P+20_D05	 | 0.2000 | 0.0500 | 1,186.8150 | 632.6152 | 0.1000 |
| P+10_D00	 | 0.1000 | 0.0000 | 1,190.4124 | 615.1547 | 0.0000 |
| P+20_D10	 | 0.2000 | 0.1000 | 1,192.4632 | 605.9781 | 0.0000 |
| P+10_D05	 | 0.1000 | 0.0500 | 1,196.4918 | 589.1199 | 0.0000 |
| P+00_D00	 | 0.0000 | 0.0000 | 1,202.5714 | 565.7582 | 0.0000 |
| P+10_D10	 | 0.1000 | 0.1000 | 1,204.0717 | 560.2791 | 0.0000 |
| P+20_D20	 | 0.2000 | 0.2000 | 1,208.9260 | 543.1427 | 0.0000 |
| P+00_D05	 | 0.0000 | 0.0500 | 1,210.6676 | 537.1820 | 0.0000 |
| P+00_D10	 | 0.0000 | 0.1000 | 1,213.3477 | 502.2505 | 0.1000 |

## Trade-off

Descrever quais cenários favorecem receita, margem ou nível de serviço.
- Cenarios que favorecem receita: P+00_D10, P-10_D00, P+10_D20
- Cenarios que favorecem margem: P+20_D00	, P+20_D05, P+10_D00
- Cenarios que favorecem nível de serviço: P+20_D00, P+20_D05, P+10_D00

## Sensibilidade

Descrever o impacto de alterar a elasticidade em 25% para mais ou para menos.

## Limitações

- Dados sintéticos;
- Elasticidade associativa, não causal;
- Possível endogeneidade de preço e promoção;
- Estoque simplificado;
- Sem lead time ou pedidos em trânsito;
- Sem concorrência ou preço de mercado;
- Cenários não são recomendações comerciais reais.

## Próximos passos

- Conectar ao forecast da Trilha B;
- Usar demanda prevista em vez de média histórica;
- Incorporar intervalos de previsão;
- Adicionar estoque de segurança e lead time;
- Criar dashboard da Trilha D;
- Validar premissas com experimento ou teste controlado.