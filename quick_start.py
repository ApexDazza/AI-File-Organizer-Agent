"""
Quick Start Guide for Ultimate File Organizer
============================================

This script will help you get started immediately!
"""

import os
import sys
from pathlib import Path

def main():
    print("🚀 Welcome to the Ultimate AI File Organizer!")
    print("=" * 60)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ No .env file found!")
        print("📝 Creating a template .env file for you...")
        
        env_content = """# Ultimate File Organizer Configuration
# Get your free API key from: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_gemini_pro_api_key_here

# Optional: Set a default directory to organize
DEFAULT_TARGET_DIR=

# Safety boundary - highest level directory the agent can access
TOP_LEVEL_ALLOWED_PATH=~

# Debug mode for detailed output
DEBUG=False

# Enhanced Configuration
ENABLE_CLOUD_SYNC=True
ENABLE_CONTENT_ANALYSIS=True
ENABLE_SMART_TAGGING=True
ORGANIZATION_STYLE=professional
AUTO_BACKUP_BEFORE_ORGANIZE=True
MAX_FILES_PER_BATCH=100
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Created {env_file}")
        print("\n🔑 IMPORTANT: You need to add your Gemini API key!")
        print("1. Visit: https://aistudio.google.com/app/apikey")
        print("2. Create a free API key")
        print("3. Edit the .env file and replace 'your_gemini_pro_api_key_here' with your actual key")
        print("\n📁 Then re-run this script to start organizing!")
        return
    
    # Check if API key is configured
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_gemini_pro_api_key_here":
        print("❌ Gemini API key not configured!")
        print("📝 Please edit the .env file and add your API key")
        print("🔗 Get one free at: https://aistudio.google.com/app/apikey")
        return
    
    print("✅ Configuration looks good!")
    print("🔑 API key configured")
    
    # Test basic imports
    try:
        import agno
        from agno.models.google.gemini import Gemini
        print("✅ Core libraries available")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💾 Try running: pip install -r requirements.txt")
        return
    
    # Check Node.js
    import subprocess
    try:
        result = subprocess.run('npx --version', shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js/npx available: {result.stdout.strip()}")
        else:
            print("❌ npx command failed")
            return
    except FileNotFoundError:
        print("❌ Node.js/npx not found!")
        print("📥 Install Node.js from: https://nodejs.org/")
        return
    
    print("\n🎯 Everything looks ready!")
    print("=" * 60)
    
    # Offer to run the organizer
    choice = input("\n🚀 Start organizing files now? (y/n): ").lower().strip()
    
    if choice in ['y', 'yes']:
        print("\n🔄 Starting the Ultimate File Organizer...")
        try:
            # Import and run the main organizer
            sys.path.append(os.getcwd())
            from ultimate_file_organizer import main as run_organizer
            import asyncio
            asyncio.run(run_organizer())
        except Exception as e:
            print(f"❌ Error starting organizer: {e}")
            print("🔧 Try running directly: python ultimate_file_organizer.py")
    else:
        print("\n📋 To start organizing later, run:")
        print("   python ultimate_file_organizer.py")
        print("   or double-click: Run_Ultimate_File_Organizer.bat")
    
    print("\n🌟 Happy organizing!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    input("\nPress Enter to close...")