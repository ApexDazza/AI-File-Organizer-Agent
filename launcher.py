"""
AI File Organizer Agent - Launcher
=================================
Choose your preferred interface for the AI File Organizer Agent.
"""

import os
import sys
import subprocess

def print_banner():
    """Print application banner"""
    print("=" * 70)
    print("🤖 AI FILE ORGANIZER AGENT")
    print("=" * 70)
    print("Intelligent file organization powered by AI")
    print("Choose your preferred interface:")
    print()

def check_dependencies():
    """Check what interfaces are available"""
    interfaces = {}
    
    # Check terminal GUI
    if os.path.exists('terminal_gui.py'):
        interfaces['terminal'] = {
            'name': '📱 Terminal Interface (Recommended)',
            'file': 'terminal_gui.py',
            'description': 'User-friendly terminal interface - works everywhere'
        }
    
    # Check tkinter GUI
    if os.path.exists('gui_organizer.py'):
        try:
            import tkinter
            interfaces['tkinter'] = {
                'name': '🖥️ Desktop GUI (tkinter)',
                'file': 'gui_organizer.py',
                'description': 'Modern desktop interface - requires working display'
            }
        except ImportError:
            pass
    
    # Check web GUI
    if os.path.exists('web_gui.py'):
        try:
            import flask
            interfaces['web'] = {
                'name': '🌐 Web Interface',
                'file': 'web_gui.py',
                'description': 'Browser-based interface - requires Flask'
            }
        except ImportError:
            interfaces['web_fallback'] = {
                'name': '🌐 Web Interface (install Flask)',
                'file': 'web_gui.py',
                'description': 'Browser-based interface - will install Flask automatically'
            }
    
    # Check command line organizers
    if os.path.exists('ultimate_file_organizer.py'):
        interfaces['ultimate'] = {
            'name': '⚡ Ultimate File Organizer (CLI)',
            'file': 'ultimate_file_organizer.py',
            'description': 'Command-line version with advanced features'
        }
    
    if os.path.exists('ai_organizer_pro.py'):
        interfaces['pro'] = {
            'name': '🧠 AI Organizer Pro (CLI)',
            'file': 'ai_organizer_pro.py',
            'description': 'Professional command-line interface'
        }
    
    # Google Drive organizer
    if os.path.exists('google_drive_organizer.py'):
        interfaces['drive'] = {
            'name': '☁️ Google Drive Organizer',
            'file': 'google_drive_organizer.py',
            'description': 'Cloud storage organization'
        }
    
    return interfaces

def show_interfaces(interfaces):
    """Display available interfaces"""
    print("Available interfaces:")
    print()
    
    choices = {}
    choice_num = 1
    
    # Prioritize terminal interface
    if 'terminal' in interfaces:
        print(f"   {choice_num}. {interfaces['terminal']['name']}")
        print(f"      {interfaces['terminal']['description']}")
        choices[str(choice_num)] = interfaces['terminal']
        choice_num += 1
        print()
    
    # Other GUI interfaces
    for key in ['tkinter', 'web', 'web_fallback']:
        if key in interfaces:
            print(f"   {choice_num}. {interfaces[key]['name']}")
            print(f"      {interfaces[key]['description']}")
            choices[str(choice_num)] = interfaces[key]
            choice_num += 1
            print()
    
    # Command line interfaces
    for key in ['ultimate', 'pro']:
        if key in interfaces:
            print(f"   {choice_num}. {interfaces[key]['name']}")
            print(f"      {interfaces[key]['description']}")
            choices[str(choice_num)] = interfaces[key]
            choice_num += 1
            print()
    
    # Cloud organizer
    if 'drive' in interfaces:
        print(f"   {choice_num}. {interfaces['drive']['name']}")
        print(f"      {interfaces['drive']['description']}")
        choices[str(choice_num)] = interfaces['drive']
        choice_num += 1
        print()
    
    # Exit option
    print(f"   {choice_num}. 🚪 Exit")
    choices[str(choice_num)] = {'name': 'Exit', 'file': None}
    
    return choices

def get_user_choice(choices):
    """Get user's interface choice"""
    max_choice = len(choices)
    
    while True:
        try:
            choice = input(f"Enter your choice (1-{max_choice}): ").strip()
            if choice in choices:
                return choices[choice]
            else:
                print(f"❌ Invalid choice. Please enter a number between 1 and {max_choice}")
        except KeyboardInterrupt:
            print("\\n👋 Goodbye!")
            sys.exit(0)

def launch_interface(interface):
    """Launch the selected interface"""
    if not interface['file']:
        print("👋 Goodbye!")
        return
    
    print(f"🚀 Launching {interface['name']}...")
    print()
    
    try:
        # Run the selected interface
        subprocess.run([sys.executable, interface['file']], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch interface: {e}")
        print("💡 Try running directly: python " + interface['file'])
    except KeyboardInterrupt:
        print("\\n⚠️ Interface interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_setup_help():
    """Show setup help if no interfaces found"""
    print("❌ No interfaces found!")
    print()
    print("📋 Setup Instructions:")
    print("   1. Make sure you're in the AI File Organizer directory")
    print("   2. Required files should include:")
    print("      • terminal_gui.py (recommended)")
    print("      • ultimate_file_organizer.py")
    print("      • google_drive_organizer.py")
    print()
    print("   3. Install dependencies:")
    print("      python install_gui.py")
    print()
    print("   4. Configure API key in .env file")
    print()
    print("💡 If you're missing files, re-download the project from:")
    print("   https://github.com/ApexDazza/AI-File-Organizer-Agent")

def main():
    """Main launcher function"""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print_banner()
        
        # Check available interfaces
        interfaces = check_dependencies()
        
        if not interfaces:
            show_setup_help()
            return
        
        # Show interfaces and get choice
        choices = show_interfaces(interfaces)
        selected = get_user_choice(choices)
        
        # Launch selected interface
        launch_interface(selected)
        
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        print("💡 Try running an interface directly:")
        print("   python terminal_gui.py")

if __name__ == "__main__":
    main()