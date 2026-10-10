# Log de Coleta de Dados — Projeto Ases e Atrito

Data de Coleta: Outubro de 2026  
Ambiente: Python 3.11 / Requests / BeautifulSoup / PDFPlumber / Pandas  

---

## 1. Visão Geral da Coleta

O objetivo desta etapa foi construir quatro conjuntos de dados históricos brutos em `/data/raw`, seguindo estritamente a **Regra de Ouro**: nenhum número foi inventado, estimado ou arredondado de memória. Todos os registros mantêm uma coluna `fonte` explícita e rastreável. Quando um dado não pôde ser determinado com precisão documental primária, o campo foi preservado como `NULL`.

---

## 2. Detalhamento por Tabela Bruta

### 2.1 `ases.csv` (`/data/raw/ases.csv`)
* **Total de Registros Coletados:** 1.020 ases da aviação.
* **Cobertura por País:**
  * **Japão:** 289 pilotos (Marinha Imperial - IJN e Exército Imperial - IJA)
  * **Reino Unido e Commonwealth:** 213 pilotos (RAF, RCAF, RAAF, SAAF, RNZAF)
  * **Estados Unidos:** 207 pilotos (USAAF, US Navy, USMC)
  * **União Soviética:** 203 pilotos (VVS)
  * **Alemanha:** 108 pilotos (todos pertencentes ao seleto grupo com 100+ vitórias aéreas confirmadas)
* **Fontes Utilizadas:**
  * English Wikipedia API (`action=parse`):
    * `List of World War II aces credited with 100 or more victories`
    * `List of World War II aces from the United States`
    * `List of World War II aces from the Soviet Union`
    * `List of World War II aces from the United Kingdom`
    * `List of World War II aces from Japan`
* **Inconsistências e Limitações Históricas:**
  1. *Critérios de Homologação da Luftwaffe vs. Aliados:* A Luftwaffe contabilizava abates individuais (*Abschuss*) com testemunhas ou confirmação de radar/destroços, porém os pilotos alemães voavam sem rotação operacional ("até a vitória ou a morte"), o que gerou totais de 100 a 352 vitórias (Erich Hartmann: 352; Gerhard Barkhorn: 301). Em contraste, pilotos dos EUA cumpriam um ciclo fixo de missões (*tour of duty*, tipicamente 25 a 50 missões) e retornavam para treinar novos recrutas, resultando em totais menores de ases individuais (Richard Bong: 40; Thomas McGuire: 38), mas garantindo uma força aérea com pilotos instrutores de altíssimo nível.
  2. *Dados Japoneses:* A partir do primeiro semestre de 1943, o Alto Comando Imperial Japonês proibiu oficialmente o registro e divulgação de recordes individuais de abates para valorizar o esforço coletivo e o sacrifício da unidade. Além disso, muitos arquivos navais foram destruídos durante o afundamento dos porta-aviões e queima sistemática de documentos em Tóquio em agosto de 1945. Como consequência, as listas de ases japoneses possuem variações entre historiadores ocidentais (ex.: Henry Sakaida, Barrett Tillman) e fontes japonesas pós-guerra (*Senshi Sōsho*).
  3. *Dados Soviéticos:* A Força Aérea Soviética (VVS) diferenciava estritamente abates individuais (*lichno*) de abates compartilhados (*v gruppe*). Para assegurar rigor, foram contabilizados os totais documentados, observando que o Lend-Lease americano forneceu o caça P-39 Airacobra para os maiores ases soviéticos (Alexander Pokryshkin e Grigori Rechkalov).

---

### 2.2 `caças.csv` (`/data/raw/caças.csv`)
* **Total de Registros Coletados:** 83 variantes de caças modeladas individualmente.
* **Cobertura:**
  * **Estados Unidos:** 26 variantes (P-51A/B/D/H, P-47B/D/M/N, P-38F/G/J/L, P-40B/E/N, F4F-3/4, FM-2, F6F-3/5, F4U-1/1D/4, P-39D/Q)
  * **Alemanha:** 18 variantes (Bf 109B/E/F/G/K, Fw 190A/D, Ta 152H, Me 262A, Me 163B, Bf 110C/G)
  * **Reino Unido:** 14 variantes (Spitfire Mk I/II/V/IX/XIV/21, Hurricane Mk I/IIb/IIc/IV, Typhoon Ib, Tempest V, Mosquito NF.II/FB.VI)
  * **União Soviética:** 13 variantes (Yak-1/1B/7B/9/9T/9D/3, LaGG-3, La-5/5FN, La-7, MiG-3, I-16)
  * **Japão:** 10 variantes (A6M2/3/5, Ki-43-I/II/III, Ki-61, Ki-84, N1K2-J, J2M3)
  * **Itália:** 2 variantes (Macchi C.202 Folgore, Macchi C.205 Veltro)
* **Fontes Utilizadas:**
  * Manuais de voo originais e relatórios de testes de voo de aceitação (USAAF Wright Field, RAF Boscombe Down, Rechlin Erprobungsstelle).
  * William Green, *Warplanes of the Third Reich* e *Famous Fighters of the Second World War*.
  * Francis K. Mason, *The British Fighter since 1912*.
  * René J. Francillon, *Japanese Aircraft of the Pacific War*.
  * Yefim Gordon, *Soviet Combat Aircraft of the Second World War*.
  * Páginas especializadas da Wikipedia com tabelas de especificações por variante.
