#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Publikationen - Schnelle Bereinigung
Automatische Bereinigung mit gespeicherten Cookies
"""

import sys
import re
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

def save_cookies(cookies):
    """Speichert Cookies in der Credentials-Datei"""
    try:
        # Versuche existierende Datei zu laden
        try:
            with open('confluence_credentials.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        
        # Cookies hinzufügen
        data['cookies'] = cookies
        
        # Datei speichern
        with open('confluence_credentials.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"⚠️  Fehler beim Speichern der Cookies: {e}")
        return False

def quick_cleanup():
    """Schnelle Bereinigung mit automatischen Cookies"""
    print("🧹 RACOON Publikationen - Schnelle Bereinigung")
    print("=" * 50)
    
    # Versuche gespeicherte Cookies zu laden
    saved_cookies = load_saved_cookies()
    
    if saved_cookies:
        print("✅ Gespeicherte Cookies gefunden")
        use_saved = input("Gespeicherte Cookies verwenden? (J/n): ").strip().lower()
        if use_saved != 'n':
            cookie_header = saved_cookies
        else:
            cookie_header = input("🔑 Neue Cookies eingeben: ").strip()
            if cookie_header:
                save_cookies(cookie_header)
    else:
        print("🔑 Keine gespeicherten Cookies gefunden")
        cookie_header = input("Cookies eingeben: ").strip()
        if cookie_header:
            save_option = input("Cookies für künftige Verwendung speichern? (J/n): ").strip().lower()
            if save_option != 'n':
                save_cookies(cookie_header)
    
    if not cookie_header:
        print("❌ Keine Cookies angegeben!")
        return False
    
    # SSO-Session erstellen
    confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
    
    if not confluence_sso.login_with_cookies(cookie_header):
        print("❌ Cookie-Login fehlgeschlagen!")
        # Bei Fehler Cookie aus Datei entfernen
        save_cookies('')
        return False
    
    try:
        # Aktuelle Seite laden
        print("📖 Lade RACOON Publikationen...")
        page = confluence_sso.get_page("165485055", "body.storage,version")
        current_content = page['body']['storage']['value']
        current_version = page['version']['number']
        
        print(f"✅ Seite geladen: Version {current_version}")
        
        # Backup vor Änderungen erstellen
        confluence_sso.create_backup(current_content, "racoon_publications_before_quick_cleanup")
        
        # Bereinigungspatterns - SEHR SPEZIFISCH für TEST-Zeilen
        test_patterns = [
            # Exakte TEST-Zeile Pattern 1 (mit ersten macro-id)
            r'<tr><td><p>TEST</p></td><td><p>TEST</p></td><td>TEST</td><td><p>TEST</p></td><td><div class="content-wrapper"><p><ac:structured-macro ac:name="status-handy" ac:schema-version="1" ac:macro-id="2f2634ba-9170-4516-b9c5-027a1e38996e"><ac:parameter ac:name="Status">TEST</ac:parameter></ac:structured-macro></p></div></td><td><div class="content-wrapper"><p>TEST</p></div></td></tr>',
            
            # Exakte TEST-Zeile Pattern 2 (mit zweiten macro-id)  
            r'<tr><td><p>TEST</p></td><td><p>TEST</p></td><td>TEST</td><td><p>TEST</p></td><td><div class="content-wrapper"><p><ac:structured-macro ac:name="status-handy" ac:schema-version="1" ac:macro-id="2dd49f60-fbbd-4660-a677-17b853d8d7aa"><ac:parameter ac:name="Status">TEST</ac:parameter></ac:structured-macro></p></div></td><td><div class="content-wrapper"><p>TEST</p></div></td></tr>',
            
            # Exakte TEST-Zeile Pattern 3 (ohne macro-id)
            r'<tr><td><p>TEST</p></td><td><p>TEST</p></td><td>TEST</td><td><p>TEST</p></td><td><div class="content-wrapper"><p><ac:structured-macro ac:name="status-handy" ac:schema-version="1"><ac:parameter ac:name="Status">TEST</ac:parameter></ac:structured-macro></p></div></td><td><div class="content-wrapper"><p>TEST</p></div></td></tr>',
        ]
        
        empty_row_patterns = [
            r'<tr>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*<td[^>]*>\s*</td>\s*</tr>',
            r'<tr>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*<td[^>]*>\s*<p>\s*</p>\s*</td>\s*</tr>',
        ]
        
        new_content = current_content
        removed_count = 0
        
        # TEST-Zeilen entfernen
        for pattern in test_patterns:
            matches = re.findall(pattern, new_content, re.DOTALL | re.IGNORECASE)
            if matches:
                print(f"🗑️  Entferne {len(matches)} TEST-Zeile(n)")
                removed_count += len(matches)
            new_content = re.sub(pattern, '', new_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Leere Zeilen entfernen
        for pattern in empty_row_patterns:
            matches = re.findall(pattern, new_content, re.DOTALL | re.IGNORECASE)
            if matches:
                print(f"🗑️  Entferne {len(matches)} leere Zeile(n)")
                removed_count += len(matches)
            new_content = re.sub(pattern, '', new_content, flags=re.DOTALL | re.IGNORECASE)
        
        if removed_count == 0:
            print("✨ Tabelle ist bereits sauber - keine Bereinigung nötig!")
            return True
        
        # Seite aktualisieren
        print(f"💾 Aktualisiere Seite... ({removed_count} Einträge entfernt)")
        success = confluence_sso.update_page("165485055", "RACOON Publikationen", new_content, current_version)
        
        if success:
            print("✅ Bereinigung erfolgreich abgeschlossen!")
            # Backup nach Änderungen erstellen
            confluence_sso.create_backup(new_content, "racoon_publications_after_quick_cleanup")
            return True
        else:
            print("❌ Fehler beim Speichern der Änderungen")
            return False
            
    except Exception as e:
        print(f"❌ Fehler bei der Bereinigung: {e}")
        return False

def main():
    """Hauptfunktion"""
    print("🚀 RACOON Publikationen - Schnell-Bereinigung")
    print("Entfernt automatisch TEST-Zeilen und leere Zeilen")
    print()
    
    confirm = input("Bereinigung starten? (J/n): ").strip().lower()
    if confirm == 'n':
        print("Abgebrochen.")
        return
    
    success = quick_cleanup()
    
    if success:
        print("\n🎉 Bereinigung abgeschlossen!")
    else:
        print("\n❌ Bereinigung fehlgeschlagen!")

if __name__ == "__main__":
    main()