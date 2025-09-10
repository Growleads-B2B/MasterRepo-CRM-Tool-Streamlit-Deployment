import streamlit as st
import pandas as pd
import plotly.express as px
from data_consolidator import DataConsolidator
from typing import Dict, List
import io

# Page configuration
st.set_page_config(
    page_title="Spreadsheet Consolidator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'consolidator' not in st.session_state:
    st.session_state.consolidator = DataConsolidator()
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'consolidated' not in st.session_state:
    st.session_state.consolidated = False
if 'master_data' not in st.session_state:
    st.session_state.master_data = pd.DataFrame()

def main():
    st.title("📊 Spreadsheet Consolidator")
    st.markdown("Upload multiple spreadsheets and consolidate them into a unified master sheet with standardized headers.")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Upload & Process", "Header Mapping", "Master Sheet", "Analytics"]
    )
    
    if page == "Upload & Process":
        upload_and_process_page()
    elif page == "Header Mapping":
        header_mapping_page()
    elif page == "Master Sheet":
        master_sheet_page()
    elif page == "Analytics":
        analytics_page()

def upload_and_process_page():
    st.header("📁 Upload & Process Files")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload spreadsheet files (CSV, Excel)",
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="You can upload multiple files at once. Supported formats: CSV, XLSX, XLS"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} files")
        
        # Display uploaded files
        with st.expander("📋 Uploaded Files"):
            for file in uploaded_files:
                st.write(f"• {file.name} ({file.size} bytes)")
        
        if st.button("🔄 Process Files", type="primary"):
            with st.spinner("Processing files..."):
                result = st.session_state.consolidator.process_files(uploaded_files)
                
                if result['success']:
                    st.session_state.processed = True
                    st.success("✅ Files processed successfully!")
                    
                    # Show processing summary
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Files Processed", result['file_count'])
                    with col2:
                        st.metric("Total Sheets", result['total_sheets'])
                    with col3:
                        st.metric("Unique Headers", len(result['headers']))
                    
                    # Store results in session state
                    st.session_state.headers = result['headers']
                    st.session_state.auto_mappings = result['auto_mappings']
                    st.session_state.mapping_suggestions = result['mapping_suggestions']
                    
                    st.info("👉 Go to 'Header Mapping' to configure column standardization.")
                    
                else:
                    st.error(f"❌ Error processing files: {result['error']}")

def header_mapping_page():
    st.header("🔧 Header Mapping Configuration")
    
    if not st.session_state.processed:
        st.warning("⚠️ Please upload and process files first.")
        return
    
    st.markdown("Review and adjust the header mappings. The system has automatically suggested standardized headers based on common patterns.")
    
    # Show automatic mappings
    headers = st.session_state.headers
    auto_mappings = st.session_state.auto_mappings
    
    # Create mapping interface
    st.subheader("📝 Header Mappings")
    
    mapping = {}
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Original Headers**")
    with col2:
        st.write("**Standardized Headers**")
    
    # Create form for header mappings
    with st.form("header_mapping_form"):
        for header in headers:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(header)
            
            with col2:
                # Get suggestions for this header
                suggestions = st.session_state.mapping_suggestions.get(header, [])
                options = [auto_mappings.get(header, header)] + [s[0] for s in suggestions[:3]]
                options = list(dict.fromkeys(options))  # Remove duplicates while preserving order
                
                mapped_header = st.selectbox(
                    f"Map '{header}' to:",
                    options=options,
                    key=f"mapping_{header}",
                    label_visibility="collapsed"
                )
                mapping[header] = mapped_header
        
        # Submit button
        if st.form_submit_button("✅ Apply Mapping", type="primary"):
            st.session_state.consolidator.update_header_mapping(mapping)
            st.success("Header mapping updated!")
            
            # Show mapping summary
            with st.expander("📊 Mapping Summary"):
                df_mapping = pd.DataFrame([
                    {"Original": orig, "Standardized": std} 
                    for orig, std in mapping.items()
                ])
                st.dataframe(df_mapping, use_container_width=True)
            
            st.info("👉 Go to 'Master Sheet' to consolidate your data.")

def master_sheet_page():
    st.header("📋 Unified Master Sheet")
    
    if not st.session_state.processed:
        st.warning("⚠️ Please upload and process files first.")
        return
    
    # Consolidate data button
    if not st.session_state.consolidated:
        if st.button("🔄 Consolidate Data", type="primary"):
            with st.spinner("Consolidating data..."):
                result = st.session_state.consolidator.consolidate_data()
                
                if result['success']:
                    st.session_state.consolidated = True
                    st.session_state.master_data = result['data']
                    st.session_state.summary = result['summary']
                    st.success("✅ Data consolidated successfully!")
                else:
                    st.error(f"❌ Error consolidating data: {result['error']}")
                    return
    
    if st.session_state.consolidated:
        master_data = st.session_state.master_data
        summary = st.session_state.summary
        
        # Show summary metrics
        st.subheader("📊 Data Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", summary['total_rows'])
        with col2:
            st.metric("Total Columns", summary['total_columns'])
        with col3:
            st.metric("Source Files", summary['source_files'])
        with col4:
            st.metric("Source Sheets", summary['source_sheets'])
        
        # Filtering section
        st.subheader("🔍 Filter Data")
        
        # Get non-metadata columns for filtering
        filter_columns = [col for col in master_data.columns if col not in ['source_file', 'source_sheet']]
        
        filters = {}
        filter_cols = st.columns(min(3, len(filter_columns)))
        
        for i, column in enumerate(filter_columns[:6]):  # Limit to 6 filters for UI
            with filter_cols[i % 3]:
                unique_values = master_data[column].dropna().astype(str).unique()
                if len(unique_values) <= 20:
                    # Multi-select for categorical data
                    selected = st.multiselect(
                        f"Filter by {column}",
                        options=unique_values,
                        key=f"filter_{column}"
                    )
                    if selected:
                        filters[column] = selected
                else:
                    # Text input for continuous data
                    text_filter = st.text_input(
                        f"Filter {column} (contains)",
                        key=f"filter_text_{column}"
                    )
                    if text_filter:
                        filters[column] = text_filter
        
        # Apply filters
        if filters:
            filtered_data = st.session_state.consolidator.filter_data(filters)
        else:
            filtered_data = master_data
        
        # Sorting section
        st.subheader("📈 Sort Data")
        col1, col2 = st.columns(2)
        with col1:
            sort_column = st.selectbox("Sort by column:", options=filter_columns)
        with col2:
            sort_ascending = st.checkbox("Ascending order", value=True)
        
        if sort_column:
            filtered_data = st.session_state.consolidator.sort_data(
                filtered_data, sort_column, sort_ascending
            )
        
        # Display data
        st.subheader("📋 Data Preview")
        st.info(f"Showing {len(filtered_data)} rows out of {len(master_data)} total rows")
        
        # Pagination for large datasets
        rows_per_page = st.selectbox("Rows per page:", [50, 100, 250, 500], index=1)
        
        if len(filtered_data) > rows_per_page:
            page_num = st.number_input("Page", min_value=1, max_value=(len(filtered_data)-1)//rows_per_page + 1, value=1)
            start_idx = (page_num - 1) * rows_per_page
            end_idx = start_idx + rows_per_page
            display_data = filtered_data.iloc[start_idx:end_idx]
        else:
            display_data = filtered_data
        
        # Display the data table
        st.dataframe(display_data, use_container_width=True, height=400)
        
        # Export section
        st.subheader("💾 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Download as Excel", type="secondary"):
                excel_data = st.session_state.consolidator.export_data(filtered_data, 'xlsx')
                st.download_button(
                    label="📥 Download Excel File",
                    data=excel_data,
                    file_name="consolidated_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            if st.button("📄 Download as CSV", type="secondary"):
                csv_data = st.session_state.consolidator.export_data(filtered_data, 'csv')
                st.download_button(
                    label="📥 Download CSV File",
                    data=csv_data,
                    file_name="consolidated_data.csv",
                    mime="text/csv"
                )

def analytics_page():
    st.header("📊 Data Analytics")
    
    if not st.session_state.consolidated:
        st.warning("⚠️ Please consolidate data first.")
        return
    
    master_data = st.session_state.master_data
    
    # Data quality overview
    st.subheader("🔍 Data Quality Overview")
    
    # Calculate data completeness
    completeness_data = []
    for col in master_data.columns:
        if col not in ['source_file', 'source_sheet']:
            try:
                col_series = master_data[col]
                if isinstance(col_series, pd.DataFrame):
                    col_series = col_series.iloc[:, 0]
                non_empty = col_series.astype(str).str.strip().ne('').sum()
                completeness = (non_empty / len(master_data)) * 100
                completeness_data.append({
                    'Column': col,
                    'Completeness (%)': round(completeness, 1),
                    'Non-empty Values': non_empty,
                    'Total Values': len(master_data)
                })
            except Exception:
                # Skip problematic columns
                completeness_data.append({
                    'Column': col,
                    'Completeness (%)': 0,
                    'Non-empty Values': 0,
                    'Total Values': len(master_data)
                })
    
    completeness_df = pd.DataFrame(completeness_data)
    
    # Visualize data completeness
    fig = px.bar(
        completeness_df,
        x='Column',
        y='Completeness (%)',
        title='Data Completeness by Column',
        color='Completeness (%)',
        color_continuous_scale='RdYlGn'
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Show completeness table
    st.dataframe(completeness_df, use_container_width=True)
    
    # Source distribution
    st.subheader("📈 Source Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # File distribution
        file_counts = master_data['source_file'].value_counts()
        fig_files = px.pie(
            values=file_counts.values,
            names=file_counts.index,
            title="Records by Source File"
        )
        st.plotly_chart(fig_files, use_container_width=True)
    
    with col2:
        # Sheet distribution
        sheet_counts = master_data['source_sheet'].value_counts()
        fig_sheets = px.pie(
            values=sheet_counts.values,
            names=sheet_counts.index,
            title="Records by Source Sheet"
        )
        st.plotly_chart(fig_sheets, use_container_width=True)
    
    # Column statistics
    st.subheader("📋 Column Statistics")
    
    selected_column = st.selectbox(
        "Select column for detailed analysis:",
        options=[col for col in master_data.columns if col not in ['source_file', 'source_sheet']]
    )
    
    if selected_column:
        stats = st.session_state.consolidator.get_column_stats(selected_column)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Values", stats['total_values'])
        with col2:
            st.metric("Non-empty Values", stats['non_empty_values'])
        with col3:
            st.metric("Unique Values", stats['unique_values'])
        
        # Show most common values
        if stats['most_common']:
            st.write("**Most Common Values:**")
            for value, count in stats['most_common'].items():
                st.write(f"• {value}: {count} occurrences")
        
        # Show numeric statistics if available
        if 'numeric_stats' in stats:
            st.write("**Numeric Statistics:**")
            numeric_stats = stats['numeric_stats']
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Mean", f"{numeric_stats['mean']:.2f}")
            with col2:
                st.metric("Median", f"{numeric_stats['median']:.2f}")
            with col3:
                st.metric("Min", f"{numeric_stats['min']:.2f}")
            with col4:
                st.metric("Max", f"{numeric_stats['max']:.2f}")
            with col5:
                st.metric("Std Dev", f"{numeric_stats['std']:.2f}")
            
            # Create histogram for numeric data
            numeric_data = pd.to_numeric(master_data[selected_column], errors='coerce').dropna()
            fig_hist = px.histogram(
                x=numeric_data,
                nbins=30,
                title=f"Distribution of {selected_column}"
            )
            st.plotly_chart(fig_hist, use_container_width=True)

if __name__ == "__main__":
    main()