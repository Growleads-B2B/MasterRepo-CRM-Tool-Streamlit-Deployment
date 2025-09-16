import streamlit as st
import pandas as pd
import plotly.express as px
from data_consolidator import DataConsolidator
from embedded_baserow import EmbeddedBaserowManager
from typing import Dict, List
import io
import time

# Page configuration
st.set_page_config(
    page_title="Spreadsheet Consolidator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Theme UI/UX
st.markdown("""
<style>
/* Global dark theme styling */
.stApp {
    background-color: #0f1419;
    color: #e5e7eb;
}

.main > div {
    padding: 1rem 2rem;
    background-color: #0f1419;
}

/* Header styling - Dark Theme */
.main-header {
    background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
    color: white;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.1rem;
    opacity: 0.9;
    color: white;
}

/* Card styling - Dark Theme */
.feature-card {
    background: #1f2937;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    border: 1px solid #374151;
    margin-bottom: 1rem;
}

/* Sidebar styling - Dark Theme */
.css-1d391kg {
    background: linear-gradient(180deg, #1f2937 0%, #111827 100%) !important;
}

.css-1d391kg .css-1v0mbdj {
    background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
}

/* Button styling - Dark Theme */
.stButton > button {
    background: linear-gradient(45deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.5);
}

/* Success/Error message styling - Dark Theme */
.stAlert {
    border-radius: 8px;
    border: none;
    background-color: #1f2937 !important;
    color: #e5e7eb !important;
}

/* Metric styling - Dark Theme */
.metric-container {
    background: #1f2937;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #4f46e5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    color: #e5e7eb;
}


/* Data table styling - Dark Theme */
.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.4);
}

.stDataFrame [data-testid="stDataFrameResizable"] {
    background-color: #1f2937;
    color: #e5e7eb;
}

/* File uploader styling - Dark Theme */
.stFileUploader {
    border: 2px dashed #4f46e5;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    background: #1f2937;
}

.stFileUploader label {
    color: #e5e7eb !important;
}

/* Navigation styling - Dark Theme */
.nav-item {
    padding: 0.5rem 1rem;
    margin: 0.2rem 0;
    border-radius: 8px;
    transition: all 0.3s ease;
    color: #e5e7eb;
}

.nav-item:hover {
    background: rgba(79, 70, 229, 0.2);
}

/* Text inputs - Dark Theme */
.stTextInput > div > div > input {
    background-color: #1f2937;
    color: #e5e7eb;
    border: 1px solid #374151;
}

.stSelectbox > div > div > div {
    background-color: #1f2937;
    color: #e5e7eb;
    border: 1px solid #374151;
}

/* Multiselect - Dark Theme */
.stMultiSelect > div > div > div {
    background-color: #1f2937;
    color: #e5e7eb;
    border: 1px solid #374151;
}

/* Radio buttons - Dark Theme */
.stRadio > div {
    color: #e5e7eb;
}

/* Expander - Dark Theme */
.streamlit-expanderHeader {
    background-color: #1f2937;
    color: #e5e7eb;
}

.streamlit-expanderContent {
    background-color: #111827;
    border: 1px solid #374151;
}

/* Tabs - Dark Theme */
.stTabs [data-baseweb="tab-list"] {
    background-color: #1f2937;
}

.stTabs [data-baseweb="tab"] {
    color: #9ca3af;
    background-color: #1f2937;
}

.stTabs [aria-selected="true"] {
    color: #4f46e5 !important;
    background-color: #374151 !important;
}

/* Sidebar text - Dark Theme */
.css-1d391kg {
    color: #e5e7eb;
}

.css-1d391kg .stMarkdown {
    color: #e5e7eb;
}

.css-1d391kg .stSelectbox label {
    color: #e5e7eb !important;
}

/* Enhanced table styling - Dark Theme */
.enhanced-table {
    font-size: 14px;
    background-color: #1f2937;
    color: #e5e7eb;
}

.enhanced-table td {
    border-bottom: 1px solid #374151;
    padding: 0.5rem;
    background-color: #1f2937;
    color: #e5e7eb;
}

.enhanced-table th {
    background: linear-gradient(45deg, #4f46e5, #7c3aed);
    color: white;
    font-weight: 600;
}

/* Success messages - Dark Theme */
.stSuccess {
    background-color: #064e3b !important;
    color: #a7f3d0 !important;
    border: 1px solid #059669 !important;
}

/* Warning messages - Dark Theme */
.stWarning {
    background-color: #451a03 !important;
    color: #fcd34d !important;
    border: 1px solid #d97706 !important;
}

/* Error messages - Dark Theme */
.stError {
    background-color: #7f1d1d !important;
    color: #fca5a5 !important;
    border: 1px solid #dc2626 !important;
}

/* Info messages - Dark Theme */
.stInfo {
    background-color: #1e3a8a !important;
    color: #93c5fd !important;
    border: 1px solid #3b82f6 !important;
}
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'consolidator' not in st.session_state:
    st.session_state.consolidator = DataConsolidator()
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'consolidated' not in st.session_state:
    st.session_state.consolidated = False
if 'master_data' not in st.session_state:
    st.session_state.master_data = pd.DataFrame()
if 'baserow_manager' not in st.session_state:
    st.session_state.baserow_manager = EmbeddedBaserowManager()



def embedded_database_sidebar():
    """Show embedded database status and controls (optional)"""
    manager = st.session_state.baserow_manager
    
    # Try to start database silently
    database_available = manager.start_baserow()
    
    # Only show database section if it's actually working
    if database_available:
        st.sidebar.markdown("---")
        st.sidebar.subheader("🗄️ Database")
        st.sidebar.success("✅ Available")
        
        # Database actions
        if st.sidebar.button("🌐 Open Database", help="Open database interface"):
            st.sidebar.markdown(f"[Open Database]({manager.base_url})")
        
        # Show configuration status
        config_exists = manager.config_file.exists()
        if config_exists:
            st.sidebar.info("⚙️ Configured")
        else:
            st.sidebar.warning("⚙️ Setup Required")

def main():
    # Modern header with gradient background
    st.markdown("""
    <div class="main-header">
        <h1>📊 Spreadsheet Consolidator</h1>
        <p>Transform multiple spreadsheets into unified, standardized data with intelligent header mapping</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar navigation
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, #667eea, #764ba2); border-radius: 10px; margin-bottom: 1rem;">
        <h2 style="color: white; margin: 0;">🎯 Navigation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "Choose a workflow step:",
        ["Upload & Process", "Header Mapping", "Master Sheet", "Analytics"],
        help="Navigate through the data consolidation workflow"
    )
    
    
    # Embedded database sidebar
    embedded_database_sidebar()
    
    
    if page == "Upload & Process":
        upload_and_process_page()
    elif page == "Header Mapping":
        header_mapping_page()
    elif page == "Master Sheet":
        master_sheet_page()
    elif page == "Analytics":
        analytics_page()



def upload_and_process_page():
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: #4f46e5; margin-top: 0;">📁 Upload & Process Files</h2>
        <p style="color: #9ca3af; margin-bottom: 0;">Start by uploading your spreadsheet files. Supported formats: CSV, Excel (.xlsx, .xls)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload spreadsheet files (CSV, Excel)",
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="You can upload multiple files at once. Supported formats: CSV, XLSX, XLS"
    )
    
    if uploaded_files:
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #10b981, #059669); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h4 style="color: white; margin: 0;">✨ Successfully uploaded {len(uploaded_files)} files</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display uploaded files in a beautiful card
        with st.expander("📋 View Uploaded Files", expanded=True):
            for file in uploaded_files:
                st.markdown(f"""
                <div style="background: #374151; padding: 0.8rem; border-radius: 6px; margin: 0.5rem 0; border-left: 3px solid #4f46e5; color: #e5e7eb;">
                    <strong>📄 {file.name}</strong><br>
                    <small style="color: #9ca3af;">Size: {file.size:,} bytes</small>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🔄 Process Files", type="primary"):
            result = st.session_state.consolidator.process_files(uploaded_files)
            
            if result['success']:
                st.session_state.processed = True
                st.success("✅ Files processed successfully!")
                
                # Show processing summary in enhanced cards
                st.markdown("### 📈 Processing Summary")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h3 style="color: #4f46e5; margin: 0 0 0.5rem 0;">{result['file_count']}</h3>
                        <p style="margin: 0; color: #9ca3af;">Files Processed</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h3 style="color: #4f46e5; margin: 0 0 0.5rem 0;">{result['total_sheets']}</h3>
                        <p style="margin: 0; color: #9ca3af;">Total Sheets</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h3 style="color: #4f46e5; margin: 0 0 0.5rem 0;">{len(result['headers'])}</h3>
                        <p style="margin: 0; color: #9ca3af;">Unique Headers</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Store results in session state
                st.session_state.headers = result['headers']
                st.session_state.auto_mappings = result['auto_mappings']
                st.session_state.mapping_suggestions = result['mapping_suggestions']
                
                st.info("👉 Go to 'Header Mapping' to configure column standardization.")
                
            else:
                st.error(f"❌ Error processing files: {result['error']}")

def header_mapping_page():
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: #4f46e5; margin-top: 0;">🔧 Header Mapping Configuration</h2>
        <p style="color: #9ca3af; margin-bottom: 0;">Review and adjust header mappings to standardize your data columns</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.processed:
        st.warning("⚠️ Please upload and process files first.")
        return
    
    st.markdown("Review and adjust the header mappings. The system has automatically suggested standardized headers based on common patterns.")
    
    # Show automatic mappings
    headers = st.session_state.headers
    auto_mappings = st.session_state.auto_mappings
    
    # Create mapping interface with better styling
    st.markdown("""
    <div style="background: #374151; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border: 1px solid #4b5563;">
        <h3 style="color: #4f46e5; margin-top: 0;">📝 Header Mappings</h3>
        <p style="color: #9ca3af; margin-bottom: 1rem;">Review the automatic mappings and adjust as needed</p>
    </div>
    """, unsafe_allow_html=True)
    
    mapping = {}
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📄 Original Headers**")
    with col2:
        st.markdown("**✨ Standardized Headers**")
    
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


def show_database_export_dialog():
    """Show database export dialog"""
    if 'export_data' not in st.session_state:
        return
    
    manager = st.session_state.baserow_manager
    
    with st.container():
        st.subheader(f"🗄️ Export to Table {manager.table_id}")
        
        # Export options
        st.markdown("**Export Options:**")
        clear_existing = st.checkbox(
            "🗑️ Clear existing data before export", 
            value=False,
            help="Remove all existing rows before adding new data"
        )
        
        # Show data preview
        data = st.session_state.export_data
        st.markdown(f"**Data Preview** ({len(data)} rows):")
        st.dataframe(data.head(), use_container_width=True)
        
        # Export buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Export Now", type="primary"):
                # Direct API export to Baserow
                success = manager.export_data(data, clear_existing=clear_existing)
                
                if success:
                    st.success(f"✅ Successfully exported {len(data)} rows to Table {manager.table_id}!")
                    st.info(f"🔗 View your data: [Table {manager.table_id}]({manager.base_url}/database/174/table/{manager.table_id})")
                    st.session_state.show_db_export = False
                    st.rerun()
                else:
                    st.error("❌ Export failed. Check your Baserow connection and API token.")
                    st.info(f"🔗 Verify table access: [Table {manager.table_id}]({manager.base_url}/database/174/table/{manager.table_id})")
                    st.info("💡 **Tip**: Ensure your API token has create/update permissions for this table.")
        
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.show_db_export = False
                st.rerun()

def master_sheet_page():
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: #4f46e5; margin-top: 0;">📋 Unified Master Sheet</h2>
        <p style="color: #9ca3af; margin-bottom: 0;">View, filter, and export your consolidated data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show database export dialog
    if st.session_state.get('show_db_export', False):
        show_database_export_dialog()
        return
    
    if not st.session_state.processed:
        st.warning("⚠️ Please upload and process files first.")
        return
    
    # Consolidate data button
    if not st.session_state.consolidated:
        if st.button("🔄 Consolidate Data", type="primary"):
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
        
        # Show summary metrics in beautiful cards
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
            <h3 style="color: white; margin: 0; text-align: center;">📊 Data Consolidation Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: #4f46e5; margin: 0 0 0.5rem 0;">{summary['total_rows']:,}</h2>
                <p style="margin: 0; color: #9ca3af; font-weight: 600;">Total Rows</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: #4f46e5; margin: 0 0 0.5rem 0;">{summary['total_columns']}</h2>
                <p style="margin: 0; color: #9ca3af; font-weight: 600;">Total Columns</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: #4f46e5; margin: 0 0 0.5rem 0;">{summary['source_files']}</h2>
                <p style="margin: 0; color: #9ca3af; font-weight: 600;">Source Files</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: #4f46e5; margin: 0 0 0.5rem 0;">{summary['source_sheets']}</h2>
                <p style="margin: 0; color: #9ca3af; font-weight: 600;">Source Sheets</p>
            </div>
            """, unsafe_allow_html=True)
        
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
        
        # Data viewing options
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h4 style="color: white; margin: 0; text-align: center;">🔍 Choose Your Data View</h4>
        </div>
        """, unsafe_allow_html=True)
        
        view_tab1, view_tab2 = st.tabs(["📊 Enhanced Data Viewer", "🗑️ Baserow Export"])
        
        with view_tab1:
            enhanced_data_viewer(display_data)
        
        with view_tab2:
            # Traditional data table view
            st.markdown("**Traditional Data Table View:**")
            st.dataframe(display_data, width='stretch', height=400)
        
        # Export section with enhanced styling
        st.markdown("""
        <div style="background: #374151; padding: 1.5rem; border-radius: 12px; margin: 2rem 0 1rem 0; border: 1px solid #4b5563;">
            <h3 style="color: #4f46e5; margin: 0 0 1rem 0; text-align: center;">💾 Export Your Data</h3>
            <p style="color: #9ca3af; margin: 0; text-align: center;">Choose your preferred export format</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
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
        
        with col3:
            # Database export to your specific table
            if st.button("🗑️ Export to Baserow Database", type="primary"):
                if len(filtered_data) > 0:
                    st.session_state.show_db_export = True
                    st.session_state.export_data = filtered_data.copy()
                    st.rerun()
                else:
                    st.error("❌ No data to export")

def analytics_page():
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: #4f46e5; margin-top: 0;">📊 Data Analytics</h2>
        <p style="color: #9ca3af; margin-bottom: 0;">Explore insights and statistics from your consolidated data</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.consolidated:
        st.warning("⚠️ Please consolidate data first.")
        return
    
    master_data = st.session_state.master_data
    
    # Data quality overview with better styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
        <h3 style="color: white; margin: 0; text-align: center;">🔍 Data Quality Analysis</h3>
        <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; text-align: center;">Comprehensive overview of your data completeness</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Source distribution with enhanced styling
    st.markdown("""
    <div style="background: #374151; padding: 1.5rem; border-radius: 12px; margin: 2rem 0 1rem 0; border: 1px solid #4b5563;">
        <h3 style="color: #4f46e5; margin: 0 0 1rem 0; text-align: center;">📈 Source Distribution Analysis</h3>
        <p style="color: #9ca3af; margin: 0; text-align: center;">Visualize how your data is distributed across files and sheets</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Column statistics with better styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 1.5rem; border-radius: 12px; margin: 2rem 0 1rem 0;">
        <h3 style="color: white; margin: 0 0 1rem 0; text-align: center;">📋 Detailed Column Analysis</h3>
        <p style="color: rgba(255,255,255,0.9); margin: 0; text-align: center;">Deep dive into individual column statistics</p>
    </div>
    """, unsafe_allow_html=True)
    
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

def enhanced_data_viewer(data):
    """Enhanced data viewer with advanced filtering, sorting, and personalization"""
    if data.empty:
        st.warning("No data to display")
        return
    
    # Enhanced viewer header
    st.markdown("""
    <div style="background: linear-gradient(45deg, #10b981, #059669); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <h4 style="color: white; margin: 0;">✨ Enhanced Data Viewer - Personalized for You</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Advanced controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # Global search
        search_query = st.text_input(
            "🔍 Global Search", 
            placeholder="Search across all columns...",
            help="Search for any value across all data columns"
        )
    
    with col2:
        # Column visibility selector
        all_columns = [col for col in data.columns if col not in ['source_file', 'source_sheet']]
        visible_columns = st.multiselect(
            "👁️ Show Columns",
            options=all_columns,
            default=all_columns[:8] if len(all_columns) > 8 else all_columns,
            help="Select which columns to display"
        )
    
    with col3:
        # View mode selector
        view_mode = st.selectbox(
            "📋 View Mode",
            ["Table", "Cards", "Summary"]
        )
    
    # Apply global search
    display_data = data.copy()
    if search_query:
        mask = False
        for col in all_columns:
            if col in display_data.columns:
                mask |= display_data[col].astype(str).str.contains(search_query, case=False, na=False)
        display_data = display_data[mask]
    
    # Advanced filtering section
    with st.expander("🎛️ Advanced Filters", expanded=False):
        filter_cols = st.columns(3)
        active_filters = {}
        
        for i, col in enumerate(visible_columns[:9]):  # Limit to 9 filters
            with filter_cols[i % 3]:
                if col in display_data.columns:
                    unique_vals = display_data[col].dropna().astype(str).unique()
                    if len(unique_vals) <= 20:
                        selected = st.multiselect(
                            f"Filter {col}",
                            options=sorted(unique_vals),
                            key=f"enhanced_filter_{col}"
                        )
                        if selected:
                            active_filters[col] = selected
                    else:
                        text_filter = st.text_input(
                            f"Filter {col} (contains)",
                            key=f"enhanced_text_filter_{col}"
                        )
                        if text_filter:
                            active_filters[col] = text_filter
        
        # Apply advanced filters
        for col, filter_val in active_filters.items():
            if isinstance(filter_val, list):
                display_data = display_data[display_data[col].isin(filter_val)]
            else:
                display_data = display_data[
                    display_data[col].astype(str).str.contains(filter_val, case=False, na=False)
                ]
    
    # Sort controls
    sort_col1, sort_col2 = st.columns(2)
    with sort_col1:
        sort_by = st.selectbox(
            "📈 Sort by Column",
            options=["None"] + visible_columns,
            help="Choose column to sort by"
        )
    with sort_col2:
        sort_order = st.radio(
            "Sort Order",
            ["Ascending ⬆️", "Descending ⬇️"],
            horizontal=True
        )
    
    # Apply sorting
    if sort_by != "None" and sort_by in display_data.columns:
        ascending = sort_order == "Ascending ⬆️"
        try:
            # Try numeric sort first
            numeric_data = pd.to_numeric(display_data[sort_by], errors='coerce')
            if not numeric_data.isna().all():
                display_data = display_data.sort_values(sort_by, ascending=ascending, 
                                                      key=lambda x: pd.to_numeric(x, errors='coerce'))
            else:
                display_data = display_data.sort_values(sort_by, ascending=ascending)
        except:
            display_data = display_data.sort_values(sort_by, ascending=ascending)
    
    # Display results info
    total_rows = len(data)
    filtered_rows = len(display_data)
    st.markdown(f"""
    <div style="background: #374151; padding: 0.8rem; border-radius: 6px; border-left: 4px solid #4f46e5; margin: 1rem 0; color: #e5e7eb;">
        <strong>📊 Results:</strong> Showing {filtered_rows:,} of {total_rows:,} rows
        {f" | 🔍 Search: '{search_query}'" if search_query else ""}
        {f" | 🎛️ {len(active_filters)} filters active" if active_filters else ""}
    </div>
    """, unsafe_allow_html=True)
    
    # Display data based on view mode
    if view_mode == "Table":
        # Enhanced table view
        if visible_columns:
            # Show only selected columns plus source info
            cols_to_show = visible_columns + ['source_file', 'source_sheet']
            cols_to_show = [col for col in cols_to_show if col in display_data.columns]
            
            # Add row selection
            if len(display_data) > 0:
                st.markdown("**📋 Interactive Data Table:**")
                
                # Color-code rows based on source file
                styled_data = display_data[cols_to_show].copy()
                
                # Custom styling for better readability
                st.markdown("""
                <style>
                .enhanced-table {
                    font-size: 14px;
                }
                .enhanced-table td {
                    border-bottom: 1px solid #e5e7eb;
                    padding: 0.5rem;
                }
                .enhanced-table th {
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    color: white;
                    font-weight: 600;
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.dataframe(
                    styled_data,
                    use_container_width=True,
                    height=min(600, max(200, len(styled_data) * 35 + 50))
                )
            else:
                st.info("No data matches your current filters")
        else:
            st.warning("Please select at least one column to display")
    
    elif view_mode == "Cards":
        # Card view for detailed record inspection
        st.markdown("**🃏 Card View - Detailed Records:**")
        
        if len(display_data) > 0:
            # Pagination for cards
            cards_per_page = 5
            total_pages = (len(display_data) - 1) // cards_per_page + 1
            
            if total_pages > 1:
                page = st.number_input("Card Page", 1, total_pages, 1) - 1
                start_idx = page * cards_per_page
                end_idx = start_idx + cards_per_page
                page_data = display_data.iloc[start_idx:end_idx]
            else:
                page_data = display_data
            
            for idx, row in page_data.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div style="background: #1f2937; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; 
                                border: 1px solid #374151; box-shadow: 0 2px 4px rgba(0,0,0,0.3); color: #e5e7eb;">
                        <h5 style="color: #4f46e5; margin: 0 0 1rem 0;">📄 Record #{idx + 1}</h5>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display each field in the record
                    card_cols = st.columns(2)
                    for i, col in enumerate(visible_columns):
                        if col in row.index:
                            with card_cols[i % 2]:
                                value = str(row[col]) if pd.notna(row[col]) else "N/A"
                                st.markdown(f"**{col}:** {value}")
                    
                    # Source information
                    st.markdown(f"""
                    <div style="background: #374151; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem; color: #e5e7eb;">
                        <small><strong>Source:</strong> {row.get('source_file', 'N/A')} → {row.get('source_sheet', 'N/A')}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No records match your current filters")
    
    elif view_mode == "Summary":
        # Summary statistics view
        st.markdown("**📈 Data Summary & Statistics:**")
        
        if len(display_data) > 0:
            # Quick stats
            summary_cols = st.columns(4)
            with summary_cols[0]:
                st.metric("Total Records", len(display_data))
            with summary_cols[1]:
                st.metric("Columns Shown", len(visible_columns))
            with summary_cols[2]:
                source_files = display_data['source_file'].nunique() if 'source_file' in display_data.columns else 0
                st.metric("Source Files", source_files)
            with summary_cols[3]:
                completeness = (display_data[visible_columns].notna().sum().sum() / 
                              (len(display_data) * len(visible_columns)) * 100) if visible_columns else 0
                st.metric("Data Completeness", f"{completeness:.1f}%")
            
            # Column-wise statistics
            st.markdown("### 📊 Column Statistics")
            for col in visible_columns[:5]:  # Show stats for first 5 columns
                if col in display_data.columns:
                    col_data = display_data[col].dropna()
                    if len(col_data) > 0:
                        with st.expander(f"📈 {col} Statistics"):
                            stat_cols = st.columns(3)
                            with stat_cols[0]:
                                st.write(f"**Unique Values:** {col_data.nunique()}")
                                st.write(f"**Non-empty:** {len(col_data)}")
                            with stat_cols[1]:
                                if col_data.dtype in ['int64', 'float64']:
                                    st.write(f"**Mean:** {col_data.mean():.2f}")
                                    st.write(f"**Median:** {col_data.median():.2f}")
                                else:
                                    most_common = col_data.value_counts().head(1)
                                    if len(most_common) > 0:
                                        st.write(f"**Most Common:** {most_common.index[0]}")
                                        st.write(f"**Frequency:** {most_common.iloc[0]}")
                            with stat_cols[2]:
                                if col_data.dtype in ['int64', 'float64']:
                                    st.write(f"**Min:** {col_data.min()}")
                                    st.write(f"**Max:** {col_data.max()}")
        else:
            st.info("No data available for summary")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    action_cols = st.columns(4)
    
    with action_cols[0]:
        if st.button("🔄 Reset All Filters"):
            st.rerun()
    
    with action_cols[1]:
        if st.button("📊 Select All Columns"):
            st.session_state["enhanced_viewer_columns"] = all_columns
            st.rerun()
    
    with action_cols[2]:
        if len(display_data) > 0:
            csv_data = display_data[visible_columns + ['source_file', 'source_sheet']].to_csv(index=False)
            st.download_button(
                "💾 Download Filtered Data",
                csv_data,
                "filtered_data.csv",
                "text/csv"
            )
    
    with action_cols[3]:
        if st.button("📋 Copy to Clipboard"):
            st.info("Use Ctrl+C on the table to copy data")

if __name__ == "__main__":
    main()