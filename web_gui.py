"""
AI File Organizer Agent - Web GUI
=================================
Modern web-based interface using Flask for better compatibility.
"""

import webbrowser
import threading
import time
import os
import sys
from pathlib import Path
import json
from datetime import datetime
import subprocess

try:
    from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

class WebGUI:
    """Web-based GUI for AI File Organizer"""
    
    def __init__(self, port=5000):
        if not HAS_FLASK:
            raise ImportError("Flask not installed. Run: pip install flask")
        
        self.port = port
        self.app = Flask(__name__, template_folder='templates', static_folder='static')
        self.setup_routes()
        self.server_thread = None
        
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return self.render_main_page()
        
        @self.app.route('/api/analyze', methods=['POST'])
        def analyze_folder():
            data = request.json
            folder_path = data.get('folder_path', '')
            
            if not folder_path or not os.path.exists(folder_path):
                return jsonify({'error': 'Invalid folder path'}), 400
            
            try:
                # Basic analysis for now
                analysis = self.analyze_folder_basic(folder_path)
                return jsonify(analysis)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/organize', methods=['POST'])
        def organize_files():
            data = request.json
            folder_path = data.get('folder_path', '')
            
            if not folder_path or not os.path.exists(folder_path):
                return jsonify({'error': 'Invalid folder path'}), 400
            
            try:
                # Organize files
                result = self.organize_folder_files(folder_path)
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/status')
        def get_status():
            return jsonify({
                'api_configured': self.check_api_configured(),
                'organizer_available': self.check_organizer_available(),
                'timestamp': datetime.now().isoformat()
            })
    
    def render_main_page(self):
        """Render the main HTML page"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 AI File Organizer Agent</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(90deg, #4f46e5, #7c3aed);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .content {
            padding: 30px;
        }
        .tabs {
            display: flex;
            margin-bottom: 30px;
            border-bottom: 2px solid #e5e7eb;
        }
        .tab-btn {
            padding: 15px 25px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            color: #6b7280;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }
        .tab-btn.active {
            color: #4f46e5;
            border-bottom-color: #4f46e5;
        }
        .tab-content {
            display: none;
            animation: fadeIn 0.3s ease;
        }
        .tab-content.active {
            display: block;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .section {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
        }
        .section h3 {
            margin-bottom: 15px;
            color: #1e293b;
            font-size: 1.3em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #374151;
        }
        .form-control {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #d1d5db;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        .form-control:focus {
            outline: none;
            border-color: #4f46e5;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
        .btn-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }
        .btn-primary {
            background: #4f46e5;
            color: white;
        }
        .btn-primary:hover {
            background: #4338ca;
            transform: translateY(-2px);
        }
        .btn-secondary {
            background: #6b7280;
            color: white;
        }
        .btn-secondary:hover {
            background: #374151;
        }
        .btn-success {
            background: #10b981;
            color: white;
        }
        .btn-success:hover {
            background: #059669;
        }
        .preview-area {
            background: #1f2937;
            color: #f9fafb;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            margin-top: 15px;
        }
        .status-bar {
            background: #f1f5f9;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }
        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }
        .status-ok { background: #10b981; }
        .status-error { background: #ef4444; }
        .status-warning { background: #f59e0b; }
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .quick-action {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .quick-action:hover {
            border-color: #4f46e5;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        .quick-action h4 {
            margin-bottom: 10px;
            color: #1e293b;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #4f46e5;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .alert-success {
            background: #d1fae5;
            border: 1px solid #a7f3d0;
            color: #065f46;
        }
        .alert-error {
            background: #fee2e2;
            border: 1px solid #fca5a5;
            color: #991b1b;
        }
        .alert-info {
            background: #dbeafe;
            border: 1px solid #93c5fd;
            color: #1e40af;
        }
        @media (max-width: 768px) {
            .container { margin: 10px; }
            .header { padding: 20px; }
            .header h1 { font-size: 2em; }
            .content { padding: 20px; }
            .tabs { flex-wrap: wrap; }
            .btn-group { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI File Organizer Agent</h1>
            <p>Intelligent file organization powered by AI • Local & Cloud Support</p>
        </div>
        
        <div class="content">
            <!-- Status Bar -->
            <div class="status-bar">
                <div class="status-item">
                    <div class="status-indicator status-warning" id="api-indicator"></div>
                    <span>API Status: <span id="api-status">Checking...</span></span>
                </div>
                <div class="status-item">
                    <div class="status-indicator status-warning" id="organizer-indicator"></div>
                    <span>Organizer: <span id="organizer-status">Checking...</span></span>
                </div>
                <div class="status-item">
                    <span>Last Update: <span id="last-update">Starting...</span></span>
                </div>
            </div>
            
            <!-- Tabs -->
            <div class="tabs">
                <button class="tab-btn active" onclick="showTab('local')">📁 Local Files</button>
                <button class="tab-btn" onclick="showTab('cloud')">☁️ Google Drive</button>
                <button class="tab-btn" onclick="showTab('settings')">⚙️ Settings</button>
                <button class="tab-btn" onclick="showTab('results')">📊 Results</button>
            </div>
            
            <!-- Local Files Tab -->
            <div id="local-tab" class="tab-content active">
                <div class="section">
                    <h3>📂 Select Folder to Organize</h3>
                    <div class="form-group">
                        <label for="folder-path">Folder Path:</label>
                        <input type="text" id="folder-path" class="form-control" placeholder="Enter folder path or use quick actions below">
                    </div>
                    <div class="quick-actions">
                        <div class="quick-action" onclick="setQuickFolder('Downloads')">
                            <h4>📥 Downloads</h4>
                            <p>Organize download folder</p>
                        </div>
                        <div class="quick-action" onclick="setQuickFolder('Documents')">
                            <h4>📄 Documents</h4>
                            <p>Organize documents folder</p>
                        </div>
                        <div class="quick-action" onclick="setQuickFolder('Pictures')">
                            <h4>🖼️ Pictures</h4>
                            <p>Organize pictures folder</p>
                        </div>
                        <div class="quick-action" onclick="setQuickFolder('Desktop')">
                            <h4>🖥️ Desktop</h4>
                            <p>Organize desktop files</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h3>🔍 Organization Preview</h3>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="analyzeFolder()">🔍 Analyze Folder</button>
                        <button class="btn btn-success" onclick="organizeFolder()">🚀 Organize Files</button>
                        <button class="btn btn-secondary" onclick="showTab('results')">📊 View Results</button>
                    </div>
                    <div id="preview-area" class="preview-area">
Click "Analyze Folder" to see organization preview...
                    </div>
                    <div id="loading-local" class="loading">
                        <div class="spinner"></div>
                        <p>Processing folder...</p>
                    </div>
                </div>
            </div>
            
            <!-- Google Drive Tab -->
            <div id="cloud-tab" class="tab-content">
                <div class="section">
                    <h3>🔗 Google Drive Connection</h3>
                    <div class="alert alert-info">
                        <strong>Coming Soon!</strong> Google Drive integration will be available in the next update. For now, use the command-line version: <code>python google_drive_organizer.py</code>
                    </div>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="connectDrive()" disabled>🔐 Connect Drive</button>
                        <button class="btn btn-secondary" onclick="showDriveHelp()">ℹ️ Setup Help</button>
                    </div>
                </div>
            </div>
            
            <!-- Settings Tab -->
            <div id="settings-tab" class="tab-content">
                <div class="section">
                    <h3>🎨 Organization Settings</h3>
                    <div class="form-group">
                        <label for="org-style">Organization Style:</label>
                        <select id="org-style" class="form-control">
                            <option value="professional">Professional</option>
                            <option value="personal">Personal</option>
                            <option value="creative">Creative</option>
                            <option value="minimal">Minimal</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="enable-backup" checked> 🔒 Create backup before organizing
                        </label>
                    </div>
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="enable-content" checked> 🧠 Enable AI content analysis
                        </label>
                    </div>
                </div>
                
                <div class="section">
                    <h3>🔑 API Configuration</h3>
                    <div class="alert alert-info">
                        <strong>Setup Required:</strong> Configure your Gemini API key in the <code>.env</code> file for AI-powered organization.
                    </div>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="testAPI()">🔍 Test API</button>
                        <button class="btn btn-secondary" onclick="openApiHelp()">📖 Get API Key</button>
                    </div>
                </div>
                
                <div class="section">
                    <h3>ℹ️ About</h3>
                    <p><strong>AI File Organizer Agent v2.0</strong></p>
                    <p>Intelligent file categorization using Google Gemini AI with support for local files and Google Drive cloud storage.</p>
                    <div class="btn-group">
                        <button class="btn btn-secondary" onclick="openGithub()">📚 View on GitHub</button>
                        <button class="btn btn-secondary" onclick="openDocumentation()">📖 Documentation</button>
                    </div>
                </div>
            </div>
            
            <!-- Results Tab -->
            <div id="results-tab" class="tab-content">
                <div class="section">
                    <h3>📊 Organization Results</h3>
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick="refreshResults()">🔄 Refresh</button>
                        <button class="btn btn-secondary" onclick="clearResults()">🗑️ Clear</button>
                    </div>
                    <div id="results-area" class="preview-area">
🎉 Welcome to AI File Organizer Agent!

Results from your organization operations will appear here.

Get started by:
1. Going to the "Local Files" tab
2. Selecting a folder to organize
3. Clicking "Analyze Folder" to see the preview
4. Clicking "Organize Files" to execute the organization

Your files will be intelligently categorized using AI!
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Tab management
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }
        
        // Quick folder selection
        function setQuickFolder(folderName) {
            const commonPaths = {
                'Downloads': 'C:\\\\Users\\\\' + (window.navigator.userAgent.includes('Windows') ? '%USERNAME%' : 'user') + '\\\\Downloads',
                'Documents': 'C:\\\\Users\\\\' + (window.navigator.userAgent.includes('Windows') ? '%USERNAME%' : 'user') + '\\\\Documents',
                'Pictures': 'C:\\\\Users\\\\' + (window.navigator.userAgent.includes('Windows') ? '%USERNAME%' : 'user') + '\\\\Pictures',
                'Desktop': 'C:\\\\Users\\\\' + (window.navigator.userAgent.includes('Windows') ? '%USERNAME%' : 'user') + '\\\\Desktop'
            };
            
            document.getElementById('folder-path').value = commonPaths[folderName] || '';
            showMessage('Folder selected: ' + folderName, 'info');
        }
        
        // Analyze folder
        async function analyzeFolder() {
            const folderPath = document.getElementById('folder-path').value.trim();
            if (!folderPath) {
                showMessage('Please enter a folder path', 'error');
                return;
            }
            
            showLoading('local', true);
            document.getElementById('preview-area').textContent = 'Analyzing folder contents...';
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ folder_path: folderPath })
                });
                
                const result = await response.json();
                
                if (result.error) {
                    throw new Error(result.error);
                }
                
                displayAnalysisResult(result);
                showMessage('Analysis completed successfully!', 'success');
                
            } catch (error) {
                document.getElementById('preview-area').textContent = 'Error: ' + error.message;
                showMessage('Analysis failed: ' + error.message, 'error');
            } finally {
                showLoading('local', false);
            }
        }
        
        // Organize folder
        async function organizeFolder() {
            const folderPath = document.getElementById('folder-path').value.trim();
            if (!folderPath) {
                showMessage('Please enter a folder path', 'error');
                return;
            }
            
            if (!confirm('This will organize files in: ' + folderPath + '\\n\\nA backup will be created. Continue?')) {
                return;
            }
            
            showLoading('local', true);
            
            try {
                const response = await fetch('/api/organize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ folder_path: folderPath })
                });
                
                const result = await response.json();
                
                if (result.error) {
                    throw new Error(result.error);
                }
                
                // Switch to results tab and show results
                showTab('results');
                displayOrganizationResult(result);
                showMessage('Files organized successfully!', 'success');
                
            } catch (error) {
                showMessage('Organization failed: ' + error.message, 'error');
            } finally {
                showLoading('local', false);
            }
        }
        
        // Display analysis result
        function displayAnalysisResult(result) {
            let display = '📊 FOLDER ANALYSIS RESULTS\\n';
            display += '='.repeat(50) + '\\n\\n';
            
            if (result.total_files !== undefined) {
                display += '📁 Total Files: ' + result.total_files + '\\n\\n';
            }
            
            if (result.file_types) {
                display += '📄 File Types:\\n';
                Object.entries(result.file_types)
                    .sort((a, b) => b[1] - a[1])
                    .forEach(([ext, count]) => {
                        display += '   • ' + (ext || 'No extension') + ': ' + count + ' files\\n';
                    });
                display += '\\n';
            }
            
            if (result.size_distribution) {
                display += '📏 Size Distribution:\\n';
                Object.entries(result.size_distribution).forEach(([size, count]) => {
                    display += '   • ' + size + ': ' + count + ' files\\n';
                });
                display += '\\n';
            }
            
            display += '💡 Ready for organization! Click "Organize Files" to proceed.';
            
            document.getElementById('preview-area').textContent = display;
        }
        
        // Display organization result
        function displayOrganizationResult(result) {
            const timestamp = new Date().toLocaleString();
            let display = '\\n🎉 ORGANIZATION COMPLETED - ' + timestamp + '\\n';
            display += '='.repeat(60) + '\\n\\n';
            
            display += '📊 Results Summary:\\n';
            display += '   • Files organized: ' + (result.files_moved || 0) + '\\n';
            display += '   • Folders created: ' + (result.folders_created || 0) + '\\n';
            display += '   • Backup location: ' + (result.backup_path || 'N/A') + '\\n\\n';
            
            if (result.organization_summary) {
                display += '📁 Folder Structure:\\n' + result.organization_summary + '\\n';
            }
            
            if (result.errors && result.errors.length > 0) {
                display += '\\n⚠️ Warnings/Errors:\\n';
                result.errors.forEach(error => {
                    display += '   • ' + error + '\\n';
                });
            }
            
            display += '\\n' + '='.repeat(60) + '\\n';
            
            document.getElementById('results-area').textContent += display;
        }
        
        // Utility functions
        function showLoading(section, show) {
            document.getElementById('loading-' + section).style.display = show ? 'block' : 'none';
        }
        
        function showMessage(message, type) {
            // Create or update message area
            let msgDiv = document.getElementById('message-area');
            if (!msgDiv) {
                msgDiv = document.createElement('div');
                msgDiv.id = 'message-area';
                msgDiv.style.position = 'fixed';
                msgDiv.style.top = '20px';
                msgDiv.style.right = '20px';
                msgDiv.style.zIndex = '1000';
                msgDiv.style.maxWidth = '400px';
                document.body.appendChild(msgDiv);
            }
            
            const alert = document.createElement('div');
            alert.className = 'alert alert-' + type;
            alert.textContent = message;
            alert.style.marginBottom = '10px';
            
            msgDiv.appendChild(alert);
            
            // Auto remove after 5 seconds
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 5000);
        }
        
        // External links
        function openApiHelp() {
            window.open('https://aistudio.google.com/app/apikey', '_blank');
        }
        
        function openGithub() {
            window.open('https://github.com/ApexDazza/AI-File-Organizer-Agent', '_blank');
        }
        
        function openDocumentation() {
            showMessage('Documentation available in the GitHub repository', 'info');
        }
        
        function showDriveHelp() {
            alert('Google Drive Setup:\\n\\n1. Run: python google_drive_organizer.py\\n2. Follow the OAuth setup process\\n3. Use the command-line interface for now\\n\\nWeb interface coming soon!');
        }
        
        // Status checking
        async function checkStatus() {
            try {
                const response = await fetch('/api/status');
                const status = response.json();
                
                // Update UI indicators
                updateStatusIndicator('api', status.api_configured);
                updateStatusIndicator('organizer', status.organizer_available);
                
                document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
                
            } catch (error) {
                console.log('Status check failed:', error);
            }
        }
        
        function updateStatusIndicator(type, isOk) {
            const indicator = document.getElementById(type + '-indicator');
            const status = document.getElementById(type + '-status');
            
            if (isOk) {
                indicator.className = 'status-indicator status-ok';
                status.textContent = 'Ready';
            } else {
                indicator.className = 'status-indicator status-error';
                status.textContent = 'Not Ready';
            }
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            checkStatus();
            setInterval(checkStatus, 30000); // Check every 30 seconds
        });
        
        // Placeholder functions
        function testAPI() { showMessage('API test functionality will be implemented', 'info'); }
        function refreshResults() { showMessage('Results refreshed', 'info'); }
        function clearResults() { 
            if (confirm('Clear all results?')) {
                document.getElementById('results-area').textContent = 'Results cleared.\\n';
            }
        }
        function connectDrive() { showMessage('Use command-line version for now: python google_drive_organizer.py', 'info'); }
    </script>
</body>
</html>
        """
        return html_content
    
    def analyze_folder_basic(self, folder_path):
        """Basic folder analysis"""
        analysis = {
            'total_files': 0,
            'file_types': {},
            'size_distribution': {}
        }
        
        try:
            for root, dirs, files in os.walk(folder_path):
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
            print(f"Error in analysis: {e}")
        
        return analysis
    
    def organize_folder_files(self, folder_path):
        """Organize files in folder"""
        try:
            # Try to import and use actual organizer
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
                    # Fallback to basic organization
                    return self.basic_file_organization(folder_path)
            
            if organizer and hasattr(organizer, 'organize_folder'):
                return organizer.organize_folder(folder_path)
            else:
                return self.basic_file_organization(folder_path)
                
        except Exception as e:
            raise Exception(f"Organization failed: {str(e)}")
    
    def basic_file_organization(self, folder_path):
        """Basic file organization fallback"""
        return {
            'files_moved': 0,
            'folders_created': 0,
            'backup_path': 'N/A',
            'organization_summary': 'Basic organization not implemented. Please install AI components.',
            'errors': ['AI organizer not available - install dependencies for full functionality']
        }
    
    def check_api_configured(self):
        """Check if API is configured"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv('GOOGLE_API_KEY')
            return api_key and api_key != 'your_gemini_pro_api_key_here'
        except:
            return False
    
    def check_organizer_available(self):
        """Check if organizer modules are available"""
        return (os.path.exists('ai_organizer_pro.py') or 
                os.path.exists('ultimate_file_organizer.py'))
    
    def start_server(self):
        """Start the Flask server"""
        if self.server_thread and self.server_thread.is_alive():
            return
        
        self.server_thread = threading.Thread(
            target=lambda: self.app.run(host='localhost', port=self.port, debug=False, use_reloader=False),
            daemon=True
        )
        self.server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(2)
    
    def open_browser(self):
        """Open the web interface in browser"""
        url = f"http://localhost:{self.port}"
        webbrowser.open(url)
    
    def run(self):
        """Run the web GUI"""
        try:
            print("🚀 Starting AI File Organizer Web GUI...")
            print(f"📡 Starting server on http://localhost:{self.port}")
            
            self.start_server()
            
            print("🌐 Opening web browser...")
            self.open_browser()
            
            print("✅ Web GUI is running!")
            print(f"🔗 Access at: http://localhost:{self.port}")
            print("⚠️  Close this terminal to stop the server")
            
            # Keep the main thread alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\\n🛑 Shutting down web server...")
                
        except Exception as e:
            print(f"❌ Failed to start web GUI: {e}")
            raise

def main():
    """Main entry point for web GUI"""
    try:
        # Check if Flask is available
        if not HAS_FLASK:
            print("❌ Flask not installed. Installing...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("✅ Flask installed successfully!")
            
            # Restart to import Flask
            print("🔄 Restarting to load Flask...")
            os.execv(sys.executable, ['python'] + sys.argv)
        
        # Create and run web GUI
        web_gui = WebGUI(port=5000)
        web_gui.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\\n💡 Falling back to command-line interface...")
        
        # Try to run command-line version
        try:
            if os.path.exists('ultimate_file_organizer.py'):
                import ultimate_file_organizer
                ultimate_file_organizer.main()
            elif os.path.exists('ai_organizer_pro.py'):
                import ai_organizer_pro
                ai_organizer_pro.main()
            else:
                print("❌ No organizer modules found")
        except Exception as fallback_error:
            print(f"❌ Fallback failed: {fallback_error}")

if __name__ == "__main__":
    main()