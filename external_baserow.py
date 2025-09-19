"""
External Baserow Manager
Connects to an external Baserow instance for cloud deployment
"""

import streamlit as st
import requests
import json
import os
from pathlib import Path
from baserow_integration import BaserowIntegration
from baserow_integration_FIXED import BaserowIntegration as FixedBaserowIntegration

class ExternalBaserowManager:
    """Manages connection to an external Baserow instance for cloud deployment"""
    
    def __init__(self):
        self.config_file = Path(".baserow_config.json")
        self._ensure_config_exists()
        
        # Load config from file or environment variables
        config = self._load_config()
        self.base_url = os.environ.get("BASEROW_URL", config.get("base_url", "https://api.baserow.io"))
        self.table_id = os.environ.get("BASEROW_TABLE_ID", config.get("table_id", ""))
        self.api_token = os.environ.get("BASEROW_API_TOKEN", config.get("api_token", ""))
        
        self.is_running = False
        self.integration = None
        
    def is_baserow_running(self) -> bool:
        """Check if Baserow is accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/", timeout=3)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def start_baserow(self) -> bool:
        """Check if Baserow is accessible (no need to start in external mode)"""
        if self.is_baserow_running():
            self.is_running = True
            return True
        return False
    
    def _ensure_config_exists(self):
        """Ensure config file exists with default values"""
        if not self.config_file.exists():
            config = {
                "api_token": os.environ.get("BASEROW_API_TOKEN", ""),
                "table_id": os.environ.get("BASEROW_TABLE_ID", ""),
                "base_url": os.environ.get("BASEROW_URL", "https://api.baserow.io")
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
        """Get existing workspace configuration or create new one"""
        # Check environment variables first
        env_token = os.environ.get("BASEROW_API_TOKEN")
        env_table = os.environ.get("BASEROW_TABLE_ID")
        env_url = os.environ.get("BASEROW_URL", "https://api.baserow.io")
        
        if env_token and env_table:
            config = {
                "api_token": env_token,
                "table_id": env_table,
                "base_url": env_url
            }
            # Test if this config works
            test_integration = BaserowIntegration()
            if test_integration.authenticate(config["base_url"], config["api_token"], config["table_id"]):
                # Save to config file
                with open(self.config_file, 'w') as f:
                    json.dump(config, f)
                return config
        
        # Load saved config if it exists
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Test if this config works
                test_integration = BaserowIntegration()
                if test_integration.authenticate(config["base_url"], config["api_token"], config["table_id"]):
                    return config
        
        # Show setup form if no valid config
        st.warning("🔑 Baserow API Setup Required")
        st.info("You need to connect to an external Baserow instance")
        
        base_url = st.text_input(
            "Baserow URL:",
            value=self.base_url,
            help="URL of your Baserow instance (e.g., https://api.baserow.io)"
        )
        
        new_token = st.text_input(
            "API Token:",
            type="password",
            value=self.api_token,
            help="Get this from Baserow Settings → API Tokens"
        )
        
        table_id = st.text_input(
            "Table ID:",
            value=self.table_id,
            help="The ID of the table where data will be exported"
        )
        
        if st.button("💾 Save Configuration", type="primary"):
            if new_token and table_id:
                config = {
                    "api_token": new_token,
                    "table_id": table_id,
                    "base_url": base_url
                }
                
                # Test connection
                integration = BaserowIntegration()
                if integration.authenticate(base_url, new_token, table_id):
                    # Save config
                    with open(self.config_file, 'w') as f:
                        json.dump(config, f)
                    st.success("✅ Configuration saved successfully!")
                    st.rerun()
                else:
                    st.error("❌ Invalid configuration. Please check your API token and table ID.")
        
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
            # Get configuration
            config = self.get_or_create_workspace()
            if not config:
                st.error("Baserow configuration is missing. Please set up your Baserow connection first.")
                return False
            
            # Initialize the FIXED integration
            fixed_integration = FixedBaserowIntegration()

            # Authenticate with the FIXED system
            if not fixed_integration.authenticate(config["base_url"], config["api_token"], str(config["table_id"])):
                st.error("❌ Baserow authentication failed")
                return False

            # Clear existing data if requested
            if clear_existing:
                fixed_integration.clear_table()

            # Upload ALL rows with the FIXED method
            success = fixed_integration.upload_dataframe(df, batch_size=20, auto_create_fields=True, speed_mode=speed_mode)

            # Verify upload completion
            if success:
                verification = fixed_integration.verify_upload_completion(len(df))
                if verification['success']:
                    st.success(f"✅ All {len(df):,} rows uploaded successfully!")
                    return True
                else:
                    st.warning(f"⚠️ Upload warning: {verification.get('message', 'Verification issue')}")
                    return success
            else:
                st.error("❌ Data upload failed")
                return False
                
        except Exception as e:
            st.error(f"Export error: {str(e)}")
            return False
