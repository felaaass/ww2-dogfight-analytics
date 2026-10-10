-- ============================================================================
-- Consulta Analítica 2: Razão entre Abates Reivindicados e Perdas Reais por Batalha
-- Objetivo: Revelar o fenômeno histórico do 'overclaiming' comparando o que um
--           lado reivindicou ter abatido contra o que o oponente realmente perdeu.
-- Utiliza: Self-joins em CTEs, Window Functions (RANK, DENSE_RANK), Casos condicionais.
-- ============================================================================

WITH BatalhasDetalhadas AS (
    SELECT 
        fp.id_fato_perda,
        b.nome AS batalha,
        b.teatro,
        d.data,
        d.fase_da_guerra,
        p.nome AS pais_reivindicador,
        p.lado AS lado_reivindicador,
        fp.aeronaves_perdidas AS perdas_proprias,
        fp.aeronaves_abatidas_reivindicadas AS abates_reivindicados
    FROM fato_perdas fp
    INNER JOIN dim_batalha b ON fp.id_batalha = b.id_batalha
    INNER JOIN dim_data d ON fp.id_data = d.id_data
    INNER JOIN dim_pais p ON fp.id_pais = p.id_pais
),
ConfrontoOponentes AS (
    -- Pareia os registros da mesma batalha e data onde os lados são opostos
    SELECT 
        a.batalha,
        a.data,
        a.teatro,
        a.pais_reivindicador,
        a.lado_reivindicador,
        a.abates_reivindicados,
        b.pais_reivindicador AS pais_oponente,
        b.perdas_proprias AS perdas_reais_oponente,
        ROUND(
            CAST(a.abates_reivindicados AS REAL) / 
            NULLIF(b.perdas_proprias, 0), 2
        ) AS fator_sobre_reivindicacao
    FROM BatalhasDetalhadas a
    INNER JOIN BatalhasDetalhadas b 
        ON a.batalha = b.batalha 
        AND a.data = b.data 
        AND a.pais_reivindicador != b.pais_reivindicador
        AND a.lado_reivindicador != b.lado_reivindicador
)
SELECT 
    batalha,
    data,
    teatro,
    pais_reivindicador,
    abates_reivindicados,
    pais_oponente,
    perdas_reais_oponente,
    (abates_reivindicados - perdas_reais_oponente) AS discrepancia_absoluta,
    fator_sobre_reivindicacao,
    CASE 
        WHEN fator_sobre_reivindicacao >= 5.0 THEN 'Distorção Extrema (> 5x)'
        WHEN fator_sobre_reivindicacao >= 2.0 THEN 'Superestimação Severa (2x a 5x)'
        WHEN fator_sobre_reivindicacao >= 1.0 THEN 'Superestimação Moderada (1x a 2x)'
        ELSE 'Subnotificação / Perdas Ocultas (< 1x)'
    END AS classificacao_distorcao,
    DENSE_RANK() OVER (ORDER BY fator_sobre_reivindicacao DESC) AS ranking_maior_inflacao
FROM ConfrontoOponentes
ORDER BY fator_sobre_reivindicacao DESC;
