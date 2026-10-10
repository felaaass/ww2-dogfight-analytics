# Log de Limpeza e Validação de Dados

Execução: Pandas 2.3 + Pandera 0.34

## 1. Regras de Integridade

- Nulos preservados como `NULL` sem imputação estatística.
- Padronização de nomes de países (Alemanha, Estados Unidos, Reino Unido, União Soviética, Japão, Itália, Aliados).
- Conversão e validação estrita de tipos por schema Pandera.

## 2. Relatório de Execução

### `ases_limpo.csv`
- Linhas: 1020 -> 1020 (0 duplicatas removidas)
- Status: VALIDADO COM SUCESSO
- Nulos por coluna:
  - `nome_piloto`: 0
  - `pais`: 0
  - `forca_aerea`: 0
  - `numero_vitorias`: 0
  - `aeronave_principal`: 0
  - `teatro_de_operacao`: 0
  - `periodo_ativo`: 0
  - `fonte`: 0

### `cacas_limpo.csv`
- Linhas: 83 -> 83 (0 duplicatas removidas)
- Status: VALIDADO COM SUCESSO
- Nulos por coluna:
  - `modelo`: 0
  - `variante`: 0
  - `pais`: 0
  - `ano_entrada_servico`: 0
  - `velocidade_max_kmh`: 0
  - `teto_operacional_m`: 0
  - `alcance_km`: 0
  - `armamento`: 0
  - `unidades_produzidas`: 0
  - `fonte`: 0

### `batalhas_perdas_limpo.csv`
- Linhas: 30 -> 30 (0 duplicatas removidas)
- Status: VALIDADO COM SUCESSO
- Nulos por coluna:
  - `batalha`: 0
  - `data`: 0
  - `pais`: 0
  - `aeronaves_perdidas`: 0
  - `aeronaves_abatidas_reivindicadas`: 0
  - `fonte`: 0

### `producao_e_atrito_limpo.csv`
- Linhas: 61 -> 61 (0 duplicatas removidas)
- Status: VALIDADO COM SUCESSO
- Nulos por coluna:
  - `pais`: 0
  - `ano`: 0
  - `teatro`: 0
  - `sorties`: 35
  - `perdas_combate`: 35
  - `abates_reivindicados`: 36
  - `unidades_produzidas`: 26
  - `fonte`: 0

