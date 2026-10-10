# Medidas DAX

Catálogo de medidas para modelo tabular.  
Tabela de suporte: `_Medidas`.

---

## 1. Ases e Performance Individual

### Total de Vitórias Aéreas
```dax
Total Vitorias = 
SUM ( fato_vitorias[total_vitorias] )
```

### Total de Ases Cadastrados
```dax
Total Ases = 
DISTINCTCOUNT ( fato_vitorias[id_piloto] )
```

### Média de Vitórias por Ás
```dax
Media Vitorias por As = 
DIVIDE ( 
    [Total Vitorias], 
    [Total Ases], 
    BLANK() 
)
```

### Ranking Dinâmico de Ases
```dax
Ranking Dinamico Ases = 
IF (
    HASONEVALUE ( dim_piloto[nome_piloto] ),
    RANKX (
        ALLSELECTED ( dim_piloto[nome_piloto] ),
        [Total Vitorias],
        ,
        DESC,
        Dense
    )
)
```

### Percentual Acumulado de Vitórias (Pareto)
```dax
Pareto % Vitorias = 
VAR TotalGeral = 
    CALCULATE ( 
        [Total Vitorias], 
        ALLSELECTED ( dim_piloto ) 
    )
VAR RankingAtual = [Ranking Dinamico Ases]
VAR VitoriasAcumuladas = 
    SUMX (
        TOPN (
            RankingAtual,
            ALLSELECTED ( dim_piloto ),
            [Total Vitorias],
            DESC
        ),
        [Total Vitorias]
    )
RETURN
    DIVIDE ( VitoriasAcumuladas, TotalGeral, BLANK() )
```

---

## 2. Batalhas, Perdas e Overclaiming

### Total de Aeronaves Perdidas
```dax
Total Aeronaves Perdidas = 
SUM ( fato_perdas[aeronaves_perdidas] )
```

### Total de Abates Reivindicados
```dax
Total Abates Reivindicados = 
SUM ( fato_perdas[aeronaves_abatidas_reivindicadas] )
```

### Razão Reivindicações vs. Perdas
```dax
Razao Reivindicacoes vs Perdas = 
DIVIDE ( 
    [Total Abates Reivindicados], 
    [Total Aeronaves Perdidas], 
    BLANK() 
)
```

### Discrepância Absoluta de Overclaiming
```dax
Distorcao Overclaiming = 
[Total Abates Reivindicados] - [Total Aeronaves Perdidas]
```

---

## 3. Produção Industrial e Atrito

### Total de Aeronaves Produzidas
```dax
Total Producao Aeronaves = 
SUM ( fato_producao[unidades_produzidas] )
```

### Total de Sorties
```dax
Total Sorties = 
SUM ( fato_producao[sorties] )
```

### Taxa de Atrito por Sortie (%)
```dax
Taxa Atrito por Sortie % = 
DIVIDE ( 
    SUM ( fato_producao[perdas_combate] ), 
    [Total Sorties], 
    BLANK() 
) * 100
```

---

## 4. Time Intelligence

### Produção no Ano Anterior
```dax
Producao Ano Anterior = 
CALCULATE ( 
    [Total Producao Aeronaves], 
    SAMEPERIODLASTYEAR ( dim_data[data] ) 
)
```

### Variação Anual de Produção (YoY %)
```dax
Variacao YoY Producao % = 
VAR ValorAtual = [Total Producao Aeronaves]
VAR ValorAnterior = [Producao Ano Anterior]
RETURN
    DIVIDE ( 
        ValorAtual - ValorAnterior, 
        ValorAnterior, 
        BLANK() 
    ) * 100
```

### Média Móvel de Perdas (3 Períodos)
```dax
Media Movel Perdas 3P = 
AVERAGEX (
    DATESINPERIOD (
        dim_data[data],
        LASTDATE ( dim_data[data] ),
        -3,
        YEAR
    ),
    [Total Aeronaves Perdidas]
)
```

---

## 5. Parâmetro de Campos (Field Parameter)

```dax
Parametro Metricas = {
    ("Total de Vitórias", NAMEOF('_Medidas'[Total Vitorias]), 0),
    ("Abates Reivindicados", NAMEOF('_Medidas'[Total Abates Reivindicados]), 1),
    ("Aeronaves Perdidas", NAMEOF('_Medidas'[Total Aeronaves Perdidas]), 2),
    ("Aeronaves Produzidas", NAMEOF('_Medidas'[Total Producao Aeronaves]), 3)
}
```
