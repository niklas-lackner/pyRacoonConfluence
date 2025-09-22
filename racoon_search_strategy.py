#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON PubMed Search Strategy
Intelligente Suchstrategie für RACOON-relevante Publikationen
"""

import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from pubmed_explorer import PubMedExplorer
from racoon_pubmed_mapper import RacoonPubMedMapper

class RacoonSearchStrategy:
    """Intelligente Suchstrategie für RACOON-relevante Publikationen"""
    
    def __init__(self):
        self.pubmed = PubMedExplorer()
        self.mapper = RacoonPubMedMapper()
        
        # RACOON-spezifische Suchkriterien
        self.racoon_keywords = [
            "COVID-19", "SARS-CoV-2", "coronavirus",
            "chest CT", "lung imaging", "pulmonary",
            "radiology", "radiological", "imaging",
            "RACOON", "chest X-ray", "pneumonia"
        ]
        
        # Bekannte RACOON-Autoren (aus der Analyse)
        self.racoon_authors = [
            "Surov A", "Pech M", "Haag F", "Teichräber U",
            "Thormann M", "Kardas H", "Meyer HJ", "Güttler F",
            "Lassen-Schmidt B", "Krämer M", "Renz D"
        ]
        
        # RACOON-Institutionen
        self.racoon_institutions = [
            "University Hospital Magdeburg", "UK Magdeburg",
            "University Hospital Jena", "UK Jena",
            "Otto-von-Guericke University", "Friedrich Schiller University"
        ]
    
    def build_racoon_search_queries(self):
        """Erstellt optimierte Suchqueries für RACOON-Publikationen"""
        queries = []
        
        # 1. Keyword-basierte Suchen
        keyword_combinations = [
            "(COVID-19) AND (radiology) AND (chest CT)",
            "(SARS-CoV-2) AND (imaging) AND (lung)",
            "(coronavirus) AND (chest X-ray)",
            "(COVID-19) AND (pneumonia) AND (CT)",
            "RACOON study",
            "(COVID-19) AND (artificial intelligence) AND (radiology)"
        ]
        
        for query in keyword_combinations:
            queries.append({
                'query': query,
                'type': 'keyword',
                'priority': 'high',
                'expected_results': 50
            })
        
        # 2. Autor-basierte Suchen (für bekannte RACOON-Forscher)
        for author in self.racoon_authors[:5]:  # Top 5 Autoren
            author_query = f'("{author}"[Author]) AND (COVID-19 OR radiology)'
            queries.append({
                'query': author_query,
                'type': 'author',
                'priority': 'medium',
                'expected_results': 20,
                'author': author
            })
        
        # 3. Institutions-basierte Suchen
        institution_queries = [
            '("Otto-von-Guericke University"[Affiliation]) AND (COVID-19)',
            '("University Hospital Magdeburg"[Affiliation]) AND (radiology)',
            '("Friedrich Schiller University"[Affiliation]) AND (imaging)'
        ]
        
        for query in institution_queries:
            queries.append({
                'query': query,
                'type': 'institution',
                'priority': 'medium',
                'expected_results': 30
            })
        
        # 4. Zeitraum-spezifische Suchen (COVID-19 Periode)
        time_queries = [
            '(COVID-19) AND (radiology) AND ("2020"[Date - Publication] : "2025"[Date - Publication])',
            '(chest CT) AND (COVID-19) AND ("2020/03"[Date - Publication] : "2025/12"[Date - Publication])'
        ]
        
        for query in time_queries:
            queries.append({
                'query': query,
                'type': 'temporal',
                'priority': 'high',
                'expected_results': 100
            })
        
        return queries
    
    def execute_search_strategy(self, max_results_per_query=10):
        """Führt die komplette Suchstrategie aus"""
        print("🎯 RACOON PubMed Suchstrategie")
        print("=" * 50)
        
        queries = self.build_racoon_search_queries()
        all_publications = []
        seen_pmids = set()
        
        print(f"📋 Geplante Suchen: {len(queries)}")
        
        for i, search_config in enumerate(queries, 1):
            query = search_config['query']
            search_type = search_config['type']
            priority = search_config['priority']
            
            print(f"\n🔍 Suche {i}/{len(queries)} [{search_type.upper()}] {priority}")
            print(f"Query: {query[:80]}...")
            
            try:
                # PubMed Suche
                pmids = self.pubmed.search_pubmed(query, max_results_per_query)
                
                if pmids:
                    # Details laden
                    publications = self.pubmed.get_publication_details(pmids)
                    
                    # Duplikate filtern
                    new_publications = []
                    for pub in publications:
                        if pub['pmid'] not in seen_pmids:
                            seen_pmids.add(pub['pmid'])
                            new_publications.append(pub)
                            
                            # RACOON-Format hinzufügen
                            pub['_search_info'] = {
                                'query_type': search_type,
                                'priority': priority,
                                'query': query
                            }
                    
                    all_publications.extend(new_publications)
                    print(f"✅ Neue Publikationen: {len(new_publications)} (Duplikate: {len(pmids) - len(new_publications)})")
                
                else:
                    print("❌ Keine Ergebnisse")
                
                # Rate limiting
                import time
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Suchfehler: {e}")
        
        print(f"\n🎉 Suchstrategie abgeschlossen!")
        print(f"📊 Gefundene Publikationen: {len(all_publications)}")
        
        return all_publications
    
    def analyze_search_results(self, publications):
        """Analysiert die Suchergebnisse für RACOON-Relevanz"""
        print(f"\n📊 Analyse von {len(publications)} Publikationen")
        print("-" * 50)
        
        # Kategorisierung
        categories = {
            'high_relevance': [],
            'medium_relevance': [],
            'low_relevance': []
        }
        
        for pub in publications:
            relevance_score = self._calculate_racoon_relevance(pub)
            pub['_relevance_score'] = relevance_score
            
            if relevance_score >= 80:
                categories['high_relevance'].append(pub)
            elif relevance_score >= 50:
                categories['medium_relevance'].append(pub)
            else:
                categories['low_relevance'].append(pub)
        
        # Ergebnisse anzeigen
        for category, pubs in categories.items():
            relevance_name = category.replace('_', ' ').title()
            print(f"\n🎯 {relevance_name}: {len(pubs)} Publikationen")
            
            if pubs:
                # Top 3 anzeigen
                for i, pub in enumerate(pubs[:3], 1):
                    print(f"  {i}. [{pub['_relevance_score']}%] {pub['title'][:60]}...")
                    print(f"     Autoren: {', '.join(pub['authors'][:3])}...")
                    print(f"     Jahr: {pub['year']}, Journal: {pub['journal']}")
        
        return categories
    
    def _calculate_racoon_relevance(self, publication):
        """Berechnet RACOON-Relevanz Score (0-100)"""
        score = 0
        
        title = publication.get('title', '').lower()
        abstract = publication.get('abstract', '').lower()
        authors = [a.lower() for a in publication.get('authors', [])]
        journal = publication.get('journal', '').lower()
        
        # COVID-19 Keywords (30 Punkte)
        covid_keywords = ['covid-19', 'sars-cov-2', 'coronavirus', 'covid']
        if any(keyword in title or keyword in abstract for keyword in covid_keywords):
            score += 30
        
        # Imaging Keywords (25 Punkte)
        imaging_keywords = ['ct', 'x-ray', 'chest', 'lung', 'radiology', 'imaging', 'radiological']
        imaging_count = sum(1 for keyword in imaging_keywords if keyword in title or keyword in abstract)
        score += min(25, imaging_count * 8)
        
        # RACOON Autoren (25 Punkte)
        author_matches = 0
        for racoon_author in self.racoon_authors:
            racoon_lastname = racoon_author.split()[0].lower()
            if any(racoon_lastname in author for author in authors):
                author_matches += 1
        score += min(25, author_matches * 15)
        
        # Journal Relevanz (10 Punkte)
        radiology_journals = ['radiology', 'european radiology', 'radiological', 'imaging']
        if any(journal_keyword in journal for journal_keyword in radiology_journals):
            score += 10
        
        # Zeitraum (10 Punkte) - COVID-19 relevant
        year = publication.get('year', '')
        if year in ['2020', '2021', '2022', '2023', '2024', '2025']:
            score += 10
        
        return min(100, score)
    
    def generate_racoon_candidates(self, publications, min_relevance=70):
        """Generiert RACOON-Kandidaten für die Tabelle"""
        candidates = []
        
        for pub in publications:
            if pub.get('_relevance_score', 0) >= min_relevance:
                # RACOON-Format konvertieren
                racoon_entry = self.mapper.pubmed_to_racoon(
                    pub, 
                    nummer=len(candidates) + 63,  # Nächste Nummer nach aktueller Tabelle
                    standort="TBD"  # Manuell zu bestimmen
                )
                
                # Zusätzliche Metadaten
                racoon_entry['_metadata'].update({
                    'relevance_score': pub['_relevance_score'],
                    'search_info': pub.get('_search_info', {}),
                    'recommended': pub['_relevance_score'] >= 80
                })
                
                candidates.append(racoon_entry)
        
        return candidates

def demo_search_strategy():
    """Demo der Suchstrategie"""
    print("🧪 RACOON Suchstrategie Demo")
    print("=" * 50)
    
    strategy = RacoonSearchStrategy()
    
    # Nur erste 3 Queries für Demo
    queries = strategy.build_racoon_search_queries()[:3]
    
    print(f"📋 Demo mit {len(queries)} Suchqueries:")
    for i, query_config in enumerate(queries, 1):
        print(f"  {i}. [{query_config['type']}] {query_config['query'][:60]}...")
    
    # Führe Suche aus (mit weniger Ergebnissen für Demo)
    publications = []
    for query_config in queries:
        try:
            pmids = strategy.pubmed.search_pubmed(query_config['query'], 3)
            if pmids:
                pubs = strategy.pubmed.get_publication_details(pmids)
                publications.extend(pubs)
            import time
            time.sleep(1)
        except Exception as e:
            print(f"Demo-Fehler: {e}")
    
    if publications:
        # Analyse
        categories = strategy.analyze_search_results(publications)
        
        # RACOON-Kandidaten
        candidates = strategy.generate_racoon_candidates(publications, min_relevance=50)
        
        print(f"\n🎯 RACOON-Kandidaten: {len(candidates)}")
        for i, candidate in enumerate(candidates[:3], 1):
            print(f"  {i}. [{candidate['_metadata']['relevance_score']}%] {candidate['pubmed_doi'][:60]}...")

if __name__ == "__main__":
    demo_search_strategy()