var tableName = "_Measures";
Table table;
if (!Model.Tables.Contains(tableName))
{
    table = Model.AddTable(tableName);
}
else
{
    table = Model.Tables[tableName];
}

var measures = new[]
{
    new {
        Name = "Total de Abates",
        Expression = "SUM(fato_vitorias[total_vitorias])",
        Format = "#,0",
        Folder = "01 Ases e Pareto"
    },
    new {
        Name = "Total de Pilotos",
        Expression = "DISTINCTCOUNT(fato_vitorias[id_piloto])",
        Format = "#,0",
        Folder = "01 Ases e Pareto"
    },
    new {
        Name = "Média de Abates por Piloto",
        Expression = "DIVIDE([Total de Abates], [Total de Pilotos], BLANK())",
        Format = "0.0",
        Folder = "01 Ases e Pareto"
    },
    new {
        Name = "Soma Acumulada de Abates",
        Expression = "VAR CurrentWins = [Total de Abates]\r\nVAR CurrentPilot = SELECTEDVALUE(dim_piloto[nome_piloto])\r\nRETURN\r\nSUMX(\r\n    FILTER(\r\n        ADDCOLUMNS(ALLSELECTED(dim_piloto[nome_piloto]), \"@Wins\", [Total de Abates]),\r\n        [@Wins] > CurrentWins || ([@Wins] = CurrentWins && dim_piloto[nome_piloto] <= CurrentPilot)\r\n    ),\r\n    [@Wins]\r\n)",
        Format = "#,0",
        Folder = "01 Ases e Pareto"
    },
    new {
        Name = "Percentual Acumulado de Pareto",
        Expression = "DIVIDE([Soma Acumulada de Abates], CALCULATE([Total de Abates], ALLSELECTED(dim_piloto)), BLANK())",
        Format = "0.0%",
        Folder = "01 Ases e Pareto"
    },
    new {
        Name = "Coeficiente de Concentração",
        Expression = "VAR TotalWins = CALCULATE([Total de Abates], ALLSELECTED(dim_piloto))\r\nVAR TotalPilots = CALCULATE([Total de Pilotos], ALLSELECTED(dim_piloto))\r\nVAR Top20Count = ROUNDUP(TotalPilots * 0.20, 0)\r\nVAR Top20Wins = SUMX(TOPN(Top20Count, ALLSELECTED(dim_piloto), [Total de Abates], DESC), [Total de Abates])\r\nRETURN\r\nDIVIDE(Top20Wins, TotalWins, BLANK())",
        Format = "0.0%",
        Folder = "01 Ases e Pareto"
    },
    new {
        Name = "Vitórias Reivindicadas",
        Expression = "SUM(fato_perdas[aeronaves_abatidas_reivindicadas])",
        Format = "#,0",
        Folder = "02 Overclaiming"
    },
    new {
        Name = "Perdas Reais Documentadas",
        Expression = "SUM(fato_perdas[aeronaves_perdidas])",
        Format = "#,0",
        Folder = "02 Overclaiming"
    },
    new {
        Name = "Razão de Overclaiming",
        Expression = "DIVIDE([Vitórias Reivindicadas], [Perdas Reais Documentadas], BLANK())",
        Format = "0.00x",
        Folder = "02 Overclaiming"
    },
    new {
        Name = "Divergência Absoluta de Abates",
        Expression = "[Vitórias Reivindicadas] - [Perdas Reais Documentadas]",
        Format = "#,0",
        Folder = "02 Overclaiming"
    },
    new {
        Name = "Produção Total de Aeronaves",
        Expression = "SUM(fato_producao[unidades_produzidas])",
        Format = "#,0",
        Folder = "03 Atrito e Engenharia"
    },
    new {
        Name = "Total de Saídas Operacionais",
        Expression = "SUM(fato_producao[sorties])",
        Format = "#,0",
        Folder = "03 Atrito e Engenharia"
    },
    new {
        Name = "Total de Perdas em Combate",
        Expression = "SUM(fato_producao[perdas_combate])",
        Format = "#,0",
        Folder = "03 Atrito e Engenharia"
    },
    new {
        Name = "Taxa de Atrito por 1.000 Saídas",
        Expression = "DIVIDE([Total de Perdas em Combate], [Total de Saídas Operacionais], BLANK()) * 1000",
        Format = "0.00",
        Folder = "03 Atrito e Engenharia"
    },
    new {
        Name = "Razão Reposição Fabril vs Perdas",
        Expression = "DIVIDE([Produção Total de Aeronaves], [Total de Perdas em Combate], BLANK())",
        Format = "0.00x",
        Folder = "03 Atrito e Engenharia"
    },
    new {
        Name = "Velocidade Máxima Média por Ano de Introdução",
        Expression = "AVERAGE(dim_aeronave[velocidade_max_kmh])",
        Format = "#,0",
        Folder = "03 Atrito e Engenharia"
    }
};

foreach (var item in measures)
{
    Measure measure;
    if (table.Measures.Contains(item.Name))
    {
        measure = table.Measures[item.Name];
    }
    else
    {
        measure = table.AddMeasure(item.Name);
    }
    measure.Expression = item.Expression;
    measure.FormatString = item.Format;
    measure.DisplayFolder = item.Folder;
}
