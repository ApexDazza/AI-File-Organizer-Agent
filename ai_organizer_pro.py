"""
AI File Organizer - Full Implementation
======================================
This script actually moves and organizes files based on Gemini AI analysis.
Includes safety features: backups, confirmation, and detailed logging.
"""

import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime
import json
import re

class FileOrganizerPro:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.target_dir = Path(os.getenv('DEFAULT_TARGET_DIR', 'C:/Users/darre/OneDrive/Documents'))
        self.backup_dir = None
        self.organization_plan = {}
        
    def create_backup(self):
        """Create a backup of the target directory."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_before_ai_organization_{timestamp}"
        self.backup_dir = self.target_dir.parent / backup_name
        
        print(f"📦 Creating backup: {self.backup_dir}")
        
        try:
            # Create backup directory
            self.backup_dir.mkdir(exist_ok=True)
            
            # Copy all files (not subdirectories for this demo)
            files_copied = 0
            for item in self.target_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, self.backup_dir / item.name)
                    files_copied += 1
            
            print(f"✅ Backup completed: {files_copied} files backed up")
            return True
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def analyze_files_with_ai(self):
        """Analyze files and get organization recommendations from AI."""
        if not self.api_key:
            print("❌ No Gemini API key found")
            return False
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Get files to analyze
        files = [f for f in self.target_dir.iterdir() if f.is_file()]
        
        if not files:
            print("📁 No files found to organize")
            return False
        
        print(f"📋 Analyzing {len(files)} files...")
        
        # Prepare file information
        file_info = []
        for file_path in files:
            try:
                stat = file_path.stat()
                file_info.append({
                    'name': file_path.name,
                    'size': stat.st_size,
                    'extension': file_path.suffix.lower(),
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d'),
                    'path': str(file_path)
                })
            except Exception as e:
                print(f"⚠️  Skipping {file_path.name}: {e}")
        
        # Create AI prompt
        prompt = f"""
        You are a professional file organization expert. Analyze these files and create a structured organization plan.
        
        Files to organize:
        {chr(10).join([f"- {f['name']} ({f['extension']}, {f['size']} bytes, modified: {f['modified']})" for f in file_info])}
        
        Please respond with ONLY a valid JSON structure like this:
        {{
            "categories": {{
                "folder_name": {{
                    "description": "What this folder contains",
                    "files": [
                        {{
                            "current_name": "original_filename.ext",
                            "new_name": "suggested_new_name.ext",
                            "reason": "Why this organization makes sense"
                        }}
                    ]
                }}
            }}
        }}
        
        Rules:
        1. Create 3-6 logical folder categories
        2. Use clear, professional folder names (no numbers/prefixes unless necessary)
        3. Suggest better file names where appropriate
        4. Group related files together
        5. Keep existing extensions
        6. Make folder names filesystem-safe (no special characters)
        
        Respond with ONLY the JSON, no other text.
        """
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            print("🤖 Getting AI recommendations...")
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up the response to extract JSON
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].strip()
            
            # Parse the JSON response
            self.organization_plan = json.loads(response_text)
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse AI response as JSON: {e}")
            print(f"Raw response: {response.text[:200]}...")
            return False
        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            return False
    
    def display_organization_plan(self):
        """Display the organization plan to the user."""
        if not self.organization_plan:
            print("❌ No organization plan available")
            return
        
        print("\n" + "="*80)
        print("🎯 AI ORGANIZATION PLAN")
        print("="*80)
        
        total_files = 0
        for folder_name, folder_info in self.organization_plan['categories'].items():
            files_count = len(folder_info['files'])
            total_files += files_count
            
            print(f"\n📁 {folder_name}/ ({files_count} files)")
            print(f"   📝 {folder_info['description']}")
            print("   " + "-"*50)
            
            for file_op in folder_info['files']:
                current = file_op['current_name']
                new = file_op['new_name']
                reason = file_op.get('reason', '')
                
                if current != new:
                    print(f"   📄 {current}")
                    print(f"   ➜  {new}")
                    if reason:
                        print(f"      💡 {reason}")
                else:
                    print(f"   📄 {new}")
                    if reason:
                        print(f"      💡 {reason}")
                print()
        
        print(f"📊 Total: {total_files} files will be organized into {len(self.organization_plan['categories'])} folders")
    
    def execute_organization(self):
        """Actually move and organize the files."""
        if not self.organization_plan:
            print("❌ No organization plan to execute")
            return False
        
        print("\n🚀 EXECUTING ORGANIZATION PLAN")
        print("="*50)
        
        moved_files = 0
        created_folders = 0
        
        try:
            for folder_name, folder_info in self.organization_plan['categories'].items():
                # Create the folder
                folder_path = self.target_dir / folder_name
                if not folder_path.exists():
                    folder_path.mkdir()
                    print(f"📁 Created folder: {folder_name}/")
                    created_folders += 1
                
                # Move files to the folder
                for file_op in folder_info['files']:
                    current_name = file_op['current_name']
                    new_name = file_op['new_name']
                    
                    current_path = self.target_dir / current_name
                    new_path = folder_path / new_name
                    
                    if current_path.exists():
                        # Handle potential filename conflicts
                        if new_path.exists():
                            base, ext = new_path.stem, new_path.suffix
                            counter = 1
                            while new_path.exists():
                                new_path = folder_path / f"{base}_{counter}{ext}"
                                counter += 1
                            print(f"⚠️  Renamed to avoid conflict: {new_path.name}")
                        
                        # Move the file
                        shutil.move(str(current_path), str(new_path))
                        print(f"✅ Moved: {current_name} → {folder_name}/{new_path.name}")
                        moved_files += 1
                    else:
                        print(f"⚠️  File not found: {current_name}")
            
            print(f"\n🎉 SUCCESS!")
            print(f"📊 Created {created_folders} folders")
            print(f"📊 Moved {moved_files} files")
            print(f"💾 Backup available at: {self.backup_dir}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during organization: {e}")
            print(f"💾 Your files are safe in backup: {self.backup_dir}")
            return False
    
    def run(self):
        """Main execution flow."""
        print("🎯 AI FILE ORGANIZER PRO")
        print("="*50)
        print(f"📂 Target Directory: {self.target_dir}")
        
        if not self.target_dir.exists():
            print(f"❌ Directory not found: {self.target_dir}")
            return
        
        # Step 1: Create backup
        print("\n🔒 STEP 1: Creating Safety Backup")
        if not self.create_backup():
            return
        
        # Step 2: AI Analysis
        print("\n🤖 STEP 2: AI Analysis")
        if not self.analyze_files_with_ai():
            return
        
        # Step 3: Show plan
        print("\n📋 STEP 3: Review Organization Plan")
        self.display_organization_plan()
        
        # Step 4: Confirmation
        print("\n❓ STEP 4: Confirmation")
        print("="*50)
        confirm = input("🚀 Proceed with this organization? (yes/no): ").lower().strip()
        
        if confirm in ['yes', 'y']:
            # Step 5: Execute
            print("\n⚡ STEP 5: Executing Organization")
            if self.execute_organization():
                print("\n🎊 All done! Your files are now professionally organized!")
            else:
                print("\n💔 Organization failed, but your files are safe in the backup.")
        else:
            print("\n👍 Organization cancelled. No files were moved.")
            print(f"💾 Backup created at: {self.backup_dir}")


if __name__ == "__main__":
    organizer = FileOrganizerPro()
    organizer.run()