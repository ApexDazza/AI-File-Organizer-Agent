"""
Ultimate File Organizer Setup Script
===================================

This script will:
1. Install all required dependencies
2. Set up your Gemini Pro API key
3. Configure cloud storage (optional)
4. Test the installation
5. Create shortcuts for easy access

Run this script to get your ultimate file organizer ready!
"""

import subprocess
import sys
import os
from pathlib import Path
import json

def print_header(text):
    print("\n" + "="*60)
    print(f"🚀 {text}")
    print("="*60)

def print_step(step, text):
    print(f"\n{step}. {text}")

def run_command(cmd, description):
    """Run a command and handle errors gracefully."""
    print(f"   Running: {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, you have {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} - Compatible!")
    return True

def check_node_installed():
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} - Installed!")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js not found!")
    print("📥 Please install Node.js from: https://nodejs.org/")
    print("   Choose the LTS version for best compatibility")
    return False

def install_python_packages():
    """Install required Python packages."""
    print_step("3", "Installing Python packages...")
    
    packages = [
        "agno",
        "pydantic", 
        "mcp",
        "google-genai",
        "python-dotenv",
        "google-api-python-client",
        "google-auth-httplib2", 
        "google-auth-oauthlib",
        "dropbox",
        "pillow",
        "python-magic-bin",  # Windows version
        "pandas",
        "openpyxl", 
        "PyPDF2",
        "python-docx",
        "mutagen",
        "exifread",
        "requests",
        "aiofiles",
        "tqdm",
        "colorama",
        "rich"
    ]
    
    success_count = 0
    for package in packages:
        if run_command(f"pip install {package}", f"Installing {package}"):
            success_count += 1
        else:
            print(f"   ⚠️  Failed to install {package} - continuing...")
    
    print(f"\n📊 Installed {success_count}/{len(packages)} packages successfully")
    return success_count > len(packages) * 0.8  # 80% success rate

def setup_gemini_api():
    """Help user set up Gemini API key."""
    print_step("4", "Setting up Gemini Pro API")
    
    env_file = Path(".env")
    
    print("🔑 You need a Gemini API key to use this organizer.")
    print("📖 Get your free API key from: https://aistudio.google.com/app/apikey")
    
    api_key = input("\n🔐 Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Create or update .env file
        env_content = f"""# Ultimate File Organizer Configuration
GOOGLE_API_KEY={api_key}

# Optional: Set a default directory to organize
DEFAULT_TARGET_DIR=

# Safety boundary - highest level directory accessible  
TOP_LEVEL_ALLOWED_PATH=~

# Debug mode for detailed output
DEBUG=False

# Enhanced features
ENABLE_CLOUD_SYNC=True
ENABLE_CONTENT_ANALYSIS=True
ENABLE_SMART_TAGGING=True
ORGANIZATION_STYLE=professional
AUTO_BACKUP_BEFORE_ORGANIZE=True
MAX_FILES_PER_BATCH=100
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ API key configured successfully!")
        return True
    else:
        print("⚠️  Skipped API key setup. You can add it later to the .env file")
        return False

def create_desktop_shortcut():
    """Create a desktop shortcut for easy access."""
    print_step("5", "Creating desktop shortcut")
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "Ultimate File Organizer.lnk")
        target_path = os.path.abspath("ultimate_file_organizer.py")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target_path}"'
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print(f"✅ Desktop shortcut created: {shortcut_path}")
        return True
        
    except ImportError:
        print("⚠️  Could not create desktop shortcut (missing winshell)")
        return False
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")
        return False

def create_run_script():
    """Create simple run scripts."""
    print_step("6", "Creating run scripts")
    
    # Windows batch file
    batch_content = f'''@echo off
echo 🚀 Starting Ultimate File Organizer...
echo.
cd /d "{os.getcwd()}"
python ultimate_file_organizer.py
pause
'''
    
    with open("run_organizer.bat", 'w') as f:
        f.write(batch_content)
    
    # PowerShell script  
    ps_content = f'''# Ultimate File Organizer Launcher
Write-Host "🚀 Starting Ultimate File Organizer..." -ForegroundColor Green
Set-Location "{os.getcwd()}"
python ultimate_file_organizer.py
Read-Host "Press Enter to close"
'''
    
    with open("run_organizer.ps1", 'w') as f:
        f.write(ps_content)
    
    print("✅ Created run_organizer.bat and run_organizer.ps1")
    return True

def test_installation():
    """Test if everything is working."""
    print_step("7", "Testing installation")
    
    # Test Node.js and npx
    if not run_command("npx --version", "Testing npx"):
        return False
    
    # Test MCP filesystem server
    if not run_command("npx -y @modelcontextprotocol/server-filesystem --help", "Testing MCP filesystem server"):
        return False
        
    # Test Python imports
    try:
        print("   Testing Python imports...")
        import agno
        from dotenv import load_dotenv
        print("   ✅ Core imports working!")
        
        # Test optional imports
        try:
            import google.generativeai
            print("   ✅ Gemini API available!")
        except ImportError:
            print("   ⚠️  Gemini API import failed - check google-genai installation")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import test failed: {e}")
        return False

def show_next_steps():
    """Show user what to do next."""
    print_header("🎉 Setup Complete!")
    
    print("""
🎯 Your Ultimate File Organizer is ready!

📋 Next Steps:
1. Double-click 'run_organizer.bat' to start organizing
2. Or run: python ultimate_file_organizer.py
3. For cloud storage, edit cloud_credentials.json (will be created on first run)

🔧 Configuration Files:
- .env - Main configuration and API keys
- ~/.ai_file_organizer/ - Organization rules and logs

🌟 Features Available:
✅ AI-powered file organization using Gemini Pro
✅ Professional folder structures  
✅ Automatic backups before organizing
✅ Content-based file analysis
✅ Smart duplicate detection
✅ Cross-platform sync (when configured)

🚀 Ready to transform your file chaos into organized perfection!
    """)

def main():
    """Main setup process."""
    print_header("Ultimate File Organizer Setup")
    
    print("""
Welcome to the Ultimate AI File Organizer setup!

This tool will transform your chaotic file system into a masterpiece of organization.
It's like hiring an obsessive-compulsive professional organizer, but powered by AI!

Features:
🧠 AI-powered organization using Google Gemini Pro
📁 Professional folder structures and naming
☁️  Cloud storage integration (Google Drive, Dropbox, OneDrive)  
🏷️  Smart content analysis and tagging
🔄 Cross-machine synchronization
💾 Automatic backups before any changes
🎨 Multiple organization styles (Professional, Personal, Creative, Minimal)
    """)
    
    input("\nPress Enter to begin setup...")
    
    # Step 1: Check Python version
    print_step("1", "Checking Python version")
    if not check_python_version():
        input("Please upgrade Python and run setup again. Press Enter to exit...")
        return False
    
    # Step 2: Check Node.js
    print_step("2", "Checking Node.js installation")
    if not check_node_installed():
        input("Please install Node.js and run setup again. Press Enter to exit...")
        return False
    
    # Step 3: Install packages
    if not install_python_packages():
        print("⚠️  Some packages failed to install. You may need to install them manually.")
        if input("Continue anyway? (y/N): ").lower() != 'y':
            return False
    
    # Step 4: Setup API key
    api_configured = setup_gemini_api()
    
    # Step 5: Create shortcuts
    create_desktop_shortcut()
    
    # Step 6: Create run scripts
    create_run_script()
    
    # Step 7: Test installation
    if test_installation():
        show_next_steps()
        return True
    else:
        print("\n❌ Installation test failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("\nSetup encountered issues. Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        input("Press Enter to exit...")