let
    Origem = Csv.Document(File.Contents("data/processed/fato_perdas.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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
