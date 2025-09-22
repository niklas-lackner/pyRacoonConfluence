#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Publikationen Seite - Spezifisches Update-Skript
Bearbeitet die Seite: Berichtswesen - RACOON - Publikationen
"""

import sys
import os
from pathlib import Path

# Importiere die Funktionen aus dem Haupt-Skript
sys.path.append(str(Path(__file__).parent))
from confluence_update import get_credentials, Confluence

def get_racoon_publications_page():
    """Holt die RACOON Publikationsseite"""
    
    CONFLUENCE_URL = "https://wms.diz-ag.med.ovgu.de/"
    PAGE_ID = "165485055"  # ID aus der URL
    SPACE_KEY = "RACOON"
    
    # Anmeldedaten laden
    username, password = get_credentials()
    
    if not username or not password:
        print("❌ Keine gültigen Anmeldedaten erhalten!")
        return None
    
    try:
        confluence = Confluence(
            url=CONFLUENCE_URL,
            username=username,
            password=password
        )
        
        print(f"📄 Lade Seite: Berichtswesen - RACOON - Publikationen")
        print(f"Page ID: {PAGE_ID}")
        
        # Seite mit vollständigem Inhalt laden
        page = confluence.get_page_by_id(
            PAGE_ID, 
            expand="body.storage,version,space,history,children.page"
        )
        
        print(f"✅ Seite erfolgreich geladen!")
        print(f"Titel: {page['title']}")
        print(f"Space: {page['space']['name']} ({page['space']['key']})")
        print(f"Version: {page['version']['number']}")
        print(f"Zuletzt geändert: {page['version']['when']}")
        print(f"Geändert von: {page['version']['by']['displayName']}")
        
        return page
        
    except Exception as e:
        print(f"❌ Fehler beim Laden der Seite: {e}")
        return None

def analyze_page_content(page):
    """Analysiert den Inhalt der Seite"""
    if not page:
        return
    
    content = page['body']['storage']['value']
    print(f"\n📊 Content-Analyse:")
    print(f"Content-Länge: {len(content)} Zeichen")
    
    # Suche nach Tabellen
    table_count = content.count('<table')
    print(f"Tabellen gefunden: {table_count}")
    
    # Suche nach spezifischen Elementen
    if '<table' in content:
        print("🔍 Tabellen-Details:")
        
        # Einfache Analyse der ersten Tabelle
        table_start = content.find('<table')
        table_end = content.find('</table>', table_start) + 8
        
        if table_start != -1 and table_end != -1:
            first_table = content[table_start:table_end]
            row_count = first_table.count('<tr')
            cell_count = first_table.count('<td') + first_table.count('<th')
            
            print(f"  - Erste Tabelle: {row_count} Zeilen, {cell_count} Zellen")
            
            # Zeige erste paar Zeilen zur Vorschau
            print("\n📋 Tabellen-Vorschau (erste 500 Zeichen):")
            preview = first_table[:500]
            if len(first_table) > 500:
                preview += "..."
            print(preview)
    
    # Speichere Original-Content für Backup
    backup_file = Path("racoon_publications_backup.html")
    with open(backup_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n💾 Backup gespeichert: {backup_file}")

def update_racoon_publications(page, updates):
    """Aktualisiert die RACOON Publikationsseite"""
    
    CONFLUENCE_URL = "https://wms.diz-ag.med.ovgu.de/"
    
    if not page:
        print("❌ Keine Seite zum Aktualisieren!")
        return False
    
    # Anmeldedaten laden
    username, password = get_credentials()
    
    try:
        confluence = Confluence(
            url=CONFLUENCE_URL,
            username=username,
            password=password
        )
        
        # Aktueller Content
        current_content = page['body']['storage']['value']
        updated_content = current_content
        
        # Führe Updates durch
        for old_text, new_text in updates.items():
            if old_text in updated_content:
                updated_content = updated_content.replace(old_text, new_text)
                print(f"✅ Ersetzt: '{old_text[:50]}...' -> '{new_text[:50]}...'")
            else:
                print(f"⚠️  Text nicht gefunden: '{old_text[:50]}...'")
        
        # Nur aktualisieren wenn sich etwas geändert hat
        if updated_content != current_content:
            print(f"\n🔄 Aktualisiere Seite...")
            
            confluence.update_page(
                page_id=page['id'],
                title=page['title'],
                body=updated_content,
                representation='storage',
                minor_edit=True,
                version_comment="Automatisches Update via Python-Skript"
            )
            
            print(f"✅ Seite erfolgreich aktualisiert!")
            return True
        else:
            print(f"ℹ️  Keine Änderungen erforderlich.")
            return True
            
    except Exception as e:
        print(f"❌ Fehler beim Aktualisieren: {e}")
        return False

def main():
    """Hauptfunktion für RACOON Publikationen Updates"""
    print("=== RACOON Publikationen Seite Manager ===")
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--analyze":
            print("📊 Analysiere Seite...")
            page = get_racoon_publications_page()
            analyze_page_content(page)
            
        elif command == "--update":
            print("🔄 Update-Modus...")
            page = get_racoon_publications_page()
            
            if page:
                # Beispiel-Updates (anpassen nach Bedarf)
                updates = {
                    # "Alter Text": "Neuer Text",
                    # "Status: In Arbeit": "Status: Abgeschlossen",
                }
                
                if not updates:
                    print("⚠️  Keine Updates definiert!")
                    print("Bearbeiten Sie das Skript und fügen Sie Updates im 'updates' Dictionary hinzu.")
                else:
                    update_racoon_publications(page, updates)
            
        elif command == "--backup":
            print("💾 Erstelle Backup...")
            page = get_racoon_publications_page()
            if page:
                analyze_page_content(page)  # Das erstellt auch ein Backup
        
        else:
            print(f"❌ Unbekannter Befehl: {command}")
            print("Verfügbare Befehle:")
            print("  --analyze  : Seite analysieren und Struktur anzeigen")
            print("  --update   : Seite aktualisieren")
            print("  --backup   : Backup der Seite erstellen")
    else:
        print("📋 Verfügbare Optionen:")
        print("  python racoon_publications.py --analyze")
        print("  python racoon_publications.py --update")
        print("  python racoon_publications.py --backup")

if __name__ == "__main__":
    main()