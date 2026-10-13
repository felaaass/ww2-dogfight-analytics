# Catálogo Técnico de Modelagem e Medidas DAX

## 1. Matriz de Relacionamentos do Star Schema

| Tabela Fato | Coluna FK | Tabela Dimensão | Coluna PK | Cardinalidade | Direção do Filtro |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `fato_vitorias` | `id_piloto` | `dim_piloto` | `id_piloto` | *:1 | Único |
| `fato_vitorias` | `id_aeronave` | `dim_aeronave` | `id_aeronave` | *:1 | Único |
| `fato_vitorias` | `id_data` | `dim_data` | `id_data` | *:1 | Único |
| `fato_vitorias` | `id_pais` | `dim_pais` | `id_pais` | *:1 | Único |
| `fato_perdas` | `id_batalha` | `dim_batalha` | `id_batalha` | *:1 | Único |
| `fato_perdas` | `id_data` | `dim_data` | `id_data` | *:1 | Único |
| `fato_perdas` | `id_pais` | `dim_pais` | `id_pais` | *:1 | Único |
| `fato_producao` | `id_pais` | `dim_pais` | `id_pais` | *:1 | Único |
| `fato_producao` | `id_data` | `dim_data` | `id_data` | *:1 | Único |

---

## 2. Medidas DAX (Tabela `_Measures`)

### Página 1: Concentração e Pareto de Ases

```dax
Total de Abates = SUM(fato_vitorias[total_vitorias])
```

```dax
Total de Pilotos = DISTINCTCOUNT(fato_vitorias[id_piloto])
```

```dax
Média de Abates por Piloto = DIVIDE([Total de Abates], [Total de Pilotos], BLANK())
```

```dax
Soma Acumulada de Abates = 
VAR CurrentWins = [Total de Abates]
VAR CurrentPilot = SELECTEDVALUE(dim_piloto[nome_piloto])
RETURN
SUMX(
    FILTER(
        ADDCOLUMNS(ALLSELECTED(dim_piloto[nome_piloto]), "@Wins", [Total de Abates]),
        [@Wins] > CurrentWins || ([@Wins] = CurrentWins && dim_piloto[nome_piloto] <= CurrentPilot)
    ),
    [@Wins]
)
```

```dax
Percentual Acumulado de Pareto = 
DIVIDE(
    [Soma Acumulada de Abates],
    CALCULATE([Total de Abates], ALLSELECTED(dim_piloto)),
    BLANK()
)
```

```dax
Coeficiente de Concentração = 
VAR TotalWins = CALCULATE([Total de Abates], ALLSELECTED(dim_piloto))
VAR TotalPilots = CALCULATE([Total de Pilotos], ALLSELECTED(dim_piloto))
VAR Top20Count = ROUNDUP(TotalPilots * 0.20, 0)
VAR Top20Wins = 
    SUMX(
        TOPN(Top20Count, ALLSELECTED(dim_piloto), [Total de Abates], DESC),
        [Total de Abates]
    )
RETURN
DIVIDE(Top20Wins, TotalWins, BLANK())
```

### Página 2: Distorção de Combate e Overclaiming

```dax
Vitórias Reivindicadas = SUM(fato_perdas[aeronaves_abatidas_reivindicadas])
```

```dax
Perdas Reais Documentadas = SUM(fato_perdas[aeronaves_perdidas])
```

```dax
Razão de Overclaiming = DIVIDE([Vitórias Reivindicadas], [Perdas Reais Documentadas], BLANK())
```

```dax
Divergência Absoluta de Abates = [Vitórias Reivindicadas] - [Perdas Reais Documentadas]
```

### Página 3: Evolução Técnica vs Atrito Industrial

```dax
Produção Total de Aeronaves = SUM(fato_producao[unidades_produzidas])
```

```dax
Total de Saídas Operacionais = SUM(fato_producao[sorties])
```

```dax
Total de Perdas em Combate = SUM(fato_producao[perdas_combate])
```

