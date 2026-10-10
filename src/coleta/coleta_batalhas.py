import os
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def get_battles_loss_claims_data():
    battles = [
        # =====================================================================
        # 1. BATALHA DA INGLATERRA (1940)
        # =====================================================================
        {
            "batalha": "Batalha da Inglaterra - Kanalkampf",
            "data": "1940-08-11",
            "pais": "Reino Unido",
            "aeronaves_perdidas": 115,
            "aeronaves_abatidas_reivindicadas": 227,
            "fonte": "Wood & Dempster 'The Narrow Margin'; RAF Fighter Command War Diary AIR 16"
        },
        {
            "batalha": "Batalha da Inglaterra - Kanalkampf",
            "data": "1940-08-11",
            "pais": "Alemanha",
            "aeronaves_perdidas": 227,
            "aeronaves_abatidas_reivindicadas": 180,
            "fonte": "Generalquartiermeister der Luftwaffe Loss Reports; Stephen Bungay 'The Most Dangerous Enemy'"
        },
        {
            "batalha": "Batalha da Inglaterra - Adlerangriff",
            "data": "1940-08-17",
            "pais": "Reino Unido",
            "aeronaves_perdidas": 95,
            "aeronaves_abatidas_reivindicadas": 255,
            "fonte": "Francis K. Mason 'Battle Over Britain'; Wood & Dempster 'The Narrow Margin'"
        },
        {
            "batalha": "Batalha da Inglaterra - Adlerangriff",
            "data": "1940-08-17",
            "pais": "Alemanha",
            "aeronaves_perdidas": 180,
            "aeronaves_abatidas_reivindicadas": 160,
            "fonte": "Luftwaffe Quartermaster General Returns; Bungay 'The Most Dangerous Enemy'"
        },
        {
            "batalha": "Batalha da Inglaterra - The Hardest Day",
            "data": "1940-08-18",
            "pais": "Reino Unido",
            "aeronaves_perdidas": 68,
            "aeronaves_abatidas_reivindicadas": 144,
            "fonte": "Alfred Price 'The Hardest Day: 18 August 1940'; UK National Archives AIR 16/AIR 22"
        },
        {
            "batalha": "Batalha da Inglaterra - The Hardest Day",
            "data": "1940-08-18",
            "pais": "Alemanha",
            "aeronaves_perdidas": 69,
            "aeronaves_abatidas_reivindicadas": 147,
            "fonte": "Alfred Price 'The Hardest Day: 18 August 1940'; Bundesarchiv-Militärarchiv Freiburg"
        },
        {
            "batalha": "Batalha da Inglaterra - Ataque a Aeródromos",
            "data": "1940-09-06",
            "pais": "Reino Unido",
            "aeronaves_perdidas": 295,
            "aeronaves_abatidas_reivindicadas": 560,
            "fonte": "Francis K. Mason 'Battle Over Britain'; Wood & Dempster 'The Narrow Margin'"
        },
        {
            "batalha": "Batalha da Inglaterra - Ataque a Aeródromos",
            "data": "1940-09-06",
            "pais": "Alemanha",
            "aeronaves_perdidas": 378,
            "aeronaves_abatidas_reivindicadas": 410,
            "fonte": "Luftwaffe Quartermaster General Returns; Stephen Bungay 'The Most Dangerous Enemy'"
        },
        {
            "batalha": "Batalha da Inglaterra - Transição Blitz Londres",
            "data": "1940-09-14",
            "pais": "Reino Unido",
            "aeronaves_perdidas": 110,
            "aeronaves_abatidas_reivindicadas": 230,
            "fonte": "Francis K. Mason 'Battle Over Britain'; RAF Fighter Command Summary"
        },
        {
            "batalha": "Batalha da Inglaterra - Transição Blitz Londres",
            "data": "1940-09-14",
            "pais": "Alemanha",
            "aeronaves_perdidas": 160,
            "aeronaves_abatidas_reivindicadas": 170,
            "fonte": "Generalquartiermeister der Luftwaffe; Bungay 'The Most Dangerous Enemy'"
        },
        {
            "batalha": "Batalha da Inglaterra - Battle of Britain Day",
            "data": "1940-09-15",
            "pais": "Reino Unido",
            "aeronaves_perdidas": 29,
            "aeronaves_abatidas_reivindicadas": 185,
            "fonte": "RAF Fighter Command Operations Record Book; UK National Archives AIR 16/949"
        },
        {
            "batalha": "Batalha da Inglaterra - Battle of Britain Day",
            "data": "1940-09-15",
            "pais": "Alemanha",
            "aeronaves_perdidas": 56,
            "aeronaves_abatidas_reivindicadas": 79,
            "fonte": "Luftwaffe Quartermaster General Returns BA-MA RL 2 III; Alfred Price 'Battle of Britain Day'"
        },
        {
            "batalha": "Batalha da Inglaterra - Fase Final Outubro",
            "data": "1940-10-31",
            "pais": "Reino Unido",
            "aeronaves_perdidas": 213,
            "aeronaves_abatidas_reivindicadas": 420,
            "fonte": "Francis K. Mason 'Battle Over Britain'; Wood & Dempster 'The Narrow Margin'"
        },
        {
            "batalha": "Batalha da Inglaterra - Fase Final Outubro",
            "data": "1940-10-31",
            "pais": "Alemanha",
            "aeronaves_perdidas": 325,
            "aeronaves_abatidas_reivindicadas": 310,
            "fonte": "Generalquartiermeister der Luftwaffe; Stephen Bungay 'The Most Dangerous Enemy'"
        },

        # =====================================================================
        # 2. BATALHA DE MIDWAY (1942)
        # =====================================================================
        {
            "batalha": "Batalha de Midway",
            "data": "1942-06-04",
            "pais": "Estados Unidos",
            "aeronaves_perdidas": 147,
            "aeronaves_abatidas_reivindicadas": 280,
            "fonte": "Jonathan Parshall & Anthony Tully 'Shattered Sword: The Untold Story of the Battle of Midway'; ONI Combat Narratives"
        },
        {
            "batalha": "Batalha de Midway",
            "data": "1942-06-04",
            "pais": "Japão",
            "aeronaves_perdidas": 288,
            "aeronaves_abatidas_reivindicadas": 160,
            "fonte": "Jonathan Parshall & Anthony Tully 'Shattered Sword'; Senshi Sōsho Vol. 43"
        },

        # =====================================================================
        # 3. BATALHA DO MAR DAS FILIPINAS - MARIANAS TURKEY SHOOT (1944)
        # =====================================================================
        {
            "batalha": "Batalha do Mar das Filipinas (Dia 1 - Turkey Shoot)",
            "data": "1944-06-19",
            "pais": "Estados Unidos",
            "aeronaves_perdidas": 23,
            "aeronaves_abatidas_reivindicadas": 385,
            "fonte": "Samuel Eliot Morison 'History of United States Naval Operations in WWII', Vol 8; Barrett Tillman 'Clash of the Carriers'"
        },
        {
            "batalha": "Batalha do Mar das Filipinas (Dia 1 - Turkey Shoot)",
            "data": "1944-06-19",
            "pais": "Japão",
            "aeronaves_perdidas": 396,
            "aeronaves_abatidas_reivindicadas": 110,
            "fonte": "Barrett Tillman 'Clash of the Carriers'; Senshi Sōsho Vol. 12; Morison Vol 8"
        },
        {
            "batalha": "Batalha do Mar das Filipinas (Dia 2 - Ataque Noturno TF58)",
            "data": "1944-06-20",
            "pais": "Estados Unidos",
            "aeronaves_perdidas": 100,
            "aeronaves_abatidas_reivindicadas": 65,
            "fonte": "Samuel Eliot Morison Vol 8; Barrett Tillman 'Clash of the Carriers' (80 aviões perdidos por falta de combustível)"
        },
        {
            "batalha": "Batalha do Mar das Filipinas (Dia 2 - Ataque Noturno TF58)",
            "data": "1944-06-20",
            "pais": "Japão",
            "aeronaves_perdidas": 65,
            "aeronaves_abatidas_reivindicadas": 35,
            "fonte": "Senshi Sōsho Vol. 12; Barrett Tillman 'Clash of the Carriers'"
        },

        # =====================================================================
        # 4. CAMPANHA DE BOMBARDEIO ESTRATÉGICO SOBRE A ALEMANHA (1943-1945)
        # =====================================================================
        {
            "batalha": "Bombardeio Estratégico - Schweinfurt-Regensburg",
            "data": "1943-08-17",
            "pais": "Estados Unidos",
            "aeronaves_perdidas": 60,
            "aeronaves_abatidas_reivindicadas": 288,
            "fonte": "Craven & Cate 'The Army Air Forces in WWII' Vol 2; Roger Freeman 'The Mighty Eighth'"
        },
        {
            "batalha": "Bombardeio Estratégico - Schweinfurt-Regensburg",
            "data": "1943-08-17",
            "pais": "Alemanha",
            "aeronaves_perdidas": 27,
            "aeronaves_abatidas_reivindicadas": 78,
            "fonte": "Donald Caldwell & Richard Muller 'The Luftwaffe Over Germany: Defense of the Reich'"
        },
        {
            "batalha": "Bombardeio Estratégico - Segundo Schweinfurt (Black Thursday)",
            "data": "1943-10-14",
            "pais": "Estados Unidos",
            "aeronaves_perdidas": 77,
            "aeronaves_abatidas_reivindicadas": 186,
            "fonte": "Martin Middlebrook 'The Schweinfurt-Regensburg Mission'; Roger Freeman 'The Mighty Eighth' (60 em combate + 17 sucata)"
        },
        {
            "batalha": "Bombardeio Estratégico - Segundo Schweinfurt (Black Thursday)",
            "data": "1943-10-14",
            "pais": "Alemanha",
            "aeronaves_perdidas": 38,
            "aeronaves_abatidas_reivindicadas": 85,
            "fonte": "Caldwell & Muller 'The Luftwaffe Over Germany: Defense of the Reich'"
        },
        {
            "batalha": "Bombardeio Estratégico - Big Week (Op. Argument)",
            "data": "1944-02-25",
            "pais": "Estados Unidos",
            "aeronaves_perdidas": 254,
            "aeronaves_abatidas_reivindicadas": 510,
            "fonte": "Craven & Cate 'The Army Air Forces in WWII' Vol 3; AAF Statistical Digest Table 158/166"
        },
        {
            "batalha": "Bombardeio Estratégico - Big Week (Op. Argument)",
            "data": "1944-02-25",
            "pais": "Alemanha",
            "aeronaves_perdidas": 262,
            "aeronaves_abatidas_reivindicadas": 380,
            "fonte": "USSBS Report: 'The German Aircraft Industry'; Caldwell & Muller 'The Luftwaffe Over Germany'"
        },
        {
            "batalha": "Bombardeio Estratégico - Grande Ataque a Berlim",
            "data": "1944-03-06",
            "pais": "Estados Unidos",
            "aeronaves_perdidas": 80,
            "aeronaves_abatidas_reivindicadas": 179,
            "fonte": "Roger Freeman 'The Mighty Eighth'; Eighth Air Force Mission 250 Report (69 bombardeiros + 11 caças perdidos)"
        },
        {
            "batalha": "Bombardeio Estratégico - Grande Ataque a Berlim",
            "data": "1944-03-06",
            "pais": "Alemanha",
            "aeronaves_perdidas": 66,
            "aeronaves_abatidas_reivindicadas": 95,
            "fonte": "Caldwell & Muller 'The Luftwaffe Over Germany: Defense of the Reich'"
        },
        {
            "batalha": "Bombardeio Estratégico - Operação Bodenplatte",
            "data": "1945-01-01",
            "pais": "Alemanha",
            "aeronaves_perdidas": 304,
            "aeronaves_abatidas_reivindicadas": 450,
            "fonte": "John Manrho & Ron Pütz 'Bodenplatte: The Luftwaffe's Last Hope'; BA-MA RL 2 III"
        },
        {
            "batalha": "Bombardeio Estratégico - Operação Bodenplatte",
            "data": "1945-01-01",
            "pais": "Aliados (EUA / Reino Unido)",
            "aeronaves_perdidas": 144,
            "aeronaves_abatidas_reivindicadas": 250,
            "fonte": "Norman Franks 'The Battle of the Airfields: 1 January 1945'; UK National Archives AIR 20"
        }
    ]
    return battles

def main():
    raw_dir = os.path.join(BASE_DIR, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    df = pd.DataFrame(get_battles_loss_claims_data())
    df.to_csv(os.path.join(raw_dir, "batalhas_perdas.csv"), index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()
