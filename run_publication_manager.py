#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Publication Manager Test
Test der neustrukturierten Module
"""

import sys
import json
from pathlib import Path

# Füge src-Verzeichnis zu Python Path hinzu
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

def load_saved_cookies():
    """Lädt gespeicherte Cookies aus der Config-Datei"""
    try:
        config_path = Path(__file__).parent / 'config' / 'confluence_credentials.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('cookies', '')
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None

def main():
    """Test der neustrukturierten Module"""
    print("🧬 RACOON Publication Manager - Structure Test")
    print("=" * 60)
    
    try:
        from core.confluence_sso import ConfluenceSSO
        print("✅ Core SSO-Module erfolgreich geladen!")
        
        # SSO testen
        confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
        
        # Cookie-Management
        cookie_header = load_saved_cookies()
        if cookie_header and cookie_header != "Bitte_Cookies_hier_eingeben":
            print("✅ Gespeicherte Cookies gefunden!")
            
            if confluence_sso.login_with_cookies(cookie_header):
                print("✅ SSO-Login erfolgreich!")
                
                # Test: Lade RACOON Publikationen
                page = confluence_sso.get_page("165485055", "body.storage,version")
                print(f"✅ RACOON-Seite geladen: Version {page['version']['number']}")
                
                return True
            else:
                print("❌ SSO-Login fehlgeschlagen!")
        else:
            print("⚠️ Keine gültigen Cookies in config/confluence_credentials.json")
            print("💡 Bitte Cookies in der Config-Datei aktualisieren")
    
    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        print("💡 Stelle sicher, dass alle Module im src/ Ordner sind")
        return False
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Neustrukturiertes System funktioniert!")
    else:
        print("\n❌ System-Test fehlgeschlagen!")