* **Decisões Metodológicas:**
  * Cada variante foi registrada separadamente, pois modificações de motor, hélice e armamento alteravam radicalmente velocidade máxima, teto e alcance (ex.: Spitfire Mk I com 582 km/h vs Spitfire Mk XIV com 721 km/h; Bf 109E-3 com motor DB 601A vs Bf 109K-4 com motor DB 605D atingindo 710 km/h).

---

### 2.3 `batalhas_perdas.csv` (`/data/raw/batalhas_perdas.csv`)
* **Total de Registros Coletados:** 30 registros comparativos de perdas reais vs. abates reivindicados.
* **Batalhas e Campanhas Cobertas:**
  1. *Batalha da Inglaterra (1940):*
     * Kanalkampf (10 Jul - 11 Ago 1940)
     * Adlerangriff (12 Ago - 17 Ago 1940)
     * The Hardest Day (18 Ago 1940)
     * Ofensiva contra Aeródromos do Fighter Command (19 Ago - 06 Set 1940)
     * Transição para o Blitz de Londres (07 Set - 14 Set 1940)
     * Battle of Britain Day (15 Set 1940)
     * Fase Final e Retirada da Luftwaffe (Outubro 1940)
  2. *Batalha de Midway (04-07 Junho 1942)*
  3. *Batalha do Mar das Filipinas / "Marianas Turkey Shoot" (19-20 Junho 1944)*
  4. *Campanha de Bombardeio Estratégico sobre a Alemanha (1943-1945):*
     * Missão Schweinfurt-Regensburg (17 Ago 1943)
     * Segunda Missão a Schweinfurt / Black Thursday (14 Out 1943)
     * Big Week / Operação Argument (20-25 Fev 1944)
     * Primeiro Grande Ataque Diurno a Berlim (06 Mar 1944)
     * Operação Bodenplatte (01 Jan 1945)
* **Fontes Utilizadas:**
  * Registros do UK National Archives (AIR 16 e AIR 22 - RAF Fighter Command).
  * Arquivos militares alemães Bundesarchiv-Militärarchiv Freiburg (RL 2 III - Relatórios do Generalquartiermeister da Luftwaffe).
  * Jonathan Parshall & Anthony Tully, *Shattered Sword: The Untold Story of the Battle of Midway*.
  * Samuel Eliot Morison, *History of United States Naval Operations in World War II*, Vol. 8.
  * Craven & Cate, *The Army Air Forces in World War II*, Volumes 2 e 3.
  * Donald Caldwell & Richard Muller, *The Luftwaffe Over Germany: Defense of the Reich*.
  * Alfred Price, *The Hardest Day* e *Battle of Britain Day*.
* **Achado Histórico Central (Overclaiming Sistemático):**
  * Em combate aéreo de alta velocidade sob estresse extremo, pilotos de ambos os lados e artilheiros de bombardeiros frequentemente atiravam na mesma aeronave inimiga ou viam fumaça de motor (ou mergulho evasivo) e acreditavam ter destruído o avião.
  * Casos documentados extremos:
    * *Battle of Britain Day (15 Set 1940):* RAF reivindicou 185 vitórias; perdas reais da Luftwaffe foram 56 aeronaves (fator de sobre-reivindicação de 3,3x). A Luftwaffe reivindicou ~80 caças; perdas reais do RAF Fighter Command foram 29 caças (fator de 2,7x).
    * *Schweinfurt-Regensburg (17 Ago 1943):* Artilheiros de B-17 da 8th Air Force reivindicaram 288 caças alemães abatidos; arquivos da Luftwaffe mostram apenas 27 caças destruídos (sobre-reivindicação de 10,6x!).

---

### 2.4 `producao_e_atrito.csv` (`/data/raw/producao_e_atrito.csv`)
* **Total de Registros Coletados:** 61 registros históricos oficiais.
* **Conteúdo e Estrutura:**
  * **USAAF Sorties, Perdas em Combate e Abates por Teatro (1942-1945):** 26 registros abrangendo Europa (ETO), Mediterrâneo (MTO), Sudoeste do Pacífico (FEAF), Pacífico Central (POA), China-Birmânia-Índia (CBI), Alasca e 20th Air Force (B-29s).
  * **Produção Militar Nacional Anual (1939-1945):** 35 registros abrangendo Estados Unidos, Alemanha, Reino Unido, União Soviética e Japão.
* **Fontes Utilizadas:**
  * *Army Air Forces Statistical Digest: World War II* (Office of Statistical Control, Headquarters AAF, Washington D.C., Dezembro 1945), Tabelas 118, 158 e 166. Extraído do PDF arquivado via `pdfplumber`.
  * United States Strategic Bombing Survey (USSBS): *The German Aircraft Industry* (1945) e *The Japanese Aircraft Industry* (Report No. 15, 1947).
  * US War Production Board: *Summary of Military Aircraft Deliveries* (1945).
  * UK Ministry of Aircraft Production (MAP): *Statistical Digest of the War*.
  * Soviet State Planning Committee (Gosplan) / V.B. Shavrov: *História da Construção Aeronáutica na URSS*.
* **Limitações da Extração via PDFPlumber:**
  * As páginas digitalizadas do *Statistical Digest* original de 1945 contêm pequenas falhas de tipografia/OCR nas linhas mensais finas (marcas d'água, traços apagados e notas de rodapé com letras minúsculas).
  * Para manter a integridade estrita e não introduzir estimativas artificiais, foram extraídos e auditados os consolidados anuais oficiais de cada teatro de operações e os números consolidados de aceitação de fábrica.
