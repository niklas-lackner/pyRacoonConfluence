#!/usr/bin/env python3
"""
Publication Management Example
=============================

This example shows how to manage RACOON publications programmatically:
- Add new publication entries
- Update existing entries
- Handle status macros (JA/NEIN)
- Create safe backups

Usage:
    python publication_management.py

Prerequisites:
    - Working SSO authentication
    - Access to RACOON publications page
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from confluence_sso import ConfluenceSSO


def create_status_macro(status="JA"):
    """Create a Confluence status macro."""
    color = "Green" if status == "JA" else "Red"
    return f'<ac:structured-macro ac:name="status" ac:schema-version="1" ac:macro-id="status-macro"><ac:parameter ac:name="colour">{color}</ac:parameter><ac:parameter ac:name="title">{status}</ac:parameter></ac:structured-macro>'


def create_publication_row(nummer, jahr_monat, standort, personen, foerder_status="JA", pubmed_doi=""):
    """Create a new publication table row."""
    
    foerder_macro = create_status_macro(foerder_status)
    
    return f"""
    <tr>
        <td><p>{nummer}</p></td>
        <td><p>{jahr_monat}</p></td>
        <td><p>{standort}</p></td>
        <td><p>{personen}</p></td>
        <td><p>{foerder_macro}</p></td>
        <td><p>{pubmed_doi}</p></td>
    </tr>"""


def add_publication_to_table(content, publication_data):
    """Add a new publication to the existing table."""
    
    # Find the table structure
    table_end = content.rfind("</tbody>")
    
    if table_end == -1:
        raise ValueError("Could not find table structure in content")
    
    # Create the new row
    new_row = create_publication_row(**publication_data)
    
    # Insert the new row before the closing </tbody> tag
    updated_content = content[:table_end] + new_row + content[table_end:]
    
    return updated_content


def main():
    """Main demonstration function."""
    
    print("📊 pyRacoonConfluence - Publication Management Example")
    print("=" * 55)
    
    # Configuration
    base_url = "https://wms.diz-ag.med.ovgu.de"
    page_id = "165485055"  # RACOON Publications page
    
    # Initialize connection
    confluence = ConfluenceSSO(base_url)
    
    # Step 1: Authentication
    print("\n🔐 Step 1: SSO Authentication")
    print("-" * 32)
    
    cookies = input("Enter your browser cookies: ")
    
    try:
        confluence.login_with_cookies(cookies)
        print("✅ Authentication successful!")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return
    
    # Step 2: Get current page content
    print("\n📖 Step 2: Retrieving Current Content")
    print("-" * 40)
    
    try:
        page = confluence.get_page(page_id, "title,body.storage,version")
        current_version = page['version']['number']
        print(f"✅ Retrieved page: {page['title']}")
        print(f"   Current version: {current_version}")
    except Exception as e:
        print(f"❌ Failed to retrieve page: {e}")
        return
    
    # Step 3: Create backup
    print("\n💾 Step 3: Creating Backup")
    print("-" * 27)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"racoon_publications_backup_{timestamp}.html"
    
    try:
        with open(backup_filename, 'w', encoding='utf-8') as f:
            f.write(page['body']['storage']['value'])
        print(f"✅ Backup saved: {backup_filename}")
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return
    
    # Step 4: Prepare new publication data
    print("\n📝 Step 4: New Publication Data")
    print("-" * 32)
    
    print("Please enter the publication details:")
    
    publication = {
        'nummer': input("Publication number: "),
        'jahr_monat': input("Year/Month (YYYY/MM): "),
        'standort': input("Institution/Location: "),
        'personen': input("Authors: "),
        'foerder_status': input("Funding acknowledgment (JA/NEIN) [JA]: ") or "JA",
        'pubmed_doi': input("PubMed DOI (optional): ")
    }
    
    print(f"\n📋 Publication Summary:")
    for key, value in publication.items():
        print(f"   {key}: {value}")
    
    # Step 5: Confirmation
    print("\n⚠️  Step 5: Confirmation")
    print("-" * 23)
    
    confirm = input("Add this publication to Confluence? (y/N): ").lower()
    
    if confirm != 'y':
        print("❌ Operation cancelled by user.")
        return
    
    # Step 6: Add publication
    print("\n🚀 Step 6: Adding Publication")
    print("-" * 30)
    
    try:
        # Update the content
        updated_content = add_publication_to_table(
            page['body']['storage']['value'], 
            publication
        )
        
        # Update the page
        result = confluence.update_page(
            page_id=page_id,
            title=page['title'],
            content=updated_content,
            current_version=current_version
        )
        
        if result:
            new_version = current_version + 1
            print(f"✅ Publication added successfully!")
            print(f"   Page updated to version: {new_version}")
            print(f"   Backup available: {backup_filename}")
        else:
            print("❌ Failed to update page")
            
    except Exception as e:
        print(f"❌ Failed to add publication: {e}")
        print(f"   Backup available: {backup_filename}")
        return
    
    print("\n🎉 Publication Management Example Completed!")
    print("\nWhat happened:")
    print(f"  ✅ Added new publication #{publication['nummer']}")
    print(f"  ✅ Updated RACOON publications table")
    print(f"  ✅ Incremented page version ({current_version} → {new_version})")
    print(f"  ✅ Created safety backup: {backup_filename}")


if __name__ == "__main__":
    main()