#!/usr/bin/env python3
"""
Basic SSO Login Example
======================

This example demonstrates how to establish an SSO connection to Confluence
and perform basic operations like listing spaces and reading pages.

Usage:
    python basic_login.py

Prerequisites:
    - Valid SSO session in your browser
    - Browser cookies extracted using cookie_help.py
"""

import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from confluence_sso import ConfluenceSSO


def main():
    """Main demonstration function."""
    
    # Initialize Confluence SSO connection
    base_url = "https://wms.diz-ag.med.ovgu.de"
    confluence = ConfluenceSSO(base_url)
    
    print("🔧 pyRacoonConfluence - Basic SSO Login Example")
    print("=" * 50)
    
    # Step 1: Login with cookies
    print("\n📋 Step 1: SSO Authentication")
    print("-" * 30)
    print("Please paste your browser cookies when prompted.")
    print("Use F12 > Application > Cookies to find them.")
    
    cookies = input("\nEnter cookies (format: JSESSIONID=...; seraph.confluence=...): ")
    
    try:
        confluence.login_with_cookies(cookies)
        print("✅ Successfully authenticated with SSO!")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return
    
    # Step 2: List available spaces
    print("\n📚 Step 2: Available Confluence Spaces")
    print("-" * 40)
    
    try:
        spaces = confluence.get_spaces()
        print(f"Found {len(spaces)} accessible spaces:")
        
        for i, space in enumerate(spaces, 1):
            print(f"  {i:2d}. {space['name']} (Key: {space['key']})")
            
    except Exception as e:
        print(f"❌ Failed to retrieve spaces: {e}")
        return
    
    # Step 3: Access RACOON space specifically
    print("\n🦝 Step 3: RACOON Space Access")
    print("-" * 35)
    
    racoon_space = None
    for space in spaces:
        if 'RACOON' in space['name']:
            racoon_space = space
            break
    
    if racoon_space:
        print(f"✅ Found RACOON space: {racoon_space['name']}")
        print(f"   Space Key: {racoon_space['key']}")
        print(f"   Space ID: {racoon_space['id']}")
    else:
        print("❌ RACOON space not found or not accessible")
        return
    
    # Step 4: Access publications page
    print("\n📊 Step 4: Publications Page Access")
    print("-" * 38)
    
    page_id = "165485055"  # RACOON Publications page
    
    try:
        page = confluence.get_page(page_id, "title,body.storage,version")
        
        if page:
            print(f"✅ Successfully accessed page: {page['title']}")
            print(f"   Page ID: {page['id']}")
            print(f"   Current Version: {page['version']['number']}")
            print(f"   Content Length: {len(page['body']['storage']['value']):,} characters")
        else:
            print("❌ Page not found or not accessible")
            
    except Exception as e:
        print(f"❌ Failed to access page: {e}")
        return
    
    print("\n🎉 Example completed successfully!")
    print("\nNext steps:")
    print("  1. Try racoon_test_update.py to add test data")
    print("  2. Explore other examples in this directory")
    print("  3. Check the main README.md for full documentation")


if __name__ == "__main__":
    main()