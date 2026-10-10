# Consultas Power Query (Linguagem M)

Consultas para carga das tabelas dimensionais e de fatos do modelo estrela.  
Utilizam o parâmetro `CaminhoBase` para desacoplar caminhos absolutos locais.

---

## 1. Parâmetro de Caminho

### `CaminhoBase`
```powerquery
"C:\caminho\para\ases-e-atrito\data\processed" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
```

---

## 2. Dimensões

### `dim_pais`
```powerquery
let
    Origem = Csv.Document(File.Contents(CaminhoBase & "\dim_pais.csv"), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    CabecalhosPromovidos = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
    TipoAlterado = Table.TransformColumnTypes(CabecalhosPromovidos, {
        {"id_pais", Int64.Type}, 
        {"nome", type text}, 
        {"lado", type text}
    })
in
    TipoAlterado
```

### `dim_data`
```powerquery
let
    Origem = Csv.Document(File.Contents(CaminhoBase & "\dim_data.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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

### `dim_batalha`
```powerquery
let
    Origem = Csv.Document(File.Contents(CaminhoBase & "\dim_batalha.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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

### `dim_aeronave`
```powerquery
let
    Origem = Csv.Document(File.Contents(CaminhoBase & "\dim_aeronave.csv"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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

### `dim_piloto`
```powerquery
let
    Origem = Csv.Document(File.Contents(CaminhoBase & "\dim_piloto.csv"), [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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

## 3. Fatos

### `fato_perdas`
```powerquery
let
    Origem = Csv.Document(File.Contents(CaminhoBase & "\fato_perdas.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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

### `fato_producao`
```powerquery
let
    Origem = Csv.Document(File.Contents(CaminhoBase & "\fato_producao.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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

### `fato_vitorias`
```powerquery
let
    Origem = Csv.Document(File.Contents(CaminhoBase & "\fato_vitorias.csv"), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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
