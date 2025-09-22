#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cookie Extractor - Hilft beim Extrahieren von Browser-Cookies
"""

print("""
=== Confluence SSO Cookie-Extraktor ===

Da Ihr Confluence SSO verwendet, brauchen wir Browser-Cookies für die API.

📋 SCHRITT-FÜR-SCHRITT ANLEITUNG:

1. 🌐 Öffnen Sie Chrome/Edge/Firefox
   
2. 🔐 Loggen Sie sich in Confluence ein:
   https://wms.diz-ag.med.ovgu.de
   
3. 🔧 Öffnen Sie Entwicklertools:
   - Windows: F12 oder Strg+Shift+I
   - Mac: Cmd+Opt+I
   
4. 📂 Gehen Sie zum "Network" (Netzwerk) Tab
   
5. 🔄 Besuchen Sie diese URL (neue Registerkarte):
   https://wms.diz-ag.med.ovgu.de/rest/api/space
   
6. 📋 In den Entwicklertools:
   - Finden Sie den Request zu "rest/api/space"
   - Klicken Sie darauf
   - Gehen Sie zu "Headers" (Kopfzeilen)
   - Scrollen Sie zu "Request Headers"
   - Finden Sie die Zeile "Cookie:"
   - Kopieren Sie den GESAMTEN Cookie-Wert
   
7. 💾 Der Cookie sollte etwa so aussehen:
   Cookie: JSESSIONID=1234567890ABCDEF; seraph.confluence=abcdef123456; andere-cookies=werte

8. ▶️  Führen Sie dann aus:
   python confluence_sso.py --manual-login

═══════════════════════════════════════════════════════════

🛡️  SICHERHEITSHINWEIS:
- Cookies enthalten Ihre Anmeldedaten
- Teilen Sie diese niemals mit anderen
- Cookies laufen normalerweise nach einigen Stunden ab
- Sie müssen den Vorgang wiederholen wenn Cookies ablaufen

═══════════════════════════════════════════════════════════

❓ PROBLEMBEHEBUNG:

Problem: "rest/api/space" gibt 401 zurück
Lösung: Sie sind nicht richtig eingeloggt, wiederholen Sie den SSO-Login

Problem: Keine Cookies sichtbar
Lösung: Stellen Sie sicher, dass Sie in Confluence eingeloggt sind

Problem: Page nicht gefunden  
Lösung: Prüfen Sie, ob Sie Berechtigung für den RACOON Space haben

═══════════════════════════════════════════════════════════

🚀 Sobald Sie die Cookies haben, können Sie:
   - Alle Spaces auflisten
   - RACOON Publikationsseite bearbeiten  
   - Automatische Updates durchführen

═══════════════════════════════════════════════════════════
""")