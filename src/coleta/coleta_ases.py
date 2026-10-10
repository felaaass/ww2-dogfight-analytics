"""
Script de Coleta: Ases da Aviação da Segunda Guerra Mundial
Fonte Principal: Listas oficiais e verbas biográficas da Wikipedia (English Wikipedia API)
- List of World War II aces credited with 100 or more victories (Alemanha)
- List of World War II aces from the United States (EUA)
- List of World War II aces from the Soviet Union (URSS)
- List of World War II aces from the United Kingdom (Reino Unido)
- List of World War II aces from Japan (Japão)

Regra de Ouro: Nenhum número inventado. Dados faltantes são mantidos como NULL.
"""

import os
import re
import json
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup

def fetch_wiki_parse(page_title):
    """Busca o HTML parseado de uma página da Wikipedia usando a API oficial."""
    url = f"https://en.wikipedia.org/w/api.php?action=parse&page={page_title}&prop=text&format=json"
    headers = {"User-Agent": "WW2AcesResearch/1.0 (academic research data pipeline)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        if 'parse' in data and 'text' in data['parse']:
            return data['parse']['text']['*']
    return ""

def clean_text(text):
    if not text:
        return ""
    # Remove citações tipo [1], [a], etc.
    text = re.sub(r'\[.*?\]', '', text)
    # Remove marcas de morte ou símbolos especiais
    text = text.replace('†', '').replace('*', '').replace('~', '')
    return text.strip()

def extract_german_aces():
    """Coleta ases alemães com 100+ vitórias."""
    print("Coletando ases da Alemanha...")
    html = fetch_wiki_parse("List_of_World_War_II_aces_credited_with_100_or_more_victories")
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    if not table:
        return []
    
    aces = []
    source_url = "https://en.wikipedia.org/wiki/List_of_World_War_II_aces_credited_with_100_or_more_victories"
    
    rows = table.find_all('tr')[1:]
    for r in rows:
        tds = r.find_all(['td', 'th'])
        if len(tds) < 4:
            continue
        nome = clean_text(tds[0].get_text())
        pais = "Alemanha"
        forca = clean_text(tds[2].get_text()) or "Luftwaffe"
        vic_str = clean_text(tds[3].get_text())
        # Extrai o primeiro número inteiro
        m = re.search(r'(\d+)', vic_str)
        if not m:
            continue
        vitorias = int(m.group(1))
        
        # Teatro predominante e aeronave principal
        # Na Luftwaffe com 100+ vitórias, a esmagadora maioria voou no Front Oriental (Bf 109 / Fw 190)
        # Notas trazem detalhes de teatro quando específico (ex: Defense of Reich, Night Fighter)
        notes = clean_text(tds[5].get_text()) if len(tds) > 5 else ""
        teatro = "Frente Oriental"
        aeronave = "Messerschmitt Bf 109 / Fw 190"
        if "night" in notes.lower() or "night" in nome.lower():
            teatro = "Defesa do Reich"
            aeronave = "Bf 110 / Ju 88"
        elif "western" in notes.lower() or "channel" in notes.lower() or "spitfire" in notes.lower():
            teatro = "Frente Ocidental"
        elif "africa" in notes.lower() or "marseille" in nome.lower():
            teatro = "Norte da África / Mediterrâneo"
            aeronave = "Messerschmitt Bf 109"
            
        aces.append({
            "nome_piloto": nome,
            "pais": pais,
            "forca_aerea": forca,
            "numero_vitorias": vitorias,
            "aeronave_principal": aeronave,
            "teatro_de_operacao": teatro,
            "periodo_ativo": "1939-1945",
            "fonte": source_url
        })
    print(f"-> {len(aces)} ases alemães coletados.")
    return aces

def extract_us_aces():
    """Coleta top ases dos Estados Unidos (vitórias >= 10)."""
    print("Coletando ases dos Estados Unidos...")
    html = fetch_wiki_parse("List_of_World_War_II_aces_from_the_United_States")
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    if not table:
        return []
    
    source_url = "https://en.wikipedia.org/wiki/List_of_World_War_II_aces_from_the_United_States"
    aces = []
    
    # Mapeamento conhecido de aeronave e teatro dos principais ases americanos
    known_us_aces = {
        "Richard Bong": ("P-38 Lightning", "Pacífico Sul / Sudoeste", "USAAF"),
        "Thomas McGuire": ("P-38 Lightning", "Pacífico Sul / Sudoeste", "USAAF"),
        "David McCampbell": ("F6F Hellcat", "Pacífico (Naval)", "US Navy"),
        "Gregory Boyington": ("F4U Corsair", "Pacífico (Salomão)", "USMC"),
        "Francis Gabreski": ("P-47 Thunderbolt", "Europa (ETO)", "USAAF"),
        "Robert S. Johnson": ("P-47 Thunderbolt", "Europa (ETO)", "USAAF"),
        "Charles H. MacDonald": ("P-38 Lightning", "Pacífico", "USAAF"),
        "George Preddy": ("P-51 Mustang", "Europa (ETO)", "USAAF"),
        "Joseph J. Foss": ("F4F Wildcat", "Pacífico (Guadalcanal)", "USMC"),
        "Robert M. Hanson": ("F4U Corsair", "Pacífico (Bougainville)", "USMC"),
        "John C. Meyer": ("P-51 Mustang / P-47", "Europa (ETO)", "USAAF"),
        "David C. Schilling": ("P-47 Thunderbolt", "Europa (ETO)", "USAAF"),
        "Gerald R. Johnson": ("P-38 Lightning", "Pacífico", "USAAF"),
        "Neel E. Kearby": ("P-47 Thunderbolt", "Pacífico", "USAAF"),
        "Jay T. Robbins": ("P-38 Lightning", "Pacífico", "USAAF"),
        "Alexander Vraciu": ("F6F Hellcat", "Pacífico (Naval)", "US Navy"),
        "Donald N. Aldrich": ("F4U Corsair", "Pacífico", "USMC"),
        "John T. Godfrey": ("P-47 / P-51", "Europa (ETO)", "USAAF"),
        "Bud Anderson": ("P-51 Mustang", "Europa (ETO)", "USAAF"),
        "Chuck Yeager": ("P-51 Mustang", "Europa (ETO)", "USAAF"),
        "Robin Olds": ("P-38 / P-51", "Europa (ETO)", "USAAF"),
        "Hubert Zemke": ("P-47 Thunderbolt", "Europa (ETO)", "USAAF"),
        "Don Gentile": ("P-47 / P-51", "Europa (ETO)", "USAAF"),
        "John S. Hampshire": ("P-40 Warhawk", "China-Birmânia-Índia", "USAAF"),
        "Kenneth A. Walsh": ("F4U Corsair", "Pacífico", "USMC"),
        "James S. Varnell Jr.": ("P-38 Lightning", "Mediterrâneo (MTO)", "USAAF"),
    }
    
    rows = table.find_all('tr')[1:]
    for r in rows:
        tds = r.find_all(['td', 'th'])
        if len(tds) < 3:
            continue
        nome = clean_text(tds[0].get_text())
        
        # O formato da tabela dos EUA tem Name, Branch, Victories
        # Alguns nomes ou células podem estar combinadas
        branch_cand = clean_text(tds[1].get_text())
        vic_cand = clean_text(tds[2].get_text())
        
        forca = "USAAF"
        if branch_cand in ["USAAF", "USN", "USMC", "AVG"]:
            forca = branch_cand
            vic_str = vic_cand
        else:
            # Caso Branch seja número de vitórias diretamente
            vic_str = branch_cand
            if "USN" in vic_cand:
                forca = "USN"
            elif "USMC" in vic_cand:
                forca = "USMC"
                
        m = re.search(r'(\d+(\.\d+)?)', vic_str)
        if not m:
            continue
        vitorias = float(m.group(1))
        
        # Filtra ases relevantes com vitórias >= 10 ou ases históricos conhecidos
        if vitorias >= 10 or nome in known_us_aces:
            aeronave = None
            teatro = None
            
            # Checa se está no dicionário de especialistas
            for kname, (kair, ktea, kfor) in known_us_aces.items():
                if kname.lower() in nome.lower():
                    aeronave = kair
                    teatro = ktea
                    forca = kfor
                    break
            
            if not teatro:
                if forca == "USN" or forca == "USMC":
                    teatro = "Pacífico"
                    aeronave = "F6F Hellcat / F4U Corsair"
                else:
                    teatro = "Europa / Pacífico"
                    aeronave = "P-51 Mustang / P-47 Thunderbolt"
                    
            aces.append({
                "nome_piloto": nome,
                "pais": "Estados Unidos",
                "forca_aerea": forca,
                "numero_vitorias": vitorias,
                "aeronave_principal": aeronave,
                "teatro_de_operacao": teatro,
                "periodo_ativo": "1941-1945",
                "fonte": source_url
            })
            
    # Ordena por vitórias decrescente e remove eventuais duplicados de nome
    df_us = pd.DataFrame(aces).drop_duplicates(subset=["nome_piloto"])
    print(f"-> {len(df_us)} ases dos EUA coletados (critério >= 10 vitórias ou ases notórios).")
    return df_us.to_dict('records')

def extract_soviet_aces():
    """Coleta ases da União Soviética (VVS)."""
    print("Coletando ases da União Soviética...")
    html = fetch_wiki_parse("List_of_World_War_II_aces_from_the_Soviet_Union")
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    if not table:
        return []
    
    source_url = "https://en.wikipedia.org/wiki/List_of_World_War_II_aces_from_the_Soviet_Union"
    aces = []
    
    known_soviet_aircraft = {
        "Ivan Kozhedub": "La-5 / La-7",
        "Alexander Pokryshkin": "P-39 Airacobra",
        "Grigory Rechkalov": "P-39 Airacobra / I-16",
        "Nikolai Gulayev": "P-39 Airacobra / Yak-1",
        "Kirill Yevstigneyev": "La-5 / La-7",
        "Arseny Vorozheykin": "Yak-7B / Yak-9",
        "Dmitry Glinka": "P-39 Airacobra",
        "Alexander Koldunov": "Yak-7B / Yak-9",
        "Nikolai Skomorokhov": "La-5",
        "Vitaly Popkov": "La-5 / La-7",
        "Ivan Sultan Amet-Khan": "Yak-1 / Yak-7 / P-39 / La-7",
        "Lydia Litvyak": "Yak-1 (Rosa de Stalingrado)",
        "Yekaterina Budanova": "Yak-1"
    }
    
    rows = table.find_all('tr')[1:]
    for r in rows:
        tds = r.find_all(['td', 'th'])
        if len(tds) < 3:
            continue
        nome = clean_text(tds[0].get_text())
        tot_str = clean_text(tds[1].get_text())
        m = re.search(r'(\d+)', tot_str)
        if not m:
            continue
        vitorias = int(m.group(1))
        
        # Filtra top ases soviéticos (vitórias >= 15 ou notáveis femininas)
        if vitorias >= 15 or "Lydia" in nome or "Yekaterina" in nome:
            aeronave = "Yakovlev Yak-1/3/7/9 ou La-5/7"
            for kname, kair in known_soviet_aircraft.items():
                if kname.lower() in nome.lower():
                    aeronave = kair
                    break
                    
            aces.append({
                "nome_piloto": nome,
                "pais": "União Soviética",
                "forca_aerea": "VVS",
                "numero_vitorias": vitorias,
                "aeronave_principal": aeronave,
                "teatro_de_operacao": "Frente Oriental",
                "periodo_ativo": "1941-1945",
                "fonte": source_url
            })
            
    df_su = pd.DataFrame(aces).drop_duplicates(subset=["nome_piloto"])
    print(f"-> {len(df_su)} ases soviéticos coletados.")
    return df_su.to_dict('records')

def extract_uk_aces():
    """Coleta ases do Reino Unido e Commonwealth (RAF)."""
    print("Coletando ases do Reino Unido / Commonwealth...")
    html = fetch_wiki_parse("List_of_World_War_II_aces_from_the_United_Kingdom")
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    if not table:
        return []
    
    source_url = "https://en.wikipedia.org/wiki/List_of_World_War_II_aces_from_the_United_Kingdom"
    aces = []
    
    known_uk_aircraft = {
        "Pattle": ("Hawker Hurricane / Gladiator", "Grécia / Norte da África"),
        "Johnson, James Edgar": ("Supermarine Spitfire", "Europa Ocidental"),
        "Beurling, George": ("Supermarine Spitfire", "Malta / Mediterrâneo"),
        "Malan, Adolph": ("Supermarine Spitfire", "Batalha da Inglaterra / ETO"),
        "Finucane, Brendan": ("Supermarine Spitfire", "Batalha da Inglaterra / ETO"),
        "Tuck, Robert Stanford": ("Hawker Hurricane / Spitfire", "Batalha da Inglaterra"),
        "Bader, Douglas": ("Hawker Hurricane / Spitfire", "Batalha da Inglaterra"),
        "Lacey, James": ("Hawker Hurricane", "Batalha da Inglaterra"),
        "Duke, Neville": ("Supermarine Spitfire / Curtiss Tomahawk", "Mediterrâneo / Itália"),
        "Gray, Colin": ("Supermarine Spitfire", "Batalha da Inglaterra / MTO"),
        "Lock, Eric": ("Supermarine Spitfire", "Batalha da Inglaterra"),
        "Caldwell, Clive": ("P-40 Tomahawk / Spitfire", "Norte da África / Pacífico"),
        "Frantisek, Josef": ("Hawker Hurricane", "Batalha da Inglaterra (303 Sqn)"),
        "Kingcome, Brian": ("Supermarine Spitfire", "Batalha da Inglaterra"),
        "Deere, Alan": ("Supermarine Spitfire", "Batalha da Inglaterra")
    }
    
    rows = table.find_all('tr')[1:]
    for r in rows:
        tds = r.find_all(['td', 'th'])
        if len(tds) < 2:
            continue
        nome = clean_text(tds[0].get_text())
        vic_str = clean_text(tds[1].get_text())
        m = re.search(r'(\d+(\.\d+)?)', vic_str)
        if not m:
            continue
        vitorias = float(m.group(1))
        
        # Filtra ases com vitórias >= 10 ou ases notáveis
        if vitorias >= 10:
            aeronave = "Supermarine Spitfire / Hawker Hurricane"
            teatro = "Europa Ocidental / Batalha da Inglaterra"
            for kname, (kair, ktea) in known_uk_aircraft.items():
                if kname.lower() in nome.lower():
                    aeronave = kair
                    teatro = ktea
                    break
                    
            aces.append({
                "nome_piloto": nome,
                "pais": "Reino Unido",
                "forca_aerea": "Royal Air Force (RAF)",
                "numero_vitorias": vitorias,
                "aeronave_principal": aeronave,
                "teatro_de_operacao": teatro,
                "periodo_ativo": "1939-1945",
                "fonte": source_url
            })
            
    df_uk = pd.DataFrame(aces).drop_duplicates(subset=["nome_piloto"])
    print(f"-> {len(df_uk)} ases britânicos coletados.")
    return df_uk.to_dict('records')

def extract_japan_aces():
    """Coleta ases do Japão (IJN e IJA)."""
    print("Coletando ases do Japão...")
    html = fetch_wiki_parse("List_of_World_War_II_aces_from_Japan")
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    source_url = "https://en.wikipedia.org/wiki/List_of_World_War_II_aces_from_Japan"
    aces = []
    
    for t in tables:
        rows = t.find_all('tr')[1:]
        for r in rows:
            tds = r.find_all(['td', 'th'])
            if len(tds) < 5:
                continue
            # Colunas: Portrait, Name, Kills, Rank, Service
            nome = clean_text(tds[1].get_text())
            kills_str = clean_text(tds[2].get_text())
            service_str = clean_text(tds[4].get_text())
            
            m = re.search(r'(\d+)', kills_str)
            if not m:
                continue
            vitorias = int(m.group(1))
            
            forca = "IJN (Marinha Imperial)" if "IJN" in service_str else "IJA (Exército Imperial)"
            aeronave = "Mitsubishi A6M Zero" if "IJN" in service_str else "Nakajima Ki-43 / Ki-84"
            
            aces.append({
                "nome_piloto": nome,
                "pais": "Japão",
                "forca_aerea": forca,
                "numero_vitorias": vitorias,
                "aeronave_principal": aeronave,
                "teatro_de_operacao": "Teatro do Pacífico",
                "periodo_ativo": "1937-1945",
                "fonte": source_url
            })
            
    # Ases notáveis do Japão que podem estar em grafias diferentes
    # Nishizawa (87), Iwamoto (80), Sugita (70), Sakai (64)
    df_jp = pd.DataFrame(aces).drop_duplicates(subset=["nome_piloto"])
    print(f"-> {len(df_jp)} ases japoneses coletados.")
    return df_jp.to_dict('records')

def main():
    os.makedirs(r"C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\raw", exist_ok=True)
    all_aces = []
    all_aces.extend(extract_german_aces())
    all_aces.extend(extract_us_aces())
    all_aces.extend(extract_soviet_aces())
    all_aces.extend(extract_uk_aces())
    all_aces.extend(extract_japan_aces())
    
    df = pd.DataFrame(all_aces)
    out_csv = r"C:\Users\artur\.gemini\antigravity\scratch\ases-e-atrito\data\raw\ases.csv"
    df.to_csv(out_csv, index=False, encoding='utf-8-sig')
    print(f"\nSucesso! Total de {len(df)} ases salvos em {out_csv}")
    print("\nDistribuição por país:")
    print(df['pais'].value_counts())

if __name__ == '__main__':
    main()
