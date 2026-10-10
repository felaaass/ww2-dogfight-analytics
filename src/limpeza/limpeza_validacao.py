"""
Pipeline de Limpeza e Validação de Dados — Segunda Guerra Mundial
Utiliza pandas + pandera para validação rigorosa de esquemas e tipos.

Regras:
1. Padronização de nomes de países (Alemanha, Estados Unidos, Reino Unido, União Soviética, Japão, Itália, Aliados).
2. Manutenção de NULLs históricos sem imputação artificial.
3. Remoção de duplicatas.
4. Validação por Pandera Schema.
5. Geração de log_limpeza.md detalhando decisões e contagem de nulos.
"""

import os
import pandera.pandas as pa
from pandera.pandas import Column, Check, DataFrameSchema
import pandas as pd
import numpy as np

# Mapeamento oficial de países
COUNTRY_MAP = {
    "usa": "Estados Unidos",
    "united states": "Estados Unidos",
    "us": "Estados Unidos",
    "estados unidos": "Estados Unidos",
    "eua": "Estados Unidos",
    "germany": "Alemanha",
    "alemanha": "Alemanha",
    "deutschland": "Alemanha",
    "uk": "Reino Unido",
    "united kingdom": "Reino Unido",
    "great britain": "Reino Unido",
    "reino unido": "Reino Unido",
    "ussr": "União Soviética",
    "soviet union": "União Soviética",
    "urss": "União Soviética",
    "união soviética": "União Soviética",
    "uniao sovietica": "União Soviética",
    "japan": "Japão",
    "japao": "Japão",
    "japão": "Japão",
    "italy": "Itália",
    "italia": "Itália",
    "itália": "Itália",
    "aliados (eua / reino unido)": "Aliados",
    "aliados": "Aliados"
}

def standardize_country(c):
    if pd.isna(c) or not str(c).strip():
        return None
    c_clean = str(c).strip().lower()
    return COUNTRY_MAP.get(c_clean, str(c).strip())

# =============================================================================
# ESQUEMAS PANDERA (com coerce=True)
# =============================================================================

ases_schema = DataFrameSchema({
    "nome_piloto": Column(str, Check.str_length(min_value=2), nullable=False),
    "pais": Column(str, Check.isin(["Alemanha", "Estados Unidos", "Reino Unido", "União Soviética", "Japão"]), nullable=False),
    "forca_aerea": Column(str, nullable=True),
    "numero_vitorias": Column(float, Check.greater_than_or_equal_to(5.0), nullable=False, coerce=True),
    "aeronave_principal": Column(str, nullable=True),
    "teatro_de_operacao": Column(str, nullable=True),
    "periodo_ativo": Column(str, nullable=True),
    "fonte": Column(str, Check.str_length(min_value=5), nullable=False)
})

cacas_schema = DataFrameSchema({
    "modelo": Column(str, nullable=False),
    "variante": Column(str, nullable=False),
    "pais": Column(str, Check.isin(["Alemanha", "Estados Unidos", "Reino Unido", "União Soviética", "Japão", "Itália"]), nullable=False),
    "ano_entrada_servico": Column(int, Check.in_range(1935, 1945), nullable=False, coerce=True),
    "velocidade_max_kmh": Column(float, Check.in_range(400, 1000), nullable=False, coerce=True),
    "teto_operacional_m": Column(float, Check.in_range(5000, 16000), nullable=False, coerce=True),
    "alcance_km": Column(float, Check.greater_than(0), nullable=False, coerce=True),
    "armamento": Column(str, nullable=True),
    "unidades_produzidas": Column(float, Check.greater_than_or_equal_to(0), nullable=True, coerce=True),
    "fonte": Column(str, Check.str_length(min_value=5), nullable=False)
})

batalhas_schema = DataFrameSchema({
    "batalha": Column(str, nullable=False),
    "data": Column(str, Check.str_matches(r"^\d{4}-\d{2}-\d{2}$"), nullable=False),
    "pais": Column(str, Check.isin(["Alemanha", "Estados Unidos", "Reino Unido", "Japão", "Aliados"]), nullable=False),
    "aeronaves_perdidas": Column(float, Check.greater_than_or_equal_to(0), nullable=False, coerce=True),
    "aeronaves_abatidas_reivindicadas": Column(float, Check.greater_than_or_equal_to(0), nullable=False, coerce=True),
    "fonte": Column(str, Check.str_length(min_value=5), nullable=False)
})

producao_schema = DataFrameSchema({
    "pais": Column(str, Check.isin(["Alemanha", "Estados Unidos", "Reino Unido", "União Soviética", "Japão"]), nullable=False),
    "ano": Column(int, Check.in_range(1939, 1945), nullable=False, coerce=True),
    "teatro": Column(str, nullable=False),
    "sorties": Column(float, Check.greater_than_or_equal_to(0), nullable=True, coerce=True),
    "perdas_combate": Column(float, Check.greater_than_or_equal_to(0), nullable=True, coerce=True),
    "abates_reivindicados": Column(float, Check.greater_than_or_equal_to(0), nullable=True, coerce=True),
    "unidades_produzidas": Column(float, Check.greater_than_or_equal_to(0), nullable=True, coerce=True),
    "fonte": Column(str, Check.str_length(min_value=5), nullable=False)
})

