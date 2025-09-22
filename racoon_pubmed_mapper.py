#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RACOON-PubMed Schema Mapping
Definiert die Konvertierung zwischen PubMed-Daten und RACOON-Tabellenformat
"""

class RacoonPubMedMapper:
    """Mapping zwischen PubMed und RACOON Publikationsformat"""
    
    def __init__(self):
        self.month_mapping = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
            'January': '01', 'February': '02', 'March': '03', 'April': '04',
            'May': '05', 'June': '06', 'July': '07', 'August': '08',
            'September': '09', 'October': '10', 'November': '11', 'December': '12'
        }
        
        # RACOON-spezifische Standorte
        self.racoon_standorte = [
            "UK Jena", "UK Magdeburg", "UK Dresden", "UK Leipzig",
            "UK Berlin", "UK Hamburg", "UK München", "UK Köln",
            "UK Düsseldorf", "UK Frankfurt", "UK Heidelberg"
        ]
    
    def pubmed_to_racoon(self, pubmed_data, nummer, standort="TBD", foerder_num="AUTO"):
        """
        Konvertiert PubMed-Publikationsdaten in RACOON-Tabellenformat
        
        Args:
            pubmed_data: Dict mit PubMed-Daten
            nummer: Fortlaufende Nummer für RACOON-Tabelle
            standort: RACOON-Standort (falls bekannt)
            foerder_num: Fördernummer (AUTO für automatische Generierung)
        
        Returns:
            Dict mit RACOON-formatierten Daten
        """
        
        # 1. Nummer (fortlaufend)
        racoon_nummer = str(nummer)
        
        # 2. Jahr/Monat formatieren
        racoon_jahr_monat = self._format_year_month(
            pubmed_data.get('year', 'N/A'),
            pubmed_data.get('month', 'N/A')
        )
        
        # 3. Standort (manuell oder aus Affiliation ableiten)
        racoon_standort = self._determine_standort(pubmed_data, standort)
        
        # 4. Personen (Autoren formatieren)
        racoon_personen = self._format_authors(pubmed_data.get('authors', []))
        
        # 5. Förderhinweis
        racoon_foerderhinweis = self._format_foerderhinweis(foerder_num, nummer)
        
        # 6. PubMed DOI (Titel + Links)
        racoon_pubmed_doi = self._format_pubmed_doi_field(pubmed_data)
        
        return {
            'nummer': racoon_nummer,
            'jahr_monat': racoon_jahr_monat,
            'standort': racoon_standort,
            'personen': racoon_personen,
            'foerderhinweis': racoon_foerderhinweis,
            'pubmed_doi': racoon_pubmed_doi,
            '_metadata': {
                'original_pmid': pubmed_data.get('pmid', 'N/A'),
                'original_doi': pubmed_data.get('doi', 'N/A'),
                'journal': pubmed_data.get('journal', 'N/A')
            }
        }
    
    def _format_year_month(self, year, month):
        """Formatiert Jahr/Monat im RACOON-Format (YYYY/MM)"""
        if year == 'N/A':
            return "????/??"
        
        if month == 'N/A':
            return f"{year}/??"
        
        # Monat konvertieren
        month_num = self.month_mapping.get(month, month)
        
        # Falls schon numerisch
        if month_num.isdigit() and len(month_num) <= 2:
            month_num = month_num.zfill(2)
        else:
            month_num = "??"
        
        return f"{year}/{month_num}"
    
    def _determine_standort(self, pubmed_data, provided_standort):
        """Bestimmt RACOON-Standort aus Daten oder nutzt vorgegebenen"""
        if provided_standort != "TBD":
            return provided_standort
        
        # TODO: Affiliation-basierte Standort-Erkennung
        # Hier könnte man aus den Autor-Affiliationen den Standort ableiten
        return "TBD"
    
    def _format_authors(self, authors):
        """Formatiert Autorenliste im RACOON-Format"""
        if not authors:
            return "N/A"
        
        # RACOON nutzt: "Nachname Initialen, Nachname Initialen, ..."
        formatted_authors = []
        for author in authors:
            # Author ist bereits im Format "Lastname F" 
            formatted_authors.append(author)
        
        return ", ".join(formatted_authors)
    
    def _format_foerderhinweis(self, foerder_num, nummer):
        """Formatiert Förderhinweis"""
        if foerder_num == "AUTO":
            # Automatische Generierung basierend auf Nummer
            auto_num = 70000 + int(nummer)  # Basierend auf beobachtetes Muster
            return f"JA {auto_num}"
        
        return f"JA {foerder_num}"
    
    def _format_pubmed_doi_field(self, pubmed_data):
        """Formatiert die PubMed DOI Spalte mit Titel und Links"""
        title = pubmed_data.get('title', 'N/A')
        doi = pubmed_data.get('doi', 'N/A')
        pmid = pubmed_data.get('pmid', 'N/A')
        
        # Basis: Titel
        result = title
        
        # DOI hinzufügen (wenn vorhanden)
        if doi != 'N/A':
            result += f". DOI: {doi}"
        
        # PubMed Link hinzufügen
        if pmid != 'N/A':
            result += f" &lt;https://pubmed.ncbi.nlm.nih.gov/{pmid}/&gt;"
        
        return result
    
    def validate_racoon_entry(self, racoon_data):
        """Validiert RACOON-Eintrag auf Vollständigkeit"""
        required_fields = ['nummer', 'jahr_monat', 'standort', 'personen', 'foerderhinweis', 'pubmed_doi']
        
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Pflichtfelder prüfen
        for field in required_fields:
            if field not in racoon_data or not racoon_data[field]:
                validation_result['errors'].append(f"Fehlendes Feld: {field}")
                validation_result['valid'] = False
        
        # Spezifische Validierungen
        if racoon_data.get('standort') == 'TBD':
            validation_result['warnings'].append("Standort muss manuell gesetzt werden")
        
        if '????' in racoon_data.get('jahr_monat', ''):
            validation_result['warnings'].append("Unvollständiges Datum")
        
        if racoon_data.get('personen') == 'N/A':
            validation_result['warnings'].append("Keine Autoren gefunden")
        
        return validation_result

def demo_mapping():
    """Demo der Mapping-Funktionalität"""
    print("🧪 RACOON-PubMed Schema Mapping Demo")
    print("=" * 50)
    
    # Beispiel PubMed-Daten
    example_pubmed = {
        'pmid': '12345678',
        'title': 'COVID-19 chest CT findings in pediatric patients',
        'authors': ['Schmidt M', 'Müller K', 'Wagner S'],
        'journal': 'European Radiology',
        'year': '2023',
        'month': 'Mar',
        'doi': '10.1007/s00330-023-09234-x',
        'abstract': 'This study analyzes chest CT findings...'
    }
    
    # Mapper erstellen
    mapper = RacoonPubMedMapper()
    
    # Konvertierung
    racoon_entry = mapper.pubmed_to_racoon(
        example_pubmed, 
        nummer=63,  # Nächste Nummer in RACOON-Tabelle
        standort="UK Magdeburg"
    )
    
    print("📊 Konvertierungs-Beispiel:")
    print("-" * 30)
    print(f"📚 PMID: {example_pubmed['pmid']}")
    print(f"📖 Titel: {example_pubmed['title']}")
    print(f"👥 Autoren: {example_pubmed['authors']}")
    print(f"📅 Datum: {example_pubmed['year']}/{example_pubmed['month']}")
    
    print("\n➡️ RACOON Format:")
    print("-" * 30)
    for field, value in racoon_entry.items():
        if not field.startswith('_'):
            print(f"  {field}: {value}")
    
    # Validierung
    validation = mapper.validate_racoon_entry(racoon_entry)
    print(f"\n✅ Validierung: {'Erfolgreich' if validation['valid'] else 'Fehlgeschlagen'}")
    
    if validation['warnings']:
        print("⚠️ Warnungen:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
    
    if validation['errors']:
        print("❌ Fehler:")
        for error in validation['errors']:
            print(f"  - {error}")

if __name__ == "__main__":
    demo_mapping()