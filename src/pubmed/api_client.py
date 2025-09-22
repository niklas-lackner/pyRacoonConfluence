#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PubMed API Explorer - NCBI E-utilities
Testet PubMed API für RACOON Integration
"""

import requests
import xml.etree.ElementTree as ET
import json
from urllib.parse import quote_plus
import time

class PubMedExplorer:
    """PubMed API Explorer für RACOON"""
    
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.email = "your.email@example.com"  # NCBI empfiehlt E-Mail anzugeben
        self.tool = "RACOON-PubMed-Explorer"
        
    def search_pubmed(self, query, max_results=10):
        """Suche in PubMed nach Begriffen"""
        print(f"🔍 Suche nach: '{query}'")
        
        # ESearch - Finde PubMed IDs
        search_url = f"{self.base_url}esearch.fcgi"
        search_params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'email': self.email,
            'tool': self.tool,
            'retmode': 'json'
        }
        
        try:
            response = requests.get(search_url, params=search_params)
            response.raise_for_status()
            
            search_data = response.json()
            pmids = search_data['esearchresult']['idlist']
            
            print(f"✅ Gefunden: {len(pmids)} Publikationen")
            return pmids
            
        except Exception as e:
            print(f"❌ Suchfehler: {e}")
            return []
    
    def get_publication_details(self, pmids):
        """Hole detaillierte Informationen zu PubMed IDs"""
        if not pmids:
            return []
            
        print(f"📖 Lade Details für {len(pmids)} Publikationen...")
        
        # EFetch - Hole Details
        fetch_url = f"{self.base_url}efetch.fcgi"
        fetch_params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'rettype': 'xml',
            'email': self.email,
            'tool': self.tool
        }
        
        try:
            response = requests.get(fetch_url, params=fetch_params)
            response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(response.content)
            publications = []
            
            for article in root.findall('.//PubmedArticle'):
                pub_data = self.parse_article(article)
                if pub_data:
                    publications.append(pub_data)
            
            print(f"✅ Details geladen: {len(publications)} Publikationen")
            return publications
            
        except Exception as e:
            print(f"❌ Detail-Fehler: {e}")
            return []
    
    def parse_article(self, article):
        """Parse einzelne Publikation aus XML"""
        try:
            # PMID
            pmid_elem = article.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else "N/A"
            
            # Titel
            title_elem = article.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else "N/A"
            
            # Autoren
            authors = []
            for author in article.findall('.//Author'):
                lastname = author.find('LastName')
                forename = author.find('ForeName')
                if lastname is not None:
                    name = lastname.text
                    if forename is not None:
                        name = f"{lastname.text} {forename.text[0]}"  # Nur erster Buchstabe
                    authors.append(name)
            
            # Journal & Datum
            journal_elem = article.find('.//Journal/Title')
            journal = journal_elem.text if journal_elem is not None else "N/A"
            
            # Publikationsdatum
            pub_date = article.find('.//PubDate')
            year, month = "N/A", "N/A"
            if pub_date is not None:
                year_elem = pub_date.find('Year')
                month_elem = pub_date.find('Month')
                year = year_elem.text if year_elem is not None else "N/A"
                month = month_elem.text if month_elem is not None else "N/A"
            
            # DOI
            doi = "N/A"
            for article_id in article.findall('.//ArticleId'):
                if article_id.get('IdType') == 'doi':
                    doi = article_id.text
                    break
            
            # Abstract
            abstract_elem = article.find('.//Abstract/AbstractText')
            abstract = abstract_elem.text if abstract_elem is not None else "N/A"
            
            return {
                'pmid': pmid,
                'title': title,
                'authors': authors,
                'journal': journal,
                'year': year,
                'month': month,
                'doi': doi,
                'abstract': abstract[:200] + "..." if len(abstract) > 200 else abstract
            }
            
        except Exception as e:
            print(f"⚠️ Parse-Fehler für Artikel: {e}")
            return None
    
    def demo_search(self):
        """Demo-Suche mit RACOON-relevanten Begriffen"""
        print("🧪 PubMed API Demo für RACOON")
        print("=" * 50)
        
        # Test verschiedene Suchbegriffe
        test_queries = [
            "COVID-19 radiology",
            "RACOON study",
            "(COVID-19) AND (chest CT)",
            "coronavirus imaging"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Test-Suche: {query}")
            print("-" * 30)
            
            # Suche durchführen
            pmids = self.search_pubmed(query, max_results=3)
            
            if pmids:
                # Details laden
                publications = self.get_publication_details(pmids)
                
                # Erste Publikation anzeigen
                if publications:
                    pub = publications[0]
                    print(f"📄 Beispiel-Publikation:")
                    print(f"  📚 PMID: {pub['pmid']}")
                    print(f"  📖 Titel: {pub['title'][:80]}...")
                    print(f"  👥 Autoren: {', '.join(pub['authors'][:3])}...")
                    print(f"  📅 Jahr/Monat: {pub['year']}/{pub['month']}")
                    print(f"  🔗 DOI: {pub['doi']}")
                    print(f"  📄 Journal: {pub['journal']}")
            
            # Rate limiting
            time.sleep(1)
    
    def racoon_format_conversion(self, publication):
        """Konvertiert PubMed-Daten in RACOON-Format"""
        # Autoren formatieren (wie in RACOON)
        authors_racoon = ", ".join(publication['authors'])
        
        # Jahr/Monat formatieren
        year_month = f"{publication['year']}"
        if publication['month'] != "N/A":
            # Monat zu Zahl konvertieren
            month_map = {
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
            }
            month_num = month_map.get(publication['month'][:3], '??')
            year_month = f"{publication['year']}/{month_num}"
        
        # PubMed DOI Spalte
        pubmed_doi = publication['title']
        if publication['doi'] != "N/A":
            pubmed_doi += f". DOI: {publication['doi']}"
        if publication['pmid'] != "N/A":
            pubmed_doi += f" <https://pubmed.ncbi.nlm.nih.gov/{publication['pmid']}/>"
        
        return {
            'jahr_monat': year_month,
            'standort': "TBD",  # Manuell zu setzen
            'personen': authors_racoon,
            'foerderhinweis': "JA [NUM]",  # Automatisch zu generieren
            'pubmed_doi': pubmed_doi
        }

def main():
    """Hauptfunktion - PubMed API Test"""
    explorer = PubMedExplorer()
    explorer.demo_search()

if __name__ == "__main__":
    main()