"""
Google Drive Final Organizer - Move Remaining Files
==================================================
Moves the remaining 20 files from root into appropriate existing folders.
"""

import os
import json
from typing import Dict, List
import google.generativeai as genai
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class FinalGoogleDriveOrganizer:
    """Organizes remaining files into existing folders."""
    
    def __init__(self):
        load_dotenv()
        self.service = None
        self.gemini_api_key = os.getenv('GOOGLE_API_KEY')
        self.folder_id = "16pBA0uQYgf8afI4b3mEPDDLWdeloSclG"
        
    def setup_auth(self):
        """Setup Google Drive authentication using existing token."""
        if not os.path.exists('google_drive_token.json'):
            print("❌ No authentication token found. Run google_drive_organizer.py first.")
            return False
        
        try:
            creds = Credentials.from_authorized_user_file('google_drive_token.json')
            self.service = build('drive', 'v3', credentials=creds)
            print("✅ Google Drive authentication successful!")
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def get_folder_structure(self):
        """Get all folders in the target directory."""
        try:
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'",
                fields="files(id, name)"
            ).execute()
            
            folders = results.get('files', [])
            folder_map = {folder['name']: folder['id'] for folder in folders}
            
            print(f"📁 Found {len(folders)} existing folders:")
            for folder_name in sorted(folder_map.keys()):
                print(f"   - {folder_name}")
            
            return folder_map
            
        except Exception as e:
            print(f"❌ Error getting folders: {e}")
            return {}
    
    def get_remaining_files(self):
        """Get all files still in the root folder."""
        try:
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'",
                fields="files(id, name, mimeType, size)"
            ).execute()
            
            files = results.get('files', [])
            
            print(f"\n📄 Found {len(files)} files to organize:")
            for i, file in enumerate(files[:10], 1):  # Show first 10
                size_mb = int(file.get('size', 0)) / (1024 * 1024) if file.get('size') else 0
                print(f"   {i:2d}. {file['name']} ({size_mb:.1f} MB)")
            
            if len(files) > 10:
                print(f"       ... and {len(files) - 10} more files")
            
            return files
            
        except Exception as e:
            print(f"❌ Error getting files: {e}")
            return []
    
    def analyze_file_placement(self, files: List[Dict], folders: Dict[str, str]) -> Dict:
        """Use AI to determine which folder each file should go into."""
        if not self.gemini_api_key:
            print("❌ Gemini API key not configured")
            return {}
        
        # Configure Gemini
        genai.configure(api_key=self.gemini_api_key)
        
        # Create file list for AI
        file_list = []
        for file in files:
            file_list.append(f"- {file['name']}")
        
        # Create folder list for AI
        folder_list = list(folders.keys())
        
        prompt = f"""
        I need to organize these files into existing folders. Analyze each file and determine the best folder.
        
        FILES TO ORGANIZE:
        {chr(10).join(file_list)}
        
        EXISTING FOLDERS:
        {chr(10).join(f"- {folder}" for folder in sorted(folder_list))}
        
        Create a JSON response with this exact structure:
        {{
            "file_placements": [
                {{
                    "file_name": "exact_file_name_from_list",
                    "target_folder": "exact_folder_name_from_list",
                    "reason": "brief explanation why this file belongs in this folder"
                }}
            ]
        }}
        
        Rules:
        1. Use EXACT file names and folder names as provided - copy them character for character
        2. DO NOT add file extensions or modify names in any way
        2. Match files logically to folders based on content/purpose
        3. Consider these mappings:
           - Personal documents → "Personal & Family Records" or "ID scans and documents"
           - Work/career items → "Professional & Career"
           - Medical/health → "Health & Wellness" 
           - Bills/purchases → "Household & Finance" or "Receipts"
           - Travel → "Travel & Leisure" or "Holiday"
           - Children → "Kids"
           - Food → "Dinners and Recipes"
           - Vehicle → "Car stuff"
           - Masonic → "Masonic"
        
        Respond with ONLY valid JSON.
        """
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            print("\n🤖 Analyzing file placements with AI...")
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up response
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].strip()
            
            placement_plan = json.loads(response_text)
            return placement_plan
            
        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            print(f"Raw response: {response.text[:200] if 'response' in locals() else 'No response'}")
            return {}
    
    def display_placement_plan(self, plan: Dict):
        """Display the file placement plan."""
        print("\n🎯 FILE PLACEMENT PLAN")
        print("=" * 50)
        
        placements = plan.get('file_placements', [])
        
        # Group by target folder
        by_folder = {}
        for placement in placements:
            folder = placement['target_folder']
            if folder not in by_folder:
                by_folder[folder] = []
            by_folder[folder].append(placement)
        
        for folder_name, file_placements in by_folder.items():
            print(f"\n📁 {folder_name} ({len(file_placements)} files)")
            print("   " + "-" * 40)
            for placement in file_placements:
                print(f"   📄 {placement['file_name']}")
                print(f"      💡 {placement['reason']}")
                print()
        
        print(f"📊 Total: {len(placements)} files will be organized")
    
    def execute_placement_plan(self, plan: Dict, files: List[Dict], folders: Dict[str, str]):
        """Execute the file placement plan."""
        print("\n🚀 EXECUTING FILE ORGANIZATION")
        print("=" * 40)
        
        # Create file mapping
        files_by_name = {f['name']: f for f in files}
        
        moved_count = 0
        error_count = 0
        
        for placement in plan.get('file_placements', []):
            file_name = placement['file_name']
            target_folder = placement['target_folder']
            
            # Find the file
            file_info = files_by_name.get(file_name)
            if not file_info:
                print(f"⚠️  File not found: {file_name}")
                error_count += 1
                continue
            
            # Find the target folder
            folder_id = folders.get(target_folder)
            if not folder_id:
                print(f"⚠️  Folder not found: {target_folder}")
                error_count += 1
                continue
            
            # Move the file
            try:
                self.service.files().update(
                    fileId=file_info['id'],
                    addParents=folder_id,
                    removeParents=self.folder_id,
                    fields='id, parents'
                ).execute()
                
                moved_count += 1
                print(f"✅ Moved: {file_name} → {target_folder}/")
                
            except Exception as e:
                print(f"❌ Failed to move {file_name}: {e}")
                error_count += 1
        
        print(f"\n🎉 ORGANIZATION COMPLETE!")
        print(f"✅ Successfully moved: {moved_count} files")
        if error_count > 0:
            print(f"⚠️  Errors: {error_count} files")
        
        return moved_count, error_count
    
    def run_final_organization(self):
        """Main method to organize remaining files."""
        print("🎯 FINAL GOOGLE DRIVE ORGANIZATION")
        print("=" * 45)
        
        # Setup authentication
        if not self.setup_auth():
            return
        
        # Get folder structure
        folders = self.get_folder_structure()
        if not folders:
            print("❌ No folders found")
            return
        
        # Get remaining files
        files = self.get_remaining_files()
        if not files:
            print("✅ No files to organize - everything is already in folders!")
            return
        
        # Analyze placements
        plan = self.analyze_file_placement(files, folders)
        if not plan:
            print("❌ Failed to create placement plan")
            return
        
        # Display plan
        self.display_placement_plan(plan)
        
        # Confirm execution
        print("\n" + "=" * 50)
        confirm = input(f"🚀 Move {len(plan.get('file_placements', []))} files to folders? (yes/no): ").lower().strip()
        
        if confirm in ['yes', 'y']:
            moved, errors = self.execute_placement_plan(plan, files, folders)
            
            if moved > 0:
                print(f"\n🎊 SUCCESS! Your Google Drive is now fully organized!")
                print(f"🔗 View results: https://drive.google.com/drive/folders/{self.folder_id}")
            
        else:
            print("👍 Organization cancelled. Files remain in root folder.")

if __name__ == "__main__":
    organizer = FinalGoogleDriveOrganizer()
    organizer.run_final_organization()