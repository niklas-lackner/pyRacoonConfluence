#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON Space Explorer - Findet verfügbare Seiten und Berechtigungen
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from confluence_update import get_credentials, Confluence

def explore_racoon_space():
    """Erkundet den RACOON Space um verfügbare Seiten zu finden"""
    
    CONFLUENCE_URL = "https://wms.diz-ag.med.ovgu.de/"
    SPACE_KEY = "RACOON"
    
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
        
        print(f"🔍 Erkunde RACOON Space...")
        
        # 1. Space-Details
        space = confluence.get_space(SPACE_KEY)
        print(f"✅ Space: {space['name']} ({space['key']})")
        
        # 2. Alle Seiten im Space
        print(f"\n📋 Suche Seiten im RACOON Space...")
        
        # Hole alle Seiten (mit Pagination)
        start = 0
        limit = 50
        all_pages = []
        
        while True:
            pages = confluence.get_all_pages_from_space(
                SPACE_KEY, 
                start=start, 
                limit=limit,
                expand="version,space,history.lastUpdated"
            )
            
            if not pages:
                break
                
            all_pages.extend(pages)
            print(f"  Geladen: {len(pages)} Seiten (Total: {len(all_pages)})")
            
            if len(pages) < limit:
                break
                
            start += limit
        
        print(f"\n📊 Gefundene Seiten: {len(all_pages)}")
        
        # 3. Suche nach Publikations-relevanten Seiten
        publication_pages = []
        for page in all_pages:
            title = page['title'].lower()
            if any(keyword in title for keyword in ['publikation', 'publication', 'bericht', 'report']):
                publication_pages.append(page)
        
        print(f"\n📚 Publikations-relevante Seiten ({len(publication_pages)}):")
        for page in publication_pages:
            print(f"  - {page['title']} (ID: {page['id']})")
        
        # 4. Zeige alle Seiten (begrenzt auf erste 20)
        print(f"\n📄 Alle Seiten im RACOON Space (erste 20):")
        for i, page in enumerate(all_pages[:20]):
            print(f"  {i+1:2d}. {page['title']} (ID: {page['id']})")
            if i == 19 and len(all_pages) > 20:
                print(f"       ... und {len(all_pages) - 20} weitere Seiten")
        
        # 5. Teste Zugriff auf spezifische Seite
        target_page_id = "165485055"
        print(f"\n🎯 Teste Zugriff auf Zielseite (ID: {target_page_id})...")
        
        # Prüfe ob die Seite in unserer Liste ist
        target_found = False
        for page in all_pages:
            if str(page['id']) == target_page_id:
                print(f"✅ Zielseite gefunden: {page['title']}")
                target_found = True
                
                # Versuche detaillierte Informationen zu laden
                try:
                    detailed_page = confluence.get_page_by_id(
                        target_page_id, 
                        expand="body.storage,version"
                    )
                    print(f"✅ Detailzugriff erfolgreich!")
                    return detailed_page
                    
                except Exception as e:
                    print(f"❌ Kein Detailzugriff: {e}")
                break
        
        if not target_found:
            print(f"⚠️  Zielseite nicht in verfügbaren Seiten gefunden.")
            print(f"Mögliche Ursachen:")
            print(f"  - Seite ist in einem anderen Space")
            print(f"  - Keine Leseberechtigung für diese Seite")
            print(f"  - Seite wurde gelöscht oder verschoben")
        
        return None
        
    except Exception as e:
        print(f"❌ Fehler beim Erkunden des RACOON Space: {e}")
        return None

def search_for_publications():
    """Sucht gezielt nach Publikations-Seiten"""
    
    CONFLUENCE_URL = "https://wms.diz-ag.med.ovgu.de/"
    
    username, password = get_credentials()
    
    try:
        confluence = Confluence(
            url=CONFLUENCE_URL,
            username=username,
            password=password
        )
        
        print(f"🔎 Suche nach 'Publikation' in allen verfügbaren Spaces...")
        
        # Suche in mehreren Spaces
        search_spaces = ["RACOON", "RACOONFORSCHUNG", "RACOON2PUB"]
        
        for space_key in search_spaces:
            print(f"\n📂 Durchsuche Space: {space_key}")
            
            try:
                # Textsuche nach "Publikation"
                results = confluence.cql(
                    f'space = "{space_key}" AND text ~ "publikation"',
                    limit=10
                )
                
                if results['results']:
                    print(f"  Gefunden: {len(results['results'])} Ergebnisse")
                    for result in results['results']:
                        print(f"    - {result['title']} (ID: {result['id']})")
                        print(f"      URL: {result['_links']['webui']}")
                else:
                    print(f"  Keine Treffer für 'publikation'")
                    
            except Exception as e:
                print(f"  ❌ Fehler bei Suche in {space_key}: {e}")
        
    except Exception as e:
        print(f"❌ Fehler bei der Suche: {e}")

def main():
    """Hauptfunktion"""
    print("=== RACOON Space Explorer ===")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--search":
        search_for_publications()
    else:
        page = explore_racoon_space()
        if page:
            print(f"\n✅ Seite erfolgreich geladen und bereit für Updates!")

if __name__ == "__main__":
    main()