#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Confluence Berechtigungs-Diagnose
Testet verschiedene API-Endpunkte um Berechtigungen zu ermitteln
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from confluence_update import get_credentials, Confluence

def diagnose_permissions():
    """Diagnostiziert verfügbare Berechtigungen"""
    
    CONFLUENCE_URL = "https://wms.diz-ag.med.ovgu.de/"
    
    username, password = get_credentials()
    
    if not username or not password:
        print("❌ Keine gültigen Anmeldedaten erhalten!")
        return
    
    try:
        confluence = Confluence(
            url=CONFLUENCE_URL,
            username=username,
            password=password
        )
        
        print(f"🔍 Diagnose der Confluence-Berechtigungen für: {username}")
        print(f"=" * 60)
        
        # Test 1: Spaces auflisten
        print(f"\n1️⃣ Test: Spaces auflisten")
        try:
            spaces = confluence.get_all_spaces(start=0, limit=25)
            print(f"   ✅ Erfolgreich: {len(spaces.get('results', []))} Spaces gefunden")
            
            accessible_spaces = []
            for space in spaces.get('results', []):
                space_key = space['key']
                space_name = space['name']
                
                # Test Zugriff auf jeden Space
                print(f"\n   🔎 Teste Space: {space_name} ({space_key})")
                
                try:
                    # Versuche Space-Details zu laden
                    space_detail = confluence.get_space(space_key)
                    print(f"      ✅ Space-Details: OK")
                    
                    try:
                        # Versuche Seiten zu laden  
                        pages = confluence.get_all_pages_from_space(
                            space_key, 
                            start=0, 
                            limit=1
                        )
                        print(f"      ✅ Seiten-Zugriff: OK ({len(pages)} Seite(n) sichtbar)")
                        accessible_spaces.append({
                            'key': space_key,
                            'name': space_name,
                            'pages_count': len(pages)
                        })
                        
                    except Exception as e:
                        print(f"      ❌ Seiten-Zugriff: {str(e)[:50]}...")
                        
                except Exception as e:
                    print(f"      ❌ Space-Details: {str(e)[:50]}...")
                    
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
        
        # Test 2: Eigene Benutzerinfo
        print(f"\n2️⃣ Test: Benutzerinformationen")
        try:
            user_info = confluence.get_current_user()
            print(f"   ✅ Benutzer: {user_info.get('displayName', 'N/A')}")
            print(f"   📧 E-Mail: {user_info.get('email', 'N/A')}")
            print(f"   🔑 Username: {user_info.get('username', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
        
        # Test 3: Suchfunktion
        print(f"\n3️⃣ Test: Suchfunktion")
        try:
            # Einfache CQL-Suche
            search_results = confluence.cql(
                'type = "page"',
                limit=5
            )
            pages_found = len(search_results.get('results', []))
            print(f"   ✅ Suche erfolgreich: {pages_found} Seiten gefunden")
            
            if pages_found > 0:
                print(f"   📄 Beispiel-Seiten:")
                for result in search_results['results'][:3]:
                    print(f"      - {result.get('title', 'N/A')} (Space: {result.get('space', {}).get('key', 'N/A')})")
                    
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
        
        # Test 4: Spezifische Seiten-Suche
        print(f"\n4️⃣ Test: Publikations-Seiten suchen")
        try:
            pub_search = confluence.cql(
                'title ~ "publikation" OR title ~ "publication"',
                limit=10
            )
            pub_count = len(pub_search.get('results', []))
            print(f"   ✅ Publikations-Seiten gefunden: {pub_count}")
            
            for result in pub_search.get('results', []):
                title = result.get('title', 'N/A')
                space_key = result.get('space', {}).get('key', 'N/A')
                page_id = result.get('id', 'N/A')
                print(f"      📚 {title} (ID: {page_id}, Space: {space_key})")
                
                # Teste ob das unsere Zielseite ist
                if str(page_id) == "165485055":
                    print(f"         🎯 DAS IST UNSERE ZIELSEITE!")
                    
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
        
        # Zusammenfassung
        print(f"\n" + "=" * 60)
        print(f"📊 ZUSAMMENFASSUNG:")
        
        if 'accessible_spaces' in locals():
            print(f"✅ Zugängliche Spaces: {len(accessible_spaces)}")
            for space in accessible_spaces:
                print(f"   - {space['name']} ({space['key']}) - {space['pages_count']} Seite(n)")
        
        # Empfehlungen
        print(f"\n💡 EMPFEHLUNGEN:")
        print(f"1. Kontaktieren Sie Ihren Confluence-Administrator")
        print(f"2. Bitten Sie um Leseberechtigung für den RACOON Space")
        print(f"3. Prüfen Sie, ob Sie Mitglied der richtigen Gruppen sind")
        print(f"4. Versuchen Sie, sich über den Browser anzumelden")
        
    except Exception as e:
        print(f"❌ Allgemeiner Fehler: {e}")

def main():
    """Hauptfunktion"""
    print("=== Confluence Berechtigungs-Diagnose ===")
    diagnose_permissions()

if __name__ == "__main__":
    main()