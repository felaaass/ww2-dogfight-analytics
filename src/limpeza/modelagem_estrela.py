"""
Modelagem Dimensional em Esquema Estrela (Star Schema)
Cria o banco de dados relacional dogfight.db (SQLite) em /data/processed/dogfight.db
e exporta todas as tabelas dimensionais e de fatos como CSVs para importação no Power BI Desktop.

Tabelas:
Dimensões:
- dim_pais (id_pais, nome, lado)
- dim_data (id_data, data, ano, mes, fase_da_guerra)
- dim_batalha (id_batalha, nome, teatro, data_inicio, data_fim)
- dim_aeronave (id_aeronave, modelo, variante, id_pais, pais, ano_entrada_servico, velocidade_max_kmh, teto_operacional_m, alcance_km, armamento, unidades_produzidas, fonte)
- dim_piloto (id_piloto, nome, id_pais, pais, forca_aerea, total_vitorias, aeronave_principal, teatro_de_operacao, periodo_ativo, fonte)

Fatos:
- fato_perdas (id_fato_perda, id_batalha, id_data, id_pais, aeronaves_perdidas, abates_reivindicados, fonte)
- fato_producao (id_fato_producao, id_pais, id_data, teatro, unidades_produzidas, sorties, perdas_combate, abates_reivindicados, fonte)
- fato_vitorias (id_fato_vitoria, id_piloto, id_aeronave, id_data, id_pais, total_vitorias, faixa_vitorias, fonte)
"""

import os
import sqlite3
import pandas as pd
import numpy as np

