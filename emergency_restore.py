#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Publikationen - Notfall-Wiederherstellung
Stellt eine Backup-Version wieder her
"""

import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from confluence_sso import ConfluenceSSO

def restore_backup():
    """Stellt ein Backup wieder her"""
    print("🚨 NOTFALL-WIEDERHERSTELLUNG")
    print("=" * 50)
    
    # Verfügbare Backups anzeigen
    backup_dir = Path("backups")
    backups = sorted([f for f in backup_dir.glob("*.html") if f.name != ".gitkeep"], 
                    key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not backups:
        print("❌ Keine Backups gefunden!")
        return False
    
    print("📁 Verfügbare Backups (neueste zuerst):")
    for i, backup in enumerate(backups[:10]):  # Zeige nur die 10 neuesten
        size = backup.stat().st_size
        print(f"  {i+1}. {backup.name} ({size:,} Bytes)")
    
    # Das VOR-Bereinigung Backup als Standard vorschlagen
    suggested_backup = None
    for backup in backups:
        if "before_quick_cleanup_20250922_163314" in backup.name:
            suggested_backup = backup
            break
    
    if suggested_backup:
        print(f"\n💡 Vorschlag: {suggested_backup.name}")
        choice = input("Dieses Backup verwenden? (J/n): ").strip().lower()
        if choice != 'n':
            selected_backup = suggested_backup
        else:
            try:
                choice = int(input("Backup-Nummer eingeben: ")) - 1
                selected_backup = backups[choice]
            except (ValueError, IndexError):
                print("❌ Ungültige Auswahl!")
                return False
    else:
        try:
            choice = int(input("Backup-Nummer eingeben: ")) - 1
            selected_backup = backups[choice]
        except (ValueError, IndexError):
            print("❌ Ungültige Auswahl!")
            return False
    
    print(f"📖 Lade Backup: {selected_backup.name}")
    
    try:
        # Backup-Inhalt laden
        with open(selected_backup, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        
        print(f"✅ Backup geladen: {len(backup_content):,} Zeichen")
        
        # SSO-Session erstellen
        confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
        
        # Gespeicherte Cookies verwenden
        try:
            import json
            with open('confluence_credentials.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                cookie_header = data.get('cookies', '')
        except:
            cookie_header = input("🔑 Cookies eingeben: ").strip()
        
        if not confluence_sso.login_with_cookies(cookie_header):
            print("❌ Cookie-Login fehlgeschlagen!")
            return False
        
        # Aktuelle Seitenversion laden
        print("📖 Lade aktuelle Seitenversion...")
        page = confluence_sso.get_page("165485055", "body.storage,version")
        current_version = page['version']['number']
        
        print(f"📊 Aktuelle Version: {current_version}")
        
        # Sicherheitsbackup der aktuellen (kaputten) Version erstellen
        confluence_sso.create_backup(page['body']['storage']['value'], "racoon_publications_before_restore")
        
        # Backup wiederherstellen
        print("🔄 Stelle Backup wieder her...")
        success = confluence_sso.update_page("165485055", "RACOON Publikationen", backup_content, current_version)
        
        if success:
            print("✅ Backup erfolgreich wiederhergestellt!")
            print("🔗 URL: https://wms.diz-ag.med.ovgu.de/spaces/RACOON/pages/165485055/")
            return True
        else:
            print("❌ Fehler beim Wiederherstellen!")
            return False
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

def main():
    """Hauptfunktion"""
    print("🚨 RACOON Publikationen - Notfall-Wiederherstellung")
    print("⚠️  ACHTUNG: Dies überschreibt die aktuelle Confluence-Seite!")
    print()
    
    confirm = input("Wiederherstellung starten? (JA/n): ").strip()
    if confirm.upper() != 'JA':
        print("Abgebrochen.")
        return
    
    success = restore_backup()
    
    if success:
        print("\n🎉 Wiederherstellung erfolgreich!")
        print("📋 Überprüfen Sie die Seite in Confluence")
    else:
        print("\n❌ Wiederherstellung fehlgeschlagen!")

if __name__ == "__main__":
    main()