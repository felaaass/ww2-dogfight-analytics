let
    Origem = Csv.Document(File.Contents("data/processed/fato_vitorias.csv"), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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
