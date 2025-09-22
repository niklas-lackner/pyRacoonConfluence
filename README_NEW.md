# 🧬 pyRacoonConfluence - Strukturierte Version

**Professionelles RACOON Confluence Management Tool mit PubMed Integration**

## 📁 **Neue Projektstruktur**

```
pyRacoonConfluence/
├── 🧰 src/                        # Quellcode (organisiert)
│   ├── core/                      # 🔧 Kern-Module
│   │   ├── confluence_sso.py      # SSO-Authentifizierung
│   │   └── publication_manager.py # RACOON Publikations-Management
│   ├── pubmed/                    # 🧬 PubMed Integration
│   │   ├── api_client.py          # PubMed API Client
│   │   ├── search_strategy.py     # Intelligente Suchstrategie
│   │   ├── schema_mapper.py       # PubMed ↔ RACOON Mapping
│   │   └── integrator.py          # Vollständige Integration
│   └── tools/                     # 🛠️ Utility-Tools
│       ├── table_status.py        # Status-Monitoring
│       ├── table_analyzer.py      # Tabellenanalyse
│       ├── emergency_restore.py   # Backup-Wiederherstellung
│       └── cleanup_tools.py       # Cleanup-Utilities
├── 📚 docs/                       # Dokumentation
│   └── PUBMED_INTEGRATION.md      # PubMed Integration Guide
├── ⚙️ config/                     # Konfiguration
│   ├── confluence_credentials.json
│   └── confluence_key.key
├── 💾 backups/                    # Backup-Dateien
├── 🗑️ trash/                      # Veraltete Dateien
└── 🚀 run_*.py                    # Wrapper-Scripts (Einstiegspunkte)
```

## 🚀 **Schnellstart**

### **Installation:**
```bash
git clone https://github.com/niklas-lackner/pyRacoonConfluence.git
cd pyRacoonConfluence
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### **Hauptfunktionen:**

| Script | Funktion | Beschreibung |
|--------|----------|--------------|
| `run_pubmed_integration.py` | **🧬 PubMed Integration** | Automatische Publikations-Discovery |
| `run_table_analyzer.py` | **📊 Tabellenanalyse** | RACOON-Struktur analysieren |
| `run_table_status.py` | **📈 Status-Monitoring** | Tabellen-Status überwachen |
| `run_publication_manager.py` | **📝 Publikations-Manager** | Manuelle Publikationsverwaltung |

## 🔧 **Core-Module** (`src/core/`)

### **confluence_sso.py**
- **SSO-Authentifizierung** mit Cookie-Management
- **Session-Handling** für 14 Confluence-Spaces
- **Backup-System** mit Zeitstempel
- **Verbindungsdiagnose** und Error-Handling

### **publication_manager.py** 
- **RACOON Publikations-Management**
- **Sichere Test-Operationen** mit automatischen Backups
- **Status-Makro-Handling** (JA/NEIN)
- **Header-Schutz** und Validierung

## 🧬 **PubMed-Integration** (`src/pubmed/`)

### **Vollständiges Ecosystem:**
- **api_client.py** - NCBI E-utilities Integration
- **search_strategy.py** - Multi-dimensionale Suchstrategie  
- **schema_mapper.py** - Automatisches PubMed ↔ RACOON Mapping
- **integrator.py** - End-to-End Integration mit Dry-Run

### **Features:**
✅ **Intelligente Suchstrategie** - Keywords, Autoren, Institutionen  
✅ **Relevanz-Scoring** - 0-100% RACOON-Relevanz-Bewertung  
✅ **Schema-Mapping** - Automatische Format-Konvertierung  
✅ **Duplikat-Erkennung** - PMID-basierte Filterung  
✅ **Sichere Integration** - Dry-Run mit Backup-System  

## 🛠️ **Tools** (`src/tools/`)

### **Monitoring & Analyse:**
- **table_status.py** - Live-Status der RACOON-Tabelle
- **table_analyzer.py** - Strukturanalyse und Pattern-Erkennung

### **Maintenance:**
- **emergency_restore.py** - Backup-Wiederherstellung
- **cleanup_tools.py** - Erweiterte Cleanup-Operationen

## 📊 **Verwendung**

### **1. PubMed Integration ausführen:**
```bash
python run_pubmed_integration.py
```
**Output:**
```
🚀 RACOON PubMed Integration
🔍 Suche nach neuen RACOON-Publikationen...
✅ Gefunden: 7 Publikationen
📊 Relevante Publikationen (Score >= 60%): 2
🧪 SIMULATION: Integration von 2 Publikationen
✅ Simulation abgeschlossen!
```

### **2. Tabellenanalyse:**
```bash
python run_table_analyzer.py
```
**Output:**
```
🔍 RACOON Publikationen - Muster-Analyse
✅ Seite geladen: Version 46, 62 Publikationen
📊 Schema erkannt: 6 Spalten, konsistente Nummerierung
🎯 RACOON-Format dokumentiert für automatische Integration
```

### **3. Status-Monitoring:**
```bash
python run_table_status.py
```
**Output:**
```
📊 RACOON Publikations-Status
✅ Verbindung erfolgreich
📈 Aktuelle Publikationen: 62
🔍 Letzte Änderung: Version 46
```

## ⚙️ **Konfiguration**

### **Confluence-Credentials** (`config/confluence_credentials.json`):
```json
{
  "cookies": "JSESSIONID=...; seraph.confluence=..."
}
```

### **PubMed-Einstellungen:**
```python
# In src/pubmed/integrator.py
min_relevance = 60        # Minimum Score für Integration
dry_run = True           # Sichere Simulation (empfohlen)
max_results_per_query = 10  # PubMed Resultate pro Query
```

## 🧪 **Sicherheitsfeatures**

### **Backup-System:**
- **Automatische Backups** vor jeder Operation
- **Timestamped Files** in `backups/racoon_publications_YYYYMMDD_HHMMSS.html`
- **Emergency Restore** für vollständige Wiederherstellung

### **Dry-Run Modus:**
- **Simulation** aller Änderungen ohne Live-Integration
- **Vorschau** der generierten HTML-Tabellen
- **Validierung** aller Daten vor Integration

## 📚 **Dokumentation**

- **[PubMed Integration Guide](docs/PUBMED_INTEGRATION.md)** - Vollständige Implementierungsdokumentation
- **[Restructure Plan](RESTRUCTURE_PLAN.md)** - Organisationsprinzipien und Migration

## 🔄 **Migration von alter Struktur**

**Alte Dateien → Neue Struktur:**
```
confluence_sso.py → src/core/confluence_sso.py
racoon_test_update.py → src/core/publication_manager.py
racoon_pubmed_integrator.py → src/pubmed/integrator.py
table_status.py → src/tools/table_status.py
analyze_publications.py → src/tools/table_analyzer.py
```

**Wrapper-Scripts** im Root ermöglichen weiterhin direkte Ausführung.

## 🏗️ **Projektorganisation**

### **Vorteile der neuen Struktur:**
✅ **Modulare Architektur** - Logische Gruppierung verwandter Funktionen  
✅ **Python Package Structure** - Professionelle Import-Organisation  
✅ **Bessere Auffindbarkeit** - Core, PubMed, Tools klar getrennt  
✅ **Zentrale Konfiguration** - Alle Config-Dateien in `config/`  
✅ **Zentrale Dokumentation** - Alle Docs in `docs/`  
✅ **Einfache Nutzung** - Wrapper-Scripts für direkten Zugriff  

### **Entwicklungsprinzipien:**
- **Core-Module** - Basis-Funktionalität ohne Spezialisierung
- **Feature-Packages** - PubMed, zukünftig weitere Integrationen
- **Utility-Tools** - Standalone-Scripts für Wartung
- **Clean Imports** - Klare Abhängigkeitsstrukturen

## 🚀 **Nächste Schritte**

1. **Live-Integration** aktivieren (`dry_run=False`)
2. **Setup-Script** für automatische Installation
3. **Tests** für alle Module entwickeln
4. **CI/CD Pipeline** für automatische Deployment
5. **API Documentation** für Entwickler

---

**🎉 Vollständig strukturiertes, professionelles RACOON Management Tool!**