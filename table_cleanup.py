#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Publikationen - Tabellen-Bereinigung
Entfernt Test-Zeilen und leere Zeilen aus der Publikationstabelle
"""

import sys
import re
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from confluence_sso import ConfluenceSSO

def clean_table():
    """Bereinigt die Publikationstabelle von Test-Zeilen und leeren Zeilen"""
    print("=== RACOON Publikationen - Tabellen-Bereinigung ===")
    print("Entferne Test-Zeilen und leere Zeilen...")
    
    # SSO-Session erstellen
    confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
    cookie_header = input("Geben Sie Ihre Cookies ein: ").strip()
    
    if not confluence_sso.login_with_cookies(cookie_header):
        print("❌ Cookie-Login fehlgeschlagen!")
        return False
    
    try:
        # Aktuelle Seite laden
        print("📖 Lade aktuelle Seite...")
        page = confluence_sso.get_page("165484671", "body.storage,version")
        current_content = page['body']['storage']['value']
        current_version = page['version']['number']
        
        print(f"✅ Seite geladen: Version {current_version}")
        print(f"Original Content-Länge: {len(current_content)} Zeichen")
        
        # Backup vor Änderungen erstellen
        confluence_sso.create_backup(current_content, "racoon_publications_before_cleanup")
        
        # 1. Entferne Test-Zeilen (verschiedene mögliche Varianten)
        test_patterns = [
            # Original kompakte Zeile
            r'<tr><td><p>TEST</p></td><td><p>TEST</p></td><td>TEST</td><td><p>TEST</p></td><td><div class="content-wrapper"><p><ac:structured-macro ac:name="status-handy" ac:schema-version="1"><ac:parameter ac:name="Status">TEST</ac:parameter></ac:structured-macro></p></div></td><td><div class="content-wrapper"><p>TEST</p></div></td></tr>',
            
            # Mehrzeilige Varianten
            r'<tr>\s*<td[^>]*>\s*<p>\s*TEST\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*TEST\s*</p>\s*</td>\s*<td[^>]*>\s*TEST\s*</td>\s*<td[^>]*>\s*<p>\s*TEST\s*</p>\s*</td>\s*<td[^>]*>.*?TEST.*?</td>\s*<td[^>]*>.*?TEST.*?</td>\s*</tr>',
            
            # Einfache TEST-Zeilen
            r'<tr[^>]*>.*?TEST.*?</tr>',
        ]
        
        # 2. Entferne leere Tabellenzeilen
        empty_row_patterns = [
            # Komplett leere Zeilen
            r'<tr>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*</tr>',
            
            # Zeilen mit nur Leerzeichen/Paragraph-Tags
            r'<tr>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*</tr>',
            
            # Zeilen mit nur nbsp oder Leerzeichen
            r'<tr[^>]*>(\s*<td[^>]*>(\s*<p[^>]*>\s*(&nbsp;|\s)*\s*</p>\s*|\s*(&nbsp;|\s)*\s*)</td>\s*){6}</tr>',
        ]
        
        updated_content = current_content
        removed_count = 0
        
        print("🧹 Entferne Test-Zeilen...")
        for i, pattern in enumerate(test_patterns):
            before_length = len(updated_content)
            updated_content = re.sub(pattern, '', updated_content, flags=re.DOTALL | re.IGNORECASE)
            after_length = len(updated_content)
            
            if before_length != after_length:
                removed = before_length - after_length
                print(f"  📝 Test-Pattern {i+1}: {removed} Zeichen entfernt")
                removed_count += 1
        
        print("🧹 Entferne leere Zeilen...")
        for i, pattern in enumerate(empty_row_patterns):
            before_length = len(updated_content)
            updated_content = re.sub(pattern, '', updated_content, flags=re.DOTALL | re.IGNORECASE)
            after_length = len(updated_content)
            
            if before_length != after_length:
                removed = before_length - after_length
                print(f"  📝 Leere-Zeilen-Pattern {i+1}: {removed} Zeichen entfernt")
                removed_count += 1
        
        # 3. Entferne mehrfache aufeinanderfolgende Leerzeichen/Newlines in der Tabelle
        updated_content = re.sub(r'\s+', ' ', updated_content)
        updated_content = re.sub(r'>\s+<', '><', updated_content)
        
        print(f"📊 Bereinigte Content-Länge: {len(updated_content)} Zeichen")
        print(f"📉 Differenz: {len(current_content) - len(updated_content)} Zeichen entfernt")
        
        if updated_content == current_content:
            print("ℹ️  Keine Änderungen erforderlich - Tabelle ist bereits sauber!")
            return True
        
        # 4. Seite aktualisieren
        print("🚀 Aktualisiere Confluence-Seite...")
        result = confluence_sso.update_page(
            page_id="165485055",
            title=page['title'],
            content=updated_content,
            version=current_version
        )
        
        print(f"✅ Tabelle erfolgreich bereinigt!")
        print(f"Neue Version: {result['version']['number']}")
        print(f"URL: https://wms.diz-ag.med.ovgu.de{result['_links']['webui']}")
        
        # Backup nach Bereinigung erstellen
        confluence_sso.create_backup(updated_content, "racoon_publications_after_cleanup")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei der Bereinigung: {e}")
        return False

def main():
    """Hauptfunktion"""
    print("🧹 RACOON Publikationen Tabellen-Bereinigung")
    print("=" * 50)
    print("Dieses Script entfernt:")
    print("  - Test-Zeilen mit 'TEST'-Inhalten")
    print("  - Komplett leere Tabellenzeilen")
    print("  - Zeilen mit nur Leerzeichen")
    print()
    
    confirm = input("Möchten Sie die Bereinigung starten? (j/N): ").strip().lower()
    
    if confirm in ['j', 'ja', 'y', 'yes']:
        clean_table()
    else:
        print("❌ Bereinigung abgebrochen.")

if __name__ == "__main__":
    main()