def build_star_schema():
    proc_dir = r"C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\processed"
    db_path = os.path.join(proc_dir, "dogfight.db")
    
    # Remove se já existir para recriação limpa
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Ativa integridade de chaves estrangeiras
    cur.execute("PRAGMA foreign_keys = ON;")
    
    print("Carregando datasets limpos...")
    df_ases = pd.read_csv(os.path.join(proc_dir, "ases_limpo.csv"))
    df_cacas = pd.read_csv(os.path.join(proc_dir, "cacas_limpo.csv"))
    df_batalhas = pd.read_csv(os.path.join(proc_dir, "batalhas_perdas_limpo.csv"))
    df_producao = pd.read_csv(os.path.join(proc_dir, "producao_e_atrito_limpo.csv"))
    
    # -------------------------------------------------------------------------
    # 1. DIM_PAIS
    # -------------------------------------------------------------------------
    paises_info = [
        {"id_pais": 1, "nome": "Alemanha", "lado": "Eixo"},
        {"id_pais": 2, "nome": "Japão", "lado": "Eixo"},
        {"id_pais": 3, "nome": "Itália", "lado": "Eixo"},
        {"id_pais": 4, "nome": "Estados Unidos", "lado": "Aliados"},
        {"id_pais": 5, "nome": "Reino Unido", "lado": "Aliados"},
        {"id_pais": 6, "nome": "União Soviética", "lado": "Aliados"},
        {"id_pais": 7, "nome": "Aliados", "lado": "Aliados"} # Coalizão geral
    ]
    df_dim_pais = pd.DataFrame(paises_info)
    
    cur.execute("""
    CREATE TABLE dim_pais (
        id_pais INTEGER PRIMARY KEY,
        nome TEXT NOT NULL UNIQUE,
        lado TEXT NOT NULL
    );
    """)
    df_dim_pais.to_sql("dim_pais", conn, if_exists="append", index=False)
    df_dim_pais.to_csv(os.path.join(proc_dir, "dim_pais.csv"), index=False, encoding="utf-8-sig")
    print(f"-> dim_pais criada com {len(df_dim_pais)} registros.")
    
    pais_id_map = dict(zip(df_dim_pais["nome"], df_dim_pais["id_pais"]))
    
    # -------------------------------------------------------------------------
    # 2. DIM_DATA
    # -------------------------------------------------------------------------
    # Extraímos todas as datas únicas de batalhas, além de anos de produção e entrada de aeronaves
    datas_list = []
    # Anos 1937 a 1945 com marcos anuais (01 de janeiro de cada ano)
    for ano in range(1937, 1946):
        d_str = f"{ano}-01-01"
        datas_list.append(d_str)
        
    for d in df_batalhas["data"].unique():
        if d not in datas_list:
            datas_list.append(d)
            
    datas_list = sorted(list(set(datas_list)))
    
    def get_fase_guerra(ano):
        if ano <= 1939:
            return "Pré-Guerra e Início das Hostilidades (1937-1939)"
        elif ano <= 1941:
            return "Expansão do Eixo e Batalha da Inglaterra (1940-1941)"
        elif ano == 1942:
            return "Ponto de Inflexão (Midway, Stalingrado, Guadalcanal)"
        elif ano == 1943:
            return "Iniciativa Aliada e Batalhas de Atrito Aéreo"
        elif ano == 1944:
            return "Supremacia Aérea Aliada e Campanhas Finais"
        else:
            return "Colapso do Eixo e Vitória Aliada (1945)"
            
    dim_data_records = []
    for d in datas_list:
        ano = int(d.split("-")[0])
        mes = int(d.split("-")[1])
        id_data = int(d.replace("-", ""))
        dim_data_records.append({
            "id_data": id_data,
            "data": d,
            "ano": ano,
            "mes": mes,
            "fase_da_guerra": get_fase_guerra(ano)
        })
    df_dim_data = pd.DataFrame(dim_data_records).drop_duplicates(subset=["id_data"]).sort_values("id_data")
    
    cur.execute("""
    CREATE TABLE dim_data (
        id_data INTEGER PRIMARY KEY,
        data TEXT NOT NULL,
        ano INTEGER NOT NULL,
        mes INTEGER NOT NULL,
        fase_da_guerra TEXT NOT NULL
    );
    """)
    df_dim_data.to_sql("dim_data", conn, if_exists="append", index=False)
    df_dim_data.to_csv(os.path.join(proc_dir, "dim_data.csv"), index=False, encoding="utf-8-sig")
    print(f"-> dim_data criada com {len(df_dim_data)} registros.")
    
    # -------------------------------------------------------------------------
    # 3. DIM_BATALHA
    # -------------------------------------------------------------------------
    batalhas_unicas = df_batalhas["batalha"].unique()
    dim_batalha_records = []
    
    for idx, b_nome in enumerate(batalhas_unicas, start=1):
        # Determina teatro e período
        sub_df = df_batalhas[df_batalhas["batalha"] == b_nome]
        d_min = sub_df["data"].min()
        d_max = sub_df["data"].max()
        
        if "Inglaterra" in b_nome:
            teatro = "Europa Ocidental (Batalha da Inglaterra)"
        elif "Midway" in b_nome:
            teatro = "Pacífico Central"
        elif "Filipinas" in b_nome:
            teatro = "Pacífico Ocidental (Mar das Filipinas)"
        elif "Schweinfurt" in b_nome or "Berlin" in b_nome or "Berlim" in b_nome or "Big Week" in b_nome or "Bodenplatte" in b_nome:
            teatro = "Defesa do Reich / Europa Ocidental"
        else:
            teatro = "Outros Teatros"
            
        dim_batalha_records.append({
            "id_batalha": idx,
            "nome": b_nome,
            "teatro": teatro,
            "data_inicio": d_min,
            "data_fim": d_max
        })
    df_dim_batalha = pd.DataFrame(dim_batalha_records)
    
    cur.execute("""
    CREATE TABLE dim_batalha (
        id_batalha INTEGER PRIMARY KEY,
        nome TEXT NOT NULL UNIQUE,
        teatro TEXT NOT NULL,
        data_inicio TEXT NOT NULL,
        data_fim TEXT NOT NULL
    );
    """)
    df_dim_batalha.to_sql("dim_batalha", conn, if_exists="append", index=False)
    df_dim_batalha.to_csv(os.path.join(proc_dir, "dim_batalha.csv"), index=False, encoding="utf-8-sig")
    print(f"-> dim_batalha criada com {len(df_dim_batalha)} registros.")
    
    batalha_id_map = dict(zip(df_dim_batalha["nome"], df_dim_batalha["id_batalha"]))
    
    # -------------------------------------------------------------------------
    # 4. DIM_AERONAVE
    # -------------------------------------------------------------------------
    df_dim_aeronave = df_cacas.copy()
    df_dim_aeronave.insert(0, "id_aeronave", range(1, len(df_dim_aeronave) + 1))
    df_dim_aeronave["id_pais"] = df_dim_aeronave["pais"].map(pais_id_map)
    
    cur.execute("""
    CREATE TABLE dim_aeronave (
        id_aeronave INTEGER PRIMARY KEY,
        modelo TEXT NOT NULL,
        variante TEXT NOT NULL UNIQUE,
        id_pais INTEGER NOT NULL,
        pais TEXT NOT NULL,
        ano_entrada_servico INTEGER NOT NULL,
        velocidade_max_kmh REAL NOT NULL,
        teto_operacional_m REAL NOT NULL,
        alcance_km REAL NOT NULL,
        armamento TEXT,
        unidades_produzidas REAL,
        fonte TEXT NOT NULL,
        FOREIGN KEY (id_pais) REFERENCES dim_pais (id_pais)
    );
    """)
    df_dim_aeronave.to_sql("dim_aeronave", conn, if_exists="append", index=False)
    df_dim_aeronave.to_csv(os.path.join(proc_dir, "dim_aeronave.csv"), index=False, encoding="utf-8-sig")
    print(f"-> dim_aeronave criada com {len(df_dim_aeronave)} registros.")
    
    # -------------------------------------------------------------------------
    # 5. DIM_PILOTO
    # -------------------------------------------------------------------------
    df_dim_piloto = df_ases.copy()
    df_dim_piloto.insert(0, "id_piloto", range(1, len(df_dim_piloto) + 1))
    df_dim_piloto["id_pais"] = df_dim_piloto["pais"].map(pais_id_map)
    df_dim_piloto.rename(columns={"numero_vitorias": "total_vitorias"}, inplace=True)
    
    cur.execute("""
    CREATE TABLE dim_piloto (
        id_piloto INTEGER PRIMARY KEY,
        nome_piloto TEXT NOT NULL,
        id_pais INTEGER NOT NULL,
        pais TEXT NOT NULL,
        forca_aerea TEXT,
        total_vitorias REAL NOT NULL,
        aeronave_principal TEXT,
        teatro_de_operacao TEXT,
        periodo_ativo TEXT,
        fonte TEXT NOT NULL,
        FOREIGN KEY (id_pais) REFERENCES dim_pais (id_pais)
    );
    """)
    df_dim_piloto.to_sql("dim_piloto", conn, if_exists="append", index=False)
    df_dim_piloto.to_csv(os.path.join(proc_dir, "dim_piloto.csv"), index=False, encoding="utf-8-sig")
    print(f"-> dim_piloto criada com {len(df_dim_piloto)} registros.")
    
    # -------------------------------------------------------------------------
    # 6. FATO_PERDAS
    # -------------------------------------------------------------------------
    df_fato_perdas = df_batalhas.copy()
    df_fato_perdas.insert(0, "id_fato_perda", range(1, len(df_fato_perdas) + 1))
    df_fato_perdas["id_batalha"] = df_fato_perdas["batalha"].map(batalha_id_map)
    df_fato_perdas["id_pais"] = df_fato_perdas["pais"].map(pais_id_map)
    df_fato_perdas["id_data"] = df_fato_perdas["data"].str.replace("-", "").astype(int)
    
    fato_perdas_cols = [
        "id_fato_perda", "id_batalha", "id_data", "id_pais",
        "aeronaves_perdidas", "aeronaves_abatidas_reivindicadas", "fonte"
    ]
    df_fato_perdas = df_fato_perdas[fato_perdas_cols]
    
    cur.execute("""
    CREATE TABLE fato_perdas (
        id_fato_perda INTEGER PRIMARY KEY,
        id_batalha INTEGER NOT NULL,
        id_data INTEGER NOT NULL,
        id_pais INTEGER NOT NULL,
        aeronaves_perdidas REAL NOT NULL,
        aeronaves_abatidas_reivindicadas REAL NOT NULL,
        fonte TEXT NOT NULL,
        FOREIGN KEY (id_batalha) REFERENCES dim_batalha (id_batalha),
        FOREIGN KEY (id_data) REFERENCES dim_data (id_data),
        FOREIGN KEY (id_pais) REFERENCES dim_pais (id_pais)
    );
    """)
    df_fato_perdas.to_sql("fato_perdas", conn, if_exists="append", index=False)
    df_fato_perdas.to_csv(os.path.join(proc_dir, "fato_perdas.csv"), index=False, encoding="utf-8-sig")
    print(f"-> fato_perdas criada com {len(df_fato_perdas)} registros.")
    
    # -------------------------------------------------------------------------
    # 7. FATO_PRODUCAO
    # -------------------------------------------------------------------------
    df_fato_prod = df_producao.copy()
    df_fato_prod.insert(0, "id_fato_producao", range(1, len(df_fato_prod) + 1))
    df_fato_prod["id_pais"] = df_fato_prod["pais"].map(pais_id_map)
    df_fato_prod["id_data"] = df_fato_prod["ano"].apply(lambda y: int(f"{y}0101"))
    
    fato_prod_cols = [
        "id_fato_producao", "id_pais", "id_data", "teatro",
        "unidades_produzidas", "sorties", "perdas_combate", "abates_reivindicados", "fonte"
    ]
    df_fato_prod = df_fato_prod[fato_prod_cols]
    
    cur.execute("""
    CREATE TABLE fato_producao (
        id_fato_producao INTEGER PRIMARY KEY,
        id_pais INTEGER NOT NULL,
        id_data INTEGER NOT NULL,
        teatro TEXT NOT NULL,
        unidades_produzidas REAL,
        sorties REAL,
        perdas_combate REAL,
        abates_reivindicados REAL,
        fonte TEXT NOT NULL,
        FOREIGN KEY (id_pais) REFERENCES dim_pais (id_pais),
        FOREIGN KEY (id_data) REFERENCES dim_data (id_data)
    );
    """)
    df_fato_prod.to_sql("fato_producao", conn, if_exists="append", index=False)
    df_fato_prod.to_csv(os.path.join(proc_dir, "fato_producao.csv"), index=False, encoding="utf-8-sig")
    print(f"-> fato_producao criada com {len(df_fato_prod)} registros.")
    
    # -------------------------------------------------------------------------
    # 8. FATO_VITORIAS
    # -------------------------------------------------------------------------
    # Relaciona cada piloto ao seu país, data marco e mapeamento da aeronave mais representativa
    def get_faixa_vitorias(v):
        if v >= 100:
            return "100+ Lenda da Aviação"
        elif v >= 50:
            return "50-99 Super As"
        elif v >= 20:
            return "20-49 Grande As"
        elif v >= 10:
            return "10-19 As Veterano"
        else:
            return "5-9 As"
            
    # Mapeamento de id_aeronave padrão por país para vínculo relacional na dim_aeronave
    # Alemanha -> Bf 109G-6 (variante mais produzida da Luftwaffe)
    # Reino Unido -> Spitfire Mk IX (variante mais produzida da RAF)
    # EUA -> P-51D (caça de escolta definitivo)
    # URSS -> Yak-9 (caça mais produzido da VVS)
    # Japão -> A6M5 Zero (variante naval mais produzida)
    default_aircraft_map = {
        "Alemanha": df_dim_aeronave[df_dim_aeronave["variante"] == "Bf 109G-6"]["id_aeronave"].values[0],
        "Reino Unido": df_dim_aeronave[df_dim_aeronave["variante"] == "Spitfire Mk IX"]["id_aeronave"].values[0],
        "Estados Unidos": df_dim_aeronave[df_dim_aeronave["variante"] == "P-51D"]["id_aeronave"].values[0],
        "União Soviética": df_dim_aeronave[df_dim_aeronave["variante"] == "Yak-9"]["id_aeronave"].values[0],
        "Japão": df_dim_aeronave[df_dim_aeronave["variante"] == "A6M5 Modelo 52"]["id_aeronave"].values[0]
    }
    
    df_fato_vitorias = df_dim_piloto.copy()
    df_fato_vitorias.rename(columns={"id_piloto": "id_piloto_ref"}, inplace=True)
    df_fato_vitorias.insert(0, "id_fato_vitoria", range(1, len(df_fato_vitorias) + 1))
    df_fato_vitorias["id_piloto"] = df_fato_vitorias["id_piloto_ref"]
    df_fato_vitorias["id_aeronave"] = df_fato_vitorias["pais"].map(default_aircraft_map)
    df_fato_vitorias["id_data"] = 19440101 # Ano de pico da guerra aérea
    df_fato_vitorias["faixa_vitorias"] = df_fato_vitorias["total_vitorias"].apply(get_faixa_vitorias)
    
    fato_vit_cols = [
        "id_fato_vitoria", "id_piloto", "id_aeronave", "id_data", "id_pais",
        "total_vitorias", "faixa_vitorias", "fonte"
    ]
    df_fato_vitorias = df_fato_vitorias[fato_vit_cols]
    
    cur.execute("""
    CREATE TABLE fato_vitorias (
        id_fato_vitoria INTEGER PRIMARY KEY,
        id_piloto INTEGER NOT NULL,
        id_aeronave INTEGER NOT NULL,
        id_data INTEGER NOT NULL,
        id_pais INTEGER NOT NULL,
        total_vitorias REAL NOT NULL,
        faixa_vitorias TEXT NOT NULL,
        fonte TEXT NOT NULL,
        FOREIGN KEY (id_piloto) REFERENCES dim_piloto (id_piloto),
        FOREIGN KEY (id_aeronave) REFERENCES dim_aeronave (id_aeronave),
        FOREIGN KEY (id_data) REFERENCES dim_data (id_data),
        FOREIGN KEY (id_pais) REFERENCES dim_pais (id_pais)
    );
    """)
    df_fato_vitorias.to_sql("fato_vitorias", conn, if_exists="append", index=False)
    df_fato_vitorias.to_csv(os.path.join(proc_dir, "fato_vitorias.csv"), index=False, encoding="utf-8-sig")
    print(f"-> fato_vitorias criada com {len(df_fato_vitorias)} registros.")
    
    # Criação de índices para máxima performance em consultas
    cur.execute("CREATE INDEX idx_fato_perdas_batalha ON fato_perdas(id_batalha);")
    cur.execute("CREATE INDEX idx_fato_perdas_pais ON fato_perdas(id_pais);")
    cur.execute("CREATE INDEX idx_fato_perdas_data ON fato_perdas(id_data);")
    cur.execute("CREATE INDEX idx_fato_producao_pais ON fato_producao(id_pais);")
    cur.execute("CREATE INDEX idx_fato_producao_data ON fato_producao(id_data);")
    cur.execute("CREATE INDEX idx_fato_vitorias_piloto ON fato_vitorias(id_piloto);")
    cur.execute("CREATE INDEX idx_fato_vitorias_pais ON fato_vitorias(id_pais);")
    
    conn.commit()
    conn.close()
    print(f"\nModelagem dimensional concluída! Banco relacional: {db_path}")

if __name__ == '__main__':
    build_star_schema()
