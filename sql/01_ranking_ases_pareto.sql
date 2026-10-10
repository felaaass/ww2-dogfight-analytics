-- ============================================================================
-- Consulta Analítica 1: Ranking de Ases e Curva de Concentração de Pareto
-- Objetivo: Demonstrar a concentração extrema de vitórias na guerra aérea.
-- Utiliza: CTEs, Window Functions (SUM OVER, ROW_NUMBER, COUNT OVER, ROUND).
-- Banco: dogfight.db (SQLite / DuckDB / SQL padrão ANSI)
-- ============================================================================

WITH BaseAses AS (
    SELECT 
        p.id_piloto,
        p.nome_piloto,
        pa.nome AS pais,
        pa.lado,
        p.forca_aerea,
        p.total_vitorias,
        p.aeronave_principal,
        p.teatro_de_operacao
    FROM dim_piloto p
    INNER JOIN dim_pais pa ON p.id_pais = pa.id_pais
),
RankingAcumulado AS (
    SELECT 
        id_piloto,
        nome_piloto,
        pais,
        lado,
        forca_aerea,
        total_vitorias,
        aeronave_principal,
        teatro_de_operacao,
        ROW_NUMBER() OVER (ORDER BY total_vitorias DESC, nome_piloto ASC) AS ranking_geral,
        ROW_NUMBER() OVER (PARTITION BY pais ORDER BY total_vitorias DESC) AS ranking_pais,
        SUM(total_vitorias) OVER (
            ORDER BY total_vitorias DESC, nome_piloto ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS vitorias_acumuladas,
        SUM(total_vitorias) OVER () AS total_geral_vitorias,
        COUNT(id_piloto) OVER () AS total_pilotos
    FROM BaseAses
)
SELECT 
    ranking_geral,
    ranking_pais,
    nome_piloto,
    pais,
    lado,
    forca_aerea,
    total_vitorias,
    vitorias_acumuladas,
    ROUND((vitorias_acumuladas * 100.0) / total_geral_vitorias, 2) AS pct_acumulado_vitorias,
    ROUND((ranking_geral * 100.0) / total_pilotos, 2) AS pct_acumulado_pilotos,
    aeronave_principal,
    teatro_de_operacao
FROM RankingAcumulado
ORDER BY ranking_geral ASC;
