let
    Origem = Csv.Document(File.Contents("data/processed/dim_piloto.csv"), [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
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
