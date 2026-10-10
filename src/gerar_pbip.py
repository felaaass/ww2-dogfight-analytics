import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PBIP_DIR = os.path.join(BASE_DIR, "powerbi")
REPORT_NAME = "dogfight-analytics"

report_dir = os.path.join(PBIP_DIR, f"{REPORT_NAME}.Report")
model_dir = os.path.join(PBIP_DIR, f"{REPORT_NAME}.SemanticModel")
os.makedirs(report_dir, exist_ok=True)
os.makedirs(model_dir, exist_ok=True)

# 1. Entry point .pbip
pbip_content = {
    "version": "1.0",
    "artifacts": [
        {
            "report": {
                "path": f"{REPORT_NAME}.Report"
            }
        }
    ]
}
with open(os.path.join(PBIP_DIR, f"{REPORT_NAME}.pbip"), "w", encoding="utf-8") as f:
    json.dump(pbip_content, f, indent=2)

# 2. Report definition.pbir
pbir_content = {
    "version": "1.0",
    "datasetReference": {
        "byPath": {
            "path": f"../{REPORT_NAME}.SemanticModel"
        },
        "byConnection": None
    }
}
with open(os.path.join(report_dir, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump(pbir_content, f, indent=2)

# 3. Report layout report.json
report_json = {
    "config": "{}",
    "layoutOptimization": 0,
    "sections": [
        {
            "name": "Section_01",
            "displayName": "1. Visão Geral Executiva",
            "visualContainers": [],
            "width": 1280.0,
            "height": 720.0
        },
        {
            "name": "Section_02",
            "displayName": "2. Hall dos Ases (Pareto)",
            "visualContainers": [],
            "width": 1280.0,
            "height": 720.0
        },
        {
            "name": "Section_03",
            "displayName": "3. Hangar de Aeronaves",
            "visualContainers": [],
            "width": 1280.0,
            "height": 720.0
        },
        {
            "name": "Section_04",
            "displayName": "4. Batalhas e Overclaiming",
            "visualContainers": [],
            "width": 1280.0,
            "height": 720.0
        },
        {
            "name": "Section_05",
            "displayName": "5. Atrito e Produção",
            "visualContainers": [],
            "width": 1280.0,
            "height": 720.0
        },
        {
            "name": "Section_06",
            "displayName": "6. Síntese Estatística",
            "visualContainers": [],
            "width": 1280.0,
            "height": 720.0
        }
    ]
}
with open(os.path.join(report_dir, "report.json"), "w", encoding="utf-8") as f:
    json.dump(report_json, f, indent=2)

# 4. SemanticModel definition.pbism
pbism_content = {
    "version": "1.0"
}
with open(os.path.join(model_dir, "definition.pbism"), "w", encoding="utf-8") as f:
    json.dump(pbism_content, f, indent=2)

proc_dir = os.path.join(BASE_DIR, "data", "processed").replace("\\", "/")

def make_partition(table_name, cols_def):
    csv_file = f"{proc_dir}/{table_name}.csv"
    col_types = ", ".join([f'{{"{col}", {t}}}' for col, t in cols_def])
    return {
        "name": table_name,
        "mode": "import",
        "source": {
            "type": "m",
            "expression": [
                "let",
                f'    Source = Csv.Document(File.Contents("{csv_file}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                '    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                f'    ChangedType = Table.TransformColumnTypes(PromotedHeaders, {{{col_types}}})',
                "in",
                "    ChangedType"
            ]
        }
    }

tables = [
    {
        "name": "dim_pais",
        "columns": [
            {"name": "id_pais", "dataType": "int64", "sourceColumn": "id_pais"},
            {"name": "nome", "dataType": "string", "sourceColumn": "nome"},
            {"name": "lado", "dataType": "string", "sourceColumn": "lado"}
        ],
        "partitions": [
            make_partition("dim_pais", [("id_pais", "Int64.Type"), ("nome", "type text"), ("lado", "type text")])
        ]
    },
    {
        "name": "dim_data",
        "columns": [
            {"name": "id_data", "dataType": "int64", "sourceColumn": "id_data"},
            {"name": "data", "dataType": "dateTime", "sourceColumn": "data"},
            {"name": "ano", "dataType": "int64", "sourceColumn": "ano"},
            {"name": "mes", "dataType": "int64", "sourceColumn": "mes"},
            {"name": "fase_da_guerra", "dataType": "string", "sourceColumn": "fase_da_guerra"}
        ],
        "partitions": [
            make_partition("dim_data", [("id_data", "Int64.Type"), ("data", "type date"), ("ano", "Int64.Type"), ("mes", "Int64.Type"), ("fase_da_guerra", "type text")])
        ]
    },
    {
        "name": "dim_batalha",
        "columns": [
            {"name": "id_batalha", "dataType": "int64", "sourceColumn": "id_batalha"},
            {"name": "nome", "dataType": "string", "sourceColumn": "nome"},
            {"name": "teatro", "dataType": "string", "sourceColumn": "teatro"},
            {"name": "data_inicio", "dataType": "dateTime", "sourceColumn": "data_inicio"},
            {"name": "data_fim", "dataType": "dateTime", "sourceColumn": "data_fim"}
        ],
        "partitions": [
            make_partition("dim_batalha", [("id_batalha", "Int64.Type"), ("nome", "type text"), ("teatro", "type text"), ("data_inicio", "type date"), ("data_fim", "type date")])
        ]
    },
    {
        "name": "dim_aeronave",
        "columns": [
            {"name": "id_aeronave", "dataType": "int64", "sourceColumn": "id_aeronave"},
            {"name": "modelo", "dataType": "string", "sourceColumn": "modelo"},
            {"name": "variante", "dataType": "string", "sourceColumn": "variante"},
            {"name": "id_pais", "dataType": "int64", "sourceColumn": "id_pais"},
            {"name": "pais", "dataType": "string", "sourceColumn": "pais"},
            {"name": "ano_entrada_servico", "dataType": "int64", "sourceColumn": "ano_entrada_servico"},
            {"name": "velocidade_max_kmh", "dataType": "double", "sourceColumn": "velocidade_max_kmh"},
            {"name": "teto_operacional_m", "dataType": "double", "sourceColumn": "teto_operacional_m"},
            {"name": "alcance_km", "dataType": "double", "sourceColumn": "alcance_km"},
            {"name": "armamento", "dataType": "string", "sourceColumn": "armamento"},
            {"name": "unidades_produzidas", "dataType": "double", "sourceColumn": "unidades_produzidas"},
            {"name": "fonte", "dataType": "string", "sourceColumn": "fonte"}
        ],
        "partitions": [
            make_partition("dim_aeronave", [
                ("id_aeronave", "Int64.Type"), ("modelo", "type text"), ("variante", "type text"),
                ("id_pais", "Int64.Type"), ("pais", "type text"), ("ano_entrada_servico", "Int64.Type"),
                ("velocidade_max_kmh", "type number"), ("teto_operacional_m", "type number"),
                ("alcance_km", "type number"), ("armamento", "type text"),
                ("unidades_produzidas", "type number"), ("fonte", "type text")
            ])
        ]
    },
    {
        "name": "dim_piloto",
        "columns": [
            {"name": "id_piloto", "dataType": "int64", "sourceColumn": "id_piloto"},
            {"name": "nome_piloto", "dataType": "string", "sourceColumn": "nome_piloto"},
            {"name": "id_pais", "dataType": "int64", "sourceColumn": "id_pais"},
            {"name": "pais", "dataType": "string", "sourceColumn": "pais"},
            {"name": "forca_aerea", "dataType": "string", "sourceColumn": "forca_aerea"},
            {"name": "total_vitorias", "dataType": "double", "sourceColumn": "total_vitorias"},
            {"name": "aeronave_principal", "dataType": "string", "sourceColumn": "aeronave_principal"},
            {"name": "teatro_de_operacao", "dataType": "string", "sourceColumn": "teatro_de_operacao"},
            {"name": "periodo_ativo", "dataType": "string", "sourceColumn": "periodo_ativo"},
            {"name": "fonte", "dataType": "string", "sourceColumn": "fonte"}
        ],
        "partitions": [
            make_partition("dim_piloto", [
                ("id_piloto", "Int64.Type"), ("nome_piloto", "type text"), ("id_pais", "Int64.Type"),
                ("pais", "type text"), ("forca_aerea", "type text"), ("total_vitorias", "type number"),
                ("aeronave_principal", "type text"), ("teatro_de_operacao", "type text"),
                ("periodo_ativo", "type text"), ("fonte", "type text")
            ])
        ]
    },
    {
        "name": "fato_perdas",
        "columns": [
            {"name": "id_fato_perda", "dataType": "int64", "sourceColumn": "id_fato_perda"},
            {"name": "id_batalha", "dataType": "int64", "sourceColumn": "id_batalha"},
            {"name": "id_data", "dataType": "int64", "sourceColumn": "id_data"},
            {"name": "id_pais", "dataType": "int64", "sourceColumn": "id_pais"},
            {"name": "aeronaves_perdidas", "dataType": "double", "sourceColumn": "aeronaves_perdidas"},
            {"name": "aeronaves_abatidas_reivindicadas", "dataType": "double", "sourceColumn": "aeronaves_abatidas_reivindicadas"},
            {"name": "fonte", "dataType": "string", "sourceColumn": "fonte"}
        ],
        "partitions": [
            make_partition("fato_perdas", [
                ("id_fato_perda", "Int64.Type"), ("id_batalha", "Int64.Type"), ("id_data", "Int64.Type"),
                ("id_pais", "Int64.Type"), ("aeronaves_perdidas", "type number"),
                ("aeronaves_abatidas_reivindicadas", "type number"), ("fonte", "type text")
            ])
        ]
    },
    {
        "name": "fato_producao",
        "columns": [
            {"name": "id_fato_producao", "dataType": "int64", "sourceColumn": "id_fato_producao"},
            {"name": "id_pais", "dataType": "int64", "sourceColumn": "id_pais"},
            {"name": "id_data", "dataType": "int64", "sourceColumn": "id_data"},
            {"name": "teatro", "dataType": "string", "sourceColumn": "teatro"},
            {"name": "unidades_produzidas", "dataType": "double", "sourceColumn": "unidades_produzidas"},
            {"name": "sorties", "dataType": "double", "sourceColumn": "sorties"},
            {"name": "perdas_combate", "dataType": "double", "sourceColumn": "perdas_combate"},
            {"name": "abates_reivindicados", "dataType": "double", "sourceColumn": "abates_reivindicados"},
            {"name": "fonte", "dataType": "string", "sourceColumn": "fonte"}
        ],
        "partitions": [
            make_partition("fato_producao", [
                ("id_fato_producao", "Int64.Type"), ("id_pais", "Int64.Type"), ("id_data", "Int64.Type"),
                ("teatro", "type text"), ("unidades_produzidas", "type number"),
                ("sorties", "type number"), ("perdas_combate", "type number"),
                ("abates_reivindicados", "type number"), ("fonte", "type text")
            ])
        ]
    },
    {
        "name": "fato_vitorias",
        "columns": [
            {"name": "id_fato_vitoria", "dataType": "int64", "sourceColumn": "id_fato_vitoria"},
            {"name": "id_piloto", "dataType": "int64", "sourceColumn": "id_piloto"},
            {"name": "id_aeronave", "dataType": "int64", "sourceColumn": "id_aeronave"},
            {"name": "id_data", "dataType": "int64", "sourceColumn": "id_data"},
            {"name": "id_pais", "dataType": "int64", "sourceColumn": "id_pais"},
            {"name": "total_vitorias", "dataType": "double", "sourceColumn": "total_vitorias"},
            {"name": "faixa_vitorias", "dataType": "string", "sourceColumn": "faixa_vitorias"},
            {"name": "fonte", "dataType": "string", "sourceColumn": "fonte"}
        ],
        "partitions": [
            make_partition("fato_vitorias", [
                ("id_fato_vitoria", "Int64.Type"), ("id_piloto", "Int64.Type"), ("id_aeronave", "Int64.Type"),
                ("id_data", "Int64.Type"), ("id_pais", "Int64.Type"), ("total_vitorias", "type number"),
                ("faixa_vitorias", "type text"), ("fonte", "type text")
            ])
        ],
        "measures": [
            {
                "name": "Total Vitorias",
                "expression": "SUM(fato_vitorias[total_vitorias])"
            },
            {
                "name": "Total Ases",
                "expression": "DISTINCTCOUNT(fato_vitorias[id_piloto])"
            },
            {
                "name": "Media Vitorias por As",
                "expression": "DIVIDE([Total Vitorias], [Total Ases], BLANK())"
            },
            {
                "name": "Ranking Dinamico Ases",
                "expression": "IF(HASONEVALUE(dim_piloto[nome_piloto]), RANKX(ALLSELECTED(dim_piloto[nome_piloto]), [Total Vitorias], , DESC, Dense))"
            },
            {
                "name": "Pareto % Vitorias",
                "expression": "VAR TotalGeral = CALCULATE([Total Vitorias], ALLSELECTED(dim_piloto)) VAR RankingAtual = [Ranking Dinamico Ases] VAR VitoriasAcumuladas = SUMX(TOPN(RankingAtual, ALLSELECTED(dim_piloto), [Total Vitorias], DESC), [Total Vitorias]) RETURN DIVIDE(VitoriasAcumuladas, TotalGeral, BLANK())"
            },
            {
                "name": "Total Aeronaves Perdidas",
                "expression": "SUM(fato_perdas[aeronaves_perdidas])"
            },
            {
                "name": "Total Abates Reivindicados",
                "expression": "SUM(fato_perdas[aeronaves_abatidas_reivindicadas])"
            },
            {
                "name": "Razao Reivindicacoes vs Perdas",
                "expression": "DIVIDE([Total Abates Reivindicados], [Total Aeronaves Perdidas], BLANK())"
            },
            {
                "name": "Distorcao Overclaiming",
                "expression": "[Total Abates Reivindicados] - [Total Aeronaves Perdidas]"
            },
            {
                "name": "Total Producao Aeronaves",
                "expression": "SUM(fato_producao[unidades_produzidas])"
            },
            {
                "name": "Total Sorties",
                "expression": "SUM(fato_producao[sorties])"
            },
            {
                "name": "Taxa Atrito por Sortie %",
                "expression": "DIVIDE(SUM(fato_producao[perdas_combate]), [Total Sorties], BLANK()) * 100"
            }
        ]
    }
]

relationships = [
    {
        "name": "rel_pais_aeronave",
        "fromTable": "dim_aeronave",
        "fromColumn": "id_pais",
        "toTable": "dim_pais",
        "toColumn": "id_pais"
    },
    {
        "name": "rel_pais_piloto",
        "fromTable": "dim_piloto",
        "fromColumn": "id_pais",
        "toTable": "dim_pais",
        "toColumn": "id_pais"
    },
    {
        "name": "rel_pais_perdas",
        "fromTable": "fato_perdas",
        "fromColumn": "id_pais",
        "toTable": "dim_pais",
        "toColumn": "id_pais"
    },
    {
        "name": "rel_pais_producao",
        "fromTable": "fato_producao",
        "fromColumn": "id_pais",
        "toTable": "dim_pais",
        "toColumn": "id_pais"
    },
    {
        "name": "rel_pais_vitorias",
        "fromTable": "fato_vitorias",
        "fromColumn": "id_pais",
        "toTable": "dim_pais",
        "toColumn": "id_pais"
    },
    {
        "name": "rel_data_perdas",
        "fromTable": "fato_perdas",
        "fromColumn": "id_data",
        "toTable": "dim_data",
        "toColumn": "id_data"
    },
    {
        "name": "rel_data_producao",
        "fromTable": "fato_producao",
        "fromColumn": "id_data",
        "toTable": "dim_data",
        "toColumn": "id_data"
    },
    {
        "name": "rel_data_vitorias",
        "fromTable": "fato_vitorias",
        "fromColumn": "id_data",
        "toTable": "dim_data",
        "toColumn": "id_data"
    },
    {
        "name": "rel_batalha_perdas",
        "fromTable": "fato_perdas",
        "fromColumn": "id_batalha",
        "toTable": "dim_batalha",
        "toColumn": "id_batalha"
    },
    {
        "name": "rel_piloto_vitorias",
        "fromTable": "fato_vitorias",
        "fromColumn": "id_piloto",
        "toTable": "dim_piloto",
        "toColumn": "id_piloto"
    },
    {
        "name": "rel_aeronave_vitorias",
        "fromTable": "fato_vitorias",
        "fromColumn": "id_aeronave",
        "toTable": "dim_aeronave",
        "toColumn": "id_aeronave"
    }
]

model_bim = {
    "name": REPORT_NAME,
    "compatibilityLevel": 1550,
    "model": {
        "culture": "pt-BR",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "returnErrorValuesAsNull": True
        },
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "sourceQueryCulture": "pt-BR",
        "tables": tables,
        "relationships": relationships
    }
}

with open(os.path.join(model_dir, "model.bim"), "w", encoding="utf-8") as f:
    json.dump(model_bim, f, indent=2)

print(f"Projeto PBIP gerado com sucesso em: {os.path.join(PBIP_DIR, f'{REPORT_NAME}.pbip')}")
