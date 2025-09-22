#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Publikationen - Test Update
Fügt eine Test-Zeile zur Tabelle hinzu
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from confluence_sso import ConfluenceSSO

def add_test_row():
    """Fügt eine Test-Zeile zur RACOON Publikationstabelle hinzu"""
    
    print("=== RACOON Publikationen - Test Update ===")
    print("Füge Test-Zeile hinzu...")
    
    # SSO-Session erstellen
    confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
    
    # Cookies aus dem letzten erfolgreichen Login wiederverwenden
    cookie_header = input("Geben Sie Ihre Cookies ein (oder Enter für gespeicherte): ").strip()
    
    if not cookie_header:
        # Verwende die gleichen Cookies wie vorher
        cookie_header = "JSESSIONID=FDF7EA568195E4719718F668128D0CAC; seraph.confluence=302547384:a12fdc95ed4c55b7ce9913674db0e9d4091c5d03"
        print("📋 Verwende gespeicherte Cookies...")
    
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
        
        # 2. Test-Zeile erstellen
        test_row = """<tr><td><p>TEST</p></td><td><p>TEST</p></td><td>TEST</td><td><p>TEST</p></td><td><div class="content-wrapper"><p><ac:structured-macro ac:name="status-handy" ac:schema-version="1"><ac:parameter ac:name="Status">TEST</ac:parameter></ac:structured-macro></p></div></td><td><div class="content-wrapper"><p>TEST</p></div></td></tr>"""
        
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
        backup_file = Path("racoon_publications_with_test.html")
        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"💾 Backup mit Test-Zeile gespeichert: {backup_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Update: {e}")
        return False

def remove_test_row():
    """Entfernt die Test-Zeile wieder"""
    
    print("=== RACOON Publikationen - Test-Zeile entfernen ===")
    
    # SSO-Session erstellen
    confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
    
    cookie_header = input("Geben Sie Ihre Cookies ein: ").strip()
    
    if not confluence_sso.login_with_cookies(cookie_header):
        print("❌ Cookie-Login fehlgeschlagen!")
        return False
    
    try:
        # Aktuelle Seite laden
        page = confluence_sso.get_page("165485055", "body.storage,version")
        current_content = page['body']['storage']['value']
        
        # Test-Zeile entfernen
        test_row_pattern = """<tr><td><p>TEST</p></td><td><p>TEST</p></td><td>TEST</td><td><p>TEST</p></td><td><div class="content-wrapper"><p><ac:structured-macro ac:name="status-handy" ac:schema-version="1"><ac:parameter ac:name="Status">TEST</ac:parameter></ac:structured-macro></p></div></td><td><div class="content-wrapper"><p>TEST</p></div></td></tr>"""
        
        if test_row_pattern in current_content:
            updated_content = current_content.replace(test_row_pattern, "")
            
            result = confluence_sso.update_page(
                page_id="165485055",
                title=page['title'],
                content=updated_content,
                version=page['version']['number']
            )
            
            print(f"✅ Test-Zeile entfernt! Neue Version: {result['version']['number']}")
            return True
        else:
            print("⚠️  Test-Zeile nicht gefunden!")
            return False
            
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