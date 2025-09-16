"""Baserow Integration Module - Built from Official Documentation
Implements correct Baserow REST API endpoints for field and row management.
"""

import requests
import pandas as pd
from typing import Dict, List, Optional, Any
import json
import time
from datetime import datetime


class BaserowIntegration:
    """Official Baserow REST API integration following baserow.io documentation."""
    
    def __init__(self):
        self.base_url = None
        self.api_token = None
        self.table_id = None
        self.headers = {}
        self.connected = False
        
    def authenticate(self, base_url: str, api_token: str, table_id: str) -> bool:
        """
        Authenticate with Baserow using official API format.
        
        Args:
            base_url: Baserow instance URL (e.g., http://localhost:8080)
            api_token: Database token from Baserow settings
            table_id: ID of the target table
        
        Returns:
            bool: Success status
        """
        try:
            self.base_url = base_url.rstrip('/')
            self.api_token = api_token
            self.table_id = table_id
            
            # Official Baserow authentication: Token format (working with new token)
            self.headers = {
                'Authorization': f'Token {api_token}',
                'Content-Type': 'application/json',
            }
            
            # Test connection by listing fields (official endpoint)
            response = requests.get(
                f'{self.base_url}/api/database/fields/table/{table_id}/',
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.connected = True
                print(f"✅ Connected to Baserow table {table_id}")
                return True
            else:
                print(f"Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False
    
    def is_connected(self) -> bool:
        """Check if connected to Baserow."""
        return self.connected
    
    def get_connection_info(self) -> Dict[str, str]:
        """Get current connection information."""
        return {
            'base_url': self.base_url or 'Not connected',
            'table_id': self.table_id or 'Not set',
            'status': 'Connected' if self.connected else 'Disconnected'
        }
    
    def get_table_fields(self) -> Dict[str, str]:
        """
        Get all fields in the table using official Baserow API endpoint.
        
        Returns:
            Dict mapping field names to field types
        """
        try:
            # Official endpoint: GET /api/database/fields/table/{table_id}/
            response = requests.get(
                f'{self.base_url}/api/database/fields/table/{self.table_id}/',
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                fields_data = response.json()
                fields = {}
                
                # Extract field names and types from response
                for field in fields_data:
                    fields[field['name']] = field['type']
                
                return fields
            else:
                print(f"Failed to get fields: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"Error getting fields: {str(e)}")
            return {}
    
    def detect_field_type(self, series: pd.Series) -> str:
        """
        Detect appropriate Baserow field type based on pandas series.
        
        Args:
            series: Pandas series to analyze
        
        Returns:
            Baserow field type string
        """
        # Remove null values for type detection
        clean_series = series.dropna()
        
        if len(clean_series) == 0:
            return 'text'
        
        # Check if all values are numeric
        if pd.api.types.is_numeric_dtype(clean_series):
            # Check if it's integer or float
            if clean_series.dtype in ['int64', 'int32', 'Int64', 'Int32']:
                return 'number'
            else:
                return 'number'
        
        # Check if it's boolean-like
        unique_vals = clean_series.astype(str).str.lower().unique()
        if set(unique_vals).issubset({'true', 'false', '1', '0', 'yes', 'no'}):
            return 'boolean'
        
        # Check if it's date-like
        sample_values = clean_series.astype(str).head(10)
        date_count = 0
        for val in sample_values:
            try:
                pd.to_datetime(val)
                date_count += 1
            except:
                continue
        
        if date_count > len(sample_values) * 0.7:  # 70% look like dates
            return 'date'
        
        # Default to text
        return 'text'
    
    def create_field(self, field_name: str, field_type: str) -> bool:
        """
        Create a new field in the table using official Baserow API.
        
        Args:
            field_name: Name of the field to create
            field_type: Type of the field (text, number, boolean, date)
        
        Returns:
            bool: Success status
        """
        try:
            field_data = {
                'name': field_name,
                'type': field_type
            }
            
            # Official endpoint: POST /api/database/fields/table/{table_id}/
            response = requests.post(
                f'{self.base_url}/api/database/fields/table/{self.table_id}/',
                headers=self.headers,
                json=field_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return True
            else:
                print(f"Failed to create field '{field_name}': {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error creating field '{field_name}': {str(e)}")
            return False
    
    def get_all_rows(self) -> List[Dict]:
        """
        Get all rows from the table.
        
        Returns:
            List of row dictionaries
        """
        try:
            all_rows = []
            page = 1
            
            while True:
                response = requests.get(
                    f'{self.base_url}/api/database/rows/table/{self.table_id}/',
                    headers=self.headers,
                    params={'page': page, 'size': 200},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    rows = data.get('results', [])
                    
                    if not rows:
                        break
                    
                    all_rows.extend(rows)
                    
                    # Check if there are more pages
                    if not data.get('next'):
                        break
                    
                    page += 1
                else:
                    print(f"Failed to get rows: {response.status_code}")
                    break
            
            return all_rows
            
        except Exception as e:
            print(f"Error getting rows: {str(e)}")
            return []
    
    def delete_row(self, row_id: int) -> bool:
        """
        Delete a row from the table using official Baserow API.
        
        Args:
            row_id: ID of the row to delete
        
        Returns:
            bool: Success status
        """
        try:
            # Official endpoint: DELETE /api/database/rows/table/{table_id}/{row_id}/
            response = requests.delete(
                f'{self.base_url}/api/database/rows/table/{self.table_id}/{row_id}/',
                headers=self.headers,
                timeout=30
            )
            
            return response.status_code in [200, 204]
            
        except Exception as e:
            print(f"Error deleting row {row_id}: {str(e)}")
            return False
    
    def clear_table(self) -> bool:
        """
        Clear all data from the table.
        
        Returns:
            bool: Success status
        """
        try:
            print("Getting all rows to delete...")
            rows = self.get_all_rows()
            
            if not rows:
                print("No rows to delete.")
                return True
            
            print(f"Deleting {len(rows)} rows...")
            
            # Delete in batches
            batch_size = 10
            deleted_count = 0
            
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                
                for row in batch:
                    if self.delete_row(row['id']):
                        deleted_count += 1
                    
                # Small delay between batches
                time.sleep(0.1)
                
                print(f"Deleted {deleted_count}/{len(rows)} rows...")
            
            print(f"Successfully deleted {deleted_count} rows.")
            return deleted_count == len(rows)
            
        except Exception as e:
            print(f"Error clearing table: {str(e)}")
            return False
    
    def create_row(self, row_data: Dict[str, Any]) -> bool:
        """
        Create a single row in the table using official Baserow API.
        
        Args:
            row_data: Dictionary of field names and values
        
        Returns:
            bool: Success status
        """
        try:
            # Official endpoint: POST /api/database/rows/table/{table_id}/
            response = requests.post(
                f'{self.base_url}/api/database/rows/table/{self.table_id}/?user_field_names=true',
                headers=self.headers,
                json=row_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return True
            else:
                print(f"Failed to create row: {response.status_code} - {response.text[:100]}")
                return False
            
        except Exception as e:
            print(f"Error creating row: {str(e)}")
            return False
    
    def upload_dataframe(self, df: pd.DataFrame, batch_size: int = 10, 
                        auto_create_fields: bool = True) -> bool:
        """
        Upload a pandas DataFrame to Baserow using official API.
        
        Args:
            df: DataFrame to upload
            batch_size: Number of rows to upload per batch
            auto_create_fields: Whether to automatically create missing fields
        
        Returns:
            bool: Success status
        """
        try:
            print(f"📊 Starting upload of {len(df)} rows to Baserow...")
            
            # Get existing fields using official API
            existing_fields = self.get_table_fields()
            print(f"📋 Existing fields: {list(existing_fields.keys())}")
            
            # Find missing fields that need to be created
            missing_fields = [col for col in df.columns if col not in existing_fields]
            
            if missing_fields and auto_create_fields:
                print(f"🔧 Creating {len(missing_fields)} missing fields...")
                for field in missing_fields:
                    field_type = self.detect_field_type(df[field])
                    print(f"  ➕ Creating field '{field}' as type '{field_type}'")
                    if self.create_field(field, field_type):
                        print(f"  ✅ Field '{field}' created successfully")
                    else:
                        print(f"  ⚠️ Failed to create field '{field}', continuing...")
                    time.sleep(0.2)  # Small delay between field creations
            
            # Convert DataFrame to list of dictionaries for row creation
            rows_data = df.to_dict('records')
            print(f"🚀 Uploading {len(rows_data)} rows in batches of {batch_size}...")
            
            uploaded_count = 0
            failed_count = 0
            
            # Upload rows in batches using official API
            for i in range(0, len(rows_data), batch_size):
                batch = rows_data[i:i + batch_size]
                batch_start = i + 1
                batch_end = min(i + batch_size, len(rows_data))
                
                print(f"📤 Processing batch {batch_start}-{batch_end}...")
                
                for row_data in batch:
                    # Clean row data - remove NaN values and convert to strings
                    cleaned_row = {}
                    for key, value in row_data.items():
                        if pd.notna(value) and str(value).strip():
                            cleaned_row[key] = str(value).strip()
                    
                    # Only upload rows that have data
                    if cleaned_row:
                        if self.create_row(cleaned_row):
                            uploaded_count += 1
                        else:
                            failed_count += 1
                            if failed_count <= 3:  # Log first few failures
                                print(f"⚠️ Failed to upload row: {list(cleaned_row.keys())}")
                
                # Progress update
                print(f"✅ Batch complete: {uploaded_count} uploaded, {failed_count} failed")
                
                # Small delay between batches to avoid rate limiting
                if i + batch_size < len(rows_data):
                    time.sleep(0.1)
            
            # Final results
            success_rate = (uploaded_count / len(rows_data)) * 100 if rows_data else 0
            print(f"\n🎯 Upload Complete!")
            print(f"   ✅ Successfully uploaded: {uploaded_count}/{len(rows_data)} rows ({success_rate:.1f}%)")
            print(f"   ❌ Failed uploads: {failed_count}")
            
            return uploaded_count > 0  # Success if at least some rows uploaded
            
        except Exception as e:
            print(f"💥 Error uploading dataframe: {str(e)}")
            return False