```dax
Taxa de Atrito por 1.000 Saídas = DIVIDE([Total de Perdas em Combate], [Total de Saídas Operacionais], BLANK()) * 1000
```

```dax
Razão Reposição Fabril vs Perdas = DIVIDE([Produção Total de Aeronaves], [Total de Perdas em Combate], BLANK())
```

```dax
Velocidade Máxima Média por Ano de Introdução = AVERAGE(dim_aeronave[velocidade_max_kmh])
```

---

## 3. Mapeamento de Visuais das 3 Telas

| Página | Visual Nativo | Eixos / Campos | Medidas Utilizadas |
| :--- | :--- | :--- | :--- |
| 1. Concentração e Pareto de Ases | Cartão / KPI Multi-Row | N/A | `[Total de Abates]`, `[Total de Pilotos]`, `[Média de Abates por Piloto]`, `[Coeficiente de Concentração]` |
| 1. Concentração e Pareto de Ases | Gráfico de Linhas e Colunas Agrupadas | Eixo X: `dim_piloto[nome_piloto]` | Colunas: `[Total de Abates]`, Linha: `[Percentual Acumulado de Pareto]` |
| 1. Concentração e Pareto de Ases | Gráfico de Dispersão | Detalhes: `dim_piloto[nome_piloto]`, Legenda: `dim_pais[nome]` | Eixo X: `dim_piloto[total_vitorias]`, Eixo Y: `[Total de Abates]` |
| 1. Concentração e Pareto de Ases | Matriz Detalhada | Linhas: `dim_piloto[nome_piloto]`, `dim_pais[nome]`, `dim_piloto[forca_aerea]`, `dim_piloto[aeronave_principal]` | Valores: `[Total de Abates]`, `[Percentual Acumulado de Pareto]` |
| 2. Distorção de Combate e Overclaiming | Cartão / KPI Multi-Row | N/A | `[Vitórias Reivindicadas]`, `[Perdas Reais Documentadas]`, `[Razão de Overclaiming]`, `[Divergência Absoluta de Abates]` |
| 2. Distorção de Combate e Overclaiming | Gráfico de Colunas Clusterizadas | Eixo X: `dim_batalha[nome]` | `[Vitórias Reivindicadas]`, `[Perdas Reais Documentadas]` |
| 2. Distorção de Combate e Overclaiming | Gráfico de Barras Clusterizadas | Eixo Y: `dim_pais[nome]` | `[Razão de Overclaiming]` |
| 2. Distorção de Combate e Overclaiming | Matriz de Confronto | Linhas: `dim_batalha[nome]`, `dim_data[data]`, `dim_pais[nome]` | `[Vitórias Reivindicadas]`, `[Perdas Reais Documentadas]`, `[Divergência Absoluta de Abates]`, `[Razão de Overclaiming]` |
| 3. Evolução Técnica vs Atrito Industrial | Cartão / KPI Multi-Row | N/A | `[Produção Total de Aeronaves]`, `[Total de Saídas Operacionais]`, `[Total de Perdas em Combate]`, `[Razão Reposição Fabril vs Perdas]` |
| 3. Evolução Técnica vs Atrito Industrial | Gráfico de Linhas | Eixo X: `dim_data[ano]`, Legenda: `dim_pais[nome]` | `[Produção Total de Aeronaves]` |
| 3. Evolução Técnica vs Atrito Industrial | Gráfico de Dispersão | Eixo X: `dim_aeronave[ano_entrada_servico]`, Eixo Y: `dim_aeronave[velocidade_max_kmh]`, Tamanho: `dim_aeronave[unidades_produzidas]`, Legenda: `dim_pais[nome]` | `[Velocidade Máxima Média por Ano de Introdução]` |
| 3. Evolução Técnica vs Atrito Industrial | Gráfico de Área Empilhada | Eixo X: `dim_data[ano]`, Legenda: `fato_producao[teatro]` | `[Total de Saídas Operacionais]` |
| 3. Evolução Técnica vs Atrito Industrial | Gráfico de Linhas | Eixo X: `dim_data[ano]` | `[Taxa de Atrito por 1.000 Saídas]` |