def process_table(raw_path, clean_path, schema, table_name, log_dict):
    df = pd.read_csv(raw_path)
    initial_rows = len(df)
    
    # 1. Padronizar país
    if "pais" in df.columns:
        df["pais"] = df["pais"].apply(standardize_country)
        
    # 2. Tipagem e limpeza de strings
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({'': np.nan, 'nan': np.nan, 'None': np.nan, '—': np.nan, '-': np.nan})
        
    # 3. Tratar colunas numéricas
    num_cols = df.select_dtypes(include=['number']).columns
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
        
    # 4. Remoção de duplicatas
    if "nome_piloto" in df.columns:
        df = df.drop_duplicates(subset=["nome_piloto", "pais"])
    elif "variante" in df.columns:
        df = df.drop_duplicates(subset=["variante"])
    elif "batalha" in df.columns and "data" in df.columns and "pais" in df.columns:
        df = df.drop_duplicates(subset=["batalha", "data", "pais"])
    elif "pais" in df.columns and "ano" in df.columns and "teatro" in df.columns:
        df = df.drop_duplicates(subset=["pais", "ano", "teatro"])
        
    final_rows = len(df)
    
    # Contagem de nulos por coluna
    null_counts = df.isnull().sum().to_dict()
    
    # Validação via Pandera
    print(f"Validando {table_name} com Pandera...")
    validated_df = schema.validate(df)
    
    # Salvar em /data/processed
    validated_df.to_csv(clean_path, index=False, encoding='utf-8-sig')
    
    log_dict[table_name] = {
        "linhas_iniciais": initial_rows,
        "linhas_finais": final_rows,
        "duplicatas_removidas": initial_rows - final_rows,
        "contagem_nulos": null_counts,
        "status_pandera": "VALIDADO COM SUCESSO"
    }
    return validated_df

def generate_cleaning_log(log_dict, log_file_path):
    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write("# Log de Limpeza e Validação de Dados — Projeto Ases e Atrito\n\n")
        f.write("Data de Execução: Outubro de 2026  \n")
        f.write("Mecanismo de Validação: Pandas 2.3 + Pandera 0.34  \n\n")
        f.write("## 1. Princípios de Limpeza e Integridade\n\n")
        f.write("1. **Nenhum Dado Inventado:** Valores ausentes foram mantidos estritamente como `NULL` (NaN).\n")
        f.write("2. **Padronização Geopolítica:** Nomes de países unificados no padrão lusófono:\n")
        f.write("   `Alemanha`, `Estados Unidos`, `Reino Unido`, `União Soviética`, `Japão`, `Itália` e `Aliados`.\n")
        f.write("3. **Padronização de Unidades:**\n")
        f.write("   - Velocidade: km/h (quilômetros por hora)\n")
        f.write("   - Altitude / Teto: m (metros)\n")
        f.write("   - Alcance: km (quilômetros)\n")
        f.write("   - Perdas e Abates: contagem inteira de aeronaves\n")
        f.write("4. **Validação de Esquemas (Pandera):** Checagem rigorosa de tipos, faixas numéricas de plausibilidade física e completude da coluna `fonte`.\n\n")
        f.write("---\n\n")
        f.write("## 2. Relatório de Execução por Tabela\n\n")
        
        for tbl, metrics in log_dict.items():
            f.write(f"### Tabela: `{tbl}`\n")
            f.write(f"- **Linhas Iniciais:** {metrics['linhas_iniciais']}\n")
            f.write(f"- **Linhas Finais:** {metrics['linhas_finais']}\n")
            f.write(f"- **Duplicatas Removidas:** {metrics['duplicatas_removidas']}\n")
            f.write(f"- **Status Pandera:** {metrics['status_pandera']}\n")
            f.write("- **Contagem de Nulos por Coluna:**\n")
            for col, n_null in metrics['contagem_nulos'].items():
                f.write(f"  - `{col}`: {n_null} nulos\n")
            f.write("\n")

def main():
    raw_dir = r"C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\raw"
    proc_dir = r"C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed"
    docs_dir = r"C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\docs"
    os.makedirs(proc_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)
    
    log_dict = {}
    
    # 1. Ases
    process_table(
        os.path.join(raw_dir, "ases.csv"),
        os.path.join(proc_dir, "ases_limpo.csv"),
        ases_schema,
        "ases_limpo.csv",
        log_dict
    )
    
    # 2. Caças
    process_table(
        os.path.join(raw_dir, "caças.csv"),
        os.path.join(proc_dir, "cacas_limpo.csv"),
        cacas_schema,
        "cacas_limpo.csv",
        log_dict
    )
    
    # 3. Batalhas e Perdas
    process_table(
        os.path.join(raw_dir, "batalhas_perdas.csv"),
        os.path.join(proc_dir, "batalhas_perdas_limpo.csv"),
        batalhas_schema,
        "batalhas_perdas_limpo.csv",
        log_dict
    )
    
    # 4. Produção e Atrito
    process_table(
        os.path.join(raw_dir, "producao_e_atrito.csv"),
        os.path.join(proc_dir, "producao_e_atrito_limpo.csv"),
        producao_schema,
        "producao_e_atrito_limpo.csv",
        log_dict
    )
    
    # Gerar log_limpeza.md
    log_path = os.path.join(docs_dir, "log_limpeza.md")
    generate_cleaning_log(log_dict, log_path)
    print(f"\nPipeline de limpeza concluído com sucesso!")
    print(f"Log de limpeza salvo em: {log_path}")

if __name__ == '__main__':
    main()
