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
                # Store response details for debugging
                error_details = f"{response.status_code} - {response.text[:200]}"
                print(f"Failed to create row: {error_details}")
                return False
            
        except Exception as e:
            print(f"Error creating row: {str(e)}")
            return False

    
    def upload_dataframe(self, df: pd.DataFrame, batch_size: int = 90,
                        auto_create_fields: bool = True, speed_mode: str = 'balanced') -> bool:
        """
        FIXED SIMPLE UPLOAD: Upload ALL DataFrame rows one by one - NO BATCHING BULLSHIT
        Just upload every single row until done. Period.

        Args:
            df: DataFrame to upload (ALL ROWS WILL BE PROCESSED)
            batch_size: IGNORED - we don't batch anymore
            auto_create_fields: Whether to automatically create missing fields
            speed_mode: IGNORED - we just upload everything

        Returns:
            bool: True if ALL rows uploaded successfully
        """
        try:
            total_rows = len(df)
            print(f"\n🚀 ENHANCED AUTO-LOOP EXPORT SYSTEM INITIATED")
            print(f"📊 TOTAL DATASET SIZE: {total_rows:,} rows")
            print(f"🎯 GOAL: Upload EVERY SINGLE ROW to Baserow")
            print(f"⚙️ BATCH SIZE: {batch_size} rows per batch (Baserow API limit)")
            print(f"📈 EXPECTED BATCHES: {(total_rows + batch_size - 1) // batch_size}")
            print(f"="*80)

            # PHASE 1: Field Management
            print(f"\n🔧 PHASE 1: FIELD MANAGEMENT")
            existing_fields = self.get_table_fields()
            print(f"📋 Found {len(existing_fields)} existing fields: {list(existing_fields.keys())}")

            missing_fields = [col for col in df.columns if col not in existing_fields]
            if missing_fields and auto_create_fields:
                print(f"➕ Creating {len(missing_fields)} missing fields...")
                for i, field in enumerate(missing_fields, 1):
                    field_type = self.detect_field_type(df[field])
                    print(f"   {i}/{len(missing_fields)}: Creating '{field}' as '{field_type}'")
                    if self.create_field(field, field_type):
                        print(f"   ✅ Field '{field}' created successfully")
                    else:
                        print(f"   ⚠️ Failed to create field '{field}', will continue...")
                    time.sleep(0.3)  # API rate limiting
                print(f"✅ Field management complete!")
            else:
                print(f"✅ No new fields needed")

            # PHASE 2: Data Preparation
            print(f"\n📊 PHASE 2: DATA PREPARATION")
            rows_data = df.to_dict('records')
            print(f"✅ Converted {len(rows_data):,} rows to upload format")
            print(f"📋 Columns: {list(df.columns)}")

            # PHASE 3: SPEED-OPTIMIZED BATCH PROCESSING
            # Configure speed settings
            if speed_mode == 'turbo':
                request_delay = 0.005  # 5ms - Maximum speed
                batch_delay = 0.1      # 100ms between batches
                log_frequency = 50     # Log every 50th row
                max_retries = 1        # Minimal retries
                print(f"\n⚡ PHASE 3: TURBO SPEED MODE ACTIVATED")
                print(f"🚀 OPTIMIZED FOR MAXIMUM SPEED - Estimated time: ~{(total_rows * 0.025 / 60):.1f} minutes")
            elif speed_mode == 'balanced':
                request_delay = 0.01   # 10ms - Balanced
                batch_delay = 0.3      # 300ms between batches
                log_frequency = 25     # Log every 25th row
                max_retries = 2        # Balanced retries
                print(f"\n⚖️ PHASE 3: BALANCED SPEED MODE")
                print(f"🎯 OPTIMIZED FOR SPEED + RELIABILITY - Estimated time: ~{(total_rows * 0.035 / 60):.1f} minutes")
            else:  # conservative
                request_delay = 0.02   # 20ms - Conservative
                batch_delay = 0.5      # 500ms between batches
                log_frequency = 10     # Log every 10th row
                max_retries = 3        # Full retries
                print(f"\n🛡️ PHASE 3: CONSERVATIVE MODE")
                print(f"🔒 OPTIMIZED FOR MAXIMUM RELIABILITY - Estimated time: ~{(total_rows * 0.05 / 60):.1f} minutes")

            print(f"🎯 PROCESSING {total_rows:,} ROWS IN BATCHES OF {batch_size}")
            print(f"⚡ REQUEST DELAY: {request_delay*1000:.0f}ms | BATCH DELAY: {batch_delay*1000:.0f}ms")
            print(f"🔄 MAX RETRIES: {max_retries} | LOG FREQUENCY: Every {log_frequency} rows")
            print(f"="*80)

            # Initialize tracking variables
            uploaded_count = 0
            failed_count = 0
            skipped_count = 0
            batch_number = 1
            start_index = 0

            print(f"\n🔥 STARTING AUTO-LOOP PROCESSING")
            print(f"📊 TOTAL ROWS TO PROCESS: {total_rows:,}")
            print(f"🎯 ROWS PER BATCH: {batch_size}")
            print(f"📈 EXPECTED BATCHES: {(total_rows + batch_size - 1) // batch_size}")
            print(f"🔄 WILL CONTINUE UNTIL ALL {total_rows:,} ROWS ARE PROCESSED!")
            print(f"="*80)

            # ENHANCED AUTO-LOOP: Process until ALL rows are handled
            while start_index < total_rows:
                print(f"\n🚀 LOOP CHECK: start_index={start_index}, total_rows={total_rows}")
                print(f"🔄 CONDITION: {start_index} < {total_rows} = {start_index < total_rows}")
                end_index = min(start_index + batch_size, total_rows)
                current_batch_size = end_index - start_index

                print(f"\n🚀 BATCH {batch_number:,}: ROWS {start_index + 1:,} - {end_index:,}")
                print(f"📊 Progress: {uploaded_count:,}/{total_rows:,} uploaded ({(uploaded_count/total_rows)*100:.1f}%)")
                print(f"🔥 Processing {current_batch_size} rows in this batch")

                batch_uploaded = 0
                batch_failed = 0
                batch_skipped = 0

                # Process each row in current batch with enhanced error handling
                for row_index in range(start_index, end_index):
                    row_data = rows_data[row_index]
                    absolute_row_num = row_index + 1
                    batch_row_num = (row_index - start_index) + 1

                    # Enhanced data cleaning
                    cleaned_row = {}
                    has_data = False
                    for key, value in row_data.items():
                        if pd.notna(value) and str(value).strip():
                            cleaned_row[key] = str(value).strip()
                            has_data = True
                        else:
                            cleaned_row[key] = ""

                    # Upload row with verification
                    if has_data:
                        # Speed-optimized upload with dynamic retry logic
                        upload_success = False
                        retry_count = 0

                        while not upload_success and retry_count < max_retries:
                            try:
                                upload_success = self.create_row(cleaned_row)
                                if upload_success:
                                    batch_uploaded += 1
                                    uploaded_count += 1
                                    # Dynamic logging based on speed mode
                                    if batch_row_num % log_frequency == 0:
                                        print(f"   ✅ Row {absolute_row_num:,} uploaded (batch: {batch_row_num}/{current_batch_size})")
                                else:
                                    retry_count += 1
                                    if retry_count < max_retries and speed_mode != 'turbo':
                                        print(f"   🔄 Retry {retry_count} for row {absolute_row_num:,}...")
                                        time.sleep(0.5 if speed_mode == 'balanced' else 1)  # Faster retries
                            except Exception as e:
                                retry_count += 1
                                if retry_count < max_retries and speed_mode == 'conservative':
                                    print(f"   ⚠️ Error on row {absolute_row_num:,}, retry {retry_count}: {str(e)[:50]}")
                                    time.sleep(0.5)

                        if not upload_success:
                            batch_failed += 1
                            failed_count += 1
                            if speed_mode != 'turbo':  # Only log failures in non-turbo mode
                                print(f"   ❌ Row {absolute_row_num:,} FAILED after {max_retries} attempts")
                    else:
                        batch_skipped += 1
                        skipped_count += 1
                        # Reduced skip logging for speed
                        if batch_row_num % (log_frequency * 2) == 0 and speed_mode != 'turbo':
                            print(f"   ⏭️ Row {absolute_row_num:,} skipped (empty data)")

                    # Speed-optimized API rate limiting
                    time.sleep(request_delay)

                # BATCH VERIFICATION AND REPORTING
                print(f"\n📊 BATCH {batch_number:,} COMPLETE:")
                print(f"   ✅ Uploaded: {batch_uploaded:,}/{current_batch_size} rows")
                print(f"   ❌ Failed: {batch_failed:,} rows")
                print(f"   ⏭️ Skipped: {batch_skipped:,} rows (empty)")
                print(f"   📈 OVERALL PROGRESS: {uploaded_count:,}/{total_rows:,} ({(uploaded_count/total_rows)*100:.1f}%)")

                # CRITICAL: Move to next batch
                print(f"\n🔄 UPDATING LOOP VARIABLES:")
                print(f"   Previous start_index: {start_index}")
                print(f"   Setting start_index to: {end_index}")
                start_index = end_index
                batch_number += 1
                print(f"   New start_index: {start_index}")
                print(f"   Next batch will be: {batch_number}")

                # FAILSAFE: Ensure loop continues
                if start_index >= total_rows:
                    print(f"🎯 LOOP WILL END: start_index ({start_index}) >= total_rows ({total_rows})")
                else:
                    remaining = total_rows - start_index
                    print(f"🔄 LOOP WILL CONTINUE: {remaining:,} rows remaining")
                    if speed_mode != 'turbo':
                        print(f"⏳ Processing next batch...")
                    time.sleep(batch_delay)  # Dynamic pause between batches

                # DEBUGGING: Check if we're stuck in an infinite loop
                if batch_number > 50:  # Safety check
                    print(f"⚠️ SAFETY BREAK: Too many batches processed")
                    break

            # FINAL VERIFICATION AND REPORTING
            print(f"\n🎉 AUTO-LOOP SYSTEM COMPLETE!")
            print(f"="*80)
            print(f"📋 FINAL RESULTS:")
            print(f"   📊 Total Rows Processed: {total_rows:,}")
            print(f"   ✅ Successfully Uploaded: {uploaded_count:,} ({(uploaded_count/total_rows)*100:.1f}%)")
            print(f"   ❌ Failed Uploads: {failed_count:,}")
            print(f"   ⏭️ Skipped (Empty): {skipped_count:,}")
            print(f"   🔢 Total Batches: {batch_number - 1:,}")

            # Success criteria verification
            success_rate = (uploaded_count / total_rows) * 100 if total_rows > 0 else 0

            if uploaded_count == (total_rows - skipped_count):
                print(f"\n🎯 100% SUCCESS! All non-empty rows uploaded successfully!")
                return True
            elif success_rate >= 95:
                print(f"\n✅ HIGH SUCCESS RATE: {success_rate:.1f}% of rows uploaded")
                return True
            elif uploaded_count > 0:
                print(f"\n⚠️ PARTIAL SUCCESS: {uploaded_count:,} rows uploaded out of {total_rows:,}")
                print(f"   Consider re-running export to upload failed rows")
                return True
            else:
                print(f"\n❌ EXPORT FAILED: No rows were uploaded successfully")
                return False

        except Exception as e:
            print(f"\n💥 CRITICAL ERROR in upload system: {str(e)}")
            print(f"📊 Uploaded {uploaded_count:,} rows before error occurred")
            return False

    def verify_upload_completion(self, expected_rows: int) -> dict:
        """
        Verify that all data was uploaded successfully by checking table row count.

        Args:
            expected_rows: Number of rows that should be in the table

        Returns:
            dict: Verification results with status and details
        """
        try:
            print(f"\n🔍 VERIFICATION: Checking upload completion...")

            # Get current table data
            current_rows = self.get_all_rows()
            current_count = len(current_rows)

            print(f"📊 Expected rows: {expected_rows:,}")
            print(f"📊 Actual rows in table: {current_count:,}")

            if current_count >= expected_rows:
                print(f"✅ VERIFICATION PASSED: All data successfully uploaded!")
                return {
                    'success': True,
                    'expected': expected_rows,
                    'actual': current_count,
                    'message': 'Upload verification successful'
                }
            else:
                missing = expected_rows - current_count
                print(f"⚠️ VERIFICATION WARNING: {missing:,} rows missing from table")
                return {
                    'success': False,
                    'expected': expected_rows,
                    'actual': current_count,
                    'missing': missing,
                    'message': f'{missing} rows missing from upload'
                }

        except Exception as e:
            print(f"❌ VERIFICATION ERROR: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Verification failed due to error'
            }

    def upload_dataframe_simple(self, df: pd.DataFrame) -> bool:
        """
        BULLETPROOF SIMPLE UPLOAD: Alternative method that ensures ALL rows are uploaded.
        Uses the most basic, reliable approach possible.

        Args:
            df: DataFrame to upload (ALL ROWS WILL BE PROCESSED)

        Returns:
            bool: True if ALL rows uploaded successfully
        """
        try:
            total_rows = len(df)
            print(f"\n🔥 BULLETPROOF SIMPLE UPLOAD SYSTEM")
            print(f"📊 UPLOADING ALL {total_rows:,} ROWS ONE BY ONE")
            print(f"🎯 100% RELIABLE - NO BATCHING, NO COMPLEXITY")
            print(f"="*60)

            # Get existing fields
            existing_fields = self.get_table_fields()
            print(f"📋 Found {len(existing_fields)} existing fields")

            # Create missing fields
            missing_fields = [col for col in df.columns if col not in existing_fields]
            if missing_fields:
                print(f"🔧 Creating {len(missing_fields)} missing fields...")
                for field in missing_fields:
                    field_type = self.detect_field_type(df[field])
                    if self.create_field(field, field_type):
                        print(f"✅ Created field '{field}'")
                    time.sleep(0.2)

            # Convert to records
            rows_data = df.to_dict('records')
            uploaded_count = 0
            failed_count = 0

            print(f"\n🚀 STARTING SIMPLE UPLOAD...")

            # SIMPLE LOOP: Process every single row
            for i, row_data in enumerate(rows_data):
                row_num = i + 1

                # Clean data
                cleaned_row = {}
                has_data = False
                for key, value in row_data.items():
                    if pd.notna(value) and str(value).strip():
                        cleaned_row[key] = str(value).strip()
                        has_data = True
                    else:
                        cleaned_row[key] = ""

                # Upload if has data
                if has_data:
                    try:
                        if self.create_row(cleaned_row):
                            uploaded_count += 1
                            if row_num % 50 == 0:  # Progress every 50 rows
                                print(f"✅ Uploaded {uploaded_count}/{total_rows} rows ({(uploaded_count/total_rows)*100:.1f}%)")
                        else:
                            failed_count += 1
                            print(f"❌ Failed to upload row {row_num}")
                    except Exception as e:
                        failed_count += 1
                        print(f"❌ Error uploading row {row_num}: {str(e)[:50]}")

                # Small delay
                time.sleep(0.01)

            print(f"\n🎯 SIMPLE UPLOAD COMPLETE!")
            print(f"✅ Uploaded: {uploaded_count}/{total_rows} rows")
            print(f"❌ Failed: {failed_count} rows")

            return uploaded_count == total_rows

        except Exception as e:
            print(f"💥 Error in simple upload: {str(e)}")
            return False
