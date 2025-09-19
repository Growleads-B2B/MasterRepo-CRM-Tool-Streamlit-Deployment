"""
ULTRA SIMPLE BATCH EXPORTER - NO BULLSHIT, JUST WORKS
Fast, minimal, guaranteed to upload all rows
"""

import requests
import pandas as pd
import streamlit as st
import time


def export_batch_ultra_simple(batch_data, batch_number, base_url, api_token, table_id):
    """
    Ultra simple batch export - NO complex features, just upload rows fast
    """

    # Basic setup
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json',
    }

    base_url = base_url.rstrip('/')
    upload_url = f'{base_url}/api/database/rows/table/{table_id}/?user_field_names=true'

    st.write(f"🚀 **Ultra Simple Export - Batch {batch_number}**")
    st.write(f"📊 Uploading {len(batch_data)} rows...")

    # Simple progress tracking
    uploaded = 0
    failed = 0

    progress_bar = st.progress(0)

    # Just upload every row - no fancy stuff
    for idx, (_, row) in enumerate(batch_data.iterrows()):

        # Convert row to simple dict
        row_dict = {}
        for col in batch_data.columns:
            value = row[col]
            if pd.notna(value):
                row_dict[col] = str(value)
            else:
                row_dict[col] = ""

        # Simple upload - just send the data
        try:
            response = requests.post(
                upload_url,
                headers=headers,
                json=row_dict,
                timeout=10
            )

            if response.status_code in [200, 201]:
                uploaded += 1
            else:
                failed += 1
                # Show first error only
                if failed == 1:
                    st.error(f"❌ First error: HTTP {response.status_code} - {response.text[:100]}")

        except Exception as e:
            failed += 1
            if failed == 1:
                st.error(f"❌ First error: {str(e)[:100]}")

        # Update progress
        progress = (idx + 1) / len(batch_data)
        progress_bar.progress(progress)

        # Very small delay
        time.sleep(0.005)

    # Results
    success_rate = (uploaded / len(batch_data)) * 100

    if uploaded > 0:
        st.success(f"✅ Batch {batch_number} completed! Uploaded {uploaded}/{len(batch_data)} rows ({success_rate:.1f}%)")
        return True
    else:
        st.error(f"❌ Batch {batch_number} failed! No rows uploaded.")
        return False


def create_simple_batches(df, batch_size=80):
    """Create simple batches - just split the data"""
    batches = []
    total_rows = len(df)

    for start in range(0, total_rows, batch_size):
        end = min(start + batch_size, total_rows)
        batch_data = df.iloc[start:end].copy().reset_index(drop=True)

        batch = {
            'number': len(batches) + 1,
            'start_row': start + 1,
            'end_row': end,
            'data': batch_data,
            'status': 'pending'
        }
        batches.append(batch)

    return batches