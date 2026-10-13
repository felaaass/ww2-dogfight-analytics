# Metodologia e Limitações Históricas — Projeto Ases e Atrito

> **Regra Fundamental de Governança:**  
> Nenhum número foi inventado, estimado ou inferido por intuição. Onde arquivos primários ou estudos acadêmicos consolidados apresentavam lacunas, os campos foram estritamente preservados como `NULL` (nulos). Cada registro histórico carrega sua respectiva citação na coluna `fonte`.

---

## 1. Metodologia de Coleta e Pipeline

O pipeline foi estruturado em quatro camadas progressivas:
1. **Coleta Bruta (`/data/raw`):** Scripts Python (`coleta_ases.py`, `coleta_cacas.py`, `coleta_batalhas.py`, `coleta_producao_atrito.py`) extraíram dados de APIs públicas da Wikipedia, relatórios técnicos arquivados e da publicação oficial do Departamento de Guerra dos EUA (*AAF Statistical Digest*).
2. **Limpeza e Validação (`/src/limpeza`):** Executada com Pandas e Pandera, aplicando validação estrita de tipos, faixas de plausibilidade e padronização geopolítica.
3. **Modelagem Dimensional (`/src/limpeza/modelagem_estrela.py`):** Estruturação em Esquema Estrela (*Star Schema*), persistida em SQLite local (`dogfight.db`) e exportada como CSVs limpos em `/data/processed`.
4. **Camada Analítica (`/sql`, `/src/analise`, `/powerbi`, `/docs`):** Consultas SQL analíticas com Window Functions, notebook exploratório e catálogo técnico de modelagem/DAX para o dashboard no Power BI.

---

## 2. Reivindicações de Combate vs. Realidade Documentada (Overclaiming)

Um dos achados mais marcantes deste projeto é a constatação empírica e quantitativa do **overclaiming sistemático**.

### 2.1 Por que Pilotos e Artilheiros Superestimavam Abates?
1. **Velocidade e Estresse Tridimensional:** Caças da Segunda Guerra combatiam a velocidades entre 500 e 700 km/h. O engajamento com fogo durava tipicamente frações de segundo.
2. **Fogo Concentrado Múltiplo:** Em formações de bombardeiros pesados (ex.: B-17 Flying Fortress), até uma dúzia de metralhadores de calibres .50 disparavam simultaneamente contra o mesmo caça interceptador alemão. Quando o caça mergulhava expelindo fumaça (muitas vezes vapor de radiador ou injeção de potência máxima), múltiplos atiradores registravam abates independentes para o mesmo avião.
3. **Mergulho Evasivo vs. Destruição:** Um piloto inimigo que fizesse um mergulho brusco e vertical para escapar era frequentemente considerado "abatido fora de controle" pelo atacante, que precisava retornar a atenção imediata para não ser atacado pelas costas.
4. **Propaganda de Guerra e Moral Interno:** Em momentos críticos de defesa nacional (como na Batalha da Inglaterra em 1940), os comandos operacionais aceitavam as estimativas dos esquadrões para sustentar o ânimo público e militar, realizando auditorias rigorosas somente anos após o término do conflito.

### 2.2 Casos Emblemáticos no Dataset:
* **Missão Schweinfurt-Regensburg (17 Ago 1943):**
  * *Reivindicação da 8th Air Force:* **288 caças alemães abatidos**.
  * *Perdas Reais da Luftwaffe:* **27 caças destruídos**.
  * *Fator de Discrepância:* **10,6x**.
* **Battle of Britain Day (15 Set 1940):**
  * *Reivindicação da RAF:* **185 vitórias**.
  * *Perdas Reais da Luftwaffe:* **56 aeronaves destruídas**.
  * *Fator de Discrepância:* **3,3x**.
  * *Reivindicação da Luftwaffe:* **~79-80 caças britânicos**.
  * *Perdas Reais da RAF:* **29 caças perdidos**.
  * *Fator de Discrepância:* **2,7x**.

---

## 3. Cobertura Assimétrica por País e Limitações dos Dados

### 3.1 Alemanha (Luftwaffe)
* **A Falácia do "Super-Homem":** Os números extravagantes dos ases alemães (Hartmann com 352, Barkhorn com 301, Rall com 275) não decorrem apenas de superioridade técnica, mas da **política de não-rotação**. Pilotos alemães combatiam continuamente no front leste contra pilotos soviéticos pouco treinados em 1941-1942, acumulando centenas de surtidas até o esgotamento, ferimento ou morte.
* **Perda de Veteranos:** Em 1944, a Luftwaffe havia perdido a totalidade de seus instrutores veteranos. Jovens pilotos com menos de 50 horas de instrução eram enviados para combater veteranos aliados com mais de 300 horas, acelerando o colapso aéreo do Eixo.

### 3.2 Estados Unidos (USAAF / US Navy / USMC)
* **Doutrina da Rotação Operacional:** Os EUA estabeleceram cotas fixas de missões (*tour of duty*). Ases com 20 a 40 vitórias eram retirados da frente de batalha e enviados como instrutores para escolas de voo no Arizona, Flórida e Texas. Essa decisão impediu que pilotos americanos alcançassem 100 vitórias individuais, mas produziu a força aérea mais homogênea e profissional da guerra.
* **Fonte Primária AAF Statistical Digest:** O documento de 1945 da Divisão de Controle Estatístico da USAAF é uma das fontes mais precisas da história militar, mas foca exclusivamente nas operações do Exército (USAAF). Operações navais e do Corpo de Fuzileiros Navais (USMC) possuem arquivos paralelos administrados pelo Departamento da Marinha (*Naval History and Heritage Command*).

### 3.3 União Soviética (VVS)
* **Dificuldade Documental e Lend-Lease:** Os arquivos do Ministério da Defesa da Federação Russa (TsAMO) trazem distinção estrita entre vitórias individuais (*lichno*) e vitórias compartilhadas em grupo (*v gruppe*). As listagens ocidentais frequentemente somavam as duas modalidades.
* Os caças P-39 Airacobra fornecidos pelos EUA via Lei de Empréstimo e Arrendamento (*Lend-Lease*) foram amplamente pilotados pelos principais ases soviéticos (Pokryshkin e Rechkalov), evidenciando a interdependência aliada.

### 3.4 Japão (Marinha e Exército Imperial)
* **Apagão Documental Pós-1943:** A partir do início de 1943, o Japão proibiu oficialmente os registros individuais de vitórias para coibir o individualismo em favor do espírito de sacrifício coletivo.
* **Destruição de Arquivos:** Com o afundamento dos 4 porta-aviões em Midway e as perdas no Mar das Filipinas, os diários de bordo de esquadrões inteiros foram perdidos no fundo do mar. Em agosto de 1945, ordens expressas em Tóquio determinaram a queima sistemática de documentos confidenciais antes da ocupação americana. Portanto, números de ases japoneses (como Nishizawa e Iwamoto) representam consolidações reconstruídas por historiadores (Henry Sakaida, Hata, Izawa).

---

## 4. Limitações Técnicas e de Engenharia de Dados

1. **Extração via PDFPlumber do Documento de 1945:**
   * O *Army Air Forces Statistical Digest* de 1945 foi digitalizado a partir de impressões originais do Departamento de Guerra, apresentando pequenas falhas visuais em linhas finas e caracteres ilegíveis de tabelas mensais de sub-teatros.
   * *Decisão de Engenharia:* Para não comprometer a precisão do pipeline, foram extraídos os consolidados anuais oficiais por teatro (Tabelas 118, 158 e 166), validados contra os totais gerais do próprio sumário executivo.
2. **Modelagem de Aeronaves por Variante:**
   * Foi necessário manter as variantes como entidades atômicas (ex.: Bf 109E-3 com canhões de tambor MG FF vs Bf 109G-6 com canhão MK 108 de 30mm e motor com injeção de metanol-água MW 50). A generalização por "modelo genérico" destruiria as métricas técnicas de evolução de velocidade e altitude.
