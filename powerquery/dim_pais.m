let
    Origem = Csv.Document(File.Contents("data/processed/dim_pais.csv"), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    CabecalhosPromovidos = Table.PromoteHeaders(Origem, [PromoteAllScalars=true]),
    TipoAlterado = Table.TransformColumnTypes(CabecalhosPromovidos, {
        {"id_pais", Int64.Type}, 
        {"nome", type text}, 
        {"lado", type text}
    })
in
    TipoAlterado
