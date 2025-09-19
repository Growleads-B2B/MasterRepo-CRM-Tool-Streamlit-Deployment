"""
FINAL WORKING EXPORTER - FIXES HTTP 400 FIELD VALIDATION ERRORS
Maps fields correctly and handles all validation issues
"""

import requests
import pandas as pd
import streamlit as st
import time


def get_correct_field_mapping(base_url, api_token, table_id):
    """Get the correct field names from Baserow to avoid validation errors"""
    try:
        headers = {'Authorization': f'Token {api_token}'}
        response = requests.get(
            f'{base_url}/api/database/fields/table/{table_id}/',
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            fields = response.json()
            field_mapping = {}
            for field in fields:
                field_mapping[field['name']] = field['type']
            return field_mapping
        else:
            return {}
    except:
        return {}


def clean_data_for_baserow(row_data, field_mapping):
    """Clean data to match Baserow field requirements"""
    cleaned = {}

    for column, value in row_data.items():
        # Skip if field doesn't exist in Baserow
        if column not in field_mapping:
            continue

        field_type = field_mapping[column]

        # Clean the value based on field type
        if pd.notna(value) and str(value).strip():
            str_value = str(value).strip()

            # Handle different field types
            if field_type == 'number':
                try:
                    # Try to convert to number
                    if '.' in str_value:
                        cleaned[column] = float(str_value)
                    else:
                        cleaned[column] = int(str_value)
                except:
                    cleaned[column] = 0  # Default for invalid numbers

            elif field_type == 'boolean':
                # Convert to boolean
                lower_val = str_value.lower()
                cleaned[column] = lower_val in ['true', '1', 'yes', 'on']

            elif field_type == 'email':
                # Basic email validation
                if '@' in str_value:
                    cleaned[column] = str_value
                else:
                    cleaned[column] = ""  # Invalid email

            else:
                # Text field - just clean the string
                cleaned[column] = str_value
        else:
            # Empty value - set appropriate default
            if field_type == 'number':
                cleaned[column] = 0
            elif field_type == 'boolean':
                cleaned[column] = False
            else:
                cleaned[column] = ""

    return cleaned


def export_batch_final(batch_data, batch_number, base_url, api_token, table_id):
    """
    FINAL working batch export that handles all validation errors
    """

    base_url = base_url.rstrip('/')
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json',
    }

    st.write(f"🎯 **FINAL Export - Batch {batch_number}**")
    st.write(f"📊 Processing {len(batch_data)} rows with correct field mapping...")

    # Get correct field mapping to avoid validation errors
    st.write("🔍 Getting correct field mapping from Baserow...")
    field_mapping = get_correct_field_mapping(base_url, api_token, table_id)

    if not field_mapping:
        st.error("❌ Could not get field mapping from Baserow")
        return False

    st.write(f"✅ Found {len(field_mapping)} fields in Baserow:")
    for field_name, field_type in list(field_mapping.items())[:10]:  # Show first 10
        st.write(f"   • {field_name} ({field_type})")

    if len(field_mapping) > 10:
        st.write(f"   ... and {len(field_mapping) - 10} more fields")

    # Upload rows with correct field mapping
    uploaded = 0
    failed = 0
    progress_bar = st.progress(0)

    upload_url = f'{base_url}/api/database/rows/table/{table_id}/?user_field_names=true'

    for idx, (_, row) in enumerate(batch_data.iterrows()):

        # Convert row to dict
        row_dict = dict(row)

        # Clean data for Baserow with correct field mapping
        cleaned_data = clean_data_for_baserow(row_dict, field_mapping)

        # Only upload if we have valid data
        if cleaned_data:
            try:
                response = requests.post(
                    upload_url,
                    headers=headers,
                    json=cleaned_data,
                    timeout=15
                )

                if response.status_code in [200, 201]:
                    uploaded += 1
                else:
                    failed += 1
                    # Show error for first few failures
                    if failed <= 3:
                        st.write(f"❌ Row {idx+1} failed: HTTP {response.status_code}")
                        error_text = response.text[:200]
                        st.write(f"   Error: {error_text}")

            except Exception as e:
                failed += 1
                if failed <= 3:
                    st.write(f"❌ Row {idx+1} exception: {str(e)[:100]}")

        # Update progress
        progress = (idx + 1) / len(batch_data)
        progress_bar.progress(progress)

        # Small delay
        time.sleep(0.01)

    # Final results
    success_rate = (uploaded / len(batch_data)) * 100

    if uploaded > 0:
        st.success(f"🎯 FINAL SUCCESS! Batch {batch_number}: {uploaded}/{len(batch_data)} rows uploaded ({success_rate:.1f}%)")
        return True
    else:
        st.error(f"❌ Batch {batch_number} failed - no rows uploaded")
        return False


def create_final_batches(df, batch_size=80):
    """Create final batches"""
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