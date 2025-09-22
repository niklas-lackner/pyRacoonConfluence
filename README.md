# Sichere Confluence API Nutzung

## Übersicht
Dieses Skript stellt eine sichere Verbindung zu Ihrem selbst-gehosteten Confluence Server her.

## Erste Einrichtung

### 1. Anmeldedaten einrichten
```bash
python confluence_update.py --setup
```

Wählen Sie eine der Sicherheitsoptionen:

### Option 1: Verschlüsselte Speicherung (EMPFOHLEN) 🔐
- Passwort wird mit AES-Verschlüsselung gespeichert
- Erstellt zwei Dateien:
  - `confluence_key.key` - Verschlüsselungsschlüssel
  - `confluence_credentials.json` - Verschlüsselte Anmeldedaten
- **WICHTIG**: Beide Dateien sind erforderlich und sollten sicher aufbewahrt werden

### Option 2: Einfache Textdatei (UNSICHER) ⚠️
- Erstellt `password.txt` mit unverschlüsseltem Passwort
- **NUR FÜR TESTS** verwenden
- Datei nach Gebrauch löschen!

### Option 3: Manuelle Eingabe (SICHERSTE)
- Passwort wird bei jeder Ausführung abgefragt
- Keine Speicherung auf der Festplatte

## Verwendung

### Verbindung testen
```bash
python confluence_update.py
```

### Anmeldedaten neu konfigurieren
```bash
python confluence_update.py --setup
```

## Sicherheitshinweise

### ✅ SICHERE Praktiken:
- Verwenden Sie verschlüsselte Speicherung
- Halten Sie `confluence_key.key` sicher
- Teilen Sie die Schlüsseldatei nicht
- Verwenden Sie starke Passwörter

### ❌ UNSICHERE Praktiken:
- Passwörter im Quellcode
- Unverschlüsselte Textdateien
- Schlüssel in Git-Repositories
- Schwache Passwörter

## Dateien

- `confluence_update.py` - Hauptskript
- `confluence_key.key` - Verschlüsselungsschlüssel (GEHEIM!)
- `confluence_credentials.json` - Verschlüsselte Anmeldedaten
- `password.txt` - Temporäre Passwort-Datei (falls verwendet)

## Fehlerbehebung

### "ModuleNotFoundError"
```bash
pip install atlassian-python-api cryptography
```

### "Unauthorized (401)"
- Prüfen Sie Username und Passwort
- Führen Sie `python confluence_update.py --setup` aus
- Kontaktieren Sie Ihren Confluence-Administrator

### Schlüssel verloren
- Führen Sie `python confluence_update.py --setup` aus
- Wählen Sie Option 1 für neue verschlüsselte Speicherung