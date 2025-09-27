"""
AI File Organizer - Interactive Directory Selection
=================================================
This script helps you select any directory to organize, including Google Drive.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

def find_possible_directories():
    """Find common directories that might need organization."""
    user_home = Path.home()
    
    possible_dirs = [
        user_home / "Downloads",
        user_home / "Documents", 
        user_home / "Desktop",
        user_home / "Pictures",
        user_home / "OneDrive",
        user_home / "Google Drive",
        user_home / "Dropbox",
        Path("G:/"),  # Common Google Drive mapping
        Path("H:/"),  # Alternative drive mapping
    ]
    
    existing_dirs = []
    for dir_path in possible_dirs:
        if dir_path.exists() and dir_path.is_dir():
            try:
                # Check if we can read the directory
                file_count = len(list(dir_path.iterdir()))
                existing_dirs.append({
                    'path': str(dir_path),
                    'name': dir_path.name,
                    'file_count': file_count
                })
            except PermissionError:
                pass
    
    return existing_dirs

def select_directory():
    """Interactive directory selection."""
    print("🎯 AI FILE ORGANIZER - DIRECTORY SELECTION")
    print("=" * 50)
    
    # Find possible directories
    dirs = find_possible_directories()
    
    if dirs:
        print("\n📁 Found these directories that might need organization:")
        for i, dir_info in enumerate(dirs, 1):
            print(f"{i}. {dir_info['name']}")
            print(f"   Path: {dir_info['path']}")
            print(f"   Files: ~{dir_info['file_count']} items")
            print()
        
        print(f"{len(dirs) + 1}. Enter custom path")
        print(f"{len(dirs) + 2}. Exit")
        
        while True:
            try:
                choice = input(f"\nSelect directory (1-{len(dirs) + 2}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(dirs):
                    selected_path = dirs[choice_num - 1]['path']
                    return Path(selected_path)
                elif choice_num == len(dirs) + 1:
                    custom_path = input("Enter full path to directory: ").strip().strip('"')
                    path = Path(custom_path)
                    if path.exists() and path.is_dir():
                        return path
                    else:
                        print("❌ Directory not found or not accessible")
                elif choice_num == len(dirs) + 2:
                    return None
                else:
                    print("❌ Invalid selection")
                    
            except ValueError:
                print("❌ Please enter a number")
    else:
        print("❌ No accessible directories found automatically")
        custom_path = input("Enter full path to directory to organize: ").strip().strip('"')
        path = Path(custom_path)
        if path.exists() and path.is_dir():
            return path
        else:
            print("❌ Directory not found")
            return None

def preview_directory(target_dir):
    """Preview what's in the directory before organizing."""
    print(f"\n🔍 PREVIEWING: {target_dir}")
    print("=" * 50)
    
    try:
        items = list(target_dir.iterdir())
        files = [f for f in items if f.is_file()]
        folders = [f for f in items if f.is_dir()]
        
        print(f"📊 Found: {len(files)} files, {len(folders)} folders")
        
        if files:
            print("\n📄 Files (first 10):")
            for i, file_path in enumerate(files[:10], 1):
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"  {i:2d}. {file_path.name} ({size_mb:.1f} MB)")
            
            if len(files) > 10:
                print(f"     ... and {len(files) - 10} more files")
        
        if folders:
            print(f"\n📁 Folders: {', '.join([f.name for f in folders[:5]])}")
            if len(folders) > 5:
                print(f"    ... and {len(folders) - 5} more folders")
        
        return True
        
    except PermissionError:
        print("❌ Permission denied - cannot access this directory")
        return False
    except Exception as e:
        print(f"❌ Error accessing directory: {e}")
        return False

if __name__ == "__main__":
    # Load environment
    load_dotenv()
    
    print("🎯 Welcome to the AI File Organizer!")
    print("This tool will help you organize any directory using AI.")
    print()
    
    # Select directory
    target_dir = select_directory()
    
    if target_dir:
        print(f"\n✅ Selected: {target_dir}")
        
        # Preview the directory
        if preview_directory(target_dir):
            proceed = input("\n🚀 Proceed with AI analysis and organization? (y/n): ").lower().strip()
            
            if proceed in ['y', 'yes']:
                print(f"\n🤖 To organize this directory, run:")
                print(f"   py ai_organizer_pro.py")
                print(f"\n💡 Or update your .env file with:")
                print(f"   DEFAULT_TARGET_DIR={target_dir}")
            else:
                print("👍 Organization cancelled.")
        
    else:
        print("👍 Exiting without changes.")