let
    Origem = Csv.Document(File.Contents("data/processed/dim_data.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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
