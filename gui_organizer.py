"""
AI File Organizer Agent - GUI Interface
=======================================
Modern graphical user interface for the AI File Organizer Agent.
Provides an intuitive way to organize both local files and Google Drive.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
import json
from datetime import datetime
import webbrowser
import re

# Try to import modern UI libraries
try:
    import customtkinter as ctk
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    USE_MODERN_UI = True
except ImportError:
    USE_MODERN_UI = False

class AIFileOrganizerGUI:
    """Main GUI application for AI File Organizer"""
    
    def __init__(self):
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.check_dependencies()
        
    def setup_window(self):
        """Initialize the main window"""
        if USE_MODERN_UI:
            self.root = ctk.CTk()
            self.root.title("🤖 AI File Organizer Agent")
            self.root.geometry("900x700")
        else:
            self.root = tk.Tk()
            self.root.title("🤖 AI File Organizer Agent")
            self.root.geometry("900x700")
            
        self.root.minsize(700, 500)
        
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"900x700+{x}+{y}")
        
    def setup_variables(self):
        """Initialize application variables"""
        self.selected_folder = tk.StringVar()
        self.organization_style = tk.StringVar(value="professional")
        self.enable_backup = tk.BooleanVar(value=True)
        self.enable_content_analysis = tk.BooleanVar(value=True)
        self.cloud_mode = tk.BooleanVar(value=False)
        self.drive_url = tk.StringVar()
        
        # Status variables
        self.api_status = tk.StringVar(value="Checking...")
        self.cloud_status = tk.StringVar(value="Not connected")
        self.last_operation = tk.StringVar(value="Ready")
        
    def setup_ui(self):
        """Create the user interface"""
        # Main container
        if USE_MODERN_UI:
            main_frame = ctk.CTkFrame(self.root)
            main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        else:
            main_frame = ttk.Frame(self.root)
            main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
        # Main content (notebook/tabs)
        self.create_notebook(main_frame)
        
    def create_header(self, parent):
        """Create the application header"""
        header_frame = self.create_frame(parent)
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Title and description
        if USE_MODERN_UI:
            title_label = ctk.CTkLabel(header_frame, text="🤖 AI File Organizer Agent", 
                                     font=ctk.CTkFont(size=26, weight="bold"))
        else:
            title_label = ttk.Label(header_frame, text="🤖 AI File Organizer Agent", 
                                  font=("Arial", 20, "bold"))
        title_label.pack(pady=(0, 5))
        
        subtitle_text = "Intelligent file organization powered by AI • Local & Cloud Support"
        subtitle_label = self.create_label(header_frame, subtitle_text)
        if hasattr(subtitle_label, 'configure'):
            try:
                if USE_MODERN_UI:
                    subtitle_label.configure(text_color="gray60")
                else:
                    subtitle_label.configure(foreground="gray60")
            except:
                pass
        
    def create_status_bar(self, parent):
        """Create status bar showing current state"""
        status_frame = self.create_frame(parent)
        status_frame.pack(fill="x", pady=(0, 10))
        
        # Status indicators
        status_grid = self.create_frame(status_frame)
        status_grid.pack(fill="x")
        
        # API Status
        api_frame = self.create_frame(status_grid)
        api_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.create_label(api_frame, "🔑 API Status:").pack(side="left")
        self.api_status_label = self.create_label(api_frame, "")
        self.api_status_label.pack(side="left", padx=(5, 0))
        
        # Cloud Status  
        cloud_frame = self.create_frame(status_grid)
        cloud_frame.pack(side="left", fill="x", expand=True, padx=5)
        self.create_label(cloud_frame, "☁️ Cloud:").pack(side="left")
        self.cloud_status_label = self.create_label(cloud_frame, "")
        self.cloud_status_label.pack(side="left", padx=(5, 0))
        
        # Last Operation
        op_frame = self.create_frame(status_grid)
        op_frame.pack(side="right", padx=(5, 0))
        self.create_label(op_frame, "📊 Status:").pack(side="left")
        self.operation_label = self.create_label(op_frame, "Ready")
        self.operation_label.pack(side="left", padx=(5, 0))
        
    def create_notebook(self, parent):
        """Create the main tabbed interface"""
        if USE_MODERN_UI:
            self.notebook = ctk.CTkTabview(parent)
            self.notebook.pack(fill="both", expand=True)
            
            # Create tabs
            self.tab_local = self.notebook.add("📁 Local Files")
            self.tab_cloud = self.notebook.add("☁️ Google Drive")
            self.tab_settings = self.notebook.add("⚙️ Settings")
            self.tab_results = self.notebook.add("📊 Results")
        else:
            self.notebook = ttk.Notebook(parent)
            self.notebook.pack(fill="both", expand=True)
            
            # Create tab frames
            self.tab_local = ttk.Frame(self.notebook)
            self.tab_cloud = ttk.Frame(self.notebook)
            self.tab_settings = ttk.Frame(self.notebook)
            self.tab_results = ttk.Frame(self.notebook)
            
            # Add to notebook
            self.notebook.add(self.tab_local, text="📁 Local Files")
            self.notebook.add(self.tab_cloud, text="☁️ Google Drive")
            self.notebook.add(self.tab_settings, text="⚙️ Settings")
            self.notebook.add(self.tab_results, text="📊 Results")
        
        # Setup each tab
        self.setup_local_tab()
        self.setup_cloud_tab()
        self.setup_settings_tab()
        self.setup_results_tab()
        
    def setup_local_tab(self):
        """Setup the local file organization tab"""
        # Main container for local tab
        container = self.create_frame(self.tab_local)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Folder selection section
        folder_section = self.create_frame(container)
        folder_section.pack(fill="x", pady=(0, 15))
        
        self.create_label(folder_section, "📂 Select Folder to Organize:").pack(anchor="w")
        
        # Folder input row
        folder_input = self.create_frame(folder_section)
        folder_input.pack(fill="x", pady=(5, 0))
        
        self.folder_entry = self.create_entry(folder_input, textvariable=self.selected_folder)
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.create_button(folder_input, "📁 Browse", self.browse_folder).pack(side="right")
        
        # Quick access buttons
        quick_frame = self.create_frame(folder_section)
        quick_frame.pack(fill="x", pady=(5, 0))
        
        quick_folders = [
            ("📥 Downloads", "~/Downloads"),
            ("📄 Documents", "~/Documents"), 
            ("🖼️ Pictures", "~/Pictures"),
            ("🎵 Music", "~/Music"),
            ("🎬 Videos", "~/Videos")
        ]
        
        for text, path in quick_folders:
            self.create_button(quick_frame, text, 
                             lambda p=path: self.set_quick_folder(p)).pack(side="left", padx=(0, 5))
        
        # Organization preview section
        preview_section = self.create_frame(container)
        preview_section.pack(fill="both", expand=True, pady=(0, 15))
        
        preview_header = self.create_frame(preview_section)
        preview_header.pack(fill="x")
        
        self.create_label(preview_header, "🔍 Organization Preview:").pack(side="left")
        self.create_button(preview_header, "🔄 Refresh", self.refresh_preview).pack(side="right")
        
        # Preview text area
        if USE_MODERN_UI:
            self.preview_text = ctk.CTkTextbox(preview_section, height=300)
        else:
            self.preview_text = scrolledtext.ScrolledText(preview_section, height=15, wrap=tk.WORD)
        self.preview_text.pack(fill="both", expand=True, pady=(10, 0))
        
        # Action buttons
        action_frame = self.create_frame(container)
        action_frame.pack(fill="x")
        
        self.analyze_btn = self.create_button(action_frame, "🔍 Analyze Folder", self.analyze_folder)
        self.analyze_btn.pack(side="left", padx=(0, 10))
        
        self.organize_btn = self.create_button(action_frame, "🚀 Organize Files", self.organize_files)
        self.organize_btn.pack(side="left", padx=(0, 10))
        
        self.create_button(action_frame, "📊 View Results", self.show_results).pack(side="left")
        
    def setup_cloud_tab(self):
        """Setup the Google Drive cloud organization tab"""
        container = self.create_frame(self.tab_cloud)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Google Drive connection section
        connection_section = self.create_frame(container)
        connection_section.pack(fill="x", pady=(0, 15))
        
        self.create_label(connection_section, "🔗 Google Drive Connection:").pack(anchor="w")
        
        # Connection status and buttons
        conn_controls = self.create_frame(connection_section)
        conn_controls.pack(fill="x", pady=(5, 0))
        
        self.create_button(conn_controls, "🔐 Connect Drive", self.connect_google_drive).pack(side="left", padx=(0, 10))
        self.create_button(conn_controls, "📋 Test Connection", self.test_drive_connection).pack(side="left", padx=(0, 10))
        self.create_button(conn_controls, "ℹ️ Setup Help", self.show_drive_help).pack(side="left")
        
        # Drive folder URL section
        url_section = self.create_frame(container)
        url_section.pack(fill="x", pady=(0, 15))
        
        self.create_label(url_section, "📁 Google Drive Folder URL:").pack(anchor="w")
        
        url_input = self.create_frame(url_section)
        url_input.pack(fill="x", pady=(5, 0))
        
        self.drive_url_entry = self.create_entry(url_input, textvariable=self.drive_url)
        self.drive_url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.create_button(url_input, "🔗 Parse URL", self.parse_drive_url).pack(side="right")
        
        # Cloud preview section
        cloud_preview_section = self.create_frame(container)
        cloud_preview_section.pack(fill="both", expand=True, pady=(0, 15))
        
        cloud_header = self.create_frame(cloud_preview_section)
        cloud_header.pack(fill="x")
        
        self.create_label(cloud_header, "☁️ Drive Organization Preview:").pack(side="left")
        self.create_button(cloud_header, "🔄 Refresh Drive", self.refresh_drive_preview).pack(side="right")
        
        if USE_MODERN_UI:
            self.cloud_preview_text = ctk.CTkTextbox(cloud_preview_section, height=300)
        else:
            self.cloud_preview_text = scrolledtext.ScrolledText(cloud_preview_section, height=15, wrap=tk.WORD)
        self.cloud_preview_text.pack(fill="both", expand=True, pady=(10, 0))
        
        # Cloud action buttons
        cloud_actions = self.create_frame(container)
        cloud_actions.pack(fill="x")
        
        self.analyze_drive_btn = self.create_button(cloud_actions, "🔍 Analyze Drive", self.analyze_drive_folder)
        self.analyze_drive_btn.pack(side="left", padx=(0, 10))
        
        self.organize_drive_btn = self.create_button(cloud_actions, "☁️ Organize Drive", self.organize_drive_files)
        self.organize_drive_btn.pack(side="left", padx=(0, 10))
        
        self.create_button(cloud_actions, "✅ Check Results", self.check_drive_results).pack(side="left")
        
    def setup_settings_tab(self):
        """Setup the settings and configuration tab"""
        container = self.create_frame(self.tab_settings)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Organization settings
        org_section = self.create_frame(container)
        org_section.pack(fill="x", pady=(0, 20))
        
        self.create_label(org_section, "🎨 Organization Settings:").pack(anchor="w")
        
        # Style selection
        style_frame = self.create_frame(org_section)
        style_frame.pack(fill="x", pady=(5, 10))
        
        self.create_label(style_frame, "Organization Style:").pack(side="left")
        
        if USE_MODERN_UI:
            style_menu = ctk.CTkOptionMenu(style_frame, variable=self.organization_style,
                                         values=["professional", "personal", "creative", "minimal"])
        else:
            style_menu = ttk.Combobox(style_frame, textvariable=self.organization_style,
                                    values=["professional", "personal", "creative", "minimal"],
                                    state="readonly", width=15)
        style_menu.pack(side="right")
        
        # Options checkboxes
        options_frame = self.create_frame(org_section)
        options_frame.pack(fill="x")
        
        self.create_checkbox(options_frame, "🔒 Create backup before organizing", self.enable_backup)
        self.create_checkbox(options_frame, "🧠 Enable AI content analysis", self.enable_content_analysis)
        
        # API Configuration
        api_section = self.create_frame(container)
        api_section.pack(fill="x", pady=(0, 20))
        
        self.create_label(api_section, "🔑 API Configuration:").pack(anchor="w")
        
        api_status_frame = self.create_frame(api_section)
        api_status_frame.pack(fill="x", pady=5)
        
        self.detailed_api_status = self.create_label(api_status_frame, "Checking API status...")
        self.detailed_api_status.pack(side="left")
        
        api_buttons = self.create_frame(api_section)
        api_buttons.pack(fill="x", pady=5)
        
        self.create_button(api_buttons, "🔍 Test API", self.test_api).pack(side="left", padx=(0, 10))
        self.create_button(api_buttons, "⚙️ Configure API", self.configure_api).pack(side="left", padx=(0, 10))
        self.create_button(api_buttons, "📖 API Help", self.show_api_help).pack(side="left")
        
        # About section
        about_section = self.create_frame(container)
        about_section.pack(fill="both", expand=True)
        
        self.create_label(about_section, "ℹ️ About AI File Organizer:").pack(anchor="w")
        
        if USE_MODERN_UI:
            about_text = ctk.CTkTextbox(about_section, height=150)
        else:
            about_text = scrolledtext.ScrolledText(about_section, height=8, wrap=tk.WORD)
        about_text.pack(fill="both", expand=True, pady=(5, 0))
        
        about_content = """AI File Organizer Agent v2.0

🤖 Features:
• Intelligent file categorization using Google Gemini AI
• Local file organization with safety backups
• Google Drive cloud organization support
• Multiple organization styles (professional, personal, creative, minimal)
• Real-time preview and progress tracking
• Secure credential management

🚀 Usage:
1. Configure your Gemini API key in Settings
2. Select a folder or Google Drive URL to organize
3. Choose your organization style
4. Preview the proposed organization
5. Execute the organization with confidence

💡 Tips:
• Always enable backups for safety
• Use content analysis for better categorization
• Test with small folders first
• Check results after organization

For more information, visit: https://github.com/ApexDazza/AI-File-Organizer-Agent"""
        
        about_text.insert("1.0" if USE_MODERN_UI else tk.INSERT, about_content)
        if hasattr(about_text, 'configure'):
            about_text.configure(state="disabled")
        
    def setup_results_tab(self):
        """Setup the results and history tab"""
        container = self.create_frame(self.tab_results)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Results header
        results_header = self.create_frame(container)
        results_header.pack(fill="x", pady=(0, 10))
        
        self.create_label(results_header, "📊 Organization Results & History:").pack(side="left")
        
        # Control buttons
        results_controls = self.create_frame(results_header)
        results_controls.pack(side="right")
        
        self.create_button(results_controls, "🔄 Refresh", self.refresh_results).pack(side="left", padx=(0, 5))
        self.create_button(results_controls, "💾 Save Report", self.save_results_report).pack(side="left", padx=(0, 5))
        self.create_button(results_controls, "🗑️ Clear", self.clear_results).pack(side="left")
        
        # Results display
        if USE_MODERN_UI:
            self.results_text = ctk.CTkTextbox(container, height=500)
        else:
            self.results_text = scrolledtext.ScrolledText(container, height=25, wrap=tk.WORD)
        self.results_text.pack(fill="both", expand=True)
        
        # Initialize with welcome message
        self.update_results_display("🎉 Welcome to AI File Organizer Agent!\n\nResults from your organization operations will appear here.\n")
        
    # UI Helper Methods
    def create_frame(self, parent):
        """Create a frame widget"""
        if USE_MODERN_UI:
            return ctk.CTkFrame(parent)
        else:
            return ttk.Frame(parent)
    
    def create_label(self, parent, text):
        """Create a label widget"""
        if USE_MODERN_UI:
            label = ctk.CTkLabel(parent, text=text)
        else:
            label = ttk.Label(parent, text=text)
        return label
    
    def create_button(self, parent, text, command):
        """Create a button widget"""
        if USE_MODERN_UI:
            return ctk.CTkButton(parent, text=text, command=command)
        else:
            return ttk.Button(parent, text=text, command=command)
    
    def create_entry(self, parent, textvariable=None):
        """Create an entry widget"""
        if USE_MODERN_UI:
            return ctk.CTkEntry(parent, textvariable=textvariable)
        else:
            return ttk.Entry(parent, textvariable=textvariable)
    
    def create_checkbox(self, parent, text, variable):
        """Create a checkbox widget"""
        if USE_MODERN_UI:
            cb = ctk.CTkCheckBox(parent, text=text, variable=variable)
        else:
            cb = ttk.Checkbutton(parent, text=text, variable=variable)
        cb.pack(anchor="w", pady=2)
        return cb
    
    # Event Handlers and Main Methods
    def browse_folder(self):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(
            title="Select folder to organize",
            initialdir=os.path.expanduser("~")
        )
        if folder:
            self.selected_folder.set(folder)
            self.update_status("Folder selected", f"Selected: {os.path.basename(folder)}")
    
    def set_quick_folder(self, path):
        """Set a quick access folder"""
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            self.selected_folder.set(expanded_path)
            self.update_status("Quick folder set", f"Selected: {os.path.basename(expanded_path)}")
        else:
            messagebox.showwarning("Folder Not Found", f"Folder {expanded_path} does not exist")
    
    def refresh_preview(self):
        """Refresh the organization preview"""
        self.analyze_folder(preview_only=True)
    
    def analyze_folder(self, preview_only=False):
        """Analyze the selected folder"""
        folder = self.selected_folder.get().strip()
        if not folder:
            messagebox.showwarning("No Folder Selected", "Please select a folder to analyze")
            return
        
        if not os.path.exists(folder):
            messagebox.showerror("Folder Not Found", f"The folder {folder} does not exist")
            return
        
        self.update_preview_text("🔍 Analyzing folder contents...\n")
        self.update_status("Analyzing", "Processing folder structure")
        
        # Disable analyze button during operation
        if hasattr(self, 'analyze_btn'):
            self.analyze_btn.configure(state="disabled" if not USE_MODERN_UI else "disabled")
        
        # Run analysis in background thread
        thread = threading.Thread(target=self._analyze_folder_background, args=(folder, preview_only), daemon=True)
        thread.start()
    
    def _analyze_folder_background(self, folder, preview_only=False):
        """Background thread for folder analysis"""
        try:
            # Try to import and use the actual organizer
            sys.path.insert(0, os.path.dirname(__file__))
            
            # Try different organizer imports
            organizer = None
            try:
                from ai_organizer_pro import AIFileOrganizerPro
                organizer = AIFileOrganizerPro()
            except ImportError:
                try:
                    from ultimate_file_organizer import UltimateFileOrganizer
                    organizer = UltimateFileOrganizer()
                except ImportError:
                    # Fallback to basic analysis
                    pass
            
            if organizer and hasattr(organizer, 'analyze_files'):
                analysis = organizer.analyze_files(folder)
                self.root.after(0, self._update_preview_with_analysis, analysis)
            else:
                # Basic folder analysis fallback
                analysis = self._basic_folder_analysis(folder)
                self.root.after(0, self._update_preview_with_basic_analysis, analysis)
            
        except Exception as e:
            error_msg = f"Analysis failed: {str(e)}"
            self.root.after(0, self._show_analysis_error, error_msg)
        finally:
            # Re-enable analyze button
            if hasattr(self, 'analyze_btn'):
                self.root.after(0, lambda: self.analyze_btn.configure(state="normal"))
    
    def _basic_folder_analysis(self, folder):
        """Basic folder analysis when AI organizer is not available"""
        analysis = {
            'total_files': 0,
            'file_types': {},
            'size_distribution': {},
            'organization_plan': {}
        }
        
        try:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    analysis['total_files'] += 1
                    
                    # Track file extensions
                    ext = os.path.splitext(file)[1].lower()
                    analysis['file_types'][ext] = analysis['file_types'].get(ext, 0) + 1
                    
                    # Basic size info
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
            print(f"Error in basic analysis: {e}")
        
        return analysis
    
    def _update_preview_with_analysis(self, analysis):
        """Update preview with full AI analysis"""
        if not analysis:
            self.update_preview_text("❌ No analysis results available")
            return
        
        preview_text = "📊 FOLDER ANALYSIS RESULTS\n"
        preview_text += "=" * 50 + "\n\n"
        
        if 'organization_plan' in analysis and analysis['organization_plan']:
            preview_text += "📁 Proposed Organization:\n\n"
            
            for category, files in analysis['organization_plan'].items():
                preview_text += f"📂 {category}/\n"
                
                # Show first few files as examples
                for i, file_info in enumerate(files[:3]):
                    if isinstance(file_info, dict):
                        name = file_info.get('new_name', file_info.get('name', 'Unknown'))
                    else:
                        name = str(file_info)
                    preview_text += f"   • {name}\n"
                
                if len(files) > 3:
                    preview_text += f"   ... and {len(files) - 3} more files\n"
                preview_text += "\n"
        
        # Add summary statistics
        if 'file_count' in analysis:
            preview_text += f"📊 Summary:\n"
            preview_text += f"   • Total files: {analysis.get('file_count', 0)}\n"
            preview_text += f"   • Folders to create: {len(analysis.get('organization_plan', {}))}\n"
        
        self.update_preview_text(preview_text)
        self.update_status("Analysis complete", f"Found {analysis.get('file_count', 0)} files")
    
    def _update_preview_with_basic_analysis(self, analysis):
        """Update preview with basic analysis"""
        preview_text = "📊 BASIC FOLDER ANALYSIS\n"
        preview_text += "=" * 40 + "\n\n"
        
        preview_text += f"📁 Total Files: {analysis['total_files']}\n\n"
        
        if analysis['file_types']:
            preview_text += "📄 File Types:\n"
            for ext, count in sorted(analysis['file_types'].items(), key=lambda x: x[1], reverse=True):
                ext_name = ext if ext else 'No extension'
                preview_text += f"   • {ext_name}: {count} files\n"
            preview_text += "\n"
        
        if analysis['size_distribution']:
            preview_text += "📏 Size Distribution:\n"
            for size_cat, count in analysis['size_distribution'].items():
                preview_text += f"   • {size_cat}: {count} files\n"
            preview_text += "\n"
        
        preview_text += "💡 Note: Install AI components for intelligent organization suggestions.\n"
        preview_text += "   Run: python install_gui.py\n"
        
        self.update_preview_text(preview_text)
        self.update_status("Basic analysis complete", f"Found {analysis['total_files']} files")
    
    def _show_analysis_error(self, error_msg):
        """Show analysis error"""
        self.update_preview_text(f"❌ {error_msg}\n\n💡 Tips:\n• Check folder permissions\n• Ensure AI components are installed\n• Try a different folder")
        self.update_status("Analysis failed", "Check error details")
        messagebox.showerror("Analysis Error", error_msg)
    
    def organize_files(self):
        """Execute file organization"""
        folder = self.selected_folder.get().strip()
        if not folder:
            messagebox.showwarning("No Folder Selected", "Please select a folder to organize")
            return
        
        # Confirm organization
        if not messagebox.askyesno("Confirm Organization", 
                                  f"This will organize files in:\n{folder}\n\nA backup will be created if enabled.\n\nContinue?"):
            return
        
        self.update_status("Organizing", "Processing files...")
        
        # Disable organize button
        if hasattr(self, 'organize_btn'):
            self.organize_btn.configure(state="disabled")
        
        # Run organization in background
        thread = threading.Thread(target=self._organize_files_background, args=(folder,), daemon=True)
        thread.start()
    
    def _organize_files_background(self, folder):
        """Background thread for file organization"""
        try:
            # Import organizer
            sys.path.insert(0, os.path.dirname(__file__))
            
            organizer = None
            try:
                from ai_organizer_pro import AIFileOrganizerPro
                organizer = AIFileOrganizerPro()
            except ImportError:
                try:
                    from ultimate_file_organizer import UltimateFileOrganizer
                    organizer = UltimateFileOrganizer()
                except ImportError:
                    raise ImportError("No organizer module found")
            
            # Execute organization
            result = organizer.organize_folder(folder)
            
            self.root.after(0, self._show_organization_result, result)
            
        except Exception as e:
            error_msg = f"Organization failed: {str(e)}"
            self.root.after(0, self._show_organization_error, error_msg)
        finally:
            # Re-enable organize button
            if hasattr(self, 'organize_btn'):
                self.root.after(0, lambda: self.organize_btn.configure(state="normal"))
    
    def _show_organization_result(self, result):
        """Display organization results"""
        # Switch to results tab
        if USE_MODERN_UI:
            self.notebook.set("📊 Results")
        else:
            self.notebook.select(3)  # Results tab index
        
        # Format results
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results_text = f"\n🎉 ORGANIZATION COMPLETED - {timestamp}\n"
        results_text += "=" * 60 + "\n\n"
        
        results_text += f"📊 Results Summary:\n"
        results_text += f"   • Files organized: {result.get('files_moved', 0)}\n"
        results_text += f"   • Folders created: {result.get('folders_created', 0)}\n"
        results_text += f"   • Backup location: {result.get('backup_path', 'N/A')}\n"
        results_text += f"   • Organization style: {self.organization_style.get()}\n\n"
        
        if 'organization_summary' in result:
            results_text += f"📁 Folder Structure:\n{result['organization_summary']}\n"
        
        if 'errors' in result and result['errors']:
            results_text += f"\n⚠️ Warnings/Errors:\n"
            for error in result['errors']:
                results_text += f"   • {error}\n"
        
        results_text += "\n" + "=" * 60 + "\n"
        
        self.append_results(results_text)
        self.update_status("Organization complete", f"Organized {result.get('files_moved', 0)} files")
        
        messagebox.showinfo("Success", f"Files organized successfully!\n\nFiles moved: {result.get('files_moved', 0)}\nFolders created: {result.get('folders_created', 0)}")
    
    def _show_organization_error(self, error_msg):
        """Show organization error"""
        self.update_status("Organization failed", "Check error details")
        messagebox.showerror("Organization Error", error_msg)
        
        # Log error to results
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_text = f"\n❌ ORGANIZATION FAILED - {timestamp}\n"
        error_text += f"Error: {error_msg}\n"
        error_text += "=" * 60 + "\n"
        self.append_results(error_text)
    
    # Google Drive Methods
    def connect_google_drive(self):
        """Connect to Google Drive"""
        self.update_status("Connecting", "Setting up Google Drive")
        
        try:
            # Check if drive organizer exists
            from google_drive_organizer import GoogleDriveCloudOrganizer
            
            organizer = GoogleDriveCloudOrganizer()
            success = organizer.setup_auth()
            
            if success:
                self.cloud_status.set("✅ Connected")
                self.update_cloud_status_label()
                messagebox.showinfo("Success", "Connected to Google Drive successfully!")
                self.update_status("Drive connected", "Ready for cloud organization")
            else:
                self.cloud_status.set("❌ Failed")
                self.update_cloud_status_label()
                messagebox.showerror("Connection Failed", "Failed to connect to Google Drive. Check your credentials.")
                
        except ImportError:
            messagebox.showwarning("Module Not Found", 
                                 "Google Drive organizer not found. Please ensure google_drive_organizer.py exists.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Error connecting to Google Drive: {str(e)}")
    
    def test_drive_connection(self):
        """Test Google Drive connection"""
        try:
            from google_drive_organizer import GoogleDriveCloudOrganizer
            
            organizer = GoogleDriveCloudOrganizer()
            if organizer.setup_auth():
                messagebox.showinfo("Connection Test", "✅ Google Drive connection is working!")
                self.cloud_status.set("✅ Connected")
            else:
                messagebox.showerror("Connection Test", "❌ Google Drive connection failed!")
                self.cloud_status.set("❌ Failed")
            
            self.update_cloud_status_label()
            
        except Exception as e:
            messagebox.showerror("Test Failed", f"Connection test failed: {str(e)}")
    
    def show_drive_help(self):
        """Show Google Drive setup help"""
        help_msg = """🔧 Google Drive Setup Help

To use Google Drive organization:

1. 📋 Create Google Cloud Project:
   • Go to console.cloud.google.com
   • Create a new project or select existing
   • Enable Google Drive API

2. 🔑 Create Credentials:
   • Go to APIs & Credentials > Credentials
   • Create OAuth 2.0 Client ID (Desktop Application)
   • Download the JSON file as 'google_drive_credentials.json'

3. 📁 Place Credentials:
   • Put the JSON file in this folder
   • Keep the filename as 'google_drive_credentials.json'

4. 🚀 Connect:
   • Click 'Connect Drive' button
   • Complete OAuth authorization in browser

Need detailed help? Check google_auth_guide.md"""
        
        messagebox.showinfo("Google Drive Setup", help_msg)
    
    def parse_drive_url(self):
        """Parse Google Drive URL to extract folder ID"""
        url = self.drive_url.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a Google Drive folder URL")
            return
        
        # Extract folder ID from various URL formats
        folder_id = None
        
        # Standard sharing URL format
        if '/folders/' in url:
            folder_id = url.split('/folders/')[1].split('?')[0].split('/')[0]
        # Direct drive URL
        elif 'id=' in url:
            folder_id = url.split('id=')[1].split('&')[0]
        
        if folder_id:
            messagebox.showinfo("URL Parsed", f"Extracted folder ID: {folder_id}")
            self.update_status("URL parsed", f"Folder ID: {folder_id[:10]}...")
            # Store folder ID for use
            self.drive_folder_id = folder_id
        else:
            messagebox.showwarning("Invalid URL", "Could not extract folder ID from URL. Please check the URL format.")
    
    def refresh_drive_preview(self):
        """Refresh Google Drive preview"""
        self.analyze_drive_folder()
    
    def analyze_drive_folder(self):
        """Analyze Google Drive folder"""
        # Implementation would connect to Google Drive API
        self.update_cloud_preview_text("🔍 Analyzing Google Drive folder...\n")
        
        # Placeholder for now
        preview_text = """☁️ Google Drive Analysis

📁 This feature will show:
   • Files in the selected Drive folder
   • Proposed organization structure
   • File categories and counts

🚀 To enable:
   1. Complete Google Drive setup
   2. Enter a valid folder URL
   3. Click 'Analyze Drive'

💡 The analysis will use the same AI intelligence
   as local file organization."""
        
        self.update_cloud_preview_text(preview_text)
    
    def organize_drive_files(self):
        """Organize Google Drive files"""
        if not hasattr(self, 'drive_folder_id'):
            messagebox.showwarning("No Folder Selected", "Please parse a Google Drive URL first")
            return
        
        # Placeholder implementation
        messagebox.showinfo("Drive Organization", "Google Drive organization will be implemented here using your existing google_drive_organizer.py")
    
    def check_drive_results(self):
        """Check Google Drive organization results"""
        try:
            from check_drive_results import main as check_results
            # Run in background thread
            threading.Thread(target=check_results, daemon=True).start()
            messagebox.showinfo("Checking Results", "Drive results check started. See console for details.")
        except ImportError:
            messagebox.showwarning("Module Not Found", "check_drive_results.py not found")
    
    # Settings Methods  
    def test_api(self):
        """Test Gemini API connection"""
        self.update_status("Testing API", "Connecting to Gemini")
        
        # Run test in background
        threading.Thread(target=self._test_api_background, daemon=True).start()
    
    def _test_api_background(self):
        """Background API test"""
        try:
            import google.generativeai as genai
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key or api_key == 'your_gemini_pro_api_key_here':
                raise ValueError("API key not configured")
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content("Hello, can you help organize files?")
            
            if response and response.text:
                self.root.after(0, self._api_test_success)
            else:
                raise ValueError("Empty response from API")
                
        except Exception as e:
            self.root.after(0, lambda: self._api_test_failed(str(e)))
    
    def _api_test_success(self):
        """Handle successful API test"""
        self.api_status.set("✅ Working")
        self.update_api_status_label()
        self.detailed_api_status.configure(text="✅ Gemini API is working perfectly!")
        self.update_status("API test passed", "Gemini API ready")
        messagebox.showinfo("API Test", "✅ Gemini API is working correctly!")
    
    def _api_test_failed(self, error):
        """Handle failed API test"""
        self.api_status.set("❌ Failed")
        self.update_api_status_label()
        self.detailed_api_status.configure(text=f"❌ API test failed: {error}")
        self.update_status("API test failed", "Check configuration")
        messagebox.showerror("API Test Failed", f"Gemini API test failed:\n\n{error}")
    
    def configure_api(self):
        """Open API configuration"""
        config_msg = """🔑 API Configuration

To configure your Gemini API key:

1. 📝 Get API Key:
   • Go to: https://aistudio.google.com/app/apikey
   • Create a new API key (free)
   • Copy the key

2. ⚙️ Set in Environment:
   • Edit the .env file in this folder
   • Set: GOOGLE_API_KEY=your_actual_key_here
   • Save the file

3. 🔄 Restart Application:
   • Close and reopen this GUI
   • Or click 'Test API' to verify

🔒 Security: Your API key stays on your computer and is never shared."""
        
        result = messagebox.askyesnocancel("API Configuration", f"{config_msg}\n\nOpen .env file now?")
        if result:  # Yes
            self.open_env_file()
    
    def open_env_file(self):
        """Open .env file for editing"""
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        try:
            if sys.platform == 'win32':
                os.startfile(env_file)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{env_file}"')
            else:  # Linux
                os.system(f'xdg-open "{env_file}"')
        except Exception as e:
            messagebox.showerror("Error", f"Could not open .env file: {e}")
    
    def show_api_help(self):
        """Show API help information"""
        webbrowser.open("https://aistudio.google.com/app/apikey")
        messagebox.showinfo("API Help", "Opening Google AI Studio in your browser to get an API key.")
    
    # Results Methods
    def show_results(self):
        """Switch to results tab"""
        if USE_MODERN_UI:
            self.notebook.set("📊 Results")
        else:
            self.notebook.select(3)
    
    def refresh_results(self):
        """Refresh results display"""
        # Could load from log file or recent operations
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        refresh_msg = f"\n🔄 Results refreshed at {current_time}\n"
        self.append_results(refresh_msg)
    
    def save_results_report(self):
        """Save results to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Results Report"
        )
        
        if filename:
            try:
                content = self.results_text.get("1.0", tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Saved", f"Results report saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save report: {e}")
    
    def clear_results(self):
        """Clear results display"""
        if messagebox.askyesno("Clear Results", "Are you sure you want to clear all results?"):
            self.results_text.delete("1.0", tk.END)
            self.update_results_display("📊 Results cleared.\n")
    
    # Utility Methods
    def update_status(self, operation, details):
        """Update status information"""
        self.last_operation.set(details)
        if hasattr(self, 'operation_label'):
            self.operation_label.configure(text=details)
    
    def update_api_status_label(self):
        """Update API status in status bar"""
        if hasattr(self, 'api_status_label'):
            self.api_status_label.configure(text=self.api_status.get())
    
    def update_cloud_status_label(self):
        """Update cloud status in status bar"""
        if hasattr(self, 'cloud_status_label'):
            self.cloud_status_label.configure(text=self.cloud_status.get())
    
    def update_preview_text(self, text):
        """Update preview text area"""
        if hasattr(self, 'preview_text'):
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert("1.0", text)
    
    def update_cloud_preview_text(self, text):
        """Update cloud preview text area"""
        if hasattr(self, 'cloud_preview_text'):
            self.cloud_preview_text.delete("1.0", tk.END)
            self.cloud_preview_text.insert("1.0", text)
    
    def update_results_display(self, text):
        """Update results display"""
        if hasattr(self, 'results_text'):
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert("1.0", text)
    
    def append_results(self, text):
        """Append text to results display"""
        if hasattr(self, 'results_text'):
            self.results_text.insert(tk.END, text)
            # Scroll to bottom
            self.results_text.see(tk.END)
    
    def check_dependencies(self):
        """Check and report on dependencies"""
        # Check API key
        self.root.after(1000, self._check_api_status)
        
        # Check for organizer modules
        self.root.after(2000, self._check_organizer_modules)
    
    def _check_api_status(self):
        """Check API status on startup"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key and api_key != 'your_gemini_pro_api_key_here':
                self.api_status.set("✅ Configured")
                self.detailed_api_status.configure(text="✅ API key is configured")
            else:
                self.api_status.set("❌ Not set")
                self.detailed_api_status.configure(text="❌ API key not configured - click 'Configure API'")
        except Exception as e:
            self.api_status.set("❌ Error")
            self.detailed_api_status.configure(text=f"❌ Error checking API: {str(e)}")
        
        self.update_api_status_label()
    
    def _check_organizer_modules(self):
        """Check for organizer modules"""
        modules_found = []
        
        if os.path.exists('ai_organizer_pro.py'):
            modules_found.append('AI Organizer Pro')
        if os.path.exists('ultimate_file_organizer.py'):
            modules_found.append('Ultimate File Organizer')
        if os.path.exists('google_drive_organizer.py'):
            modules_found.append('Google Drive Organizer')
        
        if modules_found:
            status = f"✅ Found: {', '.join(modules_found)}"
        else:
            status = "⚠️ No organizer modules found"
        
        self.update_status("Dependencies checked", status)
    
    def run(self):
        """Start the GUI application"""
        # Set window icon if available
        try:
            # Try to set a nice icon
            pass
        except:
            pass
        
        # Start the main loop
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        # Create and run the GUI
        print("🚀 Starting AI File Organizer GUI...")
        app = AIFileOrganizerGUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try running: python install_gui.py")
        
        # Fallback to command line
        print("🔄 Falling back to command line interface...")
        try:
            import ultimate_file_organizer
            ultimate_file_organizer.main()
        except ImportError:
            print("❌ No organizer modules found. Please check installation.")
            
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        messagebox.showerror("Startup Error", f"Failed to start GUI: {e}")

if __name__ == "__main__":
    main()