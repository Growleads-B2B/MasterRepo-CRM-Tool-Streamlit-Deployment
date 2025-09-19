"""
BULLETPROOF BATCH EXPORTER - GUARANTEED TO WORK
No complex imports, no broken dependencies - just simple, working batch export
"""

import requests
import pandas as pd
import time
import streamlit as st


class SimpleBatchExporter:
    """Simple, bulletproof batch exporter that actually works"""

    def __init__(self, base_url: str, api_token: str, table_id: str):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.table_id = table_id
        self.headers = {
            'Authorization': f'Token {api_token}',
            'Content-Type': 'application/json',
        }

    def test_connection(self) -> bool:
        """Test if we can connect to Baserow"""
        try:
            response = requests.get(
                f'{self.base_url}/api/database/fields/table/{self.table_id}/',
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def create_single_row(self, row_data: dict) -> tuple:
        """Create ONE row in Baserow - returns (success, error_message)"""
        try:
            response = requests.post(
                f'{self.base_url}/api/database/rows/table/{self.table_id}/?user_field_names=true',
                headers=self.headers,
                json=row_data,
                timeout=30
            )

            if response.status_code in [200, 201]:
                return True, "Success"
            else:
                error_msg = f"HTTP {response.status_code}: {response.text[:100]}"
                return False, error_msg

        except Exception as e:
            return False, f"Exception: {str(e)[:100]}"

    def get_table_fields(self) -> list:
        """Get existing fields in the table"""
        try:
            response = requests.get(
                f'{self.base_url}/api/database/fields/table/{self.table_id}/',
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return [field['name'] for field in response.json()]
            return []
        except:
            return []

    def create_field(self, field_name: str, field_type: str = 'text') -> bool:
        """Create a new field"""
        try:
            response = requests.post(
                f'{self.base_url}/api/database/fields/table/{self.table_id}/',
                headers=self.headers,
                json={'name': field_name, 'type': field_type},
                timeout=30
            )
            return response.status_code in [200, 201]
        except:
            return False

    def export_batch(self, batch_data: pd.DataFrame, batch_number: int) -> dict:
        """
        Export a batch of data to Baserow

        Args:
            batch_data: DataFrame containing the batch rows
            batch_number: Batch number for tracking

        Returns:
            dict: Results with success status and details
        """
        try:
            total_rows = len(batch_data)
            st.write(f"🚀 **Exporting Batch {batch_number}**")
            st.write(f"📊 Processing {total_rows} rows...")

            # Test connection first with detailed info
            st.write(f"🔗 **Testing connection to Baserow...**")
            st.write(f"📍 Base URL: {self.base_url}")
            st.write(f"📋 Table ID: {self.table_id}")
            st.write(f"🔑 API Token: {self.api_token[:10]}...{self.api_token[-4:]}")

            if not self.test_connection():
                st.error("❌ **Connection test failed!**")
                st.write("Possible issues:")
                st.write("• Invalid API token")
                st.write("• Wrong table ID")
                st.write("• Baserow server not accessible")
                return {'success': False, 'error': 'Connection failed', 'uploaded': 0, 'failed': 0}
            else:
                st.success("✅ **Connection test passed!**")

            # Get existing fields
            existing_fields = self.get_table_fields()
            st.write(f"📋 Found {len(existing_fields)} existing fields")

            # Create missing fields
            missing_fields = [col for col in batch_data.columns if col not in existing_fields]
            if missing_fields:
                st.write(f"🔧 Creating {len(missing_fields)} missing fields...")
                for field in missing_fields:
                    if self.create_field(field):
                        st.write(f"✅ Created field: {field}")
                    time.sleep(0.2)

            # Upload rows with detailed error tracking
            uploaded_count = 0
            failed_count = 0
            error_details = []

            progress_bar = st.progress(0)
            status_text = st.empty()

            # Show first few rows for debugging
            st.write(f"🔍 **Debug: First 3 rows to upload:**")
            for i in range(min(3, len(batch_data))):
                row = batch_data.iloc[i]
                st.write(f"Row {i+1}: {dict(row)}")

            for idx, (_, row) in enumerate(batch_data.iterrows()):
                row_num = idx + 1

                # Clean row data
                cleaned_row = {}
                for col in batch_data.columns:
                    value = row[col]
                    if pd.notna(value) and str(value).strip():
                        cleaned_row[col] = str(value).strip()
                    else:
                        cleaned_row[col] = ""

                # Upload row
                if any(val.strip() for val in cleaned_row.values()):  # Only if row has data
                    success, error_msg = self.create_single_row(cleaned_row)
                    if success:
                        uploaded_count += 1
                    else:
                        failed_count += 1
                        if len(error_details) < 5:  # Store first 5 errors
                            error_details.append(f"Row {row_num}: {error_msg}")

                    # Show detailed progress for first 5 rows
                    if row_num <= 5:
                        st.write(f"Row {row_num}: {'✅ Success' if success else f'❌ Failed - {error_msg}'}")

                # Update progress
                progress = row_num / total_rows
                progress_bar.progress(progress)
                status_text.text(f"Processed {row_num}/{total_rows} rows - Uploaded: {uploaded_count}, Failed: {failed_count}")

                time.sleep(0.01)  # Small delay

            # Show error details if any failures
            if error_details:
                st.error(f"❌ **Error Details (first 5 failures):**")
                for error in error_details:
                    st.write(f"• {error}")

            # Final results
            success_rate = (uploaded_count / total_rows) * 100 if total_rows > 0 else 0

            result = {
                'success': uploaded_count > 0,
                'uploaded': uploaded_count,
                'failed': failed_count,
                'total': total_rows,
                'success_rate': success_rate
            }

            if result['success']:
                st.success(f"✅ Batch {batch_number} completed! Uploaded {uploaded_count}/{total_rows} rows ({success_rate:.1f}% success)")
            else:
                st.error(f"❌ Batch {batch_number} failed! No rows uploaded.")

            return result

        except Exception as e:
            st.error(f"💥 Error in batch {batch_number}: {str(e)}")
            return {'success': False, 'error': str(e), 'uploaded': 0, 'failed': 0}


def create_batches_simple(df: pd.DataFrame, batch_size: int = 80) -> list:
    """Create simple batches from DataFrame"""
    batches = []
    total_rows = len(df)

    for start_idx in range(0, total_rows, batch_size):
        end_idx = min(start_idx + batch_size, total_rows)
        batch_data = df.iloc[start_idx:end_idx].copy().reset_index(drop=True)

        batch_info = {
            'number': (start_idx // batch_size) + 1,
            'start_row': start_idx + 1,
            'end_row': end_idx,
            'data': batch_data,
            'status': 'pending'
        }
        batches.append(batch_info)

    return batches