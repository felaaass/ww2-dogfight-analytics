# Ases e Atrito — Análise da Guerra Aérea na 2ª Guerra Mundial

Pipeline de dados analítico sobre o combate aéreo na Segunda Guerra Mundial (1939–1945), contrastando métricas de performance de ases individuais com a capacidade fabril, perdas reais e discrepâncias sistemáticas de sobre-reivindicação (*overclaiming*).

## Stack

- **Python** — extração via APIs públicas e `pdfplumber`, validação de contratos de dados com `pandera`
- **SQL (SQLite)** — banco dimensional local (`dogfight.db`) com Star Schema, Views, CTEs e Window Functions
- **Power BI** — dashboard com Star Schema e modelagem dimensional
- **Jupyter Notebook** — análise exploratória, curva de concentração de Lorenz/Gini e regressão linear

## Metodologia

- Universo de ases: 1.020 pilotos cobrindo Alemanha, EUA, Reino Unido, União Soviética e Japão com corte mínimo de 5 vitórias homologadas
- Modelagem de aeronaves: 83 caças segmentados no nível de **variante** (ex.: Bf 109E-3 vs. Bf 109G-6; Spitfire Mk I vs. Mk XIV) devido a saltos drásticos de motorização, armamento e peso que invalidariam agregações por modelo genérico
- Perdas e reivindicações: pareamento sistemático de 30 confrontos em grandes batalhas (Batalha da Inglaterra, Midway, Mar das Filipinas e Ofensiva de Bombardeio Estratégico), isolando perdas reais admitidas pelo país versus vitórias reivindicadas pelo oponente
- Produção e esforço operacional: consolidação da produção militar anual das 5 potências (1939–1945) combinada com dados de sorties e perdas da USAAF por teatro

## Notas técnicas

Durante a extração do *Army Air Forces Statistical Digest* (1945) via `pdfplumber`, as tabelas mensais de sorties e perdas apresentavam falhas de digitalização e ruído de OCR nas quebras de sub-teatros menores. Em vez de imputar ou aproximar valores, mantivemos os números auditados anuais por teatro (Tabelas 118, 158 e 166), preservando as lacunas como `NULL` para não introduzir estimativas artificiais no pipeline.

Na comparação de ases, a discrepância entre pilotos da Luftwaffe (Hartmann com 352 vitórias) e aliados (Bong com 40; Johnson com 34) reflete uma decisão de doutrina operacional: a Alemanha manteve veteranos em combate contínuo até a morte ou captura, enquanto os Aliados praticavam rotação após 25–50 missões (*tour of duty*) para formar novos pilotos como instrutores de voo.

Nos dados japoneses, a Marinha e o Exército Imperial proibiram registros individuais de abates a partir do início de 1943 em favor do sacrifício coletivo da unidade. Somado à perda de arquivos no afundamento de porta-aviões e à queima de relatórios em Tóquio em agosto de 1945, os dados japoneses representam consolidações historiográficas pós-guerra (*Senshi Sōsho* / Henry Sakaida).

## Resultados

- **Concentração de Vitórias (Pareto / Gini):** Coeficiente de Gini de **0.61** no universo de ases analisado, com os top 20% dos pilotos concentrando **60,8% de todos os abates confirmados**.
- **Overclaiming Sistemático:** O fator de sobre-reivindicação oscila de 2,7x na Batalha da Inglaterra até 10,6x na missão Schweinfurt-Regensburg (agosto de 1943: 288 caças alemães reivindicados pela 8th Air Force vs. 27 perdas reais admitidas pela Luftwaffe). A distorção é inerente à física do combate tridimensional em alta velocidade e disparos múltiplos simultâneos contra a mesma aeronave.
- **Evolução Técnica:** A velocidade máxima dos caças avançou a uma taxa média de **+27,8 km/h por ano de serviço** ($r = 0,68$), saltando de ~530 km/h em 1939 para quase 800 km/h a pistão e 900 km/h a jato em 1944–1945.
- **Predomínio Industrial:** Em 1944, a produção americana de aeronaves atingiu 96.318 unidades em 12 meses — superando a produção alemã de 1941 a 1943 somada. A capacidade fabril de reposição e formação de tripulações superou o impacto tático dos ases individuais.

## Validação cruzada

Os números foram conferidos em três camadas independentes — Python (Pandas/Pandera), SQLite (`dogfight.db`) e arquivos dimensionais processados (CSVs) — batendo exatamente: 1.020 ases, 83 variantes de caças, 30 registros de batalha e 61 registros de produção/atrito.

## Estrutura

```text
src/
├── coleta/
│   ├── coleta_ases.py             # extração de ases via Wikipedia API
│   ├── coleta_cacas.py            # especificações de 83 variantes de caças
│   ├── coleta_batalhas.py         # perdas reais vs reivindicações por batalha
│   └── coleta_producao_atrito.py  # extração de dados do AAFSD e produção nacional
├── limpeza/
│   ├── limpeza_validacao.py       # validação de esquemas via Pandera e padronização
│   └── modelagem_estrela.py       # carga relacional SQLite (dogfight.db) e exportação
└── analise/
    ├── gerar_analise.py           # pipeline de cálculo estatístico e exportação de figuras
    └── analise_exploratoria.ipynb # notebook executado com gráficos de Pareto e regressão
sql/
├── 01_ranking_ases_pareto.sql     # ranking acumulado de vitórias e curva de Pareto
├── 02_razao_reivindicacoes_perdas.sql # razão reivindicação vs perda real por batalha
├── 03_evolucao_perdas_temporal.sql# perdas acumuladas e variação temporal (LAG)
├── 04_comparacao_variantes_aeronaves.sql # evolução de especificações por linhagem
└── 05_correlacao_producao_perdas.sql # correlação entre capacidade fabril e atrito
docs/
├── dicionario_dados.md            # especificação das 8 tabelas dimensionais e fatos
├── metodologia_e_limitacoes.md    # documentação técnica de fontes e lacunas históricas
├── guia_powerbi.md                # especificação de relacionamentos e páginas do dashboard
├── log_coleta.md                  # log de extração de dados brutos
└── log_limpeza.md                 # log de validação e integridade Pandera
data/
├── raw/                           # CSVs brutos coletados e PDF original da USAAF
└── processed/                     # banco SQLite (dogfight.db) e CSVs dimensionais/fatos
requirements.txt
LICENSE
```

## Status

- [x] Etapa 1 — Coleta e extração de dados brutos (ases, caças, batalhas, produção)
- [x] Etapa 2 — Higienização e validação com Pandera
- [x] Etapa 3 — Modelagem dimensional em Star Schema (SQLite + CSVs processados)
- [x] Etapa 4 — Consultas SQL analíticas com Window Functions e CTEs
- [x] Etapa 5 — Análise exploratória e regressão em Jupyter Notebook
- [ ] Etapa 6 — Dashboard Power BI


