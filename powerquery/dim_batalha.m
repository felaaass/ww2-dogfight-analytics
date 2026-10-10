let
    Origem = Csv.Document(File.Contents("data/processed/dim_batalha.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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
