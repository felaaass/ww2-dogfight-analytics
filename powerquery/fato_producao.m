let
    Origem = Csv.Document(File.Contents("data/processed/fato_producao.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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
