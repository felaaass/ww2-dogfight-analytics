-- ============================================================================
-- Consulta Analítica 5: Relação entre Produção Industrial e Atrito Operacional
-- Objetivo: Cruzar a capacidade de reposição fabril de aeronaves com a intensidade
--           de perdas e saídas de combate por país e período.
-- Utiliza: CTEs, Window Functions (SUM, LAG, RATIO_TO_REPORT/PERCENT_RANK).
-- ============================================================================

WITH ProducaoNacional AS (
    SELECT 
        p.nome AS pais,
        p.lado,
        d.ano,
        fp.unidades_produzidas
    FROM fato_producao fp
    INNER JOIN dim_pais p ON fp.id_pais = p.id_pais
    INNER JOIN dim_data d ON fp.id_data = d.id_data
    WHERE fp.teatro = 'Total Nacional' AND fp.unidades_produzidas IS NOT NULL
),
AtritoUSAAF AS (
    SELECT 
        d.ano,
        SUM(fp.sorties) AS total_sorties,
        SUM(fp.perdas_combate) AS total_perdas_combate,
        SUM(fp.abates_reivindicados) AS total_abates_reivindicados
    FROM fato_producao fp
    INNER JOIN dim_data d ON fp.id_data = d.id_data
    WHERE fp.teatro != 'Total Nacional' AND fp.sorties IS NOT NULL
    GROUP BY d.ano
)
SELECT 
    pn.pais,
    pn.lado,
    pn.ano,
    pn.unidades_produzidas,
    LAG(pn.unidades_produzidas) OVER (
        PARTITION BY pn.pais ORDER BY pn.ano ASC
    ) AS producao_ano_anterior,
    ROUND(
        ((pn.unidades_produzidas - LAG(pn.unidades_produzidas) OVER (PARTITION BY pn.pais ORDER BY pn.ano ASC)) * 100.0) /
        NULLIF(LAG(pn.unidades_produzidas) OVER (PARTITION BY pn.pais ORDER BY pn.ano ASC), 0), 1
    ) AS crescimento_producao_pct,
    -- Métricas operacionais USAAF para correlacionar no caso dos EUA
    CASE WHEN pn.pais = 'Estados Unidos' THEN usa.total_sorties ELSE NULL END AS sorties_usaaf,
    CASE WHEN pn.pais = 'Estados Unidos' THEN usa.total_perdas_combate ELSE NULL END AS perdas_combate_usaaf,
    CASE 
        WHEN pn.pais = 'Estados Unidos' AND usa.total_perdas_combate IS NOT NULL THEN
            ROUND((usa.total_perdas_combate * 100.0) / pn.unidades_produzidas, 2)
        ELSE NULL 
    END AS taxa_desgaste_vs_producao_pct
FROM ProducaoNacional pn
LEFT JOIN AtritoUSAAF usa ON pn.ano = usa.ano
ORDER BY pn.pais ASC, pn.ano ASC;
