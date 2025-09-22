#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Publikationen - Test Update
Fügt eine Test-Zeile zur Tabelle hinzu
"""

import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from confluence_sso import ConfluenceSSO

def load_saved_cookies():
    """Lädt gespeicherte Cookies aus der Credentials-Datei"""
    try:
        with open('confluence_credentials.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('cookies', '')
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None

def get_cookies():
    """Holt Cookies - automatisch oder manuell"""
    saved_cookies = load_saved_cookies()
    
    if saved_cookies:
        print("📋 Verwende gespeicherte Cookies...")
        return saved_cookies
    else:
        return input("🔑 Cookies eingeben: ").strip()

def add_test_row():
    """Fügt eine Test-Zeile zur RACOON Publikationstabelle hinzu"""
    print("=== RACOON Publikationen - Test Update ===")
    print("Füge Test-Zeile hinzu...")
    
    # SSO-Session erstellen
    confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
    
    # Automatisches Cookie-Management
    cookie_header = input("Geben Sie Ihre Cookies ein (oder Enter für gespeicherte): ").strip()
    if not cookie_header:
        cookie_header = get_cookies()
    
    if not cookie_header:
        print("❌ Keine Cookies verfügbar!")
        return False
    
    if not confluence_sso.login_with_cookies(cookie_header):
        print("❌ Cookie-Login fehlgeschlagen!")
        return False
    
    try:
        # 1. Aktuelle Seite laden
        print("📖 Lade aktuelle Seite...")
        page = confluence_sso.get_page("165485055", "body.storage,version")
        
        current_content = page['body']['storage']['value']
        current_version = page['version']['number']
        print(f"✅ Seite geladen: Version {current_version}")
        
        # 2. Test-Zeile erstellen (kompakte Formatierung)
        test_row = (
            '<tr>'
            '<td><p>TEST</p></td>'
            '<td><p>TEST</p></td>'
            '<td>TEST</td>'
            '<td><p>TEST</p></td>'
            '<td><div class="content-wrapper"><p>'
            '<ac:structured-macro ac:name="status-handy" ac:schema-version="1">'
            '<ac:parameter ac:name="Status">TEST</ac:parameter>'
            '</ac:structured-macro></p></div></td>'
            '<td><div class="content-wrapper"><p>TEST</p></div></td>'
            '</tr>'
        )
        
        # 3. Finde die letzte Zeile der Tabelle (vor </tbody>)
        tbody_end = current_content.rfind('</tbody>')
        
        if tbody_end == -1:
            print("❌ Tabellen-Ende nicht gefunden!")
            return False
        
        # 4. Füge Test-Zeile vor </tbody> ein
        updated_content = (
            current_content[:tbody_end] + 
            test_row + 
            current_content[tbody_end:]
        )
        print("✏️ Test-Zeile wurde eingefügt")
        
        # 5. Seite aktualisieren
        print("🚀 Aktualisiere Confluence-Seite...")
        result = confluence_sso.update_page(
            page_id="165485055",
            title=page['title'],
            content=updated_content,
            version=current_version
        )
        
        print(f"✅ Seite erfolgreich aktualisiert!")
        print(f"Neue Version: {result['version']['number']}")
        print(f"URL: https://wms.diz-ag.med.ovgu.de{result['_links']['webui']}")
        
        # 6. Backup der aktualisierten Version erstellen
        confluence_sso.create_backup(updated_content, "racoon_publications_with_test")
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Update: {e}")
        return False

def remove_test_row():
    """Entfernt die Test-Zeile wieder"""
    print("=== RACOON Publikationen - Test-Zeile entfernen ===")
    
    # SSO-Session erstellen
    confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
    
    # Automatisches Cookie-Management
    cookie_header = input("Geben Sie Ihre Cookies ein (oder Enter für gespeicherte): ").strip()
    if not cookie_header:
        cookie_header = get_cookies()
    
    if not cookie_header:
        print("❌ Keine Cookies verfügbar!")
        return False
    
    if not confluence_sso.login_with_cookies(cookie_header):
        print("❌ Cookie-Login fehlgeschlagen!")
        return False
    
    try:
        # Aktuelle Seite laden
        page = confluence_sso.get_page("165485055", "body.storage,version")
        current_content = page['body']['storage']['value']
        
        # Finde die letzte Tabellenzeile (tr) vor </tbody>
        import re
        
        # EINFACHSTE und SICHERSTE Lösung: Rückwärts suchen
        
        # 1. Finde die letzte </tr> Position
        last_tr_end = current_content.rfind('</tr>')
        if last_tr_end == -1:
            print("⚠️  Keine Tabellenzeilen gefunden!")
            return False
        
        # 2. Suche rückwärts nach dem letzten <tr vor dieser Position
        search_content = current_content[:last_tr_end]
        last_tr_start = search_content.rfind('<tr')
        
        if last_tr_start == -1:
            print("⚠️  Letzte TR-Zeile nicht gefunden!")
            return False
        
        # 3. Extrahiere die letzte Zeile
        last_tr_end_complete = last_tr_end + 5  # +5 für '</tr>'
        row_content = current_content[last_tr_start:last_tr_end_complete]
        
        # 4. Prüfe ob es nicht der Header ist (enthält <th>)
        if '<th>' in row_content:
            print("⚠️  Kann Header-Zeile nicht entfernen!")
            return False
        
        print(f"🗑️  Entferne letzte Tabellenzeile: {row_content[:100]}...")
        
        # 5. Sichere Entfernung
        updated_content = current_content[:last_tr_start] + current_content[last_tr_end_complete:]
        
        result = confluence_sso.update_page(
            page_id="165485055",
            title=page['title'],
            content=updated_content,
            version=page['version']['number']
        )
        print(f"✅ Letzte Tabellenzeile entfernt! Neue Version: {result['version']['number']}")
        return True
            
    except Exception as e:
        print(f"❌ Fehler beim Entfernen: {e}")
        return False

def main():
    """Hauptfunktion"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--add":
            add_test_row()
        elif sys.argv[1] == "--remove":
            remove_test_row()
        else:
            print("Unbekannte Option!")
    else:
        print("📋 Test-Update Optionen:")
        print("  python racoon_test_update.py --add     # Test-Zeile hinzufügen")
        print("  python racoon_test_update.py --remove  # Test-Zeile entfernen")
        print()
        
        choice = input("Was möchten Sie tun? (add/remove): ").strip().lower()
        
        if choice == "add":
            add_test_row()
        elif choice == "remove":
            remove_test_row()
        else:
            print("Ungültige Eingabe!")

if __name__ == "__main__":
    main()