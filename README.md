# Ases e Atrito — A Guerra Aérea da 2ª Guerra Mundial Contada pelos Números

Pipeline de dados analítico de ponta a ponta, modelagem em esquema estrela (*Star Schema*), banco relacional, análises estatísticas, fórmulas DAX e consultas Power Query para alimentar um dashboard executivo no **Power BI Desktop**.

---

## 1. Visão Geral e Objetivo

O projeto **"Ases e Atrito"** investiga o combate aéreo na Segunda Guerra Mundial (1939–1945) através da frieza dos números. Contrastando as narrativas heroicas dos ases individuais com a realidade matemática da produção industrial, do atrito operacional e do fenômeno da supernotificação de vitórias (*overclaiming*), este pipeline entrega dados higienizados e auditados, modelagem relacional robusta e especificações prontas para montagem do dashboard no Power BI Desktop.

> **Regra de Ouro do Projeto:**  
> **Nenhum número histórico foi inventado, estimado ou arredondado de memória.** Toda linha de dado carrega sua respectiva fonte documental na coluna `fonte`. Valores não documentados com certeza primária foram preservados como `NULL`.

---

## 2. Perguntas que Este Projeto Responde

1. **A Regra de Pareto se Aplica aos Ases?**  
   Que porcentagem dos pilotos concentrava a maioria das vitórias aéreas? Qual é a diferença doutrinária entre os ases alemães (que acumulavam até 352 vitórias sem rotação operacional) e os ases aliados (retirados do fronte após 25 a 50 missões para atuarem como instrutores)?
2. **Qual a Dimensão Real do *Overclaiming*?**  
   Qual a proporção entre os abates que os aviadores e artilheiros reivindicavam ter conquistado (*kills claimed*) e as perdas reais que o inimigo efetivamente sofreu (*actual losses*) em batalhas decisivas como a Batalha da Inglaterra, Midway, Mar das Filipinas e os bombardeios a Schweinfurt?
3. **Qual Foi o Ritmo do Salto Tecnológico dos Caças?**  
   Como a velocidade máxima, o teto de serviço e o alcance evoluíram ano a ano entre as variantes de caças da mesma família (ex.: Spitfire Mk I vs. Mk XIV; Bf 109E vs. Bf 109K; P-51A vs. P-51D)?
4. **Ases vs. Capacidade Fabril: O que Realmente Decidiu a Guerra?**  
   Como se comportou a taxa de produção anual de aeronaves frente às perdas de combate? A superioridade individual dos ases alemães conseguiu compensar o esmagador rolo compressor fabril dos Aliados?

---

## 3. Stack Tecnológica

* **Linguagem & Ambiente:** Python 3.11
* **Coleta & Scraping:** Requests, BeautifulSoup4, LXML, PDFPlumber (extração direta de tabelas do relatório original do Departamento de Guerra dos EUA)
* **Limpeza & Validação de Esquema:** Pandas 2.3, Pandera 0.34 (validação estrita de contratos de dados e tipos)
* **Banco de Dados Relacional:** SQLite 3 (`dogfight.db`) com integridade de chaves estrangeiras (`PRAGMA foreign_keys = ON`) e índices analíticos
* **Análise Estatística & Visualização:** Matplotlib 3.11, Seaborn 0.13, Jupyter Notebook (`nbformat`, `nbconvert`)
* **Business Intelligence:** Power Query (Linguagem M) e DAX (Data Analysis Expressions) para Power BI Desktop

---

## 4. Estrutura do Repositório

```text
ases-e-atrito/
│
├── data/
│   ├── raw/                              # Dados brutos coletados com fontes rastreáveis
│   │   ├── ases.csv                      # 1.020 ases das 5 principais potências
│   │   ├── caças.csv                     # 83 variantes de caças com especificações técnicas
│   │   ├── batalhas_perdas.csv           # 30 registros comparativos de perdas vs reivindicações
│   │   ├── producao_e_atrito.csv         # 61 registros de produção nacional e operações USAAF
│   │   └── ArmyAirForcesStatisticalDigestWorldWarII.pdf  # PDF primário oficial (AAFSD 1945)
│   └── processed/                        # Dados limpos e modelagem dimensional
│       ├── dogfight.db                   # Banco de dados relacional SQLite completo
│       ├── dim_pais.csv                  # Dimensão Geopolítica e Alianças (Eixo vs Aliados)
│       ├── dim_data.csv                  # Dimensão Calendário e Fases da Guerra
│       ├── dim_batalha.csv               # Dimensão Batalhas e Teatros Operacionais
│       ├── dim_aeronave.csv              # Dimensão Aeronaves por Variante
│       ├── dim_piloto.csv                # Dimensão Biográfica de Ases
│       ├── fato_perdas.csv               # Fato Atrito: Perdas Reais vs Abates Reivindicados
│       ├── fato_producao.csv             # Fato Produção Fabril e Saídas de Combate (Sorties)
│       └── fato_vitorias.csv             # Fato Vitórias Aéreas dos Ases
│
├── src/
│   ├── coleta/                           # Scripts de extração e coleta de dados primários
│   │   ├── coleta_ases.py                # Coleta de ases via Wikipedia API
│   │   ├── coleta_cacas.py               # Compilação de especificações de 83 variantes
│   │   ├── coleta_batalhas.py            # Coleta de dados de grandes batalhas aéreas
│   │   └── coleta_producao_atrito.py     # Extração de PDFPlumber e produção histórica
│   ├── limpeza/                          # Pipeline de higienização, validação e modelagem
│   │   ├── limpeza_validacao.py          # Validação estrita via Pandera e padronização
│   │   └── modelagem_estrela.py          # Criação do banco dogfight.db e exportação dos CSVs
│   └── analise/                          # Análise estatística e exploratória
│       ├── gerar_analise.py              # Script motor das análises e exportação de gráficos
│       └── analise_exploratoria.ipynb    # Jupyter Notebook executado com gráficos e conclusões
│
├── sql/                                  # Consultas analíticas SQL (.sql) com CTEs e Window Functions
│   ├── 01_ranking_ases_pareto.sql        # Ranking de ases, curva de Lorenz e Pareto acumulado
│   ├── 02_razao_reivindicacoes_perdas.sql# Discrepância histórica de overclaiming por batalha
│   ├── 03_evolucao_perdas_temporal.sql   # Evolução temporal de perdas acumuladas por fase
│   ├── 04_comparacao_variantes_aeronaves.sql # Salto tecnológico entre variantes da mesma família
│   └── 05_correlacao_producao_perdas.sql # Relação entre produção fabril e intensidade operacional
│
├── powerquery/
│   └── consultas.md                      # Consultas em Linguagem M prontas para o Power Query
│
├── dax/
│   └── medidas.md                        # Medidas DAX documentadas (RANKX, Pareto, Time Intelligence, etc.)
│
├── docs/                                 # Documentação executiva, técnica e histórica
│   ├── dicionario_dados.md               # Dicionário de dados completo de todas as tabelas e colunas
│   ├── metodologia_e_limitacoes.md       # Metodologia de coleta, overclaiming e lacunas de dados
│   ├── guia_powerbi.md                   # Guia passo a passo para montagem manual das 6 páginas
│   ├── log_coleta.md                     # Registro de auditoria da etapa de coleta
│   ├── log_limpeza.md                    # Registro de auditoria da limpeza e validação Pandera
│   └── img/                              # Gráficos em alta resolução gerados pelas análises
│       ├── pareto_vitorias.png
│       ├── overclaim_batalhas.png
│       ├── evolucao_velocidade_cacas.png
│       └── producao_anual_paises.png
│
├── requirements.txt                      # Dependências do projeto
└── README.md                             # Este documento
```

---

## 5. Como Rodar o Pipeline do Zero

### 5.1 Pré-requisitos
* Python 3.11+ instalado.
* Conexão com a internet (para scraping de fontes públicas caso queira rodar a coleta novamente).

### 5.2 Passo a Passo de Execução

1. **Instalar Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar a Coleta de Dados Brutos (Etapa 1):**
   ```bash
   python src/coleta/coleta_ases.py
   python src/coleta/coleta_cacas.py
   python src/coleta/coleta_batalhas.py
   python src/coleta/coleta_producao_atrito.py
   ```
   *Gera os 4 arquivos em `/data/raw/` e baixa o PDF oficial de suporte.*

3. **Executar a Limpeza e Validação Pandera (Etapa 2):**
   ```bash
   python src/limpeza/limpeza_validacao.py
   ```
   *Higieniza os dados, valida contratos de esquema e gera `/docs/log_limpeza.md`.*

4. **Gerar o Esquema Estrela e Banco Relacional (Etapa 3):**
   ```bash
   python src/limpeza/modelagem_estrela.py
   ```
   *Cria o banco de dados `dogfight.db` (SQLite) e exporta as 8 tabelas dimensionais e fatos em `/data/processed/`.*

5. **Executar a Análise Estatística e Gerar o Notebook (Etapa 5):**
   ```bash
   python src/analise/gerar_analise.py
   jupyter nbconvert --to notebook --execute --inplace src/analise/analise_exploratoria.ipynb
   ```
   *Gera os gráficos em `/docs/img/` e pré-renderiza o notebook com todos os outputs.*

---

## 6. Principais Achados Históricos e Estatísticos

1. **Curva de Concentração de Vitórias (Pareto / Gini = 0,61):**
   * Os **top 20% dos ases concentram 60,8% de todos os abates confirmados**, confirmando a regra de Pareto no combate aéreo.
   * A distribuição alemã é hipertrofiada porque a Luftwaffe não praticava rotação operacional: ases combatiam até morrer ou serem abatidos. Os Aliados priorizaram a retenção de conhecimento, retirando os ases após um ciclo de missões (*tour of duty*) para treinarem novos cadetes, resultando em forças aéreas com letalidade média e sobrevivência muito superiores.
2. **O Fenômeno Universal do *Overclaiming*:**
   * A discrepância entre reivindicações de pilotos e perdas reais do adversário variou historicamente de **2,7x** (na Batalha da Inglaterra) até **10,6x** (na missão Schweinfurt-Regensburg de 1943, onde a 8th Air Force reivindicou 288 caças e a Luftwaffe perdeu apenas 27).
   * O overclaiming decorre da natureza do combate tridimensional em altíssima velocidade (> 600 km/h) e de disparos múltiplos simultâneos contra a mesma aeronave, e não de falsificação intencional.
3. **Evolução Técnica dos Caças (+27,8 km/h por ano):**
   * A velocidade média dos caças de combate saltou de cerca de 500 km/h em 1939 para quase 800 km/h em 1945 (e 900 km/h no jato Me 262), demonstrando uma das maiores corridas armamentistas de inovação técnica da história.
4. **Supremacia Industrial Decisiva:**
   * Em 1944, os Estados Unidos produziram **96.318 aeronaves militares em um único ano** — mais do que toda a produção alemã de 1941 a 1943 somada. A capacidade fabril e de formação de pessoal, e não as proezas individuais de ases, determinou o resultado da guerra aérea.

---

## 7. Checklist Final de Conclusão e Pontos de Atenção

| Item Requisitado | Status | Detalhes e Observações |
| :--- | :---: | :--- |
| **1.1 `ases.csv`** | **Concluído** | 1.020 ases coletados (Alemanha, EUA, Reino Unido, URSS, Japão) com fontes rastreáveis. |
| **1.2 `caças.csv`** | **Concluído** | 83 variantes modeladas com velocidade, teto, alcance, armamento e unidades produzidas. |
| **1.3 `batalhas_perdas.csv`** | **Concluído** | 30 registros comparativos de perdas reais vs. reivindicações (Inglaterra, Midway, Filipinas, Bombardeio Estratégico). |
| **1.4 `producao_e_atrito.csv`** | **Concluído** | 61 registros integrando a produção das 5 potências (1939-1945) e operações da USAAF via PDFPlumber. |
| **Etapa 2 — Limpeza & Pandera** | **Concluído** | Validação estrita via Pandera em todos os 4 datasets; log gerado em `/docs/log_limpeza.md`. |
| **Etapa 3 — Esquema Estrela & DB** | **Concluído** | Banco `dogfight.db` criado em SQLite com 5 dimensões e 3 fatos; todos os 8 CSVs exportados em `/data/processed`. |
| **Etapa 4 — Consultas SQL (.sql)** | **Concluído** | 5 consultas complexas em `/sql` com CTEs e Window Functions (testadas com 100% de sucesso). |
| **Etapa 5 — Análise Estatística** | **Concluído** | Notebook executado em `/src/analise/` e 4 gráficos exportados em `/docs/img/`. |
| **6.1 Medidas DAX** | **Concluído** | Documento `/dax/medidas.md` com RANKX, Pareto, DIVIDE, Time Intelligence e Field Parameter. |
| **6.2 Consultas Power Query (M)** | **Concluído** | Documento `/powerquery/consultas.md` com consultas M prontas para colar no Editor Avançado. |
| **6.3 Dicionário de Dados** | **Concluído** | Documento `/docs/dicionario_dados.md` detalhando todas as 8 tabelas, colunas, tipos e descrições. |
| **6.4 Metodologia e Limitações** | **Concluído** | Documento `/docs/metodologia_e_limitacoes.md` detalhando overclaiming e assimetrias documentais. |
| **6.5 Guia do Power BI** | **Concluído** | Documento `/docs/guia_powerbi.md` com mapa de relações (cardinalidade 1:*) e guia visual de 6 páginas. |
| **6.6 README.md na Raiz** | **Concluído** | Documento completo em português na raiz do projeto. |

### O que ficou incompleto ou simplificado por falta de dados confiáveis (Onde Focar no Power BI):
1. **Dados Japoneses Pós-1943:** Como o comando militar japonês proibiu registros individuais de abates após o início de 1943 e queimou arquivos em agosto de 1945, os dados de ases japoneses devem ser apresentados no dashboard com a ressalva metodológica descrita em `/docs/metodologia_e_limitacoes.md`.
2. **Separação de Abates Solo vs. Compartilhados Soviéticos:** A VVS registrava abates individuais e em grupo. Os totais na base refletem a soma consolidada aceita pela historiografia russa moderna.
3. **Dados Mensais de Sorties da Luftwaffe e Japão:** Não existem dados mensais consolidados confiáveis de saídas operacionais (*sorties*) para a Luftwaffe ou aviação japonesa que cubram todos os anos no mesmo nível de padronização do *AAF Statistical Digest*. Por essa razão, as análises de saídas de combate e taxas de perda por surtida focam na USAAF e na comparação direta entre perdas em grandes batalhas.
