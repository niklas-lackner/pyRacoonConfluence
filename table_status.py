#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Publikationen - Status-Check
Prüft den aktuellen Status der Tabelle
"""

import sys
import re
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from confluence_sso import ConfluenceSSO

def check_table_status():
    """Prüft den aktuellen Status der Tabelle"""
    print("🔍 RACOON Publikationen - Status-Check")
    print("=" * 50)
    
    # SSO-Session erstellen
    confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
    
    # Gespeicherte Cookies verwenden
    try:
        with open('confluence_credentials.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            cookie_header = data.get('cookies', '')
    except:
        cookie_header = input("🔑 Cookies eingeben: ").strip()
    
    if not confluence_sso.login_with_cookies(cookie_header):
        print("❌ Cookie-Login fehlgeschlagen!")
        return False
    
    try:
        # Aktuelle Seite laden
        print("📖 Lade aktuelle Seite...")
        page = confluence_sso.get_page("165485055", "body.storage,version")
        current_content = page['body']['storage']['value']
        current_version = page['version']['number']
        
        print(f"✅ Seite geladen: Version {current_version}")
        print(f"📊 Content-Größe: {len(current_content):,} Zeichen")
        
        # Nach TEST-Zeilen suchen
        test_patterns = [
            r'<tr[^>]*>.*?TEST.*?</tr>',
            r'<p[^>]*>.*?TEST.*?</p>',
            r'>TEST<',
        ]
        
        total_test_matches = 0
        print("\n🔍 Suche nach TEST-Inhalten:")
        
        for i, pattern in enumerate(test_patterns, 1):
            matches = re.findall(pattern, current_content, re.DOTALL | re.IGNORECASE)
            if matches:
                print(f"  Pattern {i}: {len(matches)} Treffer")
                total_test_matches += len(matches)
                for j, match in enumerate(matches[:3]):  # Zeige nur die ersten 3
                    preview = match[:100] + "..." if len(match) > 100 else match
                    print(f"    {j+1}. {preview}")
                if len(matches) > 3:
                    print(f"    ... und {len(matches)-3} weitere")
            else:
                print(f"  Pattern {i}: Keine Treffer")
        
        # Nach leeren Zeilen suchen
        empty_patterns = [
            r'<tr>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*</tr>',
            r'<tr>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>[^<]*</tr>',
        ]
        
        total_empty_matches = 0
        print("\n🗑️ Suche nach leeren Zeilen:")
        
        for i, pattern in enumerate(empty_patterns, 1):
            matches = re.findall(pattern, current_content, re.DOTALL | re.IGNORECASE)
            if matches:
                print(f"  Pattern {i}: {len(matches)} leere Zeilen")
                total_empty_matches += len(matches)
            else:
                print(f"  Pattern {i}: Keine leeren Zeilen")
        
        print(f"\n📋 Zusammenfassung:")
        print(f"  🎯 TEST-Inhalte: {total_test_matches}")
        print(f"  🗑️ Leere Zeilen: {total_empty_matches}")
        
        if total_test_matches == 0 and total_empty_matches == 0:
            print("✨ Tabelle ist sauber!")
        else:
            print("⚠️ Bereinigung empfohlen")
            
        return True
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    check_table_status()