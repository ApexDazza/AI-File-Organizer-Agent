"""
GUI Installer for AI File Organizer Agent
==========================================
This script installs the optional GUI dependencies for a modern user interface.
"""

import subprocess
import sys
import os

def install_package(package, description):
    """Install a Python package with user feedback"""
    print(f"📦 Installing {description}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {description} installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {description}: {e}")
        return False

def check_existing_package(package):
    """Check if a package is already installed"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    """Install GUI dependencies"""
    print("🎨 AI FILE ORGANIZER - GUI SETUP")
    print("=" * 45)
    print("Installing optional packages for enhanced user interface...\n")
    
    # Check if we're in the right directory
    if not os.path.exists("ultimate_file_organizer.py"):
        print("❌ Please run this script from the AI File Organizer directory")
        print("   Expected files: ultimate_file_organizer.py")
        return False
    
    # List of GUI packages to install
    packages = [
        ("customtkinter", "Modern UI Framework", "customtkinter"),
        ("pillow", "Image Processing Support", "PIL"),
        ("ttkthemes", "Additional UI Themes", "tkinter.ttk")
    ]
    
    print("🔍 Checking existing installations...")
    
    success_count = 0
    skip_count = 0
    
    for package, description, import_name in packages:
        if check_existing_package(import_name):
            print(f"✅ {description} already installed")
            skip_count += 1
            success_count += 1
        else:
            if install_package(package, description):
                success_count += 1
    
    print(f"\n📊 INSTALLATION SUMMARY")
    print("=" * 25)
    print(f"✅ Successfully available: {success_count}/{len(packages)} packages")
    if skip_count > 0:
        print(f"⏭️  Already installed: {skip_count} packages")
    
    if success_count == len(packages):
        print("\n🎉 GUI SETUP COMPLETE!")
        print("You can now run the modern GUI interface:")
        print("   python gui_organizer.py")
        print("\n💡 The GUI provides:")
        print("   • Modern visual interface")
        print("   • Drag & drop folder selection")
        print("   • Real-time progress indicators")
        print("   • Google Drive integration")
        print("   • Organization preview")
    elif success_count > 0:
        print("\n⚠️  PARTIAL INSTALLATION")
        print("Some packages failed to install, but the GUI will still work")
        print("with basic tkinter interface:")
        print("   python gui_organizer.py")
    else:
        print("\n❌ INSTALLATION FAILED")
        print("GUI packages could not be installed.")
        print("You can still use the command-line interface:")
        print("   python ultimate_file_organizer.py")
    
    return success_count > 0

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please try running the installation manually:")
        print("   pip install customtkinter pillow ttkthemes")