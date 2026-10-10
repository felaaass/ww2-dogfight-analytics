-- Comparação técnica de variantes de caças e ganho de velocidade (FIRST_VALUE / Window Functions)
WITH FamiliasPrincipais AS (
    SELECT 
        modelo,
        variante,
        pais,
        ano_entrada_servico,
        velocidade_max_kmh,
        teto_operacional_m,
        alcance_km,
        unidades_produzidas,
        armamento
    FROM dim_aeronave
    WHERE modelo IN (
        'Supermarine Spitfire', 
        'Messerschmitt Bf 109', 
        'Focke-Wulf Fw 190', 
        'North American P-51 Mustang', 
        'Republic P-47 Thunderbolt', 
        'Mitsubishi A6M Zero', 
        'Yakovlev Yak-9', 
        'Lavochkin La-5'
    )
),
EvolucaoVariantes AS (
    SELECT 
        modelo,
        variante,
        pais,
        ano_entrada_servico,
        velocidade_max_kmh,
        teto_operacional_m,
        alcance_km,
        unidades_produzidas,
        armamento,
        FIRST_VALUE(velocidade_max_kmh) OVER (
            PARTITION BY modelo 
            ORDER BY ano_entrada_servico ASC, variante ASC
        ) AS vel_variante_inicial,
        LAG(velocidade_max_kmh) OVER (
            PARTITION BY modelo 
            ORDER BY ano_entrada_servico ASC, variante ASC
        ) AS vel_variante_anterior,
        SUM(unidades_produzidas) OVER (PARTITION BY modelo) AS producao_total_familia
    FROM FamiliasPrincipais
)
SELECT 
    modelo,
    variante,
    pais,
    ano_entrada_servico,
    velocidade_max_kmh,
    (velocidade_max_kmh - vel_variante_inicial) AS ganho_velocidade_vs_base,
    ROUND(
        ((velocidade_max_kmh - vel_variante_inicial) * 100.0) / 
        vel_variante_inicial, 1
    ) AS ganho_velocidade_pct_vs_base,
    teto_operacional_m,
    alcance_km,
    unidades_produzidas,
    ROUND((unidades_produzidas * 100.0) / producao_total_familia, 1) AS share_producao_familia_pct,
    armamento
FROM EvolucaoVariantes
ORDER BY modelo ASC, ano_entrada_servico ASC, velocidade_max_kmh ASC;
