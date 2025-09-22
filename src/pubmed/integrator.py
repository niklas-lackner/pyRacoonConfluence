#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON PubMed Integration Tool
Vollständiges Tool für automatische Publikations-Discovery und RACOON-Integration
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent))

from core.confluence_sso import ConfluenceSSO
from pubmed.api_client import PubMedExplorer
from pubmed.schema_mapper import RacoonPubMedMapper
from pubmed.search_strategy import RacoonSearchStrategy
from core.confluence_sso import ConfluenceSSO
from pubmed.api_client import PubMedExplorer
from pubmed.schema_mapper import RacoonPubMedMapper
from pubmed.search_strategy import RacoonSearchStrategy

class RacoonPubMedIntegrator:
    """Vollständige PubMed-RACOON Integration"""
    
    def __init__(self):
        self.confluence_sso = ConfluenceSSO("https://wms.diz-ag.med.ovgu.de/")
        self.pubmed = PubMedExplorer()
        self.mapper = RacoonPubMedMapper()
        self.search_strategy = RacoonSearchStrategy()
        
        # Konfiguration
        self.page_id = "165485055"  # RACOON Publikationen Seite
        self.dry_run = True  # Sicherheit: erst mal nur Simulation
        
    def load_saved_cookies(self):
        """Lädt gespeicherte Cookies"""
        try:
            with open('config/confluence_credentials.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('cookies', '')
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return None
    
    def authenticate(self):
        """Authentifizierung mit Confluence"""
        print("🔑 Confluence Authentifizierung...")
        
        cookie_header = self.load_saved_cookies()
        if not cookie_header:
            cookie_header = input("🔑 Cookies eingeben: ").strip()
        
        if not self.confluence_sso.login_with_cookies(cookie_header):
            print("❌ Authentication fehlgeschlagen!")
            return False
        
        print("✅ Confluence authentifiziert!")
        return True
    
    def get_current_table_info(self):
        """Analysiert aktuelle RACOON-Tabelle"""
        print("📊 Analysiere aktuelle RACOON-Tabelle...")
        
        try:
            page = self.confluence_sso.get_page(self.page_id, "body.storage,version")
            content = page['body']['storage']['value']
            
            # Backup erstellen
            self.confluence_sso.create_backup(content, "racoon_publications_pubmed_integration")
            
            # Tabellen-Info extrahieren
            import re
            tr_pattern = r'<tr[^>]*>(.*?)</tr>'
            all_rows = re.findall(tr_pattern, content, re.DOTALL)
            
            data_rows = all_rows[1:] if len(all_rows) > 1 else []  # Ohne Header
            
            # Letzte Nummer finden
            last_number = 0
            for row in data_rows:
                td_pattern = r'<td[^>]*>(.*?)</td>'
                cells = re.findall(td_pattern, row, re.DOTALL)
                if cells:
                    first_cell = re.sub(r'<[^>]+>', '', cells[0]).strip()
                    if first_cell.isdigit():
                        last_number = max(last_number, int(first_cell))
            
            print(f"✅ Aktuelle Tabelle: {len(data_rows)} Publikationen")
            print(f"📈 Höchste Nummer: {last_number}")
            
            return {
                'content': content,
                'version': page['version']['number'],
                'total_publications': len(data_rows),
                'next_number': last_number + 1
            }
            
        except Exception as e:
            print(f"❌ Fehler beim Laden der Tabelle: {e}")
            return None
    
    def discover_new_publications(self, max_per_query=5):
        """Entdeckt neue RACOON-relevante Publikationen"""
        print("🔍 Suche nach neuen RACOON-Publikationen...")
        
        # Strategische Suche ausführen
        all_publications = []
        queries = self.search_strategy.build_racoon_search_queries()
        
        # Beschränke auf wichtigste Queries für Demo
        priority_queries = [q for q in queries if q.get('priority') == 'high'][:3]
        
        print(f"📋 Führe {len(priority_queries)} prioritäre Suchen durch...")
        
        seen_pmids = set()
        
        for i, query_config in enumerate(priority_queries, 1):
            query = query_config['query']
            print(f"\n🔍 Suche {i}/{len(priority_queries)}: {query[:60]}...")
            
            try:
                pmids = self.pubmed.search_pubmed(query, max_per_query)
                
                if pmids:
                    publications = self.pubmed.get_publication_details(pmids)
                    
                    # Duplikate filtern
                    new_pubs = []
                    for pub in publications:
                        if pub['pmid'] not in seen_pmids:
                            seen_pmids.add(pub['pmid'])
                            pub['_search_info'] = query_config
                            new_pubs.append(pub)
                    
                    all_publications.extend(new_pubs)
                    print(f"✅ Neue Publikationen: {len(new_pubs)}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Suchfehler: {e}")
        
        print(f"\n🎉 Discovery abgeschlossen: {len(all_publications)} Publikationen gefunden")
        return all_publications
    
    def filter_and_score_publications(self, publications, min_score=60):
        """Filtert und bewertet Publikationen für RACOON-Relevanz"""
        print(f"📊 Bewerte {len(publications)} Publikationen...")
        
        # Relevanz-Scores berechnen
        for pub in publications:
            score = self.search_strategy._calculate_racoon_relevance(pub)
            pub['_relevance_score'] = score
        
        # Nach Score sortieren
        publications.sort(key=lambda x: x['_relevance_score'], reverse=True)
        
        # Filtern
        relevant_pubs = [p for p in publications if p['_relevance_score'] >= min_score]
        
        print(f"✅ Relevante Publikationen (Score >= {min_score}): {len(relevant_pubs)}")
        
        # Top-Ergebnisse anzeigen
        print("\n🏆 Top 5 Kandidaten:")
        for i, pub in enumerate(relevant_pubs[:5], 1):
            print(f"  {i}. [{pub['_relevance_score']}%] {pub['title'][:60]}...")
            print(f"     Autoren: {', '.join(pub['authors'][:3])}...")
            print(f"     Jahr: {pub['year']}, PMID: {pub['pmid']}")
        
        return relevant_pubs
    
    def convert_to_racoon_format(self, publications, start_number):
        """Konvertiert Publikationen ins RACOON-Format"""
        print(f"🔄 Konvertiere {len(publications)} Publikationen...")
        
        racoon_entries = []
        
        for i, pub in enumerate(publications):
            try:
                racoon_entry = self.mapper.pubmed_to_racoon(
                    pub,
                    nummer=start_number + i,
                    standort="TBD",  # Manuell zu bestimmen
                    foerder_num="AUTO"
                )
                
                # Zusätzliche Metadaten
                racoon_entry['_metadata'].update({
                    'relevance_score': pub['_relevance_score'],
                    'search_info': pub.get('_search_info', {}),
                    'discovery_date': datetime.now().isoformat(),
                    'auto_generated': True
                })
                
                # Validierung
                validation = self.mapper.validate_racoon_entry(racoon_entry)
                racoon_entry['_validation'] = validation
                
                racoon_entries.append(racoon_entry)
                
            except Exception as e:
                print(f"⚠️ Konvertierungsfehler für PMID {pub.get('pmid', 'N/A')}: {e}")
        
        print(f"✅ Konvertiert: {len(racoon_entries)} Einträge")
        return racoon_entries
    
    def preview_table_additions(self, racoon_entries):
        """Zeigt Vorschau der Tabellen-Ergänzungen"""
        print(f"\n📋 Vorschau: {len(racoon_entries)} neue Einträge")
        print("=" * 80)
        
        for i, entry in enumerate(racoon_entries, 1):
            print(f"\n📄 Eintrag {i}:")
            print(f"  📊 Nummer: {entry['nummer']}")
            print(f"  📅 Jahr/Monat: {entry['jahr_monat']}")
            print(f"  🏥 Standort: {entry['standort']}")
            print(f"  👥 Personen: {entry['personen'][:60]}...")
            print(f"  💰 Förderhinweis: {entry['foerderhinweis']}")
            print(f"  🔗 PubMed DOI: {entry['pubmed_doi'][:80]}...")
            print(f"  🎯 Relevanz: {entry['_metadata']['relevance_score']}%")
            
            # Validierung anzeigen
            validation = entry['_validation']
            if validation['warnings']:
                print(f"  ⚠️ Warnungen: {', '.join(validation['warnings'])}")
            if validation['errors']:
                print(f"  ❌ Fehler: {', '.join(validation['errors'])}")
    
    def generate_table_html(self, racoon_entries):
        """Generiert HTML-Tabellenzeilen für neue Einträge"""
        html_rows = []
        
        for entry in racoon_entries:
            # Escape HTML-Zeichen
            def escape_html(text):
                return (text.replace('&', '&amp;')
                           .replace('<', '&lt;')
                           .replace('>', '&gt;')
                           .replace('"', '&quot;'))
            
            # Tabellenzeile erstellen
            row_html = f"""<tr>
<td>{escape_html(entry['nummer'])}</td>
<td>{escape_html(entry['jahr_monat'])}</td>
<td>{escape_html(entry['standort'])}</td>
<td>{escape_html(entry['personen'])}</td>
<td>{escape_html(entry['foerderhinweis'])}</td>
<td>{entry['pubmed_doi']}</td>
</tr>"""
            
            html_rows.append(row_html)
        
        return html_rows
    
    def simulate_integration(self, racoon_entries, current_table_info):
        """Simuliert die Integration ohne echte Änderungen"""
        print(f"\n🧪 SIMULATION: Integration von {len(racoon_entries)} Publikationen")
        print("-" * 60)
        
        # HTML generieren
        new_rows_html = self.generate_table_html(racoon_entries)
        
        print(f"✅ HTML-Zeilen generiert: {len(new_rows_html)}")
        print(f"📊 Neue Tabellengröße: {current_table_info['total_publications'] + len(racoon_entries)} Publikationen")
        
        # Beispiel-HTML anzeigen
        if new_rows_html:
            print(f"\n📄 Beispiel HTML (erste Zeile):")
            print(new_rows_html[0])
        
        return new_rows_html
    
    def run_full_integration(self, dry_run=True):
        """Führt die komplette Integration aus"""
        print("🚀 RACOON PubMed Integration")
        print("=" * 50)
        print(f"🛡️ Modus: {'SIMULATION' if dry_run else 'LIVE INTEGRATION'}")
        
        # 1. Authentifizierung
        if not self.authenticate():
            return False
        
        # 2. Aktuelle Tabelle analysieren
        table_info = self.get_current_table_info()
        if not table_info:
            return False
        
        # 3. Neue Publikationen entdecken
        new_publications = self.discover_new_publications(max_per_query=3)  # Für Demo weniger
        if not new_publications:
            print("ℹ️ Keine neuen Publikationen gefunden")
            return True
        
        # 4. Filtern und bewerten
        relevant_pubs = self.filter_and_score_publications(new_publications, min_score=60)
        if not relevant_pubs:
            print("ℹ️ Keine relevanten Publikationen gefunden")
            return True
        
        # 5. RACOON-Format konvertieren
        racoon_entries = self.convert_to_racoon_format(relevant_pubs, table_info['next_number'])
        
        # 6. Vorschau
        self.preview_table_additions(racoon_entries)
        
        # 7. Integration (simuliert oder echt)
        if dry_run:
            html_rows = self.simulate_integration(racoon_entries, table_info)
            print("\n✅ Simulation abgeschlossen!")
            print("💡 Für echte Integration: dry_run=False setzen")
        else:
            # TODO: Echte Integration implementieren
            print("🚧 Live-Integration noch nicht implementiert (Sicherheit)")
        
        return True

def main():
    """Hauptfunktion"""
    integrator = RacoonPubMedIntegrator()
    
    print("📚 RACOON PubMed Integration Tool")
    print("=" * 50)
    
    # Sicherheitsmodus: Nur Simulation
    success = integrator.run_full_integration(dry_run=True)
    
    if success:
        print("\n🎉 Integration erfolgreich!")
    else:
        print("\n❌ Integration fehlgeschlagen!")

if __name__ == "__main__":
    main()