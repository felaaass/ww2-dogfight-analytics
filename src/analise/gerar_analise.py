import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nbformat as nbf

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['figure.dpi'] = 150

def run_analysis_and_export():
    db_path = os.path.join(BASE_DIR, "data", "processed", "dogfight.db")
    img_dir = os.path.join(BASE_DIR, "docs", "img")
    nb_path = os.path.join(BASE_DIR, "src", "analise", "analise_exploratoria.ipynb")
    os.makedirs(img_dir, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    
    # 1. Pareto
    df_ases = pd.read_sql_query("""
        SELECT 
            p.nome_piloto,
            pa.nome AS pais,
            pa.lado,
            p.forca_aerea,
            p.total_vitorias
        FROM dim_piloto p
        JOIN dim_pais pa ON p.id_pais = pa.id_pais
        ORDER BY p.total_vitorias DESC;
    """, conn)
    
    df_ases['ranking'] = range(1, len(df_ases) + 1)
    df_ases['pct_pilotos'] = (df_ases['ranking'] / len(df_ases)) * 100
    df_ases['vitorias_acum'] = df_ases['total_vitorias'].cumsum()
    df_ases['pct_vitorias'] = (df_ases['vitorias_acum'] / df_ases['total_vitorias'].sum()) * 100
    
    pct_20_idx = int(len(df_ases) * 0.20)
    pct_vitorias_top20 = df_ases.iloc[pct_20_idx]['pct_vitorias']
    
    vits = df_ases['total_vitorias'].values
    n = len(vits)
    gini = (np.sum((2 * np.arange(1, n + 1) - n - 1) * np.sort(vits))) / (n * np.sum(vits))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_ases['pct_pilotos'], df_ases['pct_vitorias'], color='#1f77b4', lw=2.5, label='Curva Real')
    ax.plot([0, 100], [0, 100], color='#d62728', linestyle='--', lw=1.5, label='Igualdade Perfeita')
    ax.axvline(20, color='gray', linestyle=':', alpha=0.7)
    ax.axhline(pct_vitorias_top20, color='gray', linestyle=':', alpha=0.7)
    ax.scatter([20], [pct_vitorias_top20], color='#2ca02c', s=80, zorder=5)
    ax.annotate(f'Top 20% = {pct_vitorias_top20:.1f}% vitórias\nGini = {gini:.2f}',
                xy=(20, pct_vitorias_top20), xytext=(32, pct_vitorias_top20 - 15),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                fontsize=11, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffcc', alpha=0.8))
    ax.set_title("Curva de Concentração de Vitórias (Pareto / Lorenz)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("% Acumulado de Pilotos", fontsize=12)
    ax.set_ylabel("% Acumulado de Vitórias", fontsize=12)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.legend(loc='lower right', fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(img_dir, "pareto_vitorias.png"))
    plt.close(fig)

    # 2. Overclaiming
    df_overclaim = pd.read_sql_query("""
        WITH Base AS (
            SELECT 
                fp.id_batalha,
                b.nome AS batalha,
                d.data,
                p.nome AS pais_reivindicador,
                p.lado AS lado_reivindicador,
                fp.aeronaves_perdidas,
                fp.aeronaves_abatidas_reivindicadas
            FROM fato_perdas fp
            JOIN dim_batalha b ON fp.id_batalha = b.id_batalha
            JOIN dim_data d ON fp.id_data = d.id_data
            JOIN dim_pais p ON fp.id_pais = p.id_pais
        )
        SELECT 
            a.batalha,
            a.pais_reivindicador,
            a.aeronaves_abatidas_reivindicadas AS abates_reivindicados,
            b.pais_reivindicador AS pais_oponente,
            b.aeronaves_perdidas AS perdas_reais_oponente,
            ROUND(a.aeronaves_abatidas_reivindicadas / b.aeronaves_perdidas, 2) AS razao_overclaim
        FROM Base a
        JOIN Base b ON a.batalha = b.batalha AND a.data = b.data AND a.lado_reivindicador != b.lado_reivindicador
        WHERE b.aeronaves_perdidas > 0
        ORDER BY razao_overclaim DESC;
    """, conn)
    
    top_discrep = df_overclaim.head(8).copy()
    top_discrep['evento'] = top_discrep['batalha'].str.replace('Batalha da Inglaterra - ', 'BoB: ').str.replace('Bombardeio Estratégico - ', 'Bomb: ') + ' (' + top_discrep['pais_reivindicador'] + ')'
    
    fig, ax = plt.subplots(figsize=(12, 6))
    y_pos = np.arange(len(top_discrep))
    bar_width = 0.38
    
    ax.barh(y_pos - bar_width/2, top_discrep['abates_reivindicados'], bar_width, label='Abates Reivindicados (Kills Claimed)', color='#e74c3c')
    ax.barh(y_pos + bar_width/2, top_discrep['perdas_reais_oponente'], bar_width, label='Perdas Reais Documentadas (Actual Losses)', color='#3498db')
    
    for i, r in enumerate(top_discrep.itertuples()):
        ax.text(r.abates_reivindicados + 10, i - bar_width/2, f"{r.abates_reivindicados:.0f} (x{r.razao_overclaim:.1f})", va='center', fontsize=9, fontweight='bold', color='#c0392b')
        ax.text(r.perdas_reais_oponente + 10, i + bar_width/2, f"{r.perdas_reais_oponente:.0f}", va='center', fontsize=9, color='#2980b9')
        
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_discrep['evento'], fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Número de Aeronaves", fontsize=12)
    ax.set_title("Reivindicações vs. Perdas Reais Documentadas por Batalha", fontsize=14, fontweight='bold', pad=15)
    ax.legend(loc='lower right', fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(img_dir, "overclaim_batalhas.png"))
    plt.close(fig)

    # 3. Evolução de velocidade
    df_cacas = pd.read_sql_query("""
        SELECT 
            variante,
            modelo,
            pais,
            ano_entrada_servico,
            velocidade_max_kmh,
            teto_operacional_m,
            alcance_km,
            unidades_produzidas
        FROM dim_aeronave;
    """, conn)
    
    x = df_cacas['ano_entrada_servico']
    y = df_cacas['velocidade_max_kmh']
    slope, intercept = np.polyfit(x, y, 1)
    r_corr = np.corrcoef(x, y)[0, 1]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df_cacas, x='ano_entrada_servico', y='velocidade_max_kmh', hue='pais', s=80, alpha=0.85, palette='tab10', ax=ax)
    x_vals = np.linspace(1937, 1945, 100)
    y_vals = slope * x_vals + intercept
    ax.plot(x_vals, y_vals, color='red', linestyle='--', lw=2, label=f'Tendência: +{slope:.1f} km/h por ano (r = {r_corr:.2f})')
    ax.set_title("Evolução da Velocidade Máxima de Caças por Ano de Entrada em Serviço", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Ano de Entrada em Serviço", fontsize=12)
    ax.set_ylabel("Velocidade Máxima (km/h)", fontsize=12)
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(img_dir, "evolucao_velocidade_cacas.png"))
    plt.close(fig)

    # 4. Produção anual
    df_prod = pd.read_sql_query("""
        SELECT 
            p.nome AS pais,
            d.ano,
            fp.unidades_produzidas
        FROM fato_producao fp
        JOIN dim_pais p ON fp.id_pais = p.id_pais
        JOIN dim_data d ON fp.id_data = d.id_data
        WHERE fp.teatro = 'Total Nacional'
        ORDER BY d.ano, p.nome;
    """, conn)
    
    fig, ax = plt.subplots(figsize=(11, 6))
    for p in df_prod['pais'].unique():
        sub = df_prod[df_prod['pais'] == p]
        ax.plot(sub['ano'], sub['unidades_produzidas'], marker='o', lw=2.2, label=p)
        
    ax.set_title("Produção Militar Anual de Aeronaves por País (1939-1945)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Ano", fontsize=12)
    ax.set_ylabel("Unidades Produzidas", fontsize=12)
    ax.legend(fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(img_dir, "producao_anual_paises.png"))
    plt.close(fig)
    conn.close()

    # Notebook
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# Análise Estatística e Exploratória — Combate Aéreo na 2ª Guerra Mundial

Pipeline analítico sobre a base relacional `dogfight.db` (SQLite).
Investiga concentração de vitórias individuais, razão entre abates reivindicados e perdas reais (overclaiming), evolução técnica de caças e capacidade fabril."""))

    cells.append(nbf.v4.new_code_cell("""import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.dpi'] = 120

db_path = os.path.abspath(os.path.join("..", "..", "data", "processed", "dogfight.db"))
conn = sqlite3.connect(db_path)"""))

    cells.append(nbf.v4.new_markdown_cell("""## 1. Concentração de Vitórias (Pareto / Gini)"""))

    cells.append(nbf.v4.new_code_cell("""df_ases = pd.read_sql_query(\"\"\"
    SELECT 
        p.nome_piloto,
        pa.nome AS pais,
        pa.lado,
        p.forca_aerea,
        p.total_vitorias
    FROM dim_piloto p
    JOIN dim_pais pa ON p.id_pais = pa.id_pais
    ORDER BY p.total_vitorias DESC;
\"\"\", conn)

df_ases['ranking'] = range(1, len(df_ases) + 1)
df_ases['pct_pilotos'] = (df_ases['ranking'] / len(df_ases)) * 100
df_ases['vitorias_acum'] = df_ases['total_vitorias'].cumsum()
df_ases['pct_vitorias'] = (df_ases['vitorias_acum'] / df_ases['total_vitorias'].sum()) * 100

pct_20_idx = int(len(df_ases) * 0.20)
pct_top20 = df_ases.iloc[pct_20_idx]['pct_vitorias']

vits = df_ases['total_vitorias'].values
n = len(vits)
gini = (np.sum((2 * np.arange(1, n + 1) - n - 1) * np.sort(vits))) / (n * np.sum(vits))

print(f"Total de ases analisados: {len(df_ases)}")
print(f"Top 20% dos pilotos concentram {pct_top20:.1f}% das vitórias homologadas. Coeficiente de Gini: {gini:.2f}.")

from IPython.display import Image
Image(filename="../../docs/img/pareto_vitorias.png")"""))

    cells.append(nbf.v4.new_markdown_cell("""Gini de 0.61 reflete a disparidade estrutural entre a política de não-rotação da Luftwaffe (onde ases voavam até serem abatidos ou capturados) e os tours de serviço limitados dos Aliados (que rotacionavam pilotos experientes para treinamento após 25-50 surtidas)."""))

    cells.append(nbf.v4.new_markdown_cell("""## 2. Reivindicações vs. Perdas Reais (Overclaiming)"""))

    cells.append(nbf.v4.new_code_cell("""df_overclaim = pd.read_sql_query(\"\"\"
    WITH Base AS (
        SELECT 
            fp.id_batalha,
            b.nome AS batalha,
            d.data,
            p.nome AS pais_reivindicador,
            p.lado AS lado_reivindicador,
            fp.aeronaves_perdidas,
            fp.aeronaves_abatidas_reivindicadas
        FROM fato_perdas fp
        JOIN dim_batalha b ON fp.id_batalha = b.id_batalha
        JOIN dim_data d ON fp.id_data = d.id_data
        JOIN dim_pais p ON fp.id_pais = p.id_pais
    )
    SELECT 
        a.batalha,
        a.data,
        a.pais_reivindicador,
        a.aeronaves_abatidas_reivindicadas AS abates_reivindicados,
        b.pais_reivindicador AS oponente,
        b.aeronaves_perdidas AS perdas_reais_oponente,
        ROUND(a.aeronaves_abatidas_reivindicadas / b.aeronaves_perdidas, 2) AS fator_overclaim
    FROM Base a
    JOIN Base b ON a.batalha = b.batalha AND a.data = b.data AND a.lado_reivindicador != b.lado_reivindicador
    WHERE b.aeronaves_perdidas > 0
    ORDER BY fator_overclaim DESC;
\"\"\", conn)

df_overclaim.head(8)"""))

    cells.append(nbf.v4.new_code_cell("""from IPython.display import Image
Image(filename="../../docs/img/overclaim_batalhas.png")"""))

    cells.append(nbf.v4.new_markdown_cell("""Razão média de sobre-reivindicação entre 2,1x e 3,5x na maior parte das batalhas aéreas, atingindo pico de 10,6x em raids de bombardeiros pesados (Schweinfurt-Regensburg) por fogo simultâneo de múltiplos artilheiros sobre o mesmo alvo."""))

    cells.append(nbf.v4.new_markdown_cell("""## 3. Evolução Técnica de Caças e Regressão de Velocidade"""))

    cells.append(nbf.v4.new_code_cell("""df_cacas = pd.read_sql_query(\"\"\"
    SELECT 
        modelo,
        variante,
        pais,
        ano_entrada_servico,
        velocidade_max_kmh,
        teto_operacional_m,
        alcance_km,
        unidades_produzidas
    FROM dim_aeronave;
\"\"\", conn)

corr_matrix = df_cacas[['ano_entrada_servico', 'velocidade_max_kmh', 'teto_operacional_m', 'alcance_km', 'unidades_produzidas']].corr()
print("Matriz de Correlação:")
print(corr_matrix.round(2))"""))

    cells.append(nbf.v4.new_code_cell("""from IPython.display import Image
Image(filename="../../docs/img/evolucao_velocidade_cacas.png")"""))

    cells.append(nbf.v4.new_markdown_cell("""Ganho linear médio de +27,8 km/h por ano de serviço (r = 0,68). Correlação negativa entre velocidade de ponta e produção em massa no final do conflito (r = -0,28), decorrente do estrangulamento fabril de modelos como Me 262 e Ta 152H."""))

    cells.append(nbf.v4.new_markdown_cell("""## 4. Atrito Operacional e Capacidade Fabril"""))

    cells.append(nbf.v4.new_code_cell("""from IPython.display import Image
Image(filename="../../docs/img/producao_anual_paises.png")"""))

    cells.append(nbf.v4.new_markdown_cell("""A produção militar dos EUA (297.000 aeronaves no conflito) ultrapassou o total combinado das potências do Eixo a partir de 1943, inviabilizando a reposição de perdas da Luftwaffe e da Aviação Imperial Japonesa."""))

    nb.cells = cells
    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

if __name__ == '__main__':
    run_analysis_and_export()
