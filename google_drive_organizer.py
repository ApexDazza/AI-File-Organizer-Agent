"""
Google Drive Cloud File Organizer
================================
Organizes files directly in Google Drive cloud storage using AI.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

try:
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    print("✅ Google Drive API libraries available")
except ImportError as e:
    print(f"❌ Missing Google Drive API libraries: {e}")
    print("Install with: pip install google-api-python-client google-auth google-auth-oauthlib")

class GoogleDriveCloudOrganizer:
    """Organizes files in Google Drive cloud storage using AI."""
    
    # Google Drive API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/drive',  # Full access to organize files
        'https://www.googleapis.com/auth/drive.file'  # Access to files
    ]
    
    def __init__(self):
        load_dotenv()
        self.service = None
        self.gemini_api_key = os.getenv('GOOGLE_API_KEY')
        self.credentials_file = 'google_drive_credentials.json'
        self.token_file = 'google_drive_token.json'
        
    def setup_google_drive_auth(self):
        """Set up Google Drive authentication."""
        print("🔐 Setting up Google Drive authentication...")
        
        creds = None
        # Load existing token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("\n🚨 GOOGLE DRIVE SETUP REQUIRED:")
                print("1. Go to: https://console.cloud.google.com/")
                print("2. Create a new project or select existing")
                print("3. Enable Google Drive API")
                print("4. Create OAuth 2.0 credentials (Desktop application)")
                print("5. Download credentials.json file")
                print("6. Save it as 'google_drive_credentials.json' in this folder")
                print()
                
                if not os.path.exists(self.credentials_file):
                    print(f"❌ Credentials file not found: {self.credentials_file}")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('drive', 'v3', credentials=creds)
        print("✅ Google Drive authentication successful!")
        return True
    
    def extract_folder_id(self, drive_url: str) -> str:
        """Extract folder ID from Google Drive URL."""
        # URL format: https://drive.google.com/drive/folders/FOLDER_ID
        if '/folders/' in drive_url:
            return drive_url.split('/folders/')[-1].split('?')[0]
        return drive_url
    
    def list_files_in_folder(self, folder_id: str) -> List[Dict]:
        """List all files in a specific Google Drive folder."""
        if not self.service:
            print("❌ Google Drive not authenticated")
            return []
        
        try:
            print(f"📋 Listing files in folder: {folder_id}")
            
            # Query to get files in specific folder
            query = f"'{folder_id}' in parents and trashed=false"
            
            results = self.service.files().list(
                q=query,
                fields="files(id, name, mimeType, size, createdTime, modifiedTime, parents)"
            ).execute()
            
            files = results.get('files', [])
            
            print(f"📊 Found {len(files)} files")
            
            # Process files for better information
            file_info = []
            for file in files:
                # Skip folders for now, focus on files
                if file['mimeType'] != 'application/vnd.google-apps.folder':
                    size_mb = int(file.get('size', 0)) / (1024 * 1024) if file.get('size') else 0
                    file_info.append({
                        'id': file['id'],
                        'name': file['name'],
                        'mimeType': file['mimeType'],
                        'size_mb': round(size_mb, 2),
                        'created': file.get('createdTime', ''),
                        'modified': file.get('modifiedTime', ''),
                        'parents': file.get('parents', [])
                    })
            
            return file_info
            
        except Exception as e:
            print(f"❌ Error listing files: {e}")
            return []
    
    def analyze_files_with_ai(self, files: List[Dict]) -> Dict:
        """Analyze files using Gemini AI for organization."""
        if not self.gemini_api_key:
            print("❌ Gemini API key not configured")
            return {}
        
        if not files:
            print("📁 No files to analyze")
            return {}
        
        # Configure Gemini
        genai.configure(api_key=self.gemini_api_key)
        
        # Prepare file information for AI
        file_descriptions = []
        for file in files[:20]:  # Limit to avoid token limits
            desc = f"- {file['name']} ({file['mimeType']}, {file['size_mb']} MB)"
            file_descriptions.append(desc)
        
        prompt = f"""
        Analyze these Google Drive files and create an organization plan:
        
        Files to organize:
        {chr(10).join(file_descriptions)}
        
        Create a JSON response with this structure:
        {{
            "folders": [
                {{
                    "name": "Professional Documents",
                    "description": "Work-related files and documents",
                    "files": [
                        {{
                            "current_name": "filename.ext",
                            "suggested_name": "better_filename.ext",
                            "reason": "Why this organization makes sense"
                        }}
                    ]
                }}
            ]
        }}
        
        Rules:
        1. Create 3-6 logical folder categories
        2. Use clear, professional folder names
        3. Group related files together
        4. Consider file types and apparent purposes
        5. Suggest better names where helpful
        
        Respond with ONLY valid JSON.
        """
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            print("🤖 Analyzing files with Gemini AI...")
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up response
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].strip()
            
            organization_plan = json.loads(response_text)
            return organization_plan
            
        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            return {}
    
    def create_folders_in_drive(self, folder_names: List[str], parent_folder_id: str) -> Dict[str, str]:
        """Create folders in Google Drive."""
        created_folders = {}
        
        for folder_name in folder_names:
            try:
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [parent_folder_id]
                }
                
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                
                created_folders[folder_name] = folder.get('id')
                print(f"📁 Created folder: {folder_name}")
                
            except Exception as e:
                print(f"❌ Error creating folder {folder_name}: {e}")
        
        return created_folders
    
    def move_file_in_drive(self, file_id: str, new_parent_id: str, old_parent_id: str):
        """Move a file to a different folder in Google Drive."""
        try:
            # Remove from old parent and add to new parent
            self.service.files().update(
                fileId=file_id,
                addParents=new_parent_id,
                removeParents=old_parent_id,
                fields='id, parents'
            ).execute()
            return True
        except Exception as e:
            print(f"❌ Error moving file: {e}")
            return False
    
    def rename_file_in_drive(self, file_id: str, new_name: str):
        """Rename a file in Google Drive."""
        try:
            self.service.files().update(
                fileId=file_id,
                body={'name': new_name}
            ).execute()
            return True
        except Exception as e:
            print(f"❌ Error renaming file: {e}")
            return False
    
    def organize_google_drive_folder(self, drive_url: str):
        """Main method to organize a Google Drive folder."""
        print("🎯 GOOGLE DRIVE CLOUD ORGANIZER")
        print("=" * 50)
        
        # Setup authentication
        if not self.setup_google_drive_auth():
            return
        
        # Extract folder ID
        folder_id = self.extract_folder_id(drive_url)
        print(f"📂 Target folder ID: {folder_id}")
        
        # List files
        files = self.list_files_in_folder(folder_id)
        if not files:
            print("📁 No files found to organize")
            return
        
        # Analyze with AI
        organization_plan = self.analyze_files_with_ai(files)
        if not organization_plan:
            print("❌ Failed to create organization plan")
            return
        
        # Display plan
        self.display_organization_plan(organization_plan)
        
        # Confirm execution
        confirm = input("\n🚀 Execute this organization plan? (yes/no): ").lower().strip()
        if confirm in ['yes', 'y']:
            self.execute_organization_plan(organization_plan, files, folder_id)
        else:
            print("👍 Organization cancelled")
    
    def display_organization_plan(self, plan: Dict):
        """Display the AI organization plan."""
        print("\n🎯 AI ORGANIZATION PLAN")
        print("=" * 60)
        
        for folder in plan.get('folders', []):
            print(f"\n📁 {folder['name']}")
            print(f"   {folder['description']}")
            print("   " + "-" * 40)
            
            for file_plan in folder.get('files', []):
                current = file_plan['current_name']
                suggested = file_plan['suggested_name']
                reason = file_plan['reason']
                
                if current != suggested:
                    print(f"   📄 {current}")
                    print(f"   ➜  {suggested}")
                    print(f"      💡 {reason}")
                else:
                    print(f"   📄 {suggested}")
                    print(f"      💡 {reason}")
                print()
    
    def execute_organization_plan(self, plan: Dict, files: List[Dict], parent_folder_id: str):
        """Execute the organization plan in Google Drive."""
        print("\n🚀 EXECUTING ORGANIZATION PLAN")
        print("=" * 50)
        
        # Create folders
        folder_names = [f['name'] for f in plan.get('folders', [])]
        created_folders = self.create_folders_in_drive(folder_names, parent_folder_id)
        
        # Create file mapping
        files_by_name = {f['name']: f for f in files}
        
        # Move and rename files
        moved_count = 0
        renamed_count = 0
        
        for folder in plan.get('folders', []):
            folder_name = folder['name']
            folder_id = created_folders.get(folder_name)
            
            if not folder_id:
                print(f"❌ Failed to create folder: {folder_name}")
                continue
            
            for file_plan in folder.get('files', []):
                current_name = file_plan['current_name']
                suggested_name = file_plan['suggested_name']
                
                file_info = files_by_name.get(current_name)
                if not file_info:
                    print(f"⚠️  File not found: {current_name}")
                    continue
                
                file_id = file_info['id']
                old_parent = file_info['parents'][0] if file_info['parents'] else parent_folder_id
                
                # Move file to new folder
                if self.move_file_in_drive(file_id, folder_id, old_parent):
                    moved_count += 1
                    print(f"✅ Moved: {current_name} → {folder_name}/")
                    
                    # Rename if different
                    if current_name != suggested_name:
                        if self.rename_file_in_drive(file_id, suggested_name):
                            renamed_count += 1
                            print(f"✅ Renamed: {current_name} → {suggested_name}")
                        else:
                            print(f"⚠️  Failed to rename: {current_name}")
                else:
                    print(f"❌ Failed to move: {current_name}")
        
        print(f"\n🎉 ORGANIZATION COMPLETE!")
        print(f"📁 Created {len(created_folders)} folders")
        print(f"📄 Moved {moved_count} files")
        print(f"🏷️  Renamed {renamed_count} files")

if __name__ == "__main__":
    organizer = GoogleDriveCloudOrganizer()
    
    # Your Google Drive folder
    drive_url = "https://drive.google.com/drive/folders/16pBA0uQYgf8afI4b3mEPDDLWdeloSclG"
    
    organizer.organize_google_drive_folder(drive_url)