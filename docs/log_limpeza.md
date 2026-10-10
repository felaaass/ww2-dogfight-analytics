# Log de Limpeza e Validação de Dados — Projeto Ases e Atrito

Data de Execução: Outubro de 2026  
Mecanismo de Validação: Pandas 2.3 + Pandera 0.34  

## 1. Princípios de Limpeza e Integridade

1. **Nenhum Dado Inventado:** Valores ausentes foram mantidos estritamente como `NULL` (NaN).
2. **Padronização Geopolítica:** Nomes de países unificados no padrão lusófono:
   `Alemanha`, `Estados Unidos`, `Reino Unido`, `União Soviética`, `Japão`, `Itália` e `Aliados`.
3. **Padronização de Unidades:**
   - Velocidade: km/h (quilômetros por hora)
   - Altitude / Teto: m (metros)
   - Alcance: km (quilômetros)
   - Perdas e Abates: contagem inteira de aeronaves
4. **Validação de Esquemas (Pandera):** Checagem rigorosa de tipos, faixas numéricas de plausibilidade física e completude da coluna `fonte`.

---

## 2. Relatório de Execução por Tabela

### Tabela: `ases_limpo.csv`
- **Linhas Iniciais:** 1020
- **Linhas Finais:** 1020
- **Duplicatas Removidas:** 0
- **Status Pandera:** VALIDADO COM SUCESSO
- **Contagem de Nulos por Coluna:**
  - `nome_piloto`: 0 nulos
  - `pais`: 0 nulos
  - `forca_aerea`: 0 nulos
  - `numero_vitorias`: 0 nulos
  - `aeronave_principal`: 0 nulos
  - `teatro_de_operacao`: 0 nulos
  - `periodo_ativo`: 0 nulos
  - `fonte`: 0 nulos

### Tabela: `cacas_limpo.csv`
- **Linhas Iniciais:** 83
- **Linhas Finais:** 83
- **Duplicatas Removidas:** 0
- **Status Pandera:** VALIDADO COM SUCESSO
- **Contagem de Nulos por Coluna:**
  - `modelo`: 0 nulos
  - `variante`: 0 nulos
  - `pais`: 0 nulos
  - `ano_entrada_servico`: 0 nulos
  - `velocidade_max_kmh`: 0 nulos
  - `teto_operacional_m`: 0 nulos
  - `alcance_km`: 0 nulos
  - `armamento`: 0 nulos
  - `unidades_produzidas`: 0 nulos
  - `fonte`: 0 nulos

### Tabela: `batalhas_perdas_limpo.csv`
- **Linhas Iniciais:** 30
- **Linhas Finais:** 30
- **Duplicatas Removidas:** 0
- **Status Pandera:** VALIDADO COM SUCESSO
- **Contagem de Nulos por Coluna:**
  - `batalha`: 0 nulos
  - `data`: 0 nulos
  - `pais`: 0 nulos
  - `aeronaves_perdidas`: 0 nulos
  - `aeronaves_abatidas_reivindicadas`: 0 nulos
  - `fonte`: 0 nulos

### Tabela: `producao_e_atrito_limpo.csv`
- **Linhas Iniciais:** 61
- **Linhas Finais:** 61
- **Duplicatas Removidas:** 0
- **Status Pandera:** VALIDADO COM SUCESSO
- **Contagem de Nulos por Coluna:**
  - `pais`: 0 nulos
  - `ano`: 0 nulos
  - `teatro`: 0 nulos
  - `sorties`: 35 nulos
  - `perdas_combate`: 35 nulos
  - `abates_reivindicados`: 36 nulos
  - `unidades_produzidas`: 26 nulos
  - `fonte`: 0 nulos

