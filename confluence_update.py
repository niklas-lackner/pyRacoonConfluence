#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Confluence API Test Skript
Dieses Skript testet die Verbindung zur Confluence API
"""

# pip install atlassian-python-api
from atlassian import Confluence
import sys
import os
import getpass
from pathlib import Path
import base64
from cryptography.fernet import Fernet
import json

def create_key_file():
    """Erstellt eine Verschlüsselungsschlüssel-Datei"""
    key = Fernet.generate_key()
    key_file = Path("confluence_key.key")
    with open(key_file, "wb") as f:
        f.write(key)
    print(f"🔑 Schlüsseldatei erstellt: {key_file}")
    return key

def load_key():
    """Lädt den Verschlüsselungsschlüssel"""
    key_file = Path("confluence_key.key")
    if not key_file.exists():
        print("⚠️  Kein Verschlüsselungsschlüssel gefunden. Erstelle neuen...")
        return create_key_file()
    
    with open(key_file, "rb") as f:
        key = f.read()
    return key

def encrypt_password(password):
    """Verschlüsselt ein Passwort"""
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def save_encrypted_credentials(username, password):
    """Speichert verschlüsselte Anmeldedaten"""
    credentials = {
        "username": username,
        "password": base64.b64encode(encrypt_password(password)).decode()
    }
    
    cred_file = Path("confluence_credentials.json")
    with open(cred_file, "w") as f:
        json.dump(credentials, f, indent=2)
    
    print(f"🔐 Verschlüsselte Anmeldedaten gespeichert: {cred_file}")

def load_encrypted_credentials():
    """Lädt und entschlüsselt die Anmeldedaten"""
    cred_file = Path("confluence_credentials.json")
    key_file = Path("confluence_key.key")
    
    if not cred_file.exists() or not key_file.exists():
        return None, None
    
    try:
        with open(cred_file, "r") as f:
            credentials = json.load(f)
        
        key = load_key()
        fernet = Fernet(key)
        
        username = credentials["username"]
        encrypted_password = base64.b64decode(credentials["password"])
        password = fernet.decrypt(encrypted_password).decode()
        
        return username, password
    
    except Exception as e:
        print(f"❌ Fehler beim Laden der Anmeldedaten: {e}")
        return None, None

def load_password_from_file():
    """Lädt Passwort aus einer einfachen Textdatei (unsicher, aber einfach)"""
    password_file = Path("password.txt")
    if password_file.exists():
        with open(password_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def setup_credentials():
    """Einmalige Einrichtung der Anmeldedaten"""
    print("=== Anmeldedaten einrichten ===")
    print("Wählen Sie eine Methode:")
    print("1. Verschlüsselte Speicherung (empfohlen)")
    print("2. Einfache Textdatei (unsicher)")
    print("3. Jedes Mal manuell eingeben")
    
    choice = input("Ihre Wahl (1-3): ").strip()
    
    if choice == "1":
        username = input("Confluence Benutzername: ").strip()
        password = getpass.getpass("Confluence Passwort: ")
        save_encrypted_credentials(username, password)
        print("✅ Anmeldedaten verschlüsselt gespeichert!")
        return username, password
    
    elif choice == "2":
        print("⚠️  WARNUNG: Diese Methode speichert das Passwort unverschlüsselt!")
        username = input("Confluence Benutzername: ").strip()
        password = getpass.getpass("Confluence Passwort: ")
        
        password_file = Path("password.txt")
        with open(password_file, "w", encoding="utf-8") as f:
            f.write(password)
        
        print(f"📝 Passwort gespeichert in: {password_file}")
        print("⚠️  Löschen Sie diese Datei nach dem Test!")
        return username, password
    
    elif choice == "3":
        username = input("Confluence Benutzername: ").strip()
        password = getpass.getpass("Confluence Passwort: ")
        return username, password
    
    else:
        print("❌ Ungültige Auswahl!")
        return None, None

def get_credentials():
    """Lädt Anmeldedaten aus verschiedenen Quellen"""
    # 1. Versuche verschlüsselte Datei zu laden
    username, password = load_encrypted_credentials()
    if username and password:
        print("🔐 Verschlüsselte Anmeldedaten geladen")
        return username, password
    
    # 2. Versuche einfache Textdatei (falls vorhanden)
    password_from_file = load_password_from_file()
    if password_from_file:
        print("📝 Passwort aus password.txt geladen")
        username = input("Confluence Benutzername: ").strip()
        return username, password_from_file
    
def test_confluence_connection():
    """Teste die Confluence API Verbindung"""
    
    # KONFIGURATION
    CONFLUENCE_URL = "https://wms.diz-ag.med.ovgu.de/"
    
    # Anmeldedaten sicher laden
    username, password = get_credentials()
    
    if not username or not password:
        print("❌ Keine gültigen Anmeldedaten erhalten!")
        return False
    
    print("🔄 Teste Confluence-Verbindung (selbst-gehostet)...")
    print(f"URL: {CONFLUENCE_URL}")
    print(f"Username: {username}")
    
    try:
        # Confluence-Verbindung erstellen
        confluence = Confluence(
            url=CONFLUENCE_URL,
            username=username,
            password=password
        )
        
        # Test: Alle Spaces abrufen
        spaces = confluence.get_all_spaces(start=0, limit=10)
        
        print("✅ Verbindung erfolgreich!")
        print(f"Gefundene Spaces: {len(spaces.get('results', []))}")
        
        # Zeige erste paar Spaces an
        if spaces.get('results'):
            print("\nVerfügbare Spaces:")
            for space in spaces['results'][:5]:
                print(f"- {space.get('name')} (Key: {space.get('key')})")
        else:
            print("Keine Spaces gefunden oder keine Berechtigung")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Verbinden mit Confluence: {e}")
        print(f"Fehlertyp: {type(e).__name__}")
        
        print("\nFür selbst-gehostetes Confluence versuchen Sie:")
        print("1. Prüfen Sie Username und Passwort")
        print("2. Prüfen Sie, ob Sie Zugriff auf die REST API haben")
        print("3. Kontaktieren Sie Ihren Confluence-Administrator")
        
        return False
    """Teste die Confluence API Verbindung"""
    
    # KONFIGURATION - Diese Werte müssen angepasst werden!
    CONFLUENCE_URL = "https://wms.diz-ag.med.ovgu.de/"
    USERNAME = "niklas.lackner@uk-erlangen.de"
    
    # Für selbst-gehostetes Confluence (Server/Data Center) - verwenden Sie Ihr normales Passwort
    PASSWORD = "IHR_PASSWORT_HIER"  # Ihr normales Confluence-Passwort
    
    # Alternativ für Server mit Personal Access Token (falls aktiviert)
    # API_TOKEN = "YOUR_TOKEN_HERE"  # Replace with your actual token
    
    # Prüfe ob Konfiguration gesetzt wurde
    if PASSWORD == "IHR_PASSWORT_HIER":
        print("❌ FEHLER: Passwort nicht gesetzt!")
        print("Für selbst-gehostetes Confluence benötigen Sie Ihr normales Passwort,")
        print("nicht einen Atlassian Cloud API Token.")
        print(f"Server: {CONFLUENCE_URL}")
        print(f"Username: {USERNAME}")
        print("Bitte setzen Sie PASSWORD = 'Ihr echtes Passwort' in der Datei")
        return False
    
    print("🔄 Teste Confluence-Verbindung (selbst-gehostet)...")
    print(f"URL: {CONFLUENCE_URL}")
    print(f"Username: {USERNAME}")
    
    try:
        # Methode 1: Mit Username und Passwort (für Server/Data Center)
        confluence = Confluence(
            url=CONFLUENCE_URL,
            username=USERNAME,
            password=PASSWORD
        )
        
        # Test: Alle Spaces abrufen (einfacher Test)
        spaces = confluence.get_all_spaces(start=0, limit=10)
        
        print("✅ Verbindung erfolgreich!")
        print(f"Gefundene Spaces: {len(spaces.get('results', []))}")
        
        # Zeige erste paar Spaces an
        if spaces.get('results'):
            print("\nVerfügbare Spaces:")
            for space in spaces['results'][:5]:  # Nur erste 5 anzeigen
                print(f"- {space.get('name')} (Key: {space.get('key')})")
        else:
            print("Keine Spaces gefunden oder keine Berechtigung")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Verbinden mit Confluence: {e}")
        print(f"Fehlertyp: {type(e).__name__}")
        
        print("\nFür selbst-gehostetes Confluence versuchen Sie:")
        print("1. Verwenden Sie Ihr normales Confluence-Passwort (nicht API Token)")
        print("2. Prüfen Sie, ob Sie Zugriff auf die REST API haben")
        print("3. Kontaktieren Sie Ihren Confluence-Administrator")
        print("4. Prüfen Sie, ob Personal Access Tokens aktiviert sind")
        
        return False

def main():
    """Hauptfunktion"""
    # Prüfe auf Setup-Parameter
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        print("=== Anmeldedaten neu einrichten ===")
        username, password = setup_credentials()
        if username and password:
            print("✅ Setup abgeschlossen!")
        else:
            print("❌ Setup fehlgeschlagen!")
        return
    
    print("=== Confluence API Test ===")
    print("💡 Tipp: Verwenden Sie 'python confluence_update.py --setup' um Anmeldedaten neu zu konfigurieren")
    print()
    
    success = test_confluence_connection()
    
    if success:
        print("\n🎉 Alles funktioniert! Sie können jetzt mit der Confluence API arbeiten.")
    else:
        print("\n⚠️  Bitte beheben Sie die Konfigurationsprobleme und versuchen Sie es erneut.")
        print("💡 Versuchen Sie: python confluence_update.py --setup")
        sys.exit(1)

if __name__ == "__main__":
    main()
