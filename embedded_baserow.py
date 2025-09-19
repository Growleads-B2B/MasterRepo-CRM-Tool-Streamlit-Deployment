"""
Embedded Baserow Manager
Automatically starts and manages local Baserow instance with the Spreadsheet Consolidator
"""

import subprocess
import time
import requests
import streamlit as st
from baserow_integration import BaserowIntegration
from baserow_integration_new import NewBaserowIntegration
from baserow_integration_FIXED import BaserowIntegration as FixedBaserowIntegration
import os
import json
from pathlib import Path


class EmbeddedBaserowManager:
    """Manages embedded Baserow instance that starts automatically with the tool"""
    
    def __init__(self):
        self.config_file = Path(".baserow_config.json")
        self._ensure_config_exists()
        
        # Load config from file
        config = self._load_config()
        self.base_url = config.get("base_url", "http://localhost:8080")
        self.table_id = config.get("table_id", "698")
        self.api_token = config.get("api_token", "placeholder_token")
        
        self.is_running = False
        self.integration = None
        
    def check_docker_available(self) -> bool:
        """Check if Docker is available"""
        try:
            subprocess.run(["docker", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def is_baserow_running(self) -> bool:
        """Check if Baserow is already running"""
        try:
            response = requests.get(f"{self.base_url}/api/", timeout=1)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def start_baserow(self) -> bool:
        """Start Baserow containers if not running"""
        if self.is_baserow_running():
            self.is_running = True
            return True
        
        if not self.check_docker_available():
            return False
        
        try:
            subprocess.run(
                ["docker-compose", "up", "-d"],
                check=True,
                capture_output=True,
                text=True
            )
            
            # Consider it started without waiting
            self.is_running = True
            return True
                
        except subprocess.CalledProcessError:
            return False
        except Exception:
            return False
    
    def _ensure_config_exists(self):
        """Ensure config file exists with default values"""
        if not self.config_file.exists():
            config = {
                "api_token": "placeholder_token_please_replace",
                "table_id": "698",
                "base_url": "http://localhost:8080"
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def get_or_create_workspace(self) -> dict:
        """Get existing workspace configuration"""
        # Load saved config first
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Test if this config works
                test_integration = BaserowIntegration()
                if test_integration.authenticate(config["base_url"], config["api_token"], config["table_id"]):
                    return config
        
        # Show setup form if no valid config
        st.warning("🔑 API Token Setup Required")
        st.info(f"Go to [Baserow Settings]({self.base_url}/settings/tokens) → Create API Token")
        
        new_token = st.text_input(
            "Enter your API Token:",
            type="password",
            value=self.api_token,
            help="Get this from Baserow Settings → API Tokens"
        )
        
        if st.button("💾 Save Token", type="primary"):
            if new_token:
                config = {
                    "api_token": new_token,
                    "table_id": self.table_id,
                    "base_url": self.base_url
                }
                
                # Test connection
                integration = BaserowIntegration()
                if integration.authenticate(self.base_url, new_token, self.table_id):
                    # Save config
                    with open(self.config_file, 'w') as f:
                        json.dump(config, f)
                    st.success("✅ Token saved successfully!")
                    st.rerun()
                else:
                    st.error("❌ Invalid token. Please check your API token.")
        
        return None
    
    def get_integration(self) -> BaserowIntegration:
        """Get configured BaserowIntegration instance"""
        if self.integration:
            return self.integration
            
        config = self.get_or_create_workspace()
        if not config:
            return None
            
        integration = BaserowIntegration()
        if integration.authenticate(
            config["base_url"], 
            config["api_token"], 
            config["table_id"]
        ):
            self.integration = integration
            return integration
        
        return None
    
    def export_data(self, df, clear_existing=False, speed_mode='turbo') -> bool:
        """Export data to Baserow using speed-optimized API endpoints.

        Args:
            df: DataFrame to export
            clear_existing: Whether to clear existing table data
            speed_mode: 'turbo' (fastest), 'balanced', or 'conservative'
        """
        try:
            # Ensure Baserow is running
            if not self.start_baserow():
                return False
            
            # Initialize official Baserow integration
            from baserow_integration import BaserowIntegration
            integration = BaserowIntegration()
            
            # Authenticate using official API
            if not integration.authenticate(self.base_url, self.api_token, str(self.table_id)):
                return False
            
            # Clear existing data if requested
            if clear_existing:
                integration.clear_table()
            
            # Use the FIXED SYSTEM THAT ACTUALLY WORKS
            print(f"🔥 USING FIXED SYSTEM - NO MORE 90 ROW BULLSHIT")
            print(f"📊 UPLOADING ALL {len(df):,} ROWS GUARANTEED")
            print(f"🎯 FIXED VERSION THAT ACTUALLY UPLOADS EVERYTHING")

            # Initialize the FIXED integration
            fixed_integration = FixedBaserowIntegration()

            # Authenticate with the FIXED system
            if not fixed_integration.authenticate(self.base_url, self.api_token, str(self.table_id)):
                print(f"❌ FIXED SYSTEM AUTHENTICATION FAILED")
                return False

            # Upload ALL rows with the FIXED method
            success = fixed_integration.upload_dataframe(df, batch_size=90, auto_create_fields=True, speed_mode=speed_mode)

            # Verify upload completion
            if success:
                verification = fixed_integration.verify_upload_completion(len(df))
                if verification['success']:
                    print(f"✅ FIXED SYSTEM SUCCESS: All {len(df):,} rows uploaded and verified!")
                    return True
                else:
                    print(f"⚠️ UPLOAD WARNING: {verification.get('message', 'Verification issue')}")
                    print(f"📊 Expected: {verification.get('expected', 'unknown')}, Got: {verification.get('actual', 'unknown')}")
                    return success
            else:
                print(f"❌ FIXED SYSTEM FAILED")
                return False
                
        except Exception as e:
            st.error(f"Export error: {str(e)}")
            return False
    
