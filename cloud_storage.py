"""
Cloud Storage Integration for Ultimate File Organizer
==================================================

Supports:
- Google Drive
- Microsoft OneDrive  
- Dropbox
- Local sync and organization across all platforms

Author: Enhanced by GitHub Copilot
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio

try:
    # Google Drive API
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

try:
    # Dropbox API  
    import dropbox
    DROPBOX_AVAILABLE = True
except ImportError:
    DROPBOX_AVAILABLE = False

try:
    # OneDrive - using requests for Graph API
    import requests
    ONEDRIVE_AVAILABLE = True
except ImportError:
    ONEDRIVE_AVAILABLE = False

class CloudStorageManager:
    """Manages file organization across multiple cloud storage platforms."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or (Path.home() / '.ai_file_organizer')
        self.config_dir.mkdir(exist_ok=True)
        self.credentials_file = self.config_dir / 'cloud_credentials.json'
        self.sync_rules_file = self.config_dir / 'sync_rules.json'
        
        # Initialize available services
        self.services = {}
        self.load_credentials()
        
    def load_credentials(self):
        """Load stored cloud service credentials."""
        if not self.credentials_file.exists():
            self._create_default_credentials_file()
            return
            
        try:
            with open(self.credentials_file, 'r') as f:
                creds = json.load(f)
                
            # Initialize Google Drive if configured
            if GOOGLE_AVAILABLE and creds.get('google_drive', {}).get('enabled'):
                self._init_google_drive(creds['google_drive'])
                
            # Initialize Dropbox if configured  
            if DROPBOX_AVAILABLE and creds.get('dropbox', {}).get('enabled'):
                self._init_dropbox(creds['dropbox'])
                
            # Initialize OneDrive if configured
            if ONEDRIVE_AVAILABLE and creds.get('onedrive', {}).get('enabled'):
                self._init_onedrive(creds['onedrive'])
                
        except Exception as e:
            print(f"Warning: Could not load cloud credentials: {e}")
    
    def _create_default_credentials_file(self):
        """Create a default credentials configuration file."""
        default_config = {
            "google_drive": {
                "enabled": False,
                "client_id": "",
                "client_secret": "",
                "scopes": [
                    "https://www.googleapis.com/auth/drive"
                ],
                "sync_folders": [
                    "Documents",
                    "Pictures", 
                    "Downloads"
                ]
            },
            "dropbox": {
                "enabled": False,
                "access_token": "",
                "sync_folders": [
                    "/Documents",
                    "/Pictures",
                    "/Camera Uploads"
                ]
            },
            "onedrive": {
                "enabled": False,
                "client_id": "",
                "client_secret": "",
                "tenant_id": "common",
                "sync_folders": [
                    "Documents",
                    "Pictures",
                    "Desktop"
                ]
            }
        }
        
        with open(self.credentials_file, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        print(f"📝 Created cloud credentials template at: {self.credentials_file}")
        print("✏️  Edit this file to add your cloud service credentials")
    
    def _init_google_drive(self, config: Dict[str, Any]):
        """Initialize Google Drive service."""
        try:
            creds = None
            token_file = self.config_dir / 'google_token.json'
            
            if token_file.exists():
                creds = Credentials.from_authorized_user_file(str(token_file))
                
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_config({
                        "installed": {
                            "client_id": config['client_id'],
                            "client_secret": config['client_secret'],
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token"
                        }
                    }, config['scopes'])
                    creds = flow.run_local_server(port=0)
                    
                with open(token_file, 'w') as f:
                    f.write(creds.to_json())
            
            self.services['google_drive'] = build('drive', 'v3', credentials=creds)
            print("✅ Google Drive connected successfully")
            
        except Exception as e:
            print(f"❌ Failed to connect to Google Drive: {e}")
    
    def _init_dropbox(self, config: Dict[str, Any]):
        """Initialize Dropbox service."""
        try:
            self.services['dropbox'] = dropbox.Dropbox(config['access_token'])
            # Test connection
            self.services['dropbox'].users_get_current_account()
            print("✅ Dropbox connected successfully")
            
        except Exception as e:
            print(f"❌ Failed to connect to Dropbox: {e}")
    
    def _init_onedrive(self, config: Dict[str, Any]):
        """Initialize OneDrive service using Microsoft Graph API."""
        try:
            # This would need OAuth2 flow implementation
            # For now, store the config for manual token setup
            self.services['onedrive'] = {
                'config': config,
                'base_url': 'https://graph.microsoft.com/v1.0'
            }
            print("⚠️  OneDrive configured (manual token setup required)")
            
        except Exception as e:
            print(f"❌ Failed to configure OneDrive: {e}")
    
    async def sync_organization_rules(self, local_rules: Dict[str, Any]) -> Dict[str, Any]:
        """Sync organization rules across all connected cloud services."""
        print("🔄 Syncing organization rules across cloud services...")
        
        # Save rules locally first
        with open(self.sync_rules_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'rules': local_rules,
                'sync_status': {}
            }, f, indent=2)
        
        sync_results = {}
        
        # Sync to each connected service
        for service_name in self.services:
            try:
                if service_name == 'google_drive':
                    sync_results[service_name] = await self._sync_to_google_drive(local_rules)
                elif service_name == 'dropbox':
                    sync_results[service_name] = await self._sync_to_dropbox(local_rules)
                elif service_name == 'onedrive':
                    sync_results[service_name] = await self._sync_to_onedrive(local_rules)
                    
            except Exception as e:
                sync_results[service_name] = {'error': str(e)}
        
        return sync_results
    
    async def _sync_to_google_drive(self, rules: Dict[str, Any]) -> Dict[str, str]:
        """Sync organization rules to Google Drive."""
        try:
            service = self.services['google_drive']
            
            # Create or update the organization rules file in Google Drive
            rules_content = json.dumps(rules, indent=2)
            
            # Search for existing rules file
            results = service.files().list(
                q="name='ai_file_organizer_rules.json' and trashed=false"
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                # Update existing file
                file_id = files[0]['id']
                media = MediaIoBaseUpload(
                    io.BytesIO(rules_content.encode()),
                    mimetype='application/json'
                )
                service.files().update(
                    fileId=file_id,
                    media_body=media
                ).execute()
                return {'status': 'updated', 'file_id': file_id}
            else:
                # Create new file
                file_metadata = {'name': 'ai_file_organizer_rules.json'}
                media = MediaIoBaseUpload(
                    io.BytesIO(rules_content.encode()),
                    mimetype='application/json'
                )
                file = service.files().create(
                    body=file_metadata,
                    media_body=media
                ).execute()
                return {'status': 'created', 'file_id': file['id']}
                
        except Exception as e:
            return {'error': str(e)}
    
    async def _sync_to_dropbox(self, rules: Dict[str, Any]) -> Dict[str, str]:
        """Sync organization rules to Dropbox."""
        try:
            dbx = self.services['dropbox']
            rules_content = json.dumps(rules, indent=2).encode()
            
            # Upload rules file to Dropbox
            dbx.files_upload(
                rules_content,
                '/ai_file_organizer_rules.json',
                mode=dropbox.files.WriteMode('overwrite')
            )
            
            return {'status': 'synced'}
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _sync_to_onedrive(self, rules: Dict[str, Any]) -> Dict[str, str]:
        """Sync organization rules to OneDrive."""
        # This would require implementing the Microsoft Graph API calls
        return {'status': 'not_implemented', 'message': 'OneDrive sync requires manual setup'}
    
    async def organize_cloud_folders(self, service_name: str, folder_path: str) -> Dict[str, Any]:
        """Organize files in a specific cloud service folder."""
        print(f"🌤️  Organizing {service_name} folder: {folder_path}")
        
        if service_name not in self.services:
            return {'error': f'{service_name} not connected'}
        
        try:
            if service_name == 'google_drive':
                return await self._organize_google_drive_folder(folder_path)
            elif service_name == 'dropbox':
                return await self._organize_dropbox_folder(folder_path)
            elif service_name == 'onedrive':
                return await self._organize_onedrive_folder(folder_path)
            else:
                return {'error': f'Unknown service: {service_name}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    async def _organize_google_drive_folder(self, folder_name: str) -> Dict[str, Any]:
        """Organize a Google Drive folder using AI."""
        service = self.services['google_drive']
        
        # Find the folder
        results = service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        ).execute()
        
        folders = results.get('files', [])
        if not folders:
            return {'error': f'Folder "{folder_name}" not found'}
        
        folder_id = folders[0]['id']
        
        # List files in the folder
        files_result = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false"
        ).execute()
        
        files = files_result.get('files', [])
        
        # This would integrate with the AI organizer to create a plan
        # For now, return the file list for manual processing
        return {
            'folder_id': folder_id,
            'files_found': len(files),
            'files': [{'name': f['name'], 'id': f['id'], 'mimeType': f.get('mimeType')} for f in files[:10]]  # First 10 files
        }
    
    async def _organize_dropbox_folder(self, folder_path: str) -> Dict[str, Any]:
        """Organize a Dropbox folder using AI."""
        dbx = self.services['dropbox']
        
        try:
            # List folder contents
            result = dbx.files_list_folder(folder_path)
            
            files = []
            for entry in result.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    files.append({
                        'name': entry.name,
                        'path': entry.path_display,
                        'size': entry.size,
                        'modified': entry.server_modified.isoformat() if entry.server_modified else None
                    })
            
            return {
                'files_found': len(files),
                'files': files[:10]  # First 10 files
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _organize_onedrive_folder(self, folder_name: str) -> Dict[str, Any]:
        """Organize a OneDrive folder using AI."""
        return {'error': 'OneDrive organization not yet implemented'}
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get the current sync status across all cloud services."""
        status = {
            'connected_services': list(self.services.keys()),
            'available_services': [],
            'last_sync': None
        }
        
        if GOOGLE_AVAILABLE:
            status['available_services'].append('google_drive')
        if DROPBOX_AVAILABLE:
            status['available_services'].append('dropbox')
        if ONEDRIVE_AVAILABLE:
            status['available_services'].append('onedrive')
        
        # Check for last sync timestamp
        if self.sync_rules_file.exists():
            try:
                with open(self.sync_rules_file, 'r') as f:
                    sync_data = json.load(f)
                    status['last_sync'] = sync_data.get('timestamp')
            except Exception:
                pass
        
        return status
    
    def setup_cloud_service(self, service_name: str) -> str:
        """Return setup instructions for a cloud service."""
        instructions = {
            'google_drive': """
🔧 Google Drive Setup:
1. Go to https://console.developers.google.com/
2. Create a new project or select existing
3. Enable the Google Drive API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the client configuration
6. Add client_id and client_secret to cloud_credentials.json
7. Set enabled: true for google_drive
            """,
            'dropbox': """
🔧 Dropbox Setup:  
1. Go to https://www.dropbox.com/developers/apps
2. Create a new app
3. Choose "Scoped access" and "Full Dropbox"
4. Generate an access token
5. Add the access_token to cloud_credentials.json
6. Set enabled: true for dropbox
            """,
            'onedrive': """
🔧 OneDrive Setup:
1. Go to https://portal.azure.com/
2. Register a new application in Azure AD
3. Add Microsoft Graph permissions
4. Get client_id, client_secret, and tenant_id
5. Add credentials to cloud_credentials.json
6. Set enabled: true for onedrive
            """
        }
        
        return instructions.get(service_name, f"Setup instructions for {service_name} not available.")

# Example usage and testing
async def main():
    """Test the cloud storage integration."""
    cloud_manager = CloudStorageManager()
    
    print("🌤️  Cloud Storage Integration Status:")
    print("=" * 50)
    
    status = cloud_manager.get_sync_status()
    print(f"📡 Available services: {', '.join(status['available_services'])}")
    print(f"🔗 Connected services: {', '.join(status['connected_services'])}")
    
    if status['last_sync']:
        print(f"🕐 Last sync: {status['last_sync']}")
    else:
        print("🕐 No previous sync found")
    
    if not status['connected_services']:
        print("\n⚙️  To connect cloud services, edit the credentials file and follow setup instructions:")
        print(f"📁 {cloud_manager.credentials_file}")
        
        for service in status['available_services']:
            print(cloud_manager.setup_cloud_service(service))

if __name__ == "__main__":
    asyncio.run(main())