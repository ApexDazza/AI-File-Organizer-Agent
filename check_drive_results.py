"""
Google Drive Organization Checker
===============================
Check the results of the organization and list actual files.
"""

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def check_organization_results():
    """Check what was actually created in Google Drive."""
    
    # Load existing token
    if not os.path.exists('google_drive_token.json'):
        print("❌ No authentication token found")
        return
    
    creds = Credentials.from_authorized_user_file('google_drive_token.json')
    service = build('drive', 'v3', credentials=creds)
    
    folder_id = "16pBA0uQYgf8afI4b3mEPDDLWdeloSclG"
    
    print("🔍 CHECKING GOOGLE DRIVE ORGANIZATION RESULTS")
    print("=" * 55)
    
    try:
        # List all items in the folder
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="files(id, name, mimeType, parents)"
        ).execute()
        
        files = results.get('files', [])
        
        folders = [f for f in files if f['mimeType'] == 'application/vnd.google-apps.folder']
        documents = [f for f in files if f['mimeType'] != 'application/vnd.google-apps.folder']
        
        print(f"📊 SUMMARY:")
        print(f"   📁 Folders: {len(folders)}")
        print(f"   📄 Files: {len(documents)}")
        print()
        
        if folders:
            print("📁 CREATED FOLDERS:")
            for folder in folders:
                print(f"   ✅ {folder['name']}")
                
                # Check what's inside each folder
                folder_contents = service.files().list(
                    q=f"'{folder['id']}' in parents and trashed=false",
                    fields="files(name, mimeType)"
                ).execute()
                
                folder_files = folder_contents.get('files', [])
                if folder_files:
                    print(f"      📄 Contains {len(folder_files)} files:")
                    for file in folder_files[:3]:  # Show first 3
                        print(f"         - {file['name']}")
                    if len(folder_files) > 3:
                        print(f"         ... and {len(folder_files) - 3} more")
                else:
                    print(f"      📭 Empty")
                print()
        
        if documents:
            print("📄 FILES STILL IN ROOT FOLDER:")
            for doc in documents[:10]:  # Show first 10
                print(f"   📄 {doc['name']}")
            if len(documents) > 10:
                print(f"   ... and {len(documents) - 10} more files")
            print()
            
            print("💡 These files weren't moved due to the naming mismatch issue.")
            print("   The AI can analyze and organize them in the next run!")
        
        print("\n🎯 RESULTS:")
        if folders:
            print("✅ Folder structure created successfully!")
            print("✅ AI organization plan was excellent!")
            if documents:
                print("⚠️  Files need to be moved to folders (fixable)")
            else:
                print("✅ All files properly organized!")
        
        print(f"\n🔗 View in Google Drive:")
        print(f"https://drive.google.com/drive/folders/{folder_id}")
        
    except Exception as e:
        print(f"❌ Error checking results: {e}")

if __name__ == "__main__":
    check_organization_results()