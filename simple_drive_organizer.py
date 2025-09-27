"""
Simplified Google Drive Organizer - Service Account Method
=========================================================
Uses service account authentication to avoid OAuth consent issues.
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
    from google.oauth2 import service_account
    print("✅ Google Drive API libraries available")
except ImportError as e:
    print(f"❌ Missing Google Drive API libraries: {e}")

class SimpleGoogleDriveOrganizer:
    """Simplified Google Drive organizer using service account or API key."""
    
    def __init__(self):
        load_dotenv()
        self.service = None
        self.gemini_api_key = os.getenv('GOOGLE_API_KEY')
        
    def setup_service_account_auth(self):
        """Set up service account authentication (simpler than OAuth)."""
        print("🔐 Setting up service account authentication...")
        
        # Check for service account key file
        service_account_file = 'service_account_key.json'
        
        if os.path.exists(service_account_file):
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    service_account_file,
                    scopes=['https://www.googleapis.com/auth/drive']
                )
                self.service = build('drive', 'v3', credentials=credentials)
                print("✅ Service account authentication successful!")
                return True
            except Exception as e:
                print(f"❌ Service account auth failed: {e}")
        
        print("\n📋 SERVICE ACCOUNT SETUP NEEDED:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Navigate to 'IAM & Admin' → 'Service Accounts'")
        print("3. Click 'CREATE SERVICE ACCOUNT'")
        print("4. Name: 'ai-file-organizer'")
        print("5. Grant role: 'Editor' or 'Drive API Admin'")
        print("6. Click 'CREATE AND CONTINUE'")
        print("7. Click 'CREATE KEY' → 'JSON'")
        print("8. Save as 'service_account_key.json' in this folder")
        print("9. Share your Google Drive folder with the service account email")
        print()
        
        return False
    
    def analyze_drive_folder_readonly(self, folder_id: str):
        """Analyze folder contents without making changes (for demo)."""
        print("🔍 DEMO MODE: Analyzing Google Drive Folder")
        print("=" * 50)
        print(f"📂 Folder ID: {folder_id}")
        print()
        
        # Since we can't access the actual folder yet, let's simulate
        print("📋 This is what the organizer would do:")
        print("1. ✅ Connect to Google Drive API")
        print("2. ✅ List all files in your folder")
        print("3. ✅ Analyze files with Gemini AI")
        print("4. ✅ Create organization plan")
        print("5. ✅ Show plan for your approval")
        print("6. ✅ Execute organization (create folders, move files)")
        print()
        
        # Use Gemini to analyze what we might expect
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = """
            You are analyzing a typical user's Google Drive folder that might need organization.
            
            Create a realistic example of what files might be found and how they should be organized.
            
            Respond with a JSON structure showing:
            {
                "estimated_files": [
                    {"name": "example1.pdf", "type": "document"},
                    {"name": "photo.jpg", "type": "image"}
                ],
                "organization_plan": {
                    "folders": [
                        {
                            "name": "Documents",
                            "description": "PDF files and documents",
                            "file_count": 5
                        }
                    ]
                }
            }
            
            Make it realistic for a typical user's messy Google Drive.
            """
            
            try:
                response = model.generate_content(prompt)
                print("🤖 AI Analysis Example:")
                print(response.text)
            except Exception as e:
                print(f"⚠️  AI analysis demo failed: {e}")
        
        print("\n💡 To organize your actual Google Drive:")
        print("1. Complete the service account setup above, OR")
        print("2. Add your email as a test user in OAuth consent screen")
        print("3. Run the organizer again")

def main():
    organizer = SimpleGoogleDriveOrganizer()
    
    print("🎯 GOOGLE DRIVE ORGANIZER")
    print("=" * 40)
    
    # Your folder ID
    folder_id = "16pBA0uQYgf8afI4b3mEPDDLWdeloSclG"
    
    # Try service account first
    if organizer.setup_service_account_auth():
        print("🚀 Ready to organize! (Service Account)")
        # Would proceed with actual organization
    else:
        print("📋 Running in demo mode...")
        organizer.analyze_drive_folder_readonly(folder_id)

if __name__ == "__main__":
    main()