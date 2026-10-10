-- ============================================================================
-- Consulta Analítica 3: Evolução Temporal das Perdas e Atrição por País e Fase
-- Objetivo: Rastrear o custo em aeronaves ao longo das diferentes fases da guerra,
--           calculando totais acumulados e variação período a período.
-- Utiliza: CTEs, Window Functions (LAG, SUM OVER PARTITION BY).
-- ============================================================================

WITH PerdasPorFase AS (
    SELECT 
        p.nome AS pais,
        p.lado,
        d.fase_da_guerra,
        MIN(d.ano) AS ano_inicio_fase,
        SUM(fp.aeronaves_perdidas) AS total_aeronaves_perdidas,
        SUM(fp.aeronaves_abatidas_reivindicadas) AS total_abates_reivindicados
    FROM fato_perdas fp
    INNER JOIN dim_pais p ON fp.id_pais = p.id_pais
    INNER JOIN dim_data d ON fp.id_data = d.id_data
    GROUP BY p.nome, p.lado, d.fase_da_guerra
),
EvolucaoTemporal AS (
    SELECT 
        pais,
        lado,
        fase_da_guerra,
        ano_inicio_fase,
        total_aeronaves_perdidas,
        total_abates_reivindicados,
        LAG(total_aeronaves_perdidas) OVER (
            PARTITION BY pais 
            ORDER BY ano_inicio_fase ASC
        ) AS perdas_fase_anterior,
        SUM(total_aeronaves_perdidas) OVER (
            PARTITION BY pais 
            ORDER BY ano_inicio_fase ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS perdas_cumulativas
    FROM PerdasPorFase
)
SELECT 
    pais,
    lado,
    fase_da_guerra,
    total_aeronaves_perdidas,
    perdas_fase_anterior,
    COALESCE(
        ROUND(
            ((total_aeronaves_perdidas - perdas_fase_anterior) * 100.0) / 
            NULLIF(perdas_fase_anterior, 0), 2
        ), 0.0
    ) AS variacao_pct_fase_anterior,
    perdas_cumulativas,
    total_abates_reivindicados,
    ROUND(
        CAST(total_abates_reivindicados AS REAL) / 
        NULLIF(total_aeronaves_perdidas, 0), 2
    ) AS razao_reivindicacoes_perdas_proprias
FROM EvolucaoTemporal
ORDER BY pais ASC, ano_inicio_fase ASC;
