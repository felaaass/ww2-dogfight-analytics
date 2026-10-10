let
    Origem = Csv.Document(File.Contents("data/processed/dim_aeronave.csv"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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
