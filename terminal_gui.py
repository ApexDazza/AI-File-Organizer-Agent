"""
AI File Organizer Agent - Simple Terminal Interface
==================================================
User-friendly command-line interface for the AI File Organizer Agent.
No external dependencies required - uses only Python standard library.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime
import subprocess

class SimpleTerminalGUI:
    """Simple terminal-based GUI for file organization"""
    
    def __init__(self):
        self.selected_folder = ""
        self.organization_style = "professional"
        self.enable_backup = True
        self.enable_content_analysis = True
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print("=" * 70)
        print("🤖 AI FILE ORGANIZER AGENT - TERMINAL INTERFACE")
        print("=" * 70)
        print("Intelligent file organization powered by AI")
        print("Local & Cloud Support • Professional Results")
        print("=" * 70)
        print()
    
    def print_status(self):
        """Print current status"""
        print("📊 CURRENT STATUS:")
        print(f"   📁 Selected Folder: {self.selected_folder or 'None selected'}")
        print(f"   🎨 Organization Style: {self.organization_style}")
        print(f"   🔒 Backup Enabled: {'Yes' if self.enable_backup else 'No'}")
        print(f"   🧠 AI Analysis: {'Yes' if self.enable_content_analysis else 'No'}")
        
        # Check API status
        api_status = self.check_api_status()
        print(f"   🔑 API Status: {api_status}")
        
        # Check organizer availability
        organizer_status = self.check_organizer_status()
        print(f"   ⚙️ Organizer: {organizer_status}")
        print()
    
    def check_api_status(self):
        """Check if API is configured"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key and api_key != 'your_gemini_pro_api_key_here':
                return "✅ Configured"
            else:
                return "❌ Not configured"
        except ImportError:
            return "⚠️ dotenv not installed"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def check_organizer_status(self):
        """Check organizer availability"""
        if os.path.exists('ai_organizer_pro.py'):
            return "✅ AI Organizer Pro available"
        elif os.path.exists('ultimate_file_organizer.py'):
            return "✅ Ultimate Organizer available"
        else:
            return "⚠️ No organizer found"
    
    def show_main_menu(self):
        """Display main menu"""
        print("📋 MAIN MENU:")
        print("   1. 📁 Select folder to organize")
        print("   2. 🔍 Analyze selected folder")
        print("   3. 🚀 Organize files")
        print("   4. ☁️ Google Drive operations")
        print("   5. ⚙️ Settings")
        print("   6. 📊 View recent results")
        print("   7. ❓ Help & Documentation")
        print("   8. 🚪 Exit")
        print()
    
    def get_user_choice(self, prompt="Enter your choice: ", valid_choices=None):
        """Get user input with validation"""
        while True:
            try:
                choice = input(prompt).strip()
                if valid_choices and choice not in valid_choices:
                    print(f"❌ Invalid choice. Please select from: {', '.join(valid_choices)}")
                    continue
                return choice
            except KeyboardInterrupt:
                print("\\n👋 Goodbye!")
                sys.exit(0)
    
    def select_folder(self):
        """Folder selection menu"""
        while True:
            self.clear_screen()
            self.print_header()
            print("📁 FOLDER SELECTION")
            print("-" * 30)
            print()
            
            if self.selected_folder:
                print(f"📂 Currently selected: {self.selected_folder}")
                print()
            
            print("Quick Options:")
            print("   1. Enter custom path")
            print("   2. Downloads folder")
            print("   3. Documents folder")
            print("   4. Desktop folder")
            print("   5. Pictures folder")
            print("   6. Back to main menu")
            print()
            
            choice = self.get_user_choice("Select option (1-6): ", ['1', '2', '3', '4', '5', '6'])
            
            if choice == '1':
                print("\n💡 Tips:")
                print("   • Use full path like: C:\\Users\\YourName\\Documents")
                print("   • Or use ~ for home directory like: ~/Downloads")
                print("   • Press Enter without typing to cancel")
                print()
                
                path = input("Enter folder path: ").strip().strip('"')
                
                if not path:  # User pressed Enter without input
                    continue
                    
                # Expand ~ to home directory and normalize path
                if path.startswith('~'):
                    path = os.path.expanduser(path)
                
                # Normalize path separators for Windows
                path = os.path.normpath(path)
                
                # Check if path exists and is a directory
                if os.path.exists(path) and os.path.isdir(path):
                    self.selected_folder = path
                    print(f"\n✅ Successfully selected: {path}")
                    
                    # Show some folder info
                    try:
                        file_count = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
                        folder_count = len([f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))])
                        print(f"📊 Contains: {file_count} files, {folder_count} folders")
                    except PermissionError:
                        print("⚠️ Limited access to folder contents")
                    except Exception:
                        pass
                    
                    input("\nPress Enter to return to main menu...")
                    return
                else:
                    if not os.path.exists(path):
                        print(f"\n❌ Path does not exist: {path}")
                    elif not os.path.isdir(path):
                        print(f"\n❌ Path is not a directory: {path}")
                    else:
                        print(f"\n❌ Cannot access path: {path}")
                    
                    print("\n💡 Common Windows paths:")
                    print(f"   • C:\\Users\\{os.environ.get('USERNAME', 'YourName')}\\Documents")
                    print(f"   • C:\\Users\\{os.environ.get('USERNAME', 'YourName')}\\Downloads")
                    print(f"   • C:\\Users\\{os.environ.get('USERNAME', 'YourName')}\\Desktop")
                    
                    retry = self.get_user_choice("\nTry again? (y/N): ").lower()
                    if retry not in ['y', 'yes']:
                        continue
            
            elif choice == '2':
                path = os.path.expanduser("~/Downloads")
                if os.path.exists(path) and os.path.isdir(path):
                    self.selected_folder = path
                    print(f"\n✅ Selected Downloads: {path}")
                    input("\nPress Enter to return to main menu...")
                    return
                else:
                    print("\n❌ Downloads folder not found")
                    input("\nPress Enter to continue...")
                    
            elif choice == '3':
                path = os.path.expanduser("~/Documents")
                if os.path.exists(path) and os.path.isdir(path):
                    self.selected_folder = path
                    print(f"\n✅ Selected Documents: {path}")
                    input("\nPress Enter to return to main menu...")
                    return
                else:
                    print("\n❌ Documents folder not found")
                    input("\nPress Enter to continue...")
                    
            elif choice == '4':
                path = os.path.expanduser("~/Desktop")
                if os.path.exists(path) and os.path.isdir(path):
                    self.selected_folder = path
                    print(f"\n✅ Selected Desktop: {path}")
                    input("\nPress Enter to return to main menu...")
                    return
                else:
                    print("\n❌ Desktop folder not found")
                    input("\nPress Enter to continue...")
                    
            elif choice == '5':
                path = os.path.expanduser("~/Pictures")
                if os.path.exists(path) and os.path.isdir(path):
                    self.selected_folder = path
                    print(f"\n✅ Selected Pictures: {path}")
                    input("\nPress Enter to return to main menu...")
                    return
                else:
                    print("\n❌ Pictures folder not found")
                    input("\nPress Enter to continue...")
                    
            elif choice == '6':
                return
    
    def analyze_folder(self):
        """Analyze the selected folder"""
        if not self.selected_folder:
            print("❌ No folder selected. Please select a folder first.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        print("🔍 FOLDER ANALYSIS")
        print("-" * 25)
        print(f"Analyzing: {self.selected_folder}")
        print()
        
        try:
            # Try to use the actual organizer
            sys.path.insert(0, os.path.dirname(__file__))
            
            organizer = None
            try:
                from ai_organizer_pro import AIFileOrganizerPro
                organizer = AIFileOrganizerPro()
                print("✅ Using AI Organizer Pro")
            except ImportError:
                try:
                    from ultimate_file_organizer import UltimateFileOrganizer  
                    organizer = UltimateFileOrganizer()
                    print("✅ Using Ultimate File Organizer")
                except ImportError:
                    print("⚠️ Using basic analysis (AI components not available)")
            
            print("🔍 Scanning files...")
            
            if organizer and hasattr(organizer, 'analyze_files'):
                analysis = organizer.analyze_files(self.selected_folder)
                self.display_analysis_result(analysis)
            else:
                # Basic analysis
                analysis = self.basic_folder_analysis(self.selected_folder)
                self.display_basic_analysis(analysis)
                
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
        
        print()
        input("Press Enter to continue...")
    
    def basic_folder_analysis(self, folder_path):
        """Basic folder analysis when AI is not available"""
        analysis = {
            'total_files': 0,
            'file_types': {},
            'size_distribution': {},
            'folders': 0
        }
        
        try:
            for root, dirs, files in os.walk(folder_path):
                if root == folder_path:
                    analysis['folders'] = len(dirs)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    analysis['total_files'] += 1
                    
                    # Track file extensions
                    ext = os.path.splitext(file)[1].lower()
                    if not ext:
                        ext = 'No extension'
                    analysis['file_types'][ext] = analysis['file_types'].get(ext, 0) + 1
                    
                    # Basic size categorization
                    try:
                        size = os.path.getsize(file_path)
                        if size < 1024*1024:  # < 1MB
                            size_cat = 'Small (< 1MB)'
                        elif size < 50*1024*1024:  # < 50MB
                            size_cat = 'Medium (1-50MB)'
                        else:
                            size_cat = 'Large (> 50MB)'
                        analysis['size_distribution'][size_cat] = analysis['size_distribution'].get(size_cat, 0) + 1
                    except:
                        pass
        except Exception as e:
            print(f"Error scanning folder: {e}")
        
        return analysis
    
    def display_analysis_result(self, analysis):
        """Display AI analysis results"""
        print("\\n📊 AI ANALYSIS RESULTS:")
        print("=" * 40)
        
        if 'file_count' in analysis:
            print(f"📁 Total files: {analysis['file_count']}")
            
        if 'organization_plan' in analysis and analysis['organization_plan']:
            print("\\n📂 Proposed Organization:")
            for category, files in analysis['organization_plan'].items():
                print(f"\\n   📁 {category}/")
                for i, file_info in enumerate(files[:3]):  # Show first 3
                    if isinstance(file_info, dict):
                        name = file_info.get('new_name', file_info.get('name', 'Unknown'))
                    else:
                        name = str(file_info)
                    print(f"      • {name}")
                
                if len(files) > 3:
                    print(f"      ... and {len(files) - 3} more files")
        
        print("\\n✅ Ready for organization!")
    
    def display_basic_analysis(self, analysis):
        """Display basic analysis results"""
        print("\\n📊 BASIC ANALYSIS RESULTS:")
        print("=" * 40)
        
        print(f"📁 Total files: {analysis['total_files']}")
        print(f"📂 Subfolders: {analysis['folders']}")
        
        if analysis['file_types']:
            print("\\n📄 File types:")
            sorted_types = sorted(analysis['file_types'].items(), key=lambda x: x[1], reverse=True)
            for ext, count in sorted_types[:10]:  # Show top 10
                print(f"   • {ext}: {count} files")
            
            if len(sorted_types) > 10:
                print(f"   ... and {len(sorted_types) - 10} more types")
        
        if analysis['size_distribution']:
            print("\\n📏 Size distribution:")
            for size_cat, count in analysis['size_distribution'].items():
                print(f"   • {size_cat}: {count} files")
        
        print("\\n💡 Install AI components for intelligent organization suggestions:")
        print("   Run: python install_gui.py")
    
    def organize_files(self):
        """Execute file organization"""
        if not self.selected_folder:
            print("❌ No folder selected. Please select a folder first.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        print("🚀 FILE ORGANIZATION")
        print("-" * 30)
        print(f"Organizing: {self.selected_folder}")
        print(f"Style: {self.organization_style}")
        print(f"Backup: {'Enabled' if self.enable_backup else 'Disabled'}")
        print()
        
        # Confirm operation
        print("⚠️  IMPORTANT:")
        print("   • Files will be moved to new folders")
        if self.enable_backup:
            print("   • A backup will be created first")
        print("   • This operation cannot be easily undone")
        print()
        
        confirm = self.get_user_choice("Continue with organization? (y/N): ").lower()
        if confirm not in ['y', 'yes']:
            print("❌ Organization cancelled")
            input("Press Enter to continue...")
            return
        
        try:
            # Try to use the actual organizer
            sys.path.insert(0, os.path.dirname(__file__))
            
            organizer = None
            try:
                from ai_organizer_pro import AIFileOrganizerPro
                organizer = AIFileOrganizerPro()
                print("✅ Using AI Organizer Pro")
            except ImportError:
                try:
                    from ultimate_file_organizer import UltimateFileOrganizer
                    organizer = UltimateFileOrganizer()
                    print("✅ Using Ultimate File Organizer")
                except ImportError:
                    print("❌ No AI organizer available")
                    input("Press Enter to continue...")
                    return
            
            print("🔄 Organizing files...")
            
            if organizer and hasattr(organizer, 'organize_folder'):
                result = organizer.organize_folder(self.selected_folder)
                self.display_organization_result(result)
            else:
                print("❌ Organizer method not available")
                
        except Exception as e:
            print(f"❌ Organization failed: {e}")
        
        input("\\nPress Enter to continue...")
    
    def display_organization_result(self, result):
        """Display organization results"""
        print("\\n🎉 ORGANIZATION COMPLETE!")
        print("=" * 40)
        
        print(f"📊 Results:")
        print(f"   • Files organized: {result.get('files_moved', 0)}")
        print(f"   • Folders created: {result.get('folders_created', 0)}")
        print(f"   • Backup location: {result.get('backup_path', 'N/A')}")
        
        if 'organization_summary' in result:
            print(f"\\n📁 Organization summary:")
            print(result['organization_summary'])
        
        if 'errors' in result and result['errors']:
            print(f"\\n⚠️ Warnings:")
            for error in result['errors']:
                print(f"   • {error}")
        
        # Save results to file
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"organization_results_{timestamp}.txt"
            
            with open(results_file, 'w', encoding='utf-8') as f:
                f.write(f"AI File Organizer Results - {datetime.now()}\\n")
                f.write("=" * 50 + "\\n\\n")
                f.write(f"Folder: {self.selected_folder}\\n")
                f.write(f"Files organized: {result.get('files_moved', 0)}\\n")
                f.write(f"Folders created: {result.get('folders_created', 0)}\\n")
                f.write(f"Backup: {result.get('backup_path', 'N/A')}\\n\\n")
                
                if 'organization_summary' in result:
                    f.write("Organization Summary:\\n")
                    f.write(result['organization_summary'])
            
            print(f"\\n💾 Results saved to: {results_file}")
            
        except Exception as e:
            print(f"\\n⚠️ Could not save results: {e}")
    
    def google_drive_operations(self):
        """Google Drive operations menu"""
        self.clear_screen()
        self.print_header()
        print("☁️ GOOGLE DRIVE OPERATIONS")
        print("-" * 35)
        print()
        
        print("Available operations:")
        print("   1. 🔐 Connect to Google Drive")
        print("   2. 🔍 Analyze Drive folder")
        print("   3. 🚀 Organize Drive files")
        print("   4. ✅ Check Drive results")
        print("   5. 📖 Setup help")
        print("   6. Back to main menu")
        print()
        
        choice = self.get_user_choice("Select option (1-6): ", ['1', '2', '3', '4', '5', '6'])
        
        if choice == '1':
            self.connect_google_drive()
        elif choice == '2':
            self.analyze_google_drive()
        elif choice == '3':
            self.organize_google_drive()
        elif choice == '4':
            self.check_drive_results()
        elif choice == '5':
            self.show_drive_help()
        elif choice == '6':
            return
        
        input("\\nPress Enter to continue...")
    
    def connect_google_drive(self):
        """Connect to Google Drive"""
        print("\\n🔐 CONNECTING TO GOOGLE DRIVE")
        print("-" * 40)
        
        try:
            from google_drive_organizer import GoogleDriveCloudOrganizer
            
            print("Setting up Google Drive authentication...")
            organizer = GoogleDriveCloudOrganizer()
            success = organizer.setup_auth()
            
            if success:
                print("✅ Successfully connected to Google Drive!")
            else:
                print("❌ Failed to connect to Google Drive")
                print("💡 Check your credentials and try again")
        
        except ImportError:
            print("❌ Google Drive organizer not found")
            print("💡 Make sure google_drive_organizer.py exists")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
    
    def analyze_google_drive(self):
        """Analyze Google Drive folder"""
        print("\\n🔍 ANALYZE GOOGLE DRIVE FOLDER")
        print("-" * 40)
        
        url = input("Enter Google Drive folder URL: ").strip()
        if not url:
            print("❌ No URL provided")
            return
        
        try:
            # Extract folder ID from URL
            folder_id = None
            if '/folders/' in url:
                folder_id = url.split('/folders/')[1].split('?')[0].split('/')[0]
            
            if folder_id:
                print(f"📁 Folder ID: {folder_id}")
                print("🔍 This feature requires running google_drive_organizer.py")
                print("💡 Use: python google_drive_organizer.py")
            else:
                print("❌ Could not extract folder ID from URL")
        
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
    
    def organize_google_drive(self):
        """Organize Google Drive files"""
        print("\\n🚀 ORGANIZE GOOGLE DRIVE FILES")
        print("-" * 40)
        print("💡 For Google Drive organization, use:")
        print("   python google_drive_organizer.py")
        print("   python final_drive_organizer.py")
    
    def check_drive_results(self):
        """Check Google Drive results"""
        print("\\n✅ CHECK GOOGLE DRIVE RESULTS")
        print("-" * 40)
        
        if os.path.exists('check_drive_results.py'):
            print("🔍 Running drive results checker...")
            try:
                subprocess.run([sys.executable, 'check_drive_results.py'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to run results checker: {e}")
        else:
            print("❌ check_drive_results.py not found")
    
    def show_drive_help(self):
        """Show Google Drive setup help"""
        print("\\n📖 GOOGLE DRIVE SETUP HELP")
        print("-" * 40)
        print()
        print("To set up Google Drive integration:")
        print()
        print("1. 📋 Create Google Cloud Project:")
        print("   • Go to: console.cloud.google.com")
        print("   • Create new project or select existing")
        print("   • Enable Google Drive API")
        print()
        print("2. 🔑 Create Credentials:")
        print("   • Go to APIs & Credentials > Credentials")
        print("   • Create OAuth 2.0 Client ID (Desktop Application)")
        print("   • Download JSON as 'google_drive_credentials.json'")
        print()
        print("3. 📁 Place Credentials:")
        print("   • Put JSON file in this folder")
        print("   • Keep filename as 'google_drive_credentials.json'")
        print()
        print("4. 🚀 Run Organizer:")
        print("   • python google_drive_organizer.py")
        print("   • Complete OAuth in browser")
        print()
        print("📚 For detailed help, check google_auth_guide.md")
    
    def show_settings(self):
        """Settings menu"""
        self.clear_screen()
        self.print_header()
        print("⚙️ SETTINGS")
        print("-" * 15)
        print()
        
        print("Current Settings:")
        print(f"   🎨 Organization Style: {self.organization_style}")
        print(f"   🔒 Backup Enabled: {self.enable_backup}")
        print(f"   🧠 AI Analysis: {self.enable_content_analysis}")
        print()
        
        print("Options:")
        print("   1. Change organization style")
        print("   2. Toggle backup")
        print("   3. Toggle AI analysis")
        print("   4. Configure API key")
        print("   5. Test API connection")
        print("   6. Back to main menu")
        print()
        
        choice = self.get_user_choice("Select option (1-6): ", ['1', '2', '3', '4', '5', '6'])
        
        if choice == '1':
            self.change_organization_style()
        elif choice == '2':
            self.enable_backup = not self.enable_backup
            print(f"✅ Backup {'enabled' if self.enable_backup else 'disabled'}")
        elif choice == '3':
            self.enable_content_analysis = not self.enable_content_analysis
            print(f"✅ AI analysis {'enabled' if self.enable_content_analysis else 'disabled'}")
        elif choice == '4':
            self.configure_api_key()
        elif choice == '5':
            self.test_api_connection()
        elif choice == '6':
            return
        
        input("\\nPress Enter to continue...")
    
    def change_organization_style(self):
        """Change organization style"""
        print("\\n🎨 ORGANIZATION STYLES:")
        print("   1. Professional - Business-focused categories")
        print("   2. Personal - Home and family organization")
        print("   3. Creative - Artist and designer categories")
        print("   4. Minimal - Simple, clean organization")
        print()
        
        styles = {
            '1': 'professional',
            '2': 'personal', 
            '3': 'creative',
            '4': 'minimal'
        }
        
        choice = self.get_user_choice("Select style (1-4): ", ['1', '2', '3', '4'])
        self.organization_style = styles[choice]
        print(f"✅ Organization style set to: {self.organization_style}")
    
    def configure_api_key(self):
        """Configure API key"""
        print("\\n🔑 API KEY CONFIGURATION")
        print("-" * 30)
        print()
        print("To configure your Gemini API key:")
        print()
        print("1. 📝 Get API Key:")
        print("   • Go to: https://aistudio.google.com/app/apikey")
        print("   • Create a new API key (free)")
        print("   • Copy the key")
        print()
        print("2. ⚙️ Set in Environment:")
        print("   • Edit the .env file in this folder")
        print("   • Set: GOOGLE_API_KEY=your_actual_key_here")
        print("   • Save the file")
        print()
        print("3. 🔄 Restart Application")
        print()
        
        if self.get_user_choice("Open .env file now? (y/N): ").lower() in ['y', 'yes']:
            try:
                env_file = '.env'
                if os.name == 'nt':  # Windows
                    os.startfile(env_file)
                else:
                    os.system(f'open "{env_file}"')  # macOS/Linux
                print("✅ Opening .env file...")
            except Exception as e:
                print(f"❌ Could not open file: {e}")
                print(f"💡 Manually edit: {os.path.abspath('.env')}")
    
    def test_api_connection(self):
        """Test API connection"""
        print("\\n🔍 TESTING API CONNECTION")
        print("-" * 35)
        
        try:
            import google.generativeai as genai
            from dotenv import load_dotenv
            
            load_dotenv()
            api_key = os.getenv('GOOGLE_API_KEY')
            
            if not api_key or api_key == 'your_gemini_pro_api_key_here':
                print("❌ API key not configured")
                print("💡 Configure API key in settings first")
                return
            
            print("🔍 Testing connection...")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            response = model.generate_content("Hello, can you help organize files?")
            
            if response and response.text:
                print("✅ API connection successful!")
                print(f"🤖 Response: {response.text[:100]}...")
            else:
                print("❌ Empty response from API")
                
        except ImportError as e:
            print(f"❌ Missing dependencies: {e}")
            print("💡 Run: pip install google-generativeai python-dotenv")
        except Exception as e:
            print(f"❌ API test failed: {e}")
    
    def view_results(self):
        """View recent results"""
        self.clear_screen()
        self.print_header()
        print("📊 RECENT RESULTS")
        print("-" * 20)
        print()
        
        # Look for recent result files
        result_files = []
        try:
            for file in os.listdir('.'):
                if file.startswith('organization_results_') and file.endswith('.txt'):
                    result_files.append(file)
        except:
            pass
        
        if not result_files:
            print("📝 No recent results found")
            print("💡 Results will appear here after organizing files")
        else:
            print(f"📁 Found {len(result_files)} result files:")
            print()
            
            # Sort by modification time (newest first)
            result_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            
            for i, file in enumerate(result_files[:5], 1):  # Show latest 5
                try:
                    mtime = os.path.getmtime(file)
                    date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                    print(f"   {i}. {file} ({date_str})")
                except:
                    print(f"   {i}. {file}")
            
            print()
            choice = self.get_user_choice("Enter number to view file (or Enter to skip): ")
            
            if choice.isdigit() and 1 <= int(choice) <= len(result_files):
                file_to_show = result_files[int(choice) - 1]
                try:
                    print(f"\\n📄 Contents of {file_to_show}:")
                    print("-" * 50)
                    
                    with open(file_to_show, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Show first 2000 characters
                        if len(content) > 2000:
                            print(content[:2000])
                            print("\\n... (truncated)")
                        else:
                            print(content)
                            
                except Exception as e:
                    print(f"❌ Could not read file: {e}")
        
        input("\\nPress Enter to continue...")
    
    def show_help(self):
        """Show help and documentation"""
        self.clear_screen()
        self.print_header()
        print("❓ HELP & DOCUMENTATION")
        print("-" * 30)
        print()
        
        print("🚀 GETTING STARTED:")
        print("   1. Configure your Gemini API key in Settings")
        print("   2. Select a folder to organize")
        print("   3. Analyze the folder to see the proposed organization")
        print("   4. Execute the organization")
        print()
        
        print("🎨 ORGANIZATION STYLES:")
        print("   • Professional: Business and work categories")
        print("   • Personal: Home and family organization")
        print("   • Creative: Artist and designer focused")
        print("   • Minimal: Simple, clean categories")
        print()
        
        print("🔒 SAFETY FEATURES:")
        print("   • Automatic backups before organization")
        print("   • Preview before making changes")
        print("   • Detailed operation logs")
        print()
        
        print("☁️ GOOGLE DRIVE:")
        print("   • Full cloud organization support")
        print("   • OAuth authentication")
        print("   • Use google_drive_organizer.py for cloud operations")
        print()
        
        print("🔗 RESOURCES:")
        print("   • GitHub: https://github.com/ApexDazza/AI-File-Organizer-Agent")
        print("   • API Keys: https://aistudio.google.com/app/apikey")
        print("   • Google Cloud: https://console.cloud.google.com")
        print()
        
        input("Press Enter to continue...")
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                self.clear_screen()
                self.print_header()
                self.print_status()
                self.show_main_menu()
                
                choice = self.get_user_choice("Enter your choice (1-8): ", 
                                            ['1', '2', '3', '4', '5', '6', '7', '8'])
                
                if choice == '1':
                    self.select_folder()
                elif choice == '2':
                    self.analyze_folder()
                elif choice == '3':
                    self.organize_files()
                elif choice == '4':
                    self.google_drive_operations()
                elif choice == '5':
                    self.show_settings()
                elif choice == '6':
                    self.view_results()
                elif choice == '7':
                    self.show_help()
                elif choice == '8':
                    print("\\n👋 Thank you for using AI File Organizer Agent!")
                    print("🌟 Star us on GitHub: https://github.com/ApexDazza/AI-File-Organizer-Agent")
                    break
                    
        except KeyboardInterrupt:
            print("\\n\\n👋 Goodbye!")
        except Exception as e:
            print(f"\\n❌ Unexpected error: {e}")
            input("Press Enter to exit...")

def main():
    """Main entry point"""
    try:
        app = SimpleTerminalGUI()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()