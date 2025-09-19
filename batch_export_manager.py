"""
Manual Batch Export Manager
Creates batches of 80 rows each for manual export control
User can export each batch individually with progress tracking
"""

import pandas as pd
import streamlit as st
from typing import Dict, List, Tuple
import time
from baserow_integration_FIXED import BaserowIntegration as FixedBaserowIntegration


class BatchExportManager:
    """Manages manual batch export with 80 rows per batch"""

    def __init__(self):
        self.batch_size = 80
        self.batches = []
        self.batch_status = {}  # Track completed batches

    def create_batches(self, df: pd.DataFrame) -> List[Dict]:
        """
        Create batches of 80 rows each from the dataframe

        Args:
            df: DataFrame to split into batches (exactly from master sheet preview)

        Returns:
            List of batch dictionaries with metadata
        """
        total_rows = len(df)
        self.batches = []
        self.batch_status = {}

        print(f"📊 Creating batches from {total_rows:,} rows")
        print(f"📦 Batch size: {self.batch_size} rows per batch")

        # Create batches of exactly 80 rows each
        for batch_num in range(0, total_rows, self.batch_size):
            start_idx = batch_num
            end_idx = min(batch_num + self.batch_size, total_rows)

            # Get this batch's data (exactly as shown in preview)
            batch_data = df.iloc[start_idx:end_idx].copy().reset_index(drop=True)
            actual_batch_size = len(batch_data)

            batch_info = {
                'batch_number': (batch_num // self.batch_size) + 1,
                'start_row': start_idx + 1,  # Human readable (1-based)
                'end_row': end_idx,
                'total_rows': actual_batch_size,
                'data': batch_data,
                'status': 'pending'  # pending, exporting, completed, failed
            }

            self.batches.append(batch_info)
            self.batch_status[batch_info['batch_number']] = 'pending'

        total_batches = len(self.batches)
        print(f"✅ Created {total_batches} batches")
        print(f"📈 Batch breakdown:")
        for batch in self.batches:
            print(f"   Batch {batch['batch_number']}: Rows {batch['start_row']}-{batch['end_row']} ({batch['total_rows']} rows)")

        return self.batches

    def get_batch_summary(self) -> Dict:
        """Get summary of all batches and their status"""
        if not self.batches:
            return {}

        total_batches = len(self.batches)
        completed_batches = sum(1 for status in self.batch_status.values() if status == 'completed')
        pending_batches = sum(1 for status in self.batch_status.values() if status == 'pending')
        failed_batches = sum(1 for status in self.batch_status.values() if status == 'failed')

        total_rows = sum(batch['total_rows'] for batch in self.batches)
        completed_rows = sum(batch['total_rows'] for batch in self.batches
                           if self.batch_status[batch['batch_number']] == 'completed')

        return {
            'total_batches': total_batches,
            'completed_batches': completed_batches,
            'pending_batches': pending_batches,
            'failed_batches': failed_batches,
            'total_rows': total_rows,
            'completed_rows': completed_rows,
            'completion_percentage': (completed_rows / total_rows * 100) if total_rows > 0 else 0
        }

    def export_single_batch(self, batch_number: int, base_url: str, api_token: str, table_id: str) -> bool:
        """
        Export a single batch to Baserow - UPLOADS ALL ROWS IN THE BATCH

        Args:
            batch_number: The batch number to export (1-based)
            base_url: Baserow base URL
            api_token: Baserow API token
            table_id: Baserow table ID

        Returns:
            bool: Success status
        """
        try:
            # Find the batch
            batch = None
            for b in self.batches:
                if b['batch_number'] == batch_number:
                    batch = b
                    break

            if not batch:
                print(f"❌ Batch {batch_number} not found")
                return False

            # Update status to exporting
            self.batch_status[batch_number] = 'exporting'

            print(f"\n🚀 EXPORTING BATCH {batch_number}")
            print(f"📊 Rows {batch['start_row']}-{batch['end_row']} ({batch['total_rows']} rows)")
            print(f"🎯 UPLOADING ALL {batch['total_rows']} ROWS IN THIS BATCH")
            print(f"="*50)

            # Initialize Baserow integration
            integration = FixedBaserowIntegration()

            if not integration.authenticate(base_url, api_token, table_id):
                print(f"❌ Authentication failed for batch {batch_number}")
                self.batch_status[batch_number] = 'failed'
                return False

            # Get this batch's data
            batch_data = batch['data']
            print(f"📦 Batch data shape: {batch_data.shape}")
            print(f"📋 Columns: {list(batch_data.columns)}")
            print(f"🔥 WILL UPLOAD ALL {len(batch_data)} ROWS FROM THIS BATCH")

            # CUSTOM BATCH UPLOAD - Upload every single row in this batch
            uploaded_count = 0
            failed_count = 0

            # Get existing fields and create missing ones
            existing_fields = integration.get_table_fields()
            missing_fields = [col for col in batch_data.columns if col not in existing_fields]
            if missing_fields:
                print(f"🔧 Creating {len(missing_fields)} missing fields...")
                for field in missing_fields:
                    field_type = integration.detect_field_type(batch_data[field])
                    if integration.create_field(field, field_type):
                        print(f"✅ Created field '{field}'")

            # Upload every row in this batch
            print(f"\n🚀 UPLOADING ALL {len(batch_data)} ROWS FROM BATCH {batch_number}...")

            for idx, (_, row) in enumerate(batch_data.iterrows()):
                row_num_in_batch = idx + 1
                global_row_num = batch['start_row'] + idx

                # Clean row data
                cleaned_row = {}
                has_data = False
                for col in batch_data.columns:
                    value = row[col]
                    if pd.notna(value) and str(value).strip():
                        cleaned_row[col] = str(value).strip()
                        has_data = True
                    else:
                        cleaned_row[col] = ""

                # Upload this row if it has data
                if has_data:
                    success = integration.create_row(cleaned_row)
                    if success:
                        uploaded_count += 1
                        if row_num_in_batch % 20 == 0:  # Progress every 20 rows
                            print(f"   ✅ Uploaded {uploaded_count}/{len(batch_data)} rows from batch {batch_number}")
                    else:
                        failed_count += 1
                        print(f"   ❌ Failed row {global_row_num} in batch {batch_number}")

                # Small delay between rows
                time.sleep(0.01)

            # Final batch results
            print(f"\n📊 BATCH {batch_number} UPLOAD COMPLETE:")
            print(f"   ✅ Successfully uploaded: {uploaded_count} rows")
            print(f"   ❌ Failed: {failed_count} rows")
            print(f"   📈 Success rate: {(uploaded_count/len(batch_data))*100:.1f}%")

            # Mark batch as completed if most rows uploaded
            if uploaded_count >= len(batch_data) * 0.9:  # 90% success rate
                self.batch_status[batch_number] = 'completed'
                print(f"✅ BATCH {batch_number} MARKED AS COMPLETED!")
                return True
            else:
                self.batch_status[batch_number] = 'failed'
                print(f"❌ BATCH {batch_number} MARKED AS FAILED (too many row failures)")
                return False

        except Exception as e:
            print(f"💥 ERROR exporting batch {batch_number}: {str(e)}")
            self.batch_status[batch_number] = 'failed'
            return False

    def get_batch_data_preview(self, batch_number: int, preview_rows: int = 5) -> pd.DataFrame:
        """Get a preview of a specific batch's data"""
        for batch in self.batches:
            if batch['batch_number'] == batch_number:
                return batch['data'].head(preview_rows)
        return pd.DataFrame()

    def reset_batch_status(self, batch_number: int):
        """Reset a batch status back to pending (for retry)"""
        if batch_number in self.batch_status:
            self.batch_status[batch_number] = 'pending'

    def get_next_pending_batch(self) -> int:
        """Get the next batch that needs to be exported"""
        for batch_num, status in self.batch_status.items():
            if status == 'pending':
                return batch_num
        return None

    def is_export_complete(self) -> bool:
        """Check if all batches have been exported successfully"""
        return all(status == 'completed' for status in self.batch_status.values())

    def get_failed_batches(self) -> List[int]:
        """Get list of failed batch numbers"""
        return [batch_num for batch_num, status in self.batch_status.items() if status == 'failed']

    def export_all_remaining_batches(self, base_url: str, api_token: str, table_id: str) -> Dict:
        """
        Export all pending batches automatically (optional helper method)

        Returns:
            Dict with export results
        """
        pending_batches = [num for num, status in self.batch_status.items() if status == 'pending']

        if not pending_batches:
            return {'success': True, 'message': 'No pending batches to export'}

        results = {
            'total_attempted': len(pending_batches),
            'successful': 0,
            'failed': 0,
            'failed_batches': []
        }

        for batch_num in pending_batches:
            print(f"\n🔄 Auto-exporting batch {batch_num}...")
            success = self.export_single_batch(batch_num, base_url, api_token, table_id)

            if success:
                results['successful'] += 1
            else:
                results['failed'] += 1
                results['failed_batches'].append(batch_num)

            # Small delay between batches
            time.sleep(1)

        results['success'] = results['failed'] == 0
        return results

    def test_batch_creation(self, df: pd.DataFrame) -> str:
        """Test batch creation and show detailed info"""
        batches = self.create_batches(df)

        report = f"\n📊 BATCH CREATION TEST REPORT\n"
        report += f"="*50 + "\n"
        report += f"📈 Total rows in dataset: {len(df):,}\n"
        report += f"📦 Total batches created: {len(batches)}\n"
        report += f"🎯 Batch size: {self.batch_size} rows\n\n"

        total_batch_rows = 0
        for batch in batches:
            batch_data_rows = len(batch['data'])
            total_batch_rows += batch_data_rows
            report += f"Batch {batch['batch_number']}: "
            report += f"Rows {batch['start_row']}-{batch['end_row']} "
            report += f"({batch['total_rows']} expected, {batch_data_rows} actual)\n"

        report += f"\n📊 VERIFICATION:\n"
        report += f"   Expected total: {len(df):,} rows\n"
        report += f"   Actual total: {total_batch_rows:,} rows\n"
        report += f"   Match: {'✅ YES' if total_batch_rows == len(df) else '❌ NO'}\n"

        return report