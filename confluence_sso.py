#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Confluence SSO Session Authentifizierung
Verwendet Browser-ähnliche Session-basierte Anmeldung
"""

import sys
import requests
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs
from datetime import datetime
import re

class ConfluenceSSO:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/') + '/'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def manual_login_instructions(self):
        """Anweisungen für manuellen Login"""
        print("🔐 SSO-Authentifizierung erforderlich!")
        print("=" * 50)
        print("Da Ihr Confluence SSO verwendet, müssen Sie sich manuell anmelden:")
        print()
        print("1. Öffnen Sie Ihren Browser")
        print("2. Gehen Sie zu: https://wms.diz-ag.med.ovgu.de")
        print("3. Loggen Sie sich ein über:")
        print("   - OpenID SSO OVGU und externe User")
        print("   - MII-MIRACUM Standortnutzer") 
        print("   - MIRACUM Universitätsklinikum Erlangen")
        print("   - Datenintegrationszentrum (DIZ)")
        print("   - lacknens + Passwort")
        print()
        print("4. Nach erfolgreichem Login öffnen Sie die Entwicklertools (F12)")
        print("5. Gehen Sie zum 'Network' Tab")
        print("6. Besuchen Sie: https://wms.diz-ag.med.ovgu.de/rest/api/space")
        print("7. Kopieren Sie die 'Cookie' Header aus dem Request")
        print()
        print("Der Cookie-Header sieht etwa so aus:")
        print("Cookie: JSESSIONID=ABC123...; seraph.confluence=XYZ789...")
        print()
        return input("Geben Sie den vollständigen Cookie-Header ein: ").strip()
    
    def login_with_cookies(self, cookie_header):
        """Login mit Browser-Cookies"""
        try:
            # Parse Cookie-Header
            cookies = {}
            if cookie_header.startswith('Cookie: '):
                cookie_header = cookie_header[8:]  # Entferne "Cookie: "
            
            # Parse Cookies
            for cookie in cookie_header.split(';'):
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    cookies[name] = value
            
            # Setze Cookies in Session
            for name, value in cookies.items():
                self.session.cookies.set(name, value)
            
            print(f"🔑 Cookies gesetzt: {list(cookies.keys())}")
            
            # Teste API-Zugriff
            response = self.session.get(f"{self.base_url}rest/api/space")
            
            if response.status_code == 200:
                print("✅ SSO-Login erfolgreich!")
                return True
            else:
                print(f"❌ API-Test fehlgeschlagen: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim Cookie-Login: {e}")
            return False
    
    def get_spaces(self):
        """Hole alle Spaces"""
        response = self.session.get(f"{self.base_url}rest/api/space")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API Error: {response.status_code}")
    
    def get_page(self, page_id, expand=None):
        """Hole eine spezifische Seite"""
        url = f"{self.base_url}rest/api/content/{page_id}"
        if expand:
            url += f"?expand={expand}"
        
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Page API Error: {response.status_code} - {response.text}")
    
    def update_page(self, page_id, title, content, version):
        """Aktualisiere eine Seite"""
        url = f"{self.base_url}rest/api/content/{page_id}"
        
        data = {
            "version": {"number": version + 1},
            "title": title,
            "type": "page",
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }
        
        response = self.session.put(
            url,
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Update Error: {response.status_code} - {response.text}")
    
    def create_backup(self, content, prefix="confluence_backup"):
        """Erstellt ein zeitgestempeltes Backup im backups/ Ordner"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        
        backup_file = backup_dir / f"{prefix}_{timestamp}.html"
        
        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"💾 Backup gespeichert: {backup_file}")
        return backup_file

def main():
    """Hauptfunktion für SSO-basierte Confluence-Nutzung"""
    print("=== Confluence SSO Session Manager ===")
    
    confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--manual-login":
        # Manueller Login mit Browser-Cookies
        cookie_header = confluence_sso.manual_login_instructions()
        
        if cookie_header:
            if confluence_sso.login_with_cookies(cookie_header):
                print("\n📊 Teste API-Zugriff...")
                
                try:
                    spaces = confluence_sso.get_spaces()
                    print(f"✅ Erfolgreich! {len(spaces.get('results', []))} Spaces gefunden")
                    
                    # Teste RACOON Publikationsseite
                    print(f"\n🎯 Teste RACOON Publikationsseite (ID: 165485055)...")
                    try:
                        page = confluence_sso.get_page("165485055", "body.storage,version")
                        print(f"✅ Seite geladen: {page['title']}")
                        print(f"Version: {page['version']['number']}")
                        print(f"Content-Länge: {len(page['body']['storage']['value'])} Zeichen")
                        
                        # Backup erstellen
                        confluence_sso.create_backup(page['body']['storage']['value'], "racoon_publications_sso")
                        
                    except Exception as e:
                        print(f"❌ Seiten-Zugriff fehlgeschlagen: {e}")
                        
                except Exception as e:
                    print(f"❌ API-Zugriff fehlgeschlagen: {e}")
            else:
                print("❌ Cookie-basierter Login fehlgeschlagen")
        else:
            print("❌ Kein Cookie-Header eingegeben")
    
    else:
        print("📋 Verfügbare Optionen:")
        print("  python confluence_sso.py --manual-login")
        print()
        print("💡 Hinweis: Da Ihr Confluence SSO verwendet, können Sie nicht")
        print("   direkt mit Username/Passwort auf die API zugreifen.")
        print("   Verwenden Sie --manual-login für Cookie-basierte Authentifizierung.")

if __name__ == "__main__":
    main()