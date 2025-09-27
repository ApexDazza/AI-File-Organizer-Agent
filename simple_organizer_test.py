"""
Simple File Organizer Test - No MCP Dependencies
===============================================
This script demonstrates the core AI file organization functionality
without the complex MCP server setup.
"""

import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

def organize_files_simple(target_dir):
    """Simple file organization using Gemini AI without MCP."""
    
    # Load configuration
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ No Gemini API key found in .env file")
        return
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    print(f"🎯 Organizing files in: {target_dir}")
    print("="*60)
    
    target_path = Path(target_dir)
    if not target_path.exists():
        print(f"❌ Directory not found: {target_dir}")
        return
    
    # Get all files (not directories)
    files = [f for f in target_path.iterdir() if f.is_file()]
    
    if not files:
        print("📁 No files found to organize")
        return
    
    print(f"📋 Found {len(files)} files to analyze")
    
    # Analyze files with AI
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        file_info = []
        for file_path in files[:10]:  # Limit to 10 files for demo
            file_info.append({
                'name': file_path.name,
                'size': file_path.stat().st_size,
                'extension': file_path.suffix,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d')
            })
        
        # Create AI prompt for organization
        prompt = f"""
        Analyze these files and suggest a professional organization structure:
        
        Files to organize:
        {chr(10).join([f"- {f['name']} ({f['extension']}, {f['size']} bytes, modified: {f['modified']})" for f in file_info])}
        
        Please suggest:
        1. Professional folder categories for these files
        2. Which files should go in each category
        3. Any files that should be renamed for better organization
        
        Respond in this format:
        CATEGORIES:
        - Category Name: Description
        
        ORGANIZATION:
        - filename.ext -> Category Name (optional: rename to "new_name.ext")
        """
        
        print("🤖 Analyzing files with Gemini AI...")
        response = model.generate_content(prompt)
        
        print("\n🎯 AI Organization Recommendations:")
        print("="*60)
        print(response.text)
        
        # Ask user if they want to proceed
        print("\n" + "="*60)
        proceed = input("🚀 Apply this organization? (y/n): ").lower().strip()
        
        if proceed == 'y':
            print("✅ Organization would be applied here!")
            print("📝 Note: This demo shows recommendations only.")
            print("   The full version would create folders and move files.")
        else:
            print("👍 Organization cancelled. No files were moved.")
            
    except Exception as e:
        print(f"❌ Error during AI analysis: {e}")

if __name__ == "__main__":
    # Use the configured directory
    target = os.getenv('DEFAULT_TARGET_DIR', 'C:/Users/darre/OneDrive/Documents')
    organize_files_simple(target)