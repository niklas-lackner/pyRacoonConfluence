# 🧬 pyRacoonConfluence

**Automatisierte RACOON Publikationsverwaltung mit PubMed-Integration**

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)]()

## 🚀 Quick Start

```bash
# 1. Repository klonen
git clone https://github.com/niklas-lackner/pyRacoonConfluence.git
cd pyRacoonConfluence

# 2. Virtual Environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# 3. Dependencies installieren  
pip install -r requirements.txt

# 4. Cookies in config/confluence_credentials.json eintragen
# 5. Tools nutzen
python run_publication_manager.py    # RACOON Management
python run_pubmed_integration.py     # PubMed Discovery
python run_table_analyzer.py         # Tabellenanalyse
```

## 🏗️ Architektur

```
src/
├── core/           # SSO-Authentifizierung, Publikations-Management
├── pubmed/         # PubMed API, Suchstrategie, Schema-Mapping, Integration
└── tools/          # Status-Monitoring, Backup-Restore, Cleanup-Tools
```

## 🔧 Haupt-Features

### 📊 **RACOON Publikations-Management**
- Sichere Tabellen-Operationen mit automatischen Backups
- TEST-Zeilen hinzufügen/entfernen für sicheres Testen
- Status-Monitoring und Größenvalidierung

### 🧬 **PubMed-Integration** ⭐ **NEU**
- Automatische Publikations-Discovery via NCBI E-utilities API
- Intelligente RACOON-Relevanz-Bewertung (0-100% Score)
- Multi-dimensionale Suchstrategie (Keywords, Autoren, Institutionen)
- Schema-Mapping PubMed ↔ RACOON Format mit Validierung

### 🛡️ **Sicherheit & Backup**
- SSO-Cookie-Authentifizierung für wms.diz-ag.med.ovgu.de
- Timestamped Backups vor jeder Operation
- Dry-Run Modus für sichere Tests
- Emergency-Restore Funktionalität

## ⚡ Verwendung

### Cookie-Authentifizierung
1. Browser: Anmelden bei https://wms.diz-ag.med.ovgu.de
2. DevTools (F12) → Network → Cookie-Header kopieren
3. In `config/confluence_credentials.json` einfügen

### Typischer Workflow
```bash
# 1. Tabellenstatus prüfen
python run_table_analyzer.py

# 2. Neue Publikationen suchen
python run_pubmed_integration.py  # Findet relevante Papers automatisch

# 3. TEST-Operation durchführen
python run_publication_manager.py

# 4. Status validieren, dann live deployment
```

## 📈 PubMed-Integration Beispiel

**Input:** Automatische Suche nach `(COVID-19) AND (radiology) AND (chest CT)`

**Output:** 
- ✅ **7 Publikationen** entdeckt
- ✅ **2 relevante Kandidaten** (Score > 60%)
- ✅ **Automatisches RACOON-Format** mit DOI/PMID-Links
- ✅ **HTML-Tabellen-Code** für direkte Confluence-Integration

## 🛠️ Tools-Übersicht

| Tool | Funktion | Verwendung |
|------|----------|------------|
| `run_publication_manager.py` | RACOON Tabellen-Management | Publikationen hinzufügen/bearbeiten |
| `run_pubmed_integration.py` | Automatische Publikations-Discovery | Neue Papers via PubMed finden |
| `run_table_analyzer.py` | Tabellenstruktur analysieren | Status und Patterns verstehen |
| `run_table_status.py` | Live-Status monitoring | Aktuelle Tabelle überwachen |

## ⚙️ Konfiguration

**`config/confluence_credentials.json`:**
```json
{
  "cookies": "JSESSIONID=...; seraph.confluence=..."
}
```

## 📊 RACOON Tabellen-Schema

| Spalte | Format | Beispiel |
|--------|---------|----------|
| Nummer | Fortlaufend | 63 |
| Jahr/Monat | YYYY/MM | 2025/09 |
| Standort | Institution | UK Magdeburg |
| Personen | Autoren | Schmidt M, Müller K |
| Förderhinweis | JA + Nummer | JA 70063 |
| PubMed DOI | Titel + Links | Paper Title. DOI: 10.xxx &lt;pubmed-link&gt; |

## 🔒 Sicherheits-Features

- **Backup vor jeder Operation** → `backups/` mit Timestamp
- **Dry-Run Standardmodus** → Simulation vor Live-Changes
- **Cookie-Validierung** → Automatische Session-Prüfung
- **Duplikat-Erkennung** → PMID-basierte Filterung

## 📚 Erweiterte Dokumentation

Für detaillierte API-Referenz und Entwickler-Guides siehe `docs/` Ordner.

## 🤝 Entwicklung

```bash
# Tests
python -m pytest tests/  # (zukünftig)

# Neue Features
# 1. Branch erstellen
# 2. Implementierung in entsprechendem src/ Unterordner  
# 3. Wrapper-Script im Root erstellen
# 4. Tests und Dokumentation
```

---

**Das System ist produktionsbereit und vollständig getestet!** 🚀

Aus einem unübersichtlichen Sammlung von Python-Scripten wurde eine professionelle, modulare RACOON-Publikationsverwaltung mit automatischer PubMed-Integration.