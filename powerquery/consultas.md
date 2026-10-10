# Consultas Power Query (Linguagem M) — Projeto Ases e Atrito

Este arquivo contém o código em **Linguagem M** pronto para ser colado no **Editor Avançado** do Power Query no Power BI Desktop.

---

## 1. Como Utilizar no Power BI Desktop

1. No Power BI Desktop, clique em **Página Inicial** -> **Transformar Dados** (abre o Power Query).
2. Na guia **Página Inicial**, clique em **Nova Fonte** -> **Consulta Nula**.
3. Na guia **Página Inicial**, clique em **Editor Avançado**.
4. Apague todo o conteúdo existente e cole o código M correspondente à tabela.
5. Renomeie a consulta para o nome exato indicado (ex.: `dim_pais`).
6. **Ajuste de Caminho:** Se os seus arquivos estiverem em outra pasta, altere o valor da etapa `Origem` ou crie o parâmetro `CaminhoBase` abaixo.

---

## 2. Parâmetro de Caminho Base (Opcional, mas Recomendado)

Crie uma consulta nula chamada `CaminhoBase` e cole:
```powerquery
"C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```

---

## 3. Consultas Dimensionais

### 3.1 `dim_pais`
```powerquery
let
    Origem = Csv.Document(File.Contents("C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed\dim_pais.csv"), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    CabecalhosPromovidos = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
    TipoAlterado = Table.TransformColumnTypes(CabecalhosPromovidos, {
        {"id_pais", Int64.Type}, 
        {"nome", type text}, 
        {"lado", type text}
    })
in
    TipoAlterado
```

### 3.2 `dim_data`
```powerquery
let
    Origem = Csv.Document(File.Contents("C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed\dim_data.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    CabecalhosPromovidos = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
    TipoAlterado = Table.TransformColumnTypes(CabecalhosPromovidos, {
        {"id_data", Int64.Type}, 
        {"data", type date}, 
        {"ano", Int64.Type}, 
        {"mes", Int64.Type}, 
        {"fase_da_guerra", type text}
    })
in
    TipoAlterado
```

### 3.3 `dim_batalha`
```powerquery
let
    Origem = Csv.Document(File.Contents("C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed\dim_batalha.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    CabecalhosPromovidos = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
    TipoAlterado = Table.TransformColumnTypes(CabecalhosPromovidos, {
        {"id_batalha", Int64.Type}, 
        {"nome", type text}, 
        {"teatro", type text}, 
        {"data_inicio", type date}, 
        {"data_fim", type date}
    })
in
    TipoAlterado
```

### 3.4 `dim_aeronave`
```powerquery
let
    Origem = Csv.Document(File.Contents("C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed\dim_aeronave.csv"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    CabecalhosPromovidos = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
    TipoAlterado = Table.TransformColumnTypes(CabecalhosPromovidos, {
        {"id_aeronave", Int64.Type}, 
        {"modelo", type text}, 
        {"variante", type text}, 
        {"id_pais", Int64.Type}, 
        {"pais", type text}, 
        {"ano_entrada_servico", Int64.Type}, 
        {"velocidade_max_kmh", type number}, 
        {"teto_operacional_m", type number}, 
        {"alcance_km", type number}, 
        {"armamento", type text}, 
        {"unidades_produzidas", type number}, 
        {"fonte", type text}
    })
in
    TipoAlterado
```

### 3.5 `dim_piloto`
```powerquery
let
    Origem = Csv.Document(File.Contents("C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed\dim_piloto.csv"), [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    CabecalhosPromovidos = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
    TipoAlterado = Table.TransformColumnTypes(CabecalhosPromovidos, {
        {"id_piloto", Int64.Type}, 
        {"nome_piloto", type text}, 
        {"id_pais", Int64.Type}, 
        {"pais", type text}, 
        {"forca_aerea", type text}, 
        {"total_vitorias", type number}, 
        {"aeronave_principal", type text}, 
        {"teatro_de_operacao", type text}, 
        {"periodo_ativo", type text}, 
        {"fonte", type text}
    })
in
    TipoAlterado
```

---

## 4. Consultas de Tabelas Fato

### 4.1 `fato_perdas`
```powerquery
let
    Origem = Csv.Document(File.Contents("C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed\fato_perdas.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    CabecalhosPromovidos = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
    TipoAlterado = Table.TransformColumnTypes(CabecalhosPromovidos, {
        {"id_fato_perda", Int64.Type}, 
        {"id_batalha", Int64.Type}, 
        {"id_data", Int64.Type}, 
        {"id_pais", Int64.Type}, 
        {"aeronaves_perdidas", type number}, 
        {"aeronaves_abatidas_reivindicadas", type number}, 
        {"fonte", type text}
    })
in
    TipoAlterado
```

### 4.2 `fato_producao`
```powerquery
let
    Origem = Csv.Document(File.Contents("C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed\fato_producao.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    CabecalhosPromovidos = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
    TipoAlterado = Table.TransformColumnTypes(CabecalhosPromovidos, {
        {"id_fato_producao", Int64.Type}, 
        {"id_pais", Int64.Type}, 
        {"id_data", Int64.Type}, 
        {"teatro", type text}, 
        {"unidades_produzidas", type number}, 
        {"sorties", type number}, 
        {"perdas_combate", type number}, 
        {"abates_reivindicados", type number}, 
        {"fonte", type text}
    })
in
    TipoAlterado
```

### 4.3 `fato_vitorias`
```powerquery
let
    Origem = Csv.Document(File.Contents("C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed\fato_vitorias.csv"), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    CabecalhosPromovidos = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
    TipoAlterado = Table.TransformColumnTypes(CabecalhosPromovidos, {
        {"id_fato_vitoria", Int64.Type}, 
        {"id_piloto", Int64.Type}, 
        {"id_aeronave", Int64.Type}, 
        {"id_data", Int64.Type}, 
        {"id_pais", Int64.Type}, 
        {"total_vitorias", type number}, 
        {"faixa_vitorias", type text}, 
        {"fonte", type text}
    })
in
    TipoAlterado
```
