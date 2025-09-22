#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Publikationen - Muster-Analyse
Analysiert die vorhandenen Publikationen um Patterns zu identifizieren
"""

import sys
import json
import re
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core.confluence_sso import ConfluenceSSO

def load_saved_cookies():
    """Lädt gespeicherte Cookies aus der Credentials-Datei"""
    try:
        with open('confluence_credentials.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('cookies', '')
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None

def analyze_publication_patterns():
    """Analysiert die Publikationsmuster in der RACOON Tabelle"""
    print("🔍 RACOON Publikationen - Muster-Analyse")
    print("=" * 50)
    
    # SSO-Session erstellen
    confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
    
    # Automatisches Cookie-Management
    cookie_header = load_saved_cookies()
    if not cookie_header:
        cookie_header = input("🔑 Cookies eingeben: ").strip()
    
    if not confluence_sso.login_with_cookies(cookie_header):
        print("❌ Cookie-Login fehlgeschlagen!")
        return False
    
    try:
        # Aktuelle Seite laden
        print("📖 Lade RACOON Publikationen...")
        page = confluence_sso.get_page("165485055", "body.storage,version")
        current_content = page['body']['storage']['value']
        
        print(f"✅ Seite geladen: Version {page['version']['number']}")
        print(f"📊 Content-Größe: {len(current_content):,} Zeichen")
        
        # Backup für Analyse erstellen
        confluence_sso.create_backup(current_content, "racoon_publications_analysis")
        
        # Tabellen-Zeilen extrahieren
        print("\n🧬 Analysiere Tabellenstruktur...")
        
        # Finde alle TR-Zeilen (ohne Header)
        tr_pattern = r'<tr[^>]*>(.*?)</tr>'
        all_rows = re.findall(tr_pattern, current_content, re.DOTALL)
        
        print(f"📋 Gefundene Tabellenzeilen: {len(all_rows)}")
        
        # Header analysieren
        header_row = all_rows[0] if all_rows else ""
        print("\n📑 Header-Struktur:")
        th_pattern = r'<th[^>]*>(.*?)</th>'
        headers = re.findall(th_pattern, header_row, re.DOTALL)
        
        for i, header in enumerate(headers, 1):
            clean_header = re.sub(r'<[^>]+>', '', header).strip()
            print(f"  {i}. {clean_header}")
        
        # Datenzeilen analysieren (ohne Header)
        data_rows = all_rows[1:] if len(all_rows) > 1 else []
        print(f"\n📊 Datenzeilen zu analysieren: {len(data_rows)}")
        
        # Analysiere erste 5 Publikationen detailliert
        print("\n🔬 Detailanalyse der ersten 5 Publikationen:")
        print("-" * 60)
        
        for i, row in enumerate(data_rows[:5], 1):
            print(f"\n📄 Publikation {i}:")
            
            # TD-Zellen extrahieren
            td_pattern = r'<td[^>]*>(.*?)</td>'
            cells = re.findall(td_pattern, row, re.DOTALL)
            
            for j, cell in enumerate(cells, 1):
                # Text aus HTML extrahieren
                clean_text = re.sub(r'<[^>]+>', ' ', cell)
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                
                # Kürzen für Übersicht
                display_text = clean_text[:100] + "..." if len(clean_text) > 100 else clean_text
                
                header_name = headers[j-1] if j-1 < len(headers) else f"Spalte {j}"
                clean_header = re.sub(r'<[^>]+>', '', header_name).strip()
                
                print(f"  {clean_header}: {display_text}")
        
        # Pattern-Analyse
        print("\n🧩 Pattern-Analyse:")
        analyze_publication_fields(data_rows)
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei der Analyse: {e}")
        return False

def analyze_publication_fields(data_rows):
    """Analysiert die Felder der Publikationen für Muster"""
    
    print("\n📋 Feldanalyse:")
    
    # Sammle alle Zellen nach Position
    fields_by_position = [[] for _ in range(6)]  # 6 Spalten
    
    for row in data_rows[:10]:  # Analysiere erste 10 Zeilen
        td_pattern = r'<td[^>]*>(.*?)</td>'
        cells = re.findall(td_pattern, row, re.DOTALL)
        
        for i, cell in enumerate(cells):
            if i < 6:  # Nur erste 6 Spalten
                # Text extrahieren
                clean_text = re.sub(r'<[^>]+>', ' ', cell)
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                fields_by_position[i].append(clean_text)
    
    field_names = ["Nummer", "Jahr/Monat", "Standort", "Personen", "Förderhinweis", "PubMed DOI"]
    
    for i, field_name in enumerate(field_names):
        print(f"\n🔹 {field_name}:")
        field_data = fields_by_position[i]
        
        if field_data:
            # Zeige erste 3 Beispiele
            print("   Beispiele:")
            for j, example in enumerate(field_data[:3], 1):
                short_example = example[:80] + "..." if len(example) > 80 else example
                print(f"     {j}. {short_example}")
            
            # Pattern-Erkennung
            if field_name == "Nummer":
                numbers = [ex for ex in field_data if ex.isdigit()]
                print(f"   📊 Numerische Werte: {len(numbers)}/{len(field_data)}")
                if numbers:
                    print(f"   📈 Bereich: {min(map(int, numbers))} - {max(map(int, numbers))}")
            
            elif field_name == "Jahr/Monat":
                years = [ex for ex in field_data if re.match(r'\d{4}', ex)]
                print(f"   📅 Jahr-Format erkannt: {len(years)}/{len(field_data)}")
                
            elif field_name == "Förderhinweis":
                ja_count = sum(1 for ex in field_data if 'JA' in ex.upper())
                nein_count = sum(1 for ex in field_data if 'NEIN' in ex.upper())
                print(f"   ✅ JA: {ja_count}, ❌ NEIN: {nein_count}")
                
            elif field_name == "PubMed DOI":
                doi_count = sum(1 for ex in field_data if 'doi:' in ex.lower())
                pmid_count = sum(1 for ex in field_data if 'pubmed' in ex.lower())
                print(f"   🔗 DOI gefunden: {doi_count}/{len(field_data)}")
                print(f"   📚 PubMed Links: {pmid_count}/{len(field_data)}")

def main():
    """Hauptfunktion"""
    success = analyze_publication_patterns()
    
    if success:
        print("\n🎉 Analyse abgeschlossen!")
        print("💡 Nächster Schritt: PubMed-Integration basierend auf erkannten Mustern")
    else:
        print("\n❌ Analyse fehlgeschlagen!")

if __name__ == "__main__":
    main()