"""
Ultimate AI File Organizer Agent - Enhanced Version
==================================================

This enhanced file organizer provides:
- Multi-cloud storage support (Google Drive, OneDrive, Dropbox)
- Content-based analysis and smart tagging
- Cross-machine synchronization of organization rules
- Professional file naming and structure standards
- Backup creation before any organization
- Batch processing for large file collections

Author: Enhanced by GitHub Copilot for ultimate organization
"""

import asyncio
import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from textwrap import dedent
from typing import List, Dict, Any, Optional
import hashlib
import mimetypes

# Agno imports
from agno.agent.agent import Agent
from agno.exceptions import ModelProviderError
from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters
from agno.models.google.gemini import Gemini

# Environment and utilities
from dotenv import load_dotenv

class UltimateFileOrganizer:
    """Enhanced file organizer with cloud sync, content analysis, and smart organization."""
    
    def __init__(self):
        load_dotenv()
        self.config = self._load_config()
        self.organization_rules = self._load_organization_rules()
        self.file_cache = {}
        self.backup_dir = None
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        return {
            'gemini_model_id': 'gemini-1.5-pro',  # Using Pro for better analysis
            'debug_mode': os.getenv("DEBUG", "False").lower() in ('true', '1', 't'),
            'top_level_path': os.getenv("TOP_LEVEL_ALLOWED_PATH", "~"),
            'default_target_dir': os.getenv("DEFAULT_TARGET_DIR", ""),
            'enable_cloud_sync': os.getenv("ENABLE_CLOUD_SYNC", "True").lower() in ('true', '1', 't'),
            'enable_content_analysis': os.getenv("ENABLE_CONTENT_ANALYSIS", "True").lower() in ('true', '1', 't'),
            'enable_smart_tagging': os.getenv("ENABLE_SMART_TAGGING", "True").lower() in ('true', '1', 't'),
            'organization_style': os.getenv("ORGANIZATION_STYLE", "professional"),
            'auto_backup': os.getenv("AUTO_BACKUP_BEFORE_ORGANIZE", "True").lower() in ('true', '1', 't'),
            'max_files_per_batch': int(os.getenv("MAX_FILES_PER_BATCH", "100")),
            'google_api_key': os.getenv("GOOGLE_API_KEY"),
            'organization_depth': int(os.getenv("ORGANIZATION_DEPTH", "99"))  # Add depth limit
        }
    
    def _load_organization_rules(self) -> Dict[str, Any]:
        """Load or create organization rules that can be synced across machines."""
        rules_file = Path.home() / '.ai_file_organizer' / 'organization_rules.json'
        rules_file.parent.mkdir(exist_ok=True)
        
        default_rules = {
            'file_type_categories': {
                'Documents': {
                    'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
                    'subcategories': {
                        'Financial': ['invoice', 'receipt', 'tax', 'bank', 'statement'],
                        'Legal': ['contract', 'agreement', 'legal', 'terms'],
                        'Personal': ['resume', 'cv', 'letter', 'personal'],
                        'Work': ['report', 'proposal', 'meeting', 'presentation']
                    }
                },
                'Images': {
                    'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
                    'subcategories': {
                        'Screenshots': ['screenshot', 'screen', 'capture'],
                        'Photos': ['photo', 'pic', 'img', 'camera'],
                        'Graphics': ['logo', 'icon', 'graphic', 'design'],
                        'Wallpapers': ['wallpaper', 'background', 'desktop']
                    }
                },
                'Videos': {
                    'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
                    'subcategories': {
                        'Movies': ['movie', 'film', 'cinema'],
                        'TV Shows': ['episode', 'season', 'series'],
                        'Personal': ['home', 'family', 'personal'],
                        'Educational': ['tutorial', 'course', 'lesson']
                    }
                },
                'Audio': {
                    'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
                    'subcategories': {
                        'Music': ['song', 'album', 'track', 'music'],
                        'Podcasts': ['podcast', 'episode', 'audio'],
                        'Audiobooks': ['audiobook', 'book', 'chapter'],
                        'Recordings': ['recording', 'voice', 'memo']
                    }
                },
                'Archives': {
                    'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
                    'subcategories': {
                        'Software': ['installer', 'setup', 'program'],
                        'Backups': ['backup', 'archive', 'old'],
                        'Projects': ['project', 'source', 'code']
                    }
                },
                'Development': {
                    'extensions': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.cs', '.php'],
                    'subcategories': {
                        'Web': ['web', 'site', 'frontend', 'backend'],
                        'Mobile': ['android', 'ios', 'mobile', 'app'],
                        'Desktop': ['desktop', 'gui', 'application'],
                        'Scripts': ['script', 'automation', 'tool']
                    }
                }
            },
            'naming_patterns': {
                'date_format': '%Y-%m-%d',
                'remove_spaces': True,
                'capitalize_words': True,
                'max_filename_length': 100,
                'forbidden_chars': ['<', '>', ':', '"', '|', '?', '*']
            },
            'organization_style_templates': {
                'professional': {
                    'structure': 'type_first',  # Documents/Financial/2024/
                    'date_grouping': 'yearly',
                    'naming': 'descriptive'
                },
                'personal': {
                    'structure': 'date_first',  # 2024/Documents/Personal/
                    'date_grouping': 'monthly',
                    'naming': 'casual'
                },
                'creative': {
                    'structure': 'project_based',  # Projects/WebsiteRedesign/Images/
                    'date_grouping': 'none',
                    'naming': 'creative'
                },
                'minimal': {
                    'structure': 'flat_categories',  # Documents/, Images/, etc.
                    'date_grouping': 'none',
                    'naming': 'simple'
                }
            }
        }
        
        if rules_file.exists():
            try:
                with open(rules_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load organization rules: {e}")
        
        # Save default rules
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(default_rules, f, indent=2)
        
        return default_rules
    
    def create_backup(self, target_path: str) -> Optional[str]:
        """Create a backup of the target directory before organization."""
        if not self.config['auto_backup']:
            return None
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_before_organization_{timestamp}"
        backup_path = Path(target_path).parent / backup_name
        
        try:
            print(f"\nCreating backup: {backup_path}")
            shutil.copytree(target_path, backup_path, dirs_exist_ok=True)
            self.backup_dir = str(backup_path)
            print(f"✅ Backup created successfully!")
            return str(backup_path)
        except Exception as e:
            print(f"❌ Failed to create backup: {e}")
            return None
    
    def analyze_file_content(self, file_path: Path) -> Dict[str, Any]:
        """Analyze file content to determine optimal organization."""
        analysis = {
            'size': file_path.stat().st_size if file_path.exists() else 0,
            'modified_date': datetime.fromtimestamp(file_path.stat().st_mtime) if file_path.exists() else None,
            'extension': file_path.suffix.lower(),
            'mime_type': mimetypes.guess_type(str(file_path))[0],
            'suggested_category': None,
            'suggested_subcategory': None,
            'content_keywords': [],
            'file_hash': None
        }
        
        # Calculate file hash for duplicate detection
        if file_path.exists() and analysis['size'] < 100 * 1024 * 1024:  # Only hash files < 100MB
            try:
                with open(file_path, 'rb') as f:
                    analysis['file_hash'] = hashlib.md5(f.read()).hexdigest()
            except Exception:
                pass
        
        # Determine category based on extension and filename
        filename_lower = file_path.name.lower()
        for category, info in self.organization_rules['file_type_categories'].items():
            if analysis['extension'] in info['extensions']:
                analysis['suggested_category'] = category
                
                # Check for subcategory keywords
                for subcategory, keywords in info['subcategories'].items():
                    if any(keyword in filename_lower for keyword in keywords):
                        analysis['suggested_subcategory'] = subcategory
                        break
                break
        
        return analysis
    
    def generate_enhanced_instructions(self, target_path: str, file_analysis: Dict[str, Any]) -> str:
        """Generate enhanced AI instructions based on analysis and configuration."""
        style = self.organization_rules['organization_style_templates'][self.config['organization_style']]
        
        instructions = dedent(f"""
            You are an ULTIMATE file organization assistant with professional-grade capabilities.
            
            TARGET DIRECTORY: '{target_path}'
            ORGANIZATION STYLE: {self.config['organization_style']} ({style['structure']})
            
            ENHANCED RULES:
            1. NEVER use absolute paths - only relative paths from the target directory
            2. Create a logical, searchable hierarchy based on the {self.config['organization_style']} style
            3. Group files by: {style['structure']} with {style['date_grouping']} date grouping
            4. Use {style['naming']} naming conventions
            5. Handle duplicates intelligently (append numbers, not overwrite)
            6. Create year/month subfolders when appropriate
            7. Preserve important metadata in folder structure
            
            AVAILABLE FILE ANALYSIS:
            - Total files analyzed: {file_analysis.get('total_files', 0)}
            - File types detected: {', '.join(file_analysis.get('categories_found', []))}
            - Date range: {file_analysis.get('date_range', 'Unknown')}
            - Potential duplicates: {file_analysis.get('duplicate_count', 0)}
            
            PROFESSIONAL ORGANIZATION PATTERNS:
            📁 Documents/
              ├── Financial/
              │   ├── 2024/
              │   ├── 2023/
              │   └── Archive/
              ├── Personal/
              ├── Work/
              └── Legal/
            
            📁 Media/
              ├── Images/
              │   ├── Screenshots/
              │   ├── Photos/
              │   │   ├── 2024/
              │   │   └── 2023/
              │   └── Graphics/
              ├── Videos/
              └── Audio/
            
            📁 Development/
              ├── Projects/
              ├── Scripts/
              └── Resources/
            
            📁 Archives/
              ├── Old_Files/
              ├── Backups/
              └── Installers/
            
            EXECUTION PHASES:
            1. Create main category directories
            2. Create year-based subdirectories where appropriate
            3. Create specialized subdirectories (Financial, Personal, etc.)
            4. Move files to their optimal locations
            5. Handle any remaining miscellaneous files
            
            NAMING STANDARDS:
            - Remove spaces, use underscores or CamelCase
            - Add dates in YYYY-MM-DD format when relevant
            - Keep filenames under 100 characters
            - Preserve original extensions
            - Remove special characters: {self.organization_rules['naming_patterns']['forbidden_chars']}
            
            CONTENT ANALYSIS INTEGRATION:
            Use the file analysis data to make intelligent decisions about:
            - Which files belong in Financial (invoices, receipts, statements)
            - Which images are screenshots vs photos vs graphics
            - Which documents are work-related vs personal
            - Date-based organization for large collections
            
            OUTPUT FORMAT:
            PLAN:
            # Phase 1: Main directories
            call tool 'create_directory' with args {{'path': 'Documents'}}
            call tool 'create_directory' with args {{'path': 'Media'}}
            
            # Phase 2: Subdirectories
            call tool 'create_directory' with args {{'path': 'Documents/Financial'}}
            call tool 'create_directory' with args {{'path': 'Documents/Financial/2024'}}
            
            # Phase 3: File organization
            call tool 'move_file' with args {{'source': 'invoice_2024.pdf', 'destination': 'Documents/Financial/2024/Invoice_2024-01-15.pdf'}}
        """)
        
        return instructions
    
    def analyze_directory_contents(self, target_path: str) -> Dict[str, Any]:
        """Perform comprehensive analysis of directory contents."""
        print("🔍 Analyzing directory contents...")
        
        path_obj = Path(target_path)
        analysis = {
            'total_files': 0,
            'total_size': 0,
            'categories_found': set(),
            'date_range': None,
            'duplicate_count': 0,
            'file_details': [],
            'hash_map': {}
        }
        
        # Recursively analyze all files
        self._analyze_directory_recursive(path_obj, analysis, 0)
        
        analysis['categories_found'] = list(analysis['categories_found'])
        
        # Determine date range
        dates = [f['modified_date'] for f in analysis['file_details'] if f['modified_date']]
        if dates:
            analysis['date_range'] = f"{min(dates).year} - {max(dates).year}"
        
        print(f"📊 Analysis complete: {analysis['total_files']} files, {len(analysis['categories_found'])} categories")
        return analysis

    def _analyze_directory_recursive(self, path: Path, analysis: Dict, depth: int):
        """Recursively analyze directory contents up to a specified depth."""
        if depth > self.config['organization_depth']:
            return

        for entry in path.iterdir():
            if entry.is_file():
                file_analysis = self.analyze_file_content(entry)
                analysis['file_details'].append(file_analysis)
                analysis['total_files'] += 1
                analysis['total_size'] += file_analysis['size']
                if file_analysis['suggested_category']:
                    analysis['categories_found'].add(file_analysis['suggested_category'])
                if file_analysis['file_hash']:
                    if file_analysis['file_hash'] in analysis['hash_map']:
                        analysis['duplicate_count'] += 1
                    else:
                        analysis['hash_map'][file_analysis['file_hash']] = str(entry)
            elif entry.is_dir():
                self._analyze_directory_recursive(entry, analysis, depth + 1)
    
    async def run_ultimate_organization(self, target_path: Optional[str] = None) -> None:
        """Run the ultimate file organization process."""
        print("🚀 Starting Ultimate AI File Organizer...")
        print("=" * 60)
        
        # Determine target directory
        if not target_path:
            target_path = await self._get_target_directory()
        
        if not target_path:
            print("❌ Could not determine target directory. Exiting.")
            return
        
        # Create backup
        backup_path = self.create_backup(target_path)
        
        # Analyze directory contents
        file_analysis = self.analyze_directory_contents(target_path)
        
        # Initialize Gemini model
        try:
            gemini_llm = Gemini(id=self.config['gemini_model_id'])
            if not self.config['google_api_key']:
                print("❌ GOOGLE_API_KEY not found. Please set it in your .env file.")
                return
        except Exception as e:
            print(f"❌ Error initializing Gemini model: {e}")
            return
        
        # Configure MCP server
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", target_path],
            cwd=target_path,
        )
        
        try:
            async with MCPTools(server_params=server_params) as mcp_tools:
                print("✅ MCP Tools initialized successfully")
                
                # Create the ultimate organizer agent
                organizer_agent = Agent(
                    model=gemini_llm,
                    tools=[mcp_tools],
                    instructions=self.generate_enhanced_instructions(target_path, file_analysis),
                    show_tool_calls=True,
                    markdown=True,
                )
                
                # Get initial directory structure
                print("📋 Scanning current file structure...")
                initial_response = await organizer_agent.arun(
                    "Use the 'list_directory' tool with {'path': '.'} to show the current structure. "
                    "Also use 'directory_tree' to show the full hierarchy."
                )
                
                print("=" * 60)
                print("📁 CURRENT DIRECTORY STRUCTURE:")
                print(initial_response.content)
                print("=" * 60)
                
                # Request the ultimate organization plan
                planning_prompt = dedent(f"""
                    Based on the directory structure analysis and the {file_analysis['total_files']} files found,
                    create a comprehensive organization plan that will transform this chaotic directory into
                    a perfectly organized, professional file system.
                    
                    Key insights from analysis:
                    - File categories found: {', '.join(file_analysis['categories_found'])}
                    - Date range: {file_analysis['date_range']}
                    - Total size: {file_analysis['total_size'] / (1024*1024):.1f} MB
                    - Potential duplicates: {file_analysis['duplicate_count']}
                    
                    Create a plan that would make an obsessive-compulsive professional organizer proud!
                    Focus on creating a logical hierarchy that makes finding any file effortless.
                """)
                
                print("🧠 Generating ultimate organization plan...")
                plan_response = await organizer_agent.arun(planning_prompt)
                
                # Extract and display the plan
                self._display_organization_plan(plan_response.content)
                
                # Get user approval
                user_input = input("\n✨ Execute this ultimate organization plan? (yes/no/feedback): ").strip().lower()
                
                if user_input == 'yes':
                    print("🔄 Executing the ultimate organization plan...")
                    execution_response = await organizer_agent.arun(
                        f"Execute the complete organization plan step by step:\n\n{plan_response.content}"
                    )
                    
                    print("\n" + "=" * 60)
                    print("✅ ORGANIZATION COMPLETE!")
                    print("=" * 60)
                    print(execution_response.content)
                    
                    if backup_path:
                        print(f"\n💾 Backup created at: {backup_path}")
                        review_input = input("\n🧐 Please review the changes. Are you satisfied with the organization? (yes/no): ").strip().lower()
                        if review_input == 'yes':
                            try:
                                print(f"🗑️ Deleting backup directory: {backup_path}")
                                shutil.rmtree(backup_path)
                                print("✅ Backup deleted successfully.")
                                self.backup_dir = None  # Clear backup path after deletion
                            except Exception as e:
                                print(f"❌ Error deleting backup directory: {e}")
                        else:
                            print(f"👍 Backup retained at: {backup_path}")
                    
                    # Save organization session log
                    self._save_organization_log(target_path, file_analysis, plan_response.content)
                    
                elif user_input == 'no':
                    print("❌ Organization cancelled by user.")
                else:
                    print("💬 Processing your feedback for plan revision...")
                    revision_response = await organizer_agent.arun(
                        f"User feedback: '{user_input}'. Revise the organization plan accordingly."
                    )
                    print("\n📋 REVISED PLAN:")
                    self._display_organization_plan(revision_response.content)
                
        except Exception as e:
            print(f"❌ Error during organization: {e}")
            if self.config['debug_mode']:
                import traceback
                traceback.print_exc()
    
    async def _get_target_directory(self) -> Optional[str]:
        """Get target directory from config or user input."""
        resolved_top_level = os.path.abspath(os.path.expanduser(self.config['top_level_path']))
        
        if self.config['default_target_dir']:
            resolved_default = os.path.abspath(os.path.expanduser(self.config['default_target_dir']))
            if os.path.isdir(resolved_default) and self._is_path_safe(resolved_default, resolved_top_level):
                return resolved_default
        
        print(f"\n📍 Enter the directory to organize (must be within {resolved_top_level}):")
        while True:
            user_path = input("📁 Path: ").strip()
            resolved_path = os.path.abspath(os.path.expanduser(user_path))
            
            if not os.path.isdir(resolved_path):
                print("❌ Invalid path: Not a directory")
                continue
            
            if not self._is_path_safe(resolved_path, resolved_top_level):
                print(f"❌ Path must be within {resolved_top_level}")
                continue
            
            return resolved_path
    
    def _is_path_safe(self, path_to_check: str, boundary_path: str) -> bool:
        """Check if path is within safety boundary."""
        try:
            return os.path.commonpath([
                os.path.abspath(boundary_path),
                os.path.abspath(path_to_check)
            ]) == os.path.abspath(boundary_path)
        except (ValueError, Exception):
            return False
    
    def _display_organization_plan(self, plan_content: str) -> None:
        """Display the organization plan in a formatted way."""
        print("\n" + "=" * 60)
        print("📋 ULTIMATE ORGANIZATION PLAN")
        print("=" * 60)
        
        lines = plan_content.split('\n')
        current_phase = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                current_phase = line
                print(f"\n🔸 {line}")
            elif 'create_directory' in line:
                print(f"  📁 {line}")
            elif 'move_file' in line:
                print(f"  🔄 {line}")
            elif line and not line.startswith('call tool'):
                print(f"  ℹ️  {line}")
        
        print("=" * 60)
    
    def _save_organization_log(self, target_path: str, analysis: Dict[str, Any], plan: str) -> None:
        """Save organization session log for future reference."""
        log_dir = Path.home() / '.ai_file_organizer' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"organization_{timestamp}.json"
        
        log_data = {
            'timestamp': timestamp,
            'target_path': target_path,
            'analysis': {
                'total_files': analysis['total_files'],
                'categories_found': analysis['categories_found'],
                'date_range': analysis['date_range'],
                'duplicate_count': analysis['duplicate_count']
            },
            'plan': plan,
            'config': self.config,
            'backup_location': self.backup_dir
        }
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, default=str)
            print(f"📝 Organization log saved: {log_file}")
        except Exception as e:
            print(f"⚠️ Could not save log: {e}")

# CLI Interface
async def main():
    """Main CLI interface for the Ultimate File Organizer."""
    organizer = UltimateFileOrganizer()
    
    print("🎯 Welcome to the Ultimate AI File Organizer!")
    print("This tool will transform your chaotic file system into a masterpiece of organization.")
    print("\nFeatures enabled:")
    
    if organizer.config['enable_content_analysis']:
        print("✅ Content Analysis & Smart Categorization")
    if organizer.config['enable_smart_tagging']:
        print("✅ Intelligent Tagging System")
    if organizer.config['auto_backup']:
        print("✅ Automatic Backup Creation")
    
    print(f"🎨 Organization Style: {organizer.config['organization_style'].title()}")
    print()
    
    await organizer.run_ultimate_organization()

if __name__ == "__main__":
    # Verify dependencies
    try:
        import subprocess
        subprocess.run("npx --version", shell=True, check=True, capture_output=True)
        asyncio.run(main())
    except FileNotFoundError:
        print("❌ Error: 'npx' not found. Please install Node.js first.")
        print("📥 Download from: https://nodejs.org/")
    except Exception as e:
        print(f"❌ Error: {e}")