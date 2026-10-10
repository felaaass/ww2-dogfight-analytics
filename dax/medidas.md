# Medidas DAX — Projeto Ases e Atrito

Este documento contém todas as fórmulas DAX prontas para uso no Power BI Desktop.  
As medidas estão organizadas por contexto analítico e utilizam boas práticas de modelagem:
- Uso explícito de `DIVIDE` para prevenção de divisão por zero.
- Uso de variáveis (`VAR ... RETURN`) para otimização de cache e legibilidade.
- Time Intelligence baseado na `dim_data`.
- Field Parameter para alternância dinâmica de métricas.

---

## 1. Tabela Dedicada de Medidas

> [!TIP]
> **Boas Práticas de Governança no Power BI:**  
> Crie uma tabela vazia chamada `_Medidas` (via botão "Inserir Dados") para centralizar todas as medidas calculadas em pastas de exibição.

---

## 2. Medidas de Ases e Performance Individual

### 2.1 Total de Vitórias Aéreas
```dax
Total Vitorias = 
SUM ( fato_vitorias[total_vitorias] )
```
*Descrição:* Soma total de vitórias aéreas confirmadas no contexto de filtro atual.

### 2.2 Total de Ases Cadastrados
```dax
Total Ases = 
DISTINCTCOUNT ( fato_vitorias[id_piloto] )
```
*Descrição:* Contagem distinta de pilotos com status de ás (mínimo de 5 vitórias homologadas).

### 2.3 Média de Vitórias por Ás
```dax
Media Vitorias por As = 
DIVIDE ( 
    [Total Vitorias], 
    [Total Ases], 
    BLANK() 
)
```
*Descrição:* Média aritmética de abates por piloto no contexto selecionado.

### 2.4 Ranking Dinâmico de Ases (`RANKX`)
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
*Descrição:* Ranqueia dinamicamente os ases com base na seleção de filtros ativos (país, força aérea, aeronave ou teatro), recalculando a posição relativa instantaneamente.

### 2.5 Percentual Acumulado de Vitórias (Curva de Pareto)
```dax
Pareto % Vitorias = 
VAR TotalGeral = 
    CALCULATE ( 
        [Total Vitorias], 
        ALLSELECTED ( dim_piloto ) 
    )
VAR VitoriasPilotoAtual = [Total Vitorias]
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
*Descrição:* Calcula o percentual acumulado de vitórias para alimentar o gráfico de Pareto, permitindo observar a clássica concentração onde os top 20% dos pilotos acumulam mais de 60% dos abates.

---

## 3. Medidas de Batalhas, Perdas e Overclaiming

### 3.1 Total de Aeronaves Perdidas
```dax
Total Aeronaves Perdidas = 
SUM ( fato_perdas[aeronaves_perdidas] )
```
*Descrição:* Soma das perdas reais documentadas sofridas no contexto filtrado.

### 3.2 Total de Abates Reivindicados
```dax
Total Abates Reivindicados = 
SUM ( fato_perdas[aeronaves_abatidas_reivindicadas] )
```
*Descrição:* Soma dos abates declarados por pilotos e artilheiros em relatórios de missão (*kills claimed*).

### 3.3 Razão entre Reivindicações e Perdas Próprias
```dax
Razao Reivindicacoes vs Perdas = 
DIVIDE ( 
    [Total Abates Reivindicados], 
    [Total Aeronaves Perdidas], 
    BLANK() 
)
```
*Descrição:* Proporção entre o que uma força aérea declarou ter abatido em relação ao que ela própria perdeu. Valores > 1 indicam saldo positivo declarado.

### 3.4 Discrepância de Overclaiming (Distorção Histórica)
```dax
Distorcao Overclaiming = 
[Total Abates Reivindicados] - [Total Aeronaves Perdidas]
```
*Descrição:* Diferença líquida absoluta entre as reivindicações de combate e as perdas aceitas.

---

## 4. Medidas de Produção, Sorties e Esforço de Guerra

### 4.1 Total de Aeronaves Produzidas
```dax
Total Producao Aeronaves = 
SUM ( fato_producao[unidades_produzidas] )
```
*Descrição:* Soma das unidades fabris de aeronaves militares entregues e aceitas.

### 4.2 Total de Sorties (Saídas Operacionais)
```dax
Total Sorties = 
SUM ( fato_producao[sorties] )
```
*Descrição:* Total de decolagens operacionais de combate registradas (dados oficiais USAAF).

### 4.3 Taxa de Atrito por Sortie
```dax
Taxa Atrito por Sortie % = 
DIVIDE ( 
    SUM ( fato_producao[perdas_combate] ), 
    [Total Sorties], 
    BLANK() 
) * 100
```
*Descrição:* Percentual de aeronaves perdidas a cada saída operacional de combate. Mede diretamente a periculosidade do teatro operacional.

---

## 5. Medidas de Inteligência Temporal (Time Intelligence)

### 5.1 Produção no Ano Anterior (`SAMEPERIODLASTYEAR`)
```dax
Producao Ano Anterior = 
CALCULATE ( 
    [Total Producao Aeronaves], 
    SAMEPERIODLASTYEAR ( dim_data[data] ) 
)
```
*Descrição:* Volume fabril do mesmo período no ano civil antecedente.

### 5.2 Variação Percentual Ano a Ano (YoY)
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
*Descrição:* Taxa de expansão ou retração anual da indústria aeronáutica beligerante.

### 5.3 Média Móvel de Perdas em Batalhas (3 Períodos)
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
*Descrição:* Suaviza oscilações temporais das perdas para revelar a tendência de atrito acumulado.

---

## 6. Field Parameter para Alternância Dinâmica de Métrica

Para permitir que o usuário alterne dinamicamente em um gráfico de barras qual indicador deseja inspecionar (ex.: alternar entre `Total Vitorias`, `Aeronaves Perdidas`, `Abates Reivindicados` ou `Produção`), utilize um **Parâmetro de Campos**:

### Configuração no Power BI:
1. Vá na guia **Modelagem** -> **Novo Parâmetro** -> **Campos**.
2. Selecione as medidas desejadas.
3. O Power BI gerará automaticamente a seguinte estrutura DAX:

```dax
Parametro Metricas = {
    ("Total de Vitórias", NAMEOF('_Medidas'[Total Vitorias]), 0),
    ("Abates Reivindicados", NAMEOF('_Medidas'[Total Abates Reivindicados]), 1),
    ("Aeronaves Perdidas", NAMEOF('_Medidas'[Total Aeronaves Perdidas]), 2),
    ("Aeronaves Produzidas", NAMEOF('_Medidas'[Total Producao Aeronaves]), 3)
}
```
*Utilização:* Arraste o campo `Parametro Metricas[Parametro Metricas]` para o eixo Y de gráficos ou para um segmentador de dados (slicer) em formato de botões horizontais no topo do dashboard.
