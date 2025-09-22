# pyRacoonConfluence

**Einfaches Python-Tool für RACOON Publikations-Management in Confluence**

## 🎯 Überblick

Ein fokussiertes Tool zur sicheren Verwaltung der RACOON-Publikationsdaten in Confluence über SSO-Authentifizierung. Entwickelt speziell für das Berichtswesen der RACOON-Forschungsgemeinschaft.

## ✨ Kernfunktionen

- 🔐 **SSO-Authentifizierung** - Sichere Anmeldung über Browser-Cookies
- 📊 **Publikations-Management** - Hinzufügen, Testen und Verwalten von Publikationen
- 💾 **Automatische Backups** - Sichere Datensicherung vor jeder Änderung
- 🧪 **Sicheres Testen** - Test-Modus mit automatischer Bereinigung

## 🚀 Schnellstart

### Voraussetzungen

- Python 3.8+
- Zugriff auf RACOON Confluence-Instanz
- Gültige SSO-Anmeldung

### Installation

```bash
# Repository klonen
git clone https://github.com/niklas-lackner/pyRacoonConfluence.git
cd pyRacoonConfluence

# Virtual Environment erstellen
python -m venv .venv

# Windows
.venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt
```

### Verwendung

#### 1. SSO-Authentifizierung einrichten

```bash
python confluence_sso.py --manual-login
```

**Cookie-Extraktion:**
1. Öffnen Sie Ihren Browser und loggen Sie sich in Confluence ein
2. Öffnen Sie Entwicklertools (F12) → Network Tab
3. Besuchen Sie: `https://wms.diz-ag.med.ovgu.de/rest/api/space`
4. Kopieren Sie die Cookie-Header aus dem Request

**Cookie-Format:**
```
JSESSIONID=ABC123...; seraph.confluence=XYZ789...
```

#### 2. Publikationen testen

**Test-Publikation hinzufügen:**
```bash
python racoon_test_update.py --add
```

**Test-Publikation entfernen:**
```bash
python racoon_test_update.py --remove
```

**Verbindung testen:**
```bash
python confluence_sso.py
```

## 📁 Projektstruktur

```
pyRacoonConfluence/
├── confluence_sso.py          # SSO-Authentifizierung (Kern-Modul)
├── racoon_test_update.py      # Publikations-Management
├── backups/                   # Zeitgestempelte Backup-Dateien
├── requirements.txt           # Python-Dependencies
├── README.md                  # Diese Dokumentation
├── LICENSE                    # MIT-Lizenz
└── .gitignore                 # Git-Ausschlüsse
```

## 🔧 Kern-Module

### confluence_sso.py
**SSO-Authentifizierungs-Handler**
- Cookie-basierte Anmeldung
- Session-Management
- API-Zugriff auf 14 Confluence-Spaces
- Verbindungsdiagnose

### racoon_test_update.py
**RACOON Publikations-Manager**
- Sichere Test-Operationen
- Automatische Backup-Erstellung
- Publikationstabellen-Management
- Status-Makro-Handling (JA/NEIN)

## 📊 RACOON Publikations-Schema

Die verwaltete Tabelle enthält folgende Spalten:

| Spalte | Beschreibung | Beispiel |
|--------|--------------|----------|
| Nummer | Publikationsnummer | 63 |
| Jahr/Monat | Publikationsdatum | 2024/12 |
| Standort | Institution | UK Frankfurt |
| Beteiligte Personen | Autoren | Smith J, Doe A |
| Förderhinweis NUM/RACOON | Förderanerkennung | ✅ JA / ❌ NEIN |
| PubMed DOI | Publikationslinks | doi: 10.1234/example |

## 🛡️ Sicherheitsfeatures

- **Keine Klartext-Passwörter** - Verwendet Browser-Session-Cookies
- **Automatische Backups** - Zeitgestempelte Backups im `backups/` Ordner
- **Session-Validierung** - Überprüft Cookie-Gültigkeit
- **Sichere Speicherung** - Sensible Daten in `.gitignore`

## 💾 Backup-System

Alle Änderungen werden automatisch mit Zeitstempel gesichert:

```
backups/
├── racoon_publications_sso_20240922_161904.html
├── racoon_publications_with_test_20240922_161913.html
└── .gitkeep
```

**Backup-Naming:**
- `racoon_publications_sso_YYYYMMDD_HHMMSS.html` - SSO-Authentifizierung-Backups
- `racoon_publications_with_test_YYYYMMDD_HHMMSS.html` - Test-Operation-Backups

## 🧪 Sicherheits-Testing

Das System bietet verschiedene Test-Modi:

```bash
# Vollständiger Test-Zyklus
python racoon_test_update.py --add    # Test-Publikation hinzufügen
python racoon_test_update.py --remove # Test-Publikation entfernen

# Nur Verbindung testen (ohne Änderungen)
python confluence_sso.py

# Status der Publikationstabelle prüfen
python table_status.py
```

### 📖 Detaillierter Beispiel-Workflow

Einen kompletten dokumentierten Workflow mit erwarteten Ausgaben finden Sie in:
**→ [EXAMPLE_WORKFLOW.md](EXAMPLE_WORKFLOW.md)**

Dieses Beispiel zeigt Schritt-für-Schritt:
- ✅ Sichere TEST-Zeile hinzufügen
- 🔍 Status-Überprüfung
- 🗑️ Automatische Bereinigung
- 📊 Größenvergleiche und Validierung

**Schnelltest:**
```bash
# 1. TEST-Zeile hinzufügen
python racoon_test_update.py --add

# 2. Status prüfen  
python table_status.py

# 3. TEST-Zeile entfernen
python racoon_test_update.py --remove

# 4. Finaler Check
python table_status.py
```

## ⚠️ Wichtige Hinweise

- **SSO erforderlich** - Funktioniert nur mit SSO-aktivierten Confluence-Instanzen
- **Cookie-Ablauf** - Browser-Cookies verfallen typischerweise nach wenigen Stunden
- **Backup-Politik** - Erstellt immer Backups vor Änderungen
- **Zugriffskontrolle** - Respektiert Confluence-Berechtigungen

## 🆘 Fehlerbehebung

### Häufige Probleme

**401 Unauthorized Fehler**
- Überprüfen Sie, ob Ihre Browser-Cookies noch gültig sind
- Extrahieren Sie neue Cookies aus einer frischen Browser-Session
- Stellen Sie sicher, dass Sie Zugriff auf den Confluence-Space haben

**Verbindungstimeout**
- Überprüfen Sie Ihre Netzwerkverbindung
- Verifizieren Sie, dass die Confluence-URL korrekt ist
- Stellen Sie sicher, dass die Firewall API-Zugriff erlaubt

**Fehlende Dependencies**
```bash
pip install --upgrade -r requirements.txt
```

### Logs und Backups

- Backup-Dateien werden zeitgestempelt im `backups/` Ordner gespeichert
- Cookie-Sessions werden automatisch validiert
- Alle API-Operationen werden mit Status-Codes protokolliert
- Backup-Format: `prefix_YYYYMMDD_HHMMSS.html`

## 📝 Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe [LICENSE](LICENSE) für Details.

## 🏆 Danksagungen

- **RACOON Research Network**
- **NUM (Netzwerk Universitätsmedizin)**
- **BMBF (Bundesministerium für Bildung und Forschung)**
- **Alle beteiligten Forschungseinrichtungen**

---

**Entwickelt mit ❤️ für die RACOON-Forschungsgemeinschaft**

### 🔗 Nützliche Links

- **Repository**: https://github.com/niklas-lackner/pyRacoonConfluence
- **Issues**: https://github.com/niklas-lackner/pyRacoonConfluence/issues
- **RACOON-Netzwerk**: https://www.netzwerk-universitaetsmedizin.de/projekte/racoon