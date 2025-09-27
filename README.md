# 🚀 Ultimate AI File Organizer Agent

**Transform your chaotic file system into a masterpiece of organization!**

This enhanced AI-powered file organizer uses Google Gemini Pro to analyze, categorize, and restructure your files with the precision of a professional organizer. It's like hiring an obsessive-compulsive neat freak for 2 weeks to organize all your digital files!

## 🌟 Features

### 🧠 **AI-Powered Intelligence**
- **Gemini Pro Integration**: Uses Google's most advanced AI for intelligent file analysis
- **Content-Based Organization**: Analyzes file content, not just names
- **Smart Categorization**: Automatically detects file types and purposes
- **Professional Structure**: Creates logical, searchable folder hierarchies

### ☁️ **Multi-Cloud Support**
- **Google Drive Integration**: Organize your cloud files seamlessly
- **Dropbox Support**: Sync organization across platforms  
- **OneDrive Compatible**: (Configuration required)
- **Cross-Platform Sync**: Same organization rules on all devices

### 🛡️ **Safety & Reliability**
- **Automatic Backups**: Creates backups before any changes
- **Safe Operations**: Uses Model Context Protocol for secure file handling
- **Duplicate Detection**: Identifies and handles duplicate files intelligently
- **Rollback Capability**: Easy to undo changes if needed

### 🎨 **Customizable Organization Styles**
- **Professional**: `Documents/Financial/2024/` - Perfect for business
- **Personal**: `2024/Photos/Family/` - Date-first organization
- **Creative**: `Projects/WebsiteRedesign/Assets/` - Project-based structure  
- **Minimal**: `Documents/`, `Images/` - Simple flat categories

### 📊 **Advanced Features**
- **Metadata Extraction**: Reads EXIF data, document properties, etc.
- **Smart Tagging**: Adds searchable metadata to files
- **Batch Processing**: Handles large file collections efficiently
- **Progress Tracking**: Visual progress bars and status updates
- **Detailed Logging**: Complete audit trail of all changes

## 🚀 Quick Start

### Option 1: Super Easy Setup
1. **Double-click** `Run_Ultimate_File_Organizer.bat`
2. Follow the setup prompts
3. Enter your [Gemini API key](https://aistudio.google.com/app/apikey) 
4. Start organizing!

### Option 2: Manual Setup
1. **Install Requirements:**
   ```bash
   # Install Python 3.8+ from python.org
   # Install Node.js LTS from nodejs.org
   pip install -r requirements.txt
   ```

2. **Get Gemini API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a free API key
   - Add it to `.env` file:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Run the Organizer:**
   ```bash
   python ultimate_file_organizer.py
   ```

## 📋 Requirements

**System Requirements:**
- Windows 10/11, macOS 10.14+, or Linux
- Python 3.8 or higher  
- Node.js 16+ (for MCP filesystem operations)
- 4GB+ RAM (for large file collections)
- Internet connection (for AI processing)

**API Requirements:**
- Google Gemini API key (free tier available)
- Optional: Cloud storage API credentials

## ⚙️ Configuration Files

### `.env` - Main Configuration
```env
# Required: Your Gemini Pro API key
GOOGLE_API_KEY=your_key_here

# Optional: Default directory to organize
DEFAULT_TARGET_DIR=C:\Users\YourName\Downloads

# Safety: Highest accessible directory  
TOP_LEVEL_ALLOWED_PATH=C:\Users\YourName

# Organization style: professional, personal, creative, minimal
ORGANIZATION_STYLE=professional

# Enable advanced features
ENABLE_CONTENT_ANALYSIS=True
ENABLE_SMART_TAGGING=True
ENABLE_CLOUD_SYNC=True
AUTO_BACKUP_BEFORE_ORGANIZE=True
```

### `cloud_credentials.json` - Cloud Storage (Optional)
```json
{
  "google_drive": {
    "enabled": false,
    "client_id": "your_google_client_id",
    "client_secret": "your_google_client_secret"
  },
  "dropbox": {
    "enabled": false, 
    "access_token": "your_dropbox_token"
  }
}
```

## 🎯 Usage Examples

### Basic Local Organization
```bash
python ultimate_file_organizer.py
# Select folder: C:\Users\YourName\Downloads
# AI analyzes 500+ files
# Creates: Documents/Financial/2024/, Images/Screenshots/, etc.
# Moves files intelligently based on content
```

### Cloud Storage Sync
```bash
python cloud_storage.py
# Organizes Google Drive folders
# Syncs organization rules across devices
# Maintains consistent structure everywhere
```

### Professional Document Organization
**Before:**
```
Downloads/
├── invoice_january.pdf
├── IMG_001.jpg  
├── random_document.docx
├── screenshot.png
└── music_file.mp3
```

**After (Professional Style):**
```
Downloads/
├── Documents/
│   ├── Financial/
│   │   └── 2024/
│   │       └── Invoice_2024-01-15.pdf
│   └── Personal/
│       └── Random_Document.docx
├── Media/
│   ├── Images/
│   │   └── Screenshots/
│   │       └── Screenshot_2024-01-15.png
│   └── Audio/
│       └── Music_File.mp3
└── backup_before_organization_20240115_143022/
    └── [original files backed up]
```

## 🔧 Advanced Features

### Content Analysis
The AI analyzes file content to make intelligent decisions:
- **PDF Analysis**: Detects invoices, contracts, personal documents
- **Image Analysis**: Distinguishes screenshots, photos, graphics, wallpapers
- **Document Analysis**: Identifies work files, personal letters, reports
- **Media Analysis**: Extracts metadata from photos, audio, videos

### Smart Naming
Automatically improves filenames:
- **Date Standardization**: `IMG_20240115` → `Photo_2024-01-15`
- **Descriptive Names**: `document.pdf` → `Financial_Report_2024-01-15.pdf`
- **Special Character Removal**: `file<>name.txt` → `File_Name.txt`
- **Length Optimization**: Keeps names under 100 characters

### Cloud Integration
- **Google Drive**: Full API integration for organizing cloud files
- **Dropbox**: Sync organization rules and folder structures
- **OneDrive**: Basic support (manual configuration required)
- **Multi-Device Sync**: Same organization rules across all computers

## 🛠️ Troubleshooting

### Common Issues

**"npx not found"**
```bash
# Install Node.js from nodejs.org
# Verify installation:
node --version
npx --version
```

**"Gemini API Error"**
- Check your API key in `.env` file
- Verify internet connection
- Check API quota at [Google AI Studio](https://aistudio.google.com/)

**"Permission Denied"** 
- Run as administrator on Windows
- Check folder permissions
- Ensure target directory is writable

**"Import Errors"**
```bash
# Reinstall requirements:
pip install --upgrade -r requirements.txt

# Or install missing packages individually:
pip install agno google-genai python-dotenv
```

### Debug Mode
Enable detailed logging:
```env
DEBUG=True
```

### Backup Recovery
If something goes wrong:
```bash
# Backups are automatically created in:
# [original_folder]/../backup_before_organization_[timestamp]/

# Simply copy files back from backup folder
```

## 📝 File Organization Patterns

The AI uses professional organization patterns based on your chosen style:

### Professional Style (Business/Office)
```
📁 Documents/
  ├── 📁 Financial/
  │   ├── 📁 2024/ (Invoices, receipts, tax docs)
  │   ├── 📁 2023/
  │   └── 📁 Archive/
  ├── 📁 Legal/ (Contracts, agreements)
  ├── 📁 Work/ (Reports, presentations)
  └── 📁 Personal/ (Personal documents)

📁 Media/
  ├── 📁 Images/
  │   ├── 📁 Screenshots/
  │   ├── 📁 Photos/
  │   └── 📁 Graphics/
  └── 📁 Videos/

📁 Development/
  ├── 📁 Projects/
  ├── 📁 Scripts/
  └── 📁 Resources/
```

### Personal Style (Home/Family)
```
📁 2024/
  ├── 📁 Photos/
  │   ├── 📁 Family/
  │   ├── 📁 Vacation/
  │   └── 📁 Events/
  ├── 📁 Documents/
  │   ├── 📁 Important/
  │   └── 📁 General/
  └── 📁 Projects/

📁 2023/
  └── [Same structure]
```

## 🌟 Pro Tips

1. **Start Small**: Test with a small folder first (like Downloads)
2. **Use Backups**: Always keep the automatic backups until you're satisfied
3. **Regular Organization**: Run weekly to keep files organized
4. **Cloud Sync**: Set up cloud integration to maintain consistency
5. **Custom Rules**: Edit organization rules in `~/.ai_file_organizer/`

## 📚 API Documentation

### Main Classes
- `UltimateFileOrganizer`: Core organization engine
- `CloudStorageManager`: Multi-cloud integration  
- `FileAnalyzer`: Content analysis and metadata extraction

### Key Methods
```python
organizer = UltimateFileOrganizer()
await organizer.run_ultimate_organization("/path/to/folder")
await organizer.sync_organization_rules(rules)
```

## 🤝 Contributing

Want to improve the Ultimate File Organizer?
1. Fork the repository
2. Add your enhancements  
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

**Need Help?**
- Check the troubleshooting section above
- Review the configuration files
- Enable debug mode for detailed logs
- Create an issue if you find bugs

**Feature Requests?**
- Open an issue with your idea
- Describe your use case
- We love making this tool better!

---

## 🎉 Transform Your Digital Life Today!

Stop wasting time searching for files in chaotic folders. Let the Ultimate AI File Organizer bring order to your digital world with the precision and attention to detail that only AI can provide.

**Your files will thank you! 🙌**
*   `DEFAULT_TARGET_DIR`: Optional. Set this to the full path of the directory you usually want to organize (e.g., `/Users/yourname/Downloads`). If this is set and valid (exists and is within `TOP_LEVEL_ALLOWED_PATH`), the script will skip the prompt. If left empty (`""`), the script will always prompt you.
*   `TOP_LEVEL_ALLOWED_PATH`: Optional. Set this to the absolute highest-level directory the script should *ever* be allowed to access (even when prompting). Defaults to the user's home directory (`~`) if not set. For safety, you might restrict this further, e.g., `~/Documents`.
*   `DEBUG`: Optional. Set to `True` to enable detailed debugging output (like the full agent response object). Defaults to `False` if not set.

## Running the Script

1.  Ensure your virtual environment is activated (if using one).
2.  Make sure your `.env` file with the API key is present.
3.  Run the script from your terminal:
    ```bash
    python file_organizer_agent.py
    ```
4.  Follow the prompts:
    *   If `DEFAULT_TARGET_DIR` is not set or invalid, it will ask for the target directory (which must be inside `TOP_LEVEL_ALLOWED_PATH`).
    *   It will ask the agent to list the files (this uses the Gemini API).
    *   It will ask the agent to propose a plan (uses the Gemini API, may take time for large directories).
    *   Review the extracted plan actions.
    *   Type `yes` to execute the plan, `no` to exit, or provide text feedback to ask the agent for a revised plan.

## How it Works

1.  **Setup:** Loads the API key and configuration from the `.env` file, determines the target directory, and initializes the Gemini model via Agno.
2.  **MCP Server:** Launches the `@modelcontextprotocol/server-filesystem` process using `npx`, restricting it to operate only within the determined target directory (`ALLOWED_BASE_PATH_STR`).
3.  **Initial Scan:** Instructs the agent to use the `list_directory` tool (via MCP) to get the initial file structure.
4.  **Planning:** Sends the file structure to the Gemini model and asks for an organization plan, formatted as a sequence of `create_directory` and `move_file` tool calls with relative paths. Instructions guide the agent on desired structure, path usage, and execution order.
5.  **Review:** Extracts the tool calls from the agent's response and displays them clearly for user confirmation.
6.  **Execution (if approved):** Sends the extracted plan back to the agent, instructing it to execute the listed tool calls sequentially via the MCP server.
7.  **Revision (if feedback given):** Sends the user's feedback to the agent, asking it to generate a new plan, potentially re-listing the directory first if needed.

## Error Handling

*   Catches and reports errors during model initialization (e.g., missing API key).
*   Catches and reports errors if `npx` is not found.
*   Catches API rate limit errors (429) during agent calls, prints a message, pauses for ~65 seconds, and allows the user to retry the last action.
*   Catches other model communication errors.

## Notes

*   The quality and logic of the organization plan depend heavily on the capabilities of the Gemini model (`gemini-1.5-flash` currently).
*   Complex directory structures or ambiguous filenames might lead to suboptimal or occasionally flawed plans (like the self-move issue the prompts now try to prevent). Always review the plan carefully before executing.
*   Ensure the user running the script has appropriate read/write permissions for the target directory.
