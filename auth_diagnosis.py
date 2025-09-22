#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Erweiterte Confluence Authentifizierungs-Diagnose
Testet verschiedene Authentifizierungsmethoden
"""

import sys
import requests
import base64
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from confluence_update import get_credentials

def test_manual_http_request():
    """Testet manuelle HTTP-Requests zur Confluence API"""
    
    CONFLUENCE_URL = "https://wms.diz-ag.med.ovgu.de/"
    
    username, password = get_credentials()
    
    if not username or not password:
        print("❌ Keine gültigen Anmeldedaten erhalten!")
        return
    
    print(f"🔍 Teste manuelle HTTP-Authentifizierung für: {username}")
    print(f"=" * 60)
    
    # Test 1: Basic Auth mit requests
    print(f"\n1️⃣ Test: HTTP Basic Authentication")
    try:
        url = f"{CONFLUENCE_URL}rest/api/space"
        
        response = requests.get(
            url,
            auth=(username, password),
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Reason: {response.reason}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Erfolgreich! {len(data.get('results', []))} Spaces gefunden")
        elif response.status_code == 401:
            print(f"   ❌ Unauthorized - Benutzername/Passwort falsch")
            print(f"   Headers: {dict(response.headers)}")
        elif response.status_code == 403:
            print(f"   ❌ Forbidden - Keine API-Berechtigung")
        else:
            print(f"   ❌ Unerwarteter Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    # Test 2: Teste verschiedene API-Endpunkte
    print(f"\n2️⃣ Test: Verschiedene API-Endpunkte")
    
    endpoints = [
        ("Server Info", "rest/api/settings/systemInfo"),
        ("Spaces", "rest/api/space"),
        ("Current User", "rest/api/user/current"),
        ("Groups", "rest/api/group"),
    ]
    
    for name, endpoint in endpoints:
        try:
            url = f"{CONFLUENCE_URL}{endpoint}"
            response = requests.get(
                url,
                auth=(username, password),
                timeout=5
            )
            
            print(f"   {name}: {response.status_code} ({response.reason})")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        print(f"      📊 Keys: {list(data.keys())[:5]}")
                    elif isinstance(data, list):
                        print(f"      📊 Items: {len(data)}")
                except:
                    print(f"      📊 Text response: {len(response.text)} chars")
                    
        except Exception as e:
            print(f"   {name}: ❌ {str(e)[:50]}...")
    
    # Test 3: Teste Login-Seite
    print(f"\n3️⃣ Test: Login-Seite Verfügbarkeit")
    try:
        login_url = f"{CONFLUENCE_URL}login.action"
        response = requests.get(login_url, timeout=5)
        print(f"   Login-Seite: {response.status_code}")
        
        if "login" in response.text.lower():
            print(f"   ✅ Login-Seite verfügbar")
        else:
            print(f"   ⚠️  Unerwartete Antwort")
            
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    # Test 4: Base64 Auth Header (manuell)
    print(f"\n4️⃣ Test: Manuelle Authorization Header")
    try:
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{CONFLUENCE_URL}rest/api/space",
            headers=headers,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Auth Header: Basic {encoded_credentials[:20]}...")
        
        if response.status_code == 200:
            print(f"   ✅ Manuelle Auth erfolgreich!")
        else:
            print(f"   Response Headers: {dict(response.headers)}")
            
    except Exception as e:
        print(f"   ❌ Fehler: {e}")

def test_confluence_url_variations():
    """Testet verschiedene URL-Varianten"""
    
    username, password = get_credentials()
    
    print(f"\n5️⃣ Test: URL-Varianten")
    
    base_urls = [
        "https://wms.diz-ag.med.ovgu.de/",
        "https://wms.diz-ag.med.ovgu.de",
        "https://wms.diz-ag.med.ovgu.de/wiki/",
        "https://wms.diz-ag.med.ovgu.de/confluence/",
    ]
    
    for base_url in base_urls:
        print(f"\n   🔗 Teste URL: {base_url}")
        
        try:
            # Teste verschiedene Endpunkte
            endpoints = ["rest/api/space", "rest/api/content"]
            
            for endpoint in endpoints:
                test_url = f"{base_url.rstrip('/')}/{endpoint}"
                
                response = requests.get(
                    test_url,
                    auth=(username, password),
                    timeout=5
                )
                
                print(f"      {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"      ✅ GEFUNDEN! URL: {test_url}")
                    return test_url
                    
        except Exception as e:
            print(f"      ❌ Fehler: {str(e)[:30]}...")
    
    return None

def main():
    """Hauptfunktion"""
    print("=== Erweiterte Confluence Authentifizierungs-Diagnose ===")
    
    test_manual_http_request()
    working_url = test_confluence_url_variations()
    
    print(f"\n" + "=" * 60)
    print(f"📊 FAZIT:")
    
    if working_url:
        print(f"✅ Funktionierende URL gefunden: {working_url}")
    else:
        print(f"❌ Keine funktionierende URL/Authentifizierung gefunden")
        print(f"\n🔧 LÖSUNGSVORSCHLÄGE:")
        print(f"1. Prüfen Sie Ihr Passwort über den Browser")
        print(f"2. Kontaktieren Sie den Confluence-Administrator")
        print(f"3. Fragen Sie nach REST API Berechtigungen")
        print(f"4. Prüfen Sie, ob Ihr Account aktiv ist")

if __name__ == "__main__":
    main()