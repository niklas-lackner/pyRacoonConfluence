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

Einen kompletten dokumentierten Workflow mit erwarteten Ausgaben finden Sie weiter unten in dieser README:
**→ [Kompletter Beispiel-Workflow](#-kompletter-beispiel-workflow)**

Dieser Workflow zeigt Schritt-für-Schritt:
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

---

## 🎯 **Kompletter Beispiel-Workflow**

### Workflow-Übersicht

1. **TEST-Zeile hinzufügen** → Testet das Hinzufügen von Inhalten
2. **Status überprüfen** → Verifiziert die Änderungen  
3. **TEST-Zeile entfernen** → Bereinigt die Tabelle
4. **Finaler Check** → Bestätigt saubere Tabelle

### Schritt 1: TEST-Zeile hinzufügen
```bash
python racoon_test_update.py --add
```

**Erwartete Ausgabe:**
```
=== RACOON Publikationen - Test Update ===
Füge Test-Zeile hinzu...
📋 Verwende gespeicherte Cookies...
🔑 Cookies gesetzt: ['JSESSIONID', 'seraph.confluence']
✅ SSO-Login erfolgreich!
📖 Lade aktuelle Seite...
✅ Seite geladen: Version 44
✏️ Test-Zeile wurde eingefügt
🚀 Aktualisiere Confluence-Seite...
✅ Seite erfolgreich aktualisiert!
Neue Version: 45
💾 Backup gespeichert: backups\racoon_publications_with_test_20250922_165150.html
```

### Schritt 2: Status überprüfen
```bash
python table_status.py
```

**Erwartete Ausgabe:**
```
🔍 RACOON Publikationen - Status-Check
✅ Seite geladen: Version 45
📊 Content-Größe: 57,271 Zeichen
🎯 TEST-Inhalte: 12
✨ TEST-Zeile wurde erfolgreich hinzugefügt!
```

### Schritt 3: TEST-Zeile sicher entfernen
```bash
python racoon_test_update.py --remove
```

**Erwartete Ausgabe:**
```
=== RACOON Publikationen - Test-Zeile entfernen ===
📋 Verwende gespeicherte Cookies...
✅ SSO-Login erfolgreich!
🗑️  Entferne letzte Tabellenzeile: <tr><td><p>TEST</p></td>...
✅ Letzte Tabellenzeile entfernt! Neue Version: 46
```

### Schritt 4: Finaler Status-Check
```bash
python table_status.py
```

**Erwartete Ausgabe:**
```
🔍 RACOON Publikationen - Status-Check
✅ Seite geladen: Version 46  
📊 Content-Größe: 56,894 Zeichen
🎯 TEST-Inhalte: 0
✨ Tabelle ist sauber!
```

### 📊 **Typische Größenunterschiede**

| **Phase** | **Content-Größe** | **TEST-Inhalte** | **Version** |
|-----------|-------------------|------------------|-------------|
| **Vor Test** | ~56.894 Zeichen | 0 | 44 |
| **Mit TEST-Zeile** | ~57.271 Zeichen | 12 | 45 |
| **Nach Bereinigung** | ~56.894 Zeichen | 0 | 46 |
| **Unterschied** | ~377 Zeichen | - | +2 Versionen |

### 🔄 **Automatisierung**

Für regelmäßige Tests können Sie ein Batch-Script erstellen:

```batch
@echo off
echo === RACOON Test-Workflow ===
echo.
echo 1. Füge TEST-Zeile hinzu...
python racoon_test_update.py --add
echo.
echo 2. Prüfe Status...
python table_status.py
echo.
echo 3. Entferne TEST-Zeile...
python racoon_test_update.py --remove
echo.
echo 4. Finaler Check...
python table_status.py
echo.
echo === Test-Workflow abgeschlossen ===
```

### 🚨 **Notfall-Wiederherstellung**

Falls etwas schiefgeht:
```bash
python emergency_restore.py
```

Das Tool zeigt verfügbare Backups und stellt automatisch die letzte funktionierende Version wieder her.

### 💡 **Best Practices**

1. **Immer testen** bevor Sie Änderungen an der Live-Tabelle vornehmen
2. **Status prüfen** nach jeder Operation
3. **Backups behalten** - werden automatisch im `backups/` Ordner gespeichert
4. **Cookie-Session** bleibt 24h aktiv - danach neue Anmeldung nötig

### 🎯 **Anwendungsfälle**

- **Entwicklung**: Testen neuer Features
- **Wartung**: Überprüfung der Tabellenfunktionalität  
- **Training**: Schulung neuer Team-Mitglieder
- **Debugging**: Analysieren von Problemen