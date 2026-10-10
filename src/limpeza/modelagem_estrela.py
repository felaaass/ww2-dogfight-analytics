import os
import sqlite3
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

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
    return "Colapso do Eixo e Vitória Aliada (1945)"

def get_faixa_vitorias(v):
    if v >= 100:
        return "100+ Lenda da Aviação"
    elif v >= 50:
        return "50-99 Super As"
    elif v >= 20:
        return "20-49 Grande As"
    elif v >= 10:
        return "10-19 As Veterano"
    return "5-9 As"

def build_star_schema():
    proc_dir = os.path.join(BASE_DIR, "data", "processed")
    db_path = os.path.join(proc_dir, "dogfight.db")
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    
    df_ases = pd.read_csv(os.path.join(proc_dir, "ases_limpo.csv"))
    df_cacas = pd.read_csv(os.path.join(proc_dir, "cacas_limpo.csv"))
    df_batalhas = pd.read_csv(os.path.join(proc_dir, "batalhas_perdas_limpo.csv"))
    df_producao = pd.read_csv(os.path.join(proc_dir, "producao_e_atrito_limpo.csv"))
    
    # 1. dim_pais
    paises_info = [
        {"id_pais": 1, "nome": "Alemanha", "lado": "Eixo"},
        {"id_pais": 2, "nome": "Japão", "lado": "Eixo"},
        {"id_pais": 3, "nome": "Itália", "lado": "Eixo"},
        {"id_pais": 4, "nome": "Estados Unidos", "lado": "Aliados"},
        {"id_pais": 5, "nome": "Reino Unido", "lado": "Aliados"},
        {"id_pais": 6, "nome": "União Soviética", "lado": "Aliados"},
        {"id_pais": 7, "nome": "Aliados", "lado": "Aliados"}
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
    pais_id_map = dict(zip(df_dim_pais["nome"], df_dim_pais["id_pais"]))
    
    # 2. dim_data
    datas_list = [f"{ano}-01-01" for ano in range(1937, 1946)]
    for d in df_batalhas["data"].unique():
        if d not in datas_list:
            datas_list.append(d)
    datas_list = sorted(list(set(datas_list)))
    
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
    
    # 3. dim_batalha
    batalhas_unicas = df_batalhas["batalha"].unique()
    dim_batalha_records = []
    for idx, b_nome in enumerate(batalhas_unicas, start=1):
        sub_df = df_batalhas[df_batalhas["batalha"] == b_nome]
        d_min = sub_df["data"].min()
        d_max = sub_df["data"].max()
        
        if "Inglaterra" in b_nome:
            teatro = "Europa Ocidental (Batalha da Inglaterra)"
        elif "Midway" in b_nome:
            teatro = "Pacífico Central"
        elif "Filipinas" in b_nome:
            teatro = "Pacífico Ocidental (Mar das Filipinas)"
        elif any(k in b_nome for k in ["Schweinfurt", "Berlin", "Berlim", "Big Week", "Bodenplatte"]):
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
    batalha_id_map = dict(zip(df_dim_batalha["nome"], df_dim_batalha["id_batalha"]))
    
    # 4. dim_aeronave
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
    
    # 5. dim_piloto
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
    
    # 6. fato_perdas
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
    
    # 7. fato_producao
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
    
    # 8. fato_vitorias
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
    df_fato_vitorias["id_data"] = 19440101
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
    
    cur.execute("CREATE INDEX idx_fato_perdas_batalha ON fato_perdas(id_batalha);")
    cur.execute("CREATE INDEX idx_fato_perdas_pais ON fato_perdas(id_pais);")
    cur.execute("CREATE INDEX idx_fato_perdas_data ON fato_perdas(id_data);")
    cur.execute("CREATE INDEX idx_fato_producao_pais ON fato_producao(id_pais);")
    cur.execute("CREATE INDEX idx_fato_producao_data ON fato_producao(id_data);")
    cur.execute("CREATE INDEX idx_fato_vitorias_piloto ON fato_vitorias(id_piloto);")
    cur.execute("CREATE INDEX idx_fato_vitorias_pais ON fato_vitorias(id_pais);")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    build_star_schema()
