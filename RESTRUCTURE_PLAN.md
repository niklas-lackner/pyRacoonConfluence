# pyRacoonConfluence - Neue Projektstruktur

## 📁 Ordnerstruktur

```
pyRacoonConfluence/
├── src/                           # 🧰 Quellcode (organisiert)
│   ├── core/                      # 🔧 Kern-Module
│   │   ├── __init__.py
│   │   ├── confluence_sso.py      # SSO-Authentifizierung
│   │   └── publication_manager.py # RACOON Publikations-Management
│   ├── pubmed/                    # 🧬 PubMed Integration
│   │   ├── __init__.py
│   │   ├── api_client.py          # PubMed API Client
│   │   ├── search_strategy.py     # Intelligente Suchstrategie
│   │   ├── schema_mapper.py       # PubMed ↔ RACOON Mapping
│   │   └── integrator.py          # Vollständige Integration
│   └── tools/                     # 🛠️ Utility-Tools
│       ├── __init__.py
│       ├── table_status.py        # Status-Monitoring
│       ├── table_analyzer.py      # Tabellenanalyse
│       ├── emergency_restore.py   # Backup-Wiederherstellung
│       └── cleanup_tools.py       # Cleanup-Utilities
├── docs/                          # 📚 Dokumentation
│   ├── PUBMED_INTEGRATION.md      # PubMed Integration Guide
│   └── API_REFERENCE.md           # API-Referenz
├── backups/                       # 💾 Backup-Dateien
├── config/                        # ⚙️ Konfiguration
│   ├── confluence_credentials.json
│   └── confluence_key.key
├── tests/                         # 🧪 Tests (zukünftig)
├── requirements.txt               # 📦 Dependencies
├── setup.py                       # 📋 Projekt-Setup
├── README.md                      # 📖 Hauptdokumentation
└── .gitignore                     # 🚫 Git-Ausschlüsse
```

## 🎯 Organisationsprinzipien

### **Core-Module** (`src/core/`)
- **Basis-Funktionalität** die von anderen Modulen verwendet wird
- **SSO-Authentifizierung** und Session-Management
- **Kern-Publikationsmanagement** ohne spezialisierte Features

### **PubMed-Integration** (`src/pubmed/`)
- **Vollständiges PubMed-Ecosystem** in einem Ordner
- **API-Client**, **Suchstrategie**, **Schema-Mapping**, **Integration**
- **Modulare Architektur** für einfache Erweiterung

### **Tools** (`src/tools/`)
- **Utility-Scripte** für Wartung und Debugging
- **Status-Monitoring**, **Backup-Management**, **Cleanup**
- **Standalone-Tools** die direkt ausgeführt werden können

### **Dokumentation** (`docs/`)
- **Technische Dokumentation** getrennt von Code
- **API-Referenzen** und **Anleitungen**
- **Versionierte Dokumentation**

## 🔄 Migration Plan

1. **Ordnerstruktur erstellen** ✅
2. **Core-Module verschieben** 
3. **PubMed-Module gruppieren**
4. **Tools organisieren**
5. **Import-Statements aktualisieren**
6. **Dokumentation aktualisieren**
7. **Setup-Script erstellen**

## 🚀 Vorteile der neuen Struktur

- **🧰 Modulare Organisation** - Logische Gruppierung verwandter Funktionen
- **📦 Package-Structure** - Python-Package mit __init__.py Dateien
- **🔍 Bessere Auffindbarkeit** - Tools, Core, PubMed klar getrennt
- **📚 Zentrale Dokumentation** - Alle Docs im docs/ Ordner
- **⚙️ Saubere Konfiguration** - Config-Dateien im config/ Ordner
- **🧪 Test-Bereitschaft** - Struktur für zukünftige Tests vorbereitet
