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

# Custom CSS for Subtle Warm Light Theme UI/UX
st.markdown("""
<style>
/* Force light theme override for all browser preferences */
:root {
    color-scheme: light !important;
}

* {
    color-scheme: light !important;
}

html {
    color-scheme: light !important;
}

body {
    color-scheme: light !important;
}

/* Media queries to override dark mode preferences */
@media (prefers-color-scheme: dark) {
    :root {
        color-scheme: light !important;
    }
    
    * {
        color-scheme: light !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%) !important;
        color: #3d3530 !important;
    }
}

@media (prefers-color-scheme: light) {
    :root {
        color-scheme: light !important;
    }
    
    * {
        color-scheme: light !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%) !important;
        color: #3d3530 !important;
    }
}

/* Global subtle warm light theme styling - force override */
.stApp {
    background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%) !important;
    color: #3d3530 !important;
    color-scheme: light !important;
}

.main > div {
    padding: 1rem 2rem;
    background: transparent;
}

/* Header styling - Subtle Warm Theme */
.main-header {
    background: linear-gradient(135deg, #f8f5f2 0%, #f0ebe6 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    margin-bottom: 2.5rem;
    box-shadow: 0 6px 25px rgba(232, 168, 124, 0.08);
    text-align: center;
    border: 1px solid #f0e6d8;
    backdrop-filter: blur(10px);
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
    color: #3d3530;
    text-shadow: 0 1px 2px rgba(255,255,255,0.8);
}

.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.1rem;
    opacity: 0.95;
    color: #5a4f47;
}

/* Card styling - Subtle Warm Theme */
.feature-card {
    background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%);
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 1px solid #f0e6d8 !important;
    box-shadow: 0 3px 12px rgba(212, 146, 111, 0.06);
}

/* Sidebar styling - Subtle Warm Theme - Force override all themes */
.css-1d391kg {
    background: linear-gradient(180deg, #f8f5f2 0%, #f0ebe6 100%) !important;
    color-scheme: light !important;
    border-right: 1px solid #e8ddd4 !important;
    box-shadow: 2px 0 10px rgba(212, 146, 111, 0.08) !important;
}

.css-1d391kg .css-1v0mbdj {
    background: linear-gradient(180deg, #f8f5f2 0%, #f0ebe6 100%) !important;
    color-scheme: light !important;
}

/* Enhanced sidebar container */
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #f8f5f2 0%, #f0ebe6 100%) !important;
    border-right: 1px solid #e8ddd4 !important;
    box-shadow: 2px 0 10px rgba(212, 146, 111, 0.08) !important;
}

/* Force override for dark mode - Sidebar */
@media (prefers-color-scheme: dark) {
    .css-1d391kg {
        background: linear-gradient(180deg, #fefefe 0%, #fbfaf8 100%) !important;
        color: #3d3530 !important;
    }
    
    .css-1d391kg .css-1v0mbdj {
        background: linear-gradient(180deg, #fefbf8 0%, #faf6f2 100%) !important;
        color: #3d3530 !important;
    }
}

/* Streamlit theme override */
.stApp > div {
    background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%) !important;
    color: #3d3530 !important;
}

.stApp [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fefefe 0%, #fbfaf8 100%) !important;
    color: #3d3530 !important;
}

.stApp [data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, #fefefe 0%, #fbfaf8 100%) !important;
    color: #3d3530 !important;
}

/* Button styling - Subtle Warm Theme */
.stButton > button {
    background: linear-gradient(45deg, #e0bfa8, #d4b3a0) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(212, 146, 111, 0.15) !important;
    color-scheme: light !important;
}

/* Force button styling in dark mode */
@media (prefers-color-scheme: dark) {
    .stButton > button {
        background: linear-gradient(45deg, #e0bfa8, #d4b3a0) !important;
        color: white !important;
        border: none !important;
    }
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(212, 146, 111, 0.25) !important;
    background: linear-gradient(45deg, #d4b3a0, #c8a694) !important;
}

/* Success/Error message styling - Subtle Warm Theme */
.stAlert {
    border-radius: 8px !important;
    border: 1px solid #f0e6d8 !important;
    background-color: #fefbf8 !important;
    color: #3d3530 !important;
    box-shadow: 0 2px 6px rgba(212, 146, 111, 0.05) !important;
}

/* Metric styling - Subtle Warm Theme */
.metric-container {
    background: linear-gradient(135deg, #ffffff 0%, #fefdfb 100%);
    padding: 1.2rem;
    border-radius: 10px;
    border: 1px solid #f8f4f0;
    box-shadow: 0 2px 8px rgba(212, 146, 111, 0.04);
    margin: 0.5rem 0;
}

/* Data table styling - Subtle Warm Theme */
.stDataFrame {
    border-radius: 8px !important;
    overflow: hidden !important;
    box-shadow: 0 3px 10px rgba(212, 146, 111, 0.08) !important;
    border: 1px solid #f0e6d8 !important;
    background-color: #ffffff !important;
}

/* Streamlit specific styling fixes */
.stSelectbox > div > div {
    background-color: #fefefe !important;
    border: 1px solid #f0e6d8 !important;
    border-radius: 6px !important;
    color: #3d3530 !important;
}

.stNumberInput > div > div > input {
    background-color: #fefefe !important;
    border: 1px solid #f0e6d8 !important;
    border-radius: 6px !important;
    color: #3d3530 !important;
}

.stFileUploader > div {
    border: 2px dashed #e8ddd4 !important;
    border-radius: 10px !important;
    background-color: #fefefe !important;
    padding: 1rem !important;
}

.stExpander {
    border: 1px solid #f0e6d8 !important;
    border-radius: 8px !important;
    background-color: #fefefe !important;
}

.stExpander .streamlit-expanderHeader {
    background-color: #f9f6f3 !important;
    color: #3d3530 !important;
    border-bottom: 1px solid #f0e6d8 !important;
}

/* File uploader styling - Subtle Warm Theme */
.stFileUploader {
    border: 2px dashed #e8ddd4 !important;
    border-radius: 10px !important;
    padding: 2rem !important;
    text-align: center !important;
    background: linear-gradient(135deg, #fefefe 0%, #faf8f6 100%) !important;
}

.stFileUploader label {
    color: #3d3530 !important;
    font-weight: 600 !important;
}

/* Sidebar text styling */
.css-1d391kg .stSelectbox label {
    color: #3d3530 !important;
    font-weight: 600 !important;
}

/* Main content area text */
.main .stMarkdown {
    color: #3d3530 !important;
}

/* Warning and info messages */
.stAlert[data-baseweb="notification"] {
    background-color: #fef9f5 !important;
    border: 1px solid #f0d0a0 !important;
    color: #8b4513 !important;
}

/* Success messages */
.stSuccess {
    background-color: #f0f9f0 !important;
    border: 1px solid #90ee90 !important;
    color: #228b22 !important;
}

/* Error messages */
.stError {
    background-color: #fff5f5 !important;
    border: 1px solid #ffb3b3 !important;
    color: #dc143c !important;
}

/* Minimalist radio navigation */
.css-1d391kg .stRadio {
    margin-bottom: 2rem !important;
    position: relative !important;
    padding: 0.5rem !important;
}

.css-1d391kg .stRadio > div {
    background: transparent !important;
    padding: 0 !important;
    border: none !important;
    gap: 0.8rem !important;
    position: relative !important;
    z-index: 1 !important;
}

.css-1d391kg .stRadio > div > label {
    background: linear-gradient(135deg, #ffffff 0%, #faf9f7 100%) !important;
    border: 1px solid #e8ddd4 !important;
    border-radius: 10px !important;
    padding: 0.8rem 1.2rem !important;
    margin: 0.5rem 0 !important;
    color: #3d3530 !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    display: block !important;
    text-align: left !important;
    position: relative !important;
    padding-left: 2.5rem !important;
}

.css-1d391kg .stRadio > div > label:before {
    content: '' !important;
    position: absolute !important;
    left: 1rem !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    width: 8px !important;
    height: 8px !important;
    border-radius: 50% !important;
    background: #e0bfa8 !important;
    opacity: 0 !important;
    transition: all 0.2s ease !important;
}

.css-1d391kg .stRadio > div > label:hover {
    border-color: #d4b3a0 !important;
    background: linear-gradient(135deg, #ffffff 0%, #f8f5f2 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 8px rgba(212, 146, 111, 0.1) !important;
}

.css-1d391kg .stRadio > div > label[data-checked="true"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8f5f2 100%) !important;
    border-color: #c8a694 !important;
    border-left: 4px solid #c8a694 !important;
    color: #3d3530 !important;
    font-weight: 600 !important;
    box-shadow: 0 3px 12px rgba(212, 146, 111, 0.15) !important;
}

.css-1d391kg .stRadio > div > label[data-checked="true"]:before {
    opacity: 1 !important;
    background: #c8a694 !important;
}

/* Enhanced sidebar styling */
.css-1d391kg {
    padding: 1.5rem 1rem !important;
}

.stRadio label {
    color: #3d3530 !important;
    font-weight: 500 !important;
}

/* Subheader styling */
.stSubheader {
    color: #3d3530 !important;
    font-weight: 600 !important;
}

/* Text input styling */
.stTextInput > div > div > input {
    background-color: #fefefe !important;
    border: 1px solid #f0e6d8 !important;
    border-radius: 6px !important;
    color: #3d3530 !important;
}

/* Checkbox styling */
.stCheckbox > label {
    color: #3d3530 !important;
    font-weight: 500 !important;
}

.nav-item:hover {
    background: rgba(212, 146, 111, 0.1) !important;
}

/* Additional Streamlit component styling */
.stSlider {
    color: #3d3530 !important;
}

.stSlider > div > div {
    color: #3d3530 !important;
}

.stMetric {
    background-color: #fefefe !important;
    border: 1px solid #f0e6d8 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

.stMetric label {
    color: #3d3530 !important;
    font-weight: 600 !important;
}

.stMetric [data-testid="metric-container"] {
    background-color: #fefefe !important;
}

/* Info/Warning/Success message containers */
.stInfo {
    background-color: #f0f4ff !important;
    border: 1px solid #b3d1ff !important;
    color: #1e40af !important;
    border-radius: 8px !important;
}

.stWarning {
    background-color: #fef9f5 !important;
    border: 1px solid #f0d0a0 !important;
    color: #8b4513 !important;
    border-radius: 8px !important;
}

/* Sidebar specific overrides */
.css-1d391kg {
    background: linear-gradient(180deg, #fefefe 0%, #fbfaf8 100%) !important;
}

.css-1d391kg .stMarkdown {
    color: #3d3530 !important;
}

.css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4 {
    color: #3d3530 !important;
}

/* Table headers and cells */
thead th {
    background-color: #f9f6f3 !important;
    color: #3d3530 !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #e8ddd4 !important;
}

tbody td {
    color: #3d3530 !important;
    border-bottom: 1px solid #f0e6d8 !important;
}

/* Pagination styling */
.stPagination {
    color: #3d3530 !important;
}

.stPagination button {
    background-color: #fefefe !important;
    border: 1px solid #f0e6d8 !important;
    color: #3d3530 !important;
}

/* Download button styling */
.stDownloadButton > button {
    background: linear-gradient(45deg, #e0bfa8, #d4b3a0) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(212, 146, 111, 0.15) !important;
}
    border: 1px solid #f0e6d8 !important;
    box-shadow: 0 1px 3px rgba(212, 146, 111, 0.05) !important;
}

.stSelectbox > div > div > div {
    background-color: #ffffff !important;
    color: #3d3530 !important;
    border: 1px solid #f0e6d8 !important;
}

/* Additional global text styling - Force override all themes */
h1, h2, h3, h4, h5, h6 {
    color: #3d3530 !important;
}

p, div, span, label {
    color: #3d3530 !important;
}

/* Force text colors in dark mode */
@media (prefers-color-scheme: dark) {
    h1, h2, h3, h4, h5, h6 {
        color: #3d3530 !important;
    }
    
    p, div, span, label {
        color: #3d3530 !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%) !important;
        color: #3d3530 !important;
    }
    
    .main {
        background: transparent !important;
        color: #3d3530 !important;
    }
    
    body {
        background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%) !important;
        color: #3d3530 !important;
    }
}

/* Streamlit specific text elements */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: #3d3530 !important;
}

.stMarkdown p {
    color: #3d3530 !important;
}

/* Form elements */
.stForm {
    background-color: #fefefe !important;
    border: 1px solid #f0e6d8 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

/* Column headers and text */
.stColumn > div {
    color: #3d3530 !important;
}

/* Progress bar */
.stProgress {
    background-color: #f0e6d8 !important;
}

.stProgress > div > div {
    background-color: #e0bfa8 !important;
}

/* Tab styling */
.stTabs {
    color: #3d3530 !important;
}

.stTabs [data-baseweb="tab-list"] {
    background-color: #fefefe !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: #f9f6f3 !important;
    color: #3d3530 !important;
    border: 1px solid #f0e6d8 !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #e0bfa8 !important;
}

/* Code blocks */
.stCode {
    background-color: #f9f6f3 !important;
    border: 1px solid #f0e6d8 !important;
    color: #3d3530 !important;
}

/* Sidebar navigation improvements */
.css-1d391kg .element-container {
    color: #3d3530 !important;
}

.css-1d391kg .stRadio > label {
    color: #3d3530 !important;
    font-weight: 600 !important;
}

.css-1d391kg .stRadio [data-testid="stWidgetLabel"] {
    color: #3d3530 !important;
    font-weight: 600 !important;
}

/* Widget labels */
[data-testid="stWidgetLabel"] {
    color: #3d3530 !important;
    font-weight: 600 !important;
}

/* Caption text */
.caption {
    color: #8b7a6b !important;
}

/* Small text elements */
small {
    color: #8b7a6b !important;
}

/* Universal theme lock - Override ALL browser preferences */
@media (prefers-color-scheme: dark) {
    .stApp, .stApp > div, .main, body, html {
        background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%) !important;
        color: #3d3530 !important;
        color-scheme: light !important;
    }
    
    /* Force all Streamlit components in dark mode */
    .stSelectbox, .stTextInput, .stNumberInput, .stFileUploader, 
    .stExpander, .stDataFrame, .stMetric, .stAlert, .stForm,
    .stCheckbox, .stRadio, .stSlider, .stTabs {
        background-color: #fefefe !important;
        color: #3d3530 !important;
        border-color: #f0e6d8 !important;
    }
    
    /* Force all input elements */
    input, select, textarea, button:not(.stButton > button) {
        background-color: #fefefe !important;
        color: #3d3530 !important;
        border-color: #f0e6d8 !important;
    }
    
    /* Sidebar dark mode override */
    [data-testid="stSidebar"], .css-1d391kg {
        background: linear-gradient(180deg, #fefefe 0%, #fbfaf8 100%) !important;
        color: #3d3530 !important;
    }
    
    /* All text elements in dark mode */
    * {
        color: #3d3530 !important;
    }
    
    /* Override any dark theme variables */
    :root {
        --background-color: #fefefe !important;
        --text-color: #3d3530 !important;
        --border-color: #f0e6d8 !important;
    }
}

/* Force light mode styling regardless of system preference */
.stApp * {
    color-scheme: light !important;
}

/* Override Streamlit's default theme detection */
.stApp[data-theme="dark"] {
    background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%) !important;
    color: #3d3530 !important;
}

.stApp[data-theme="light"] {
    background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%) !important;
    color: #3d3530 !important;
}

/* Force override any auto-detected theme */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #fefefe 0%, #faf9f7 100%) !important;
    color: #3d3530 !important;
}

/* Complete theme lock */
*, *::before, *::after {
    color-scheme: light !important;
}

/* Multiselect - Subtle Warm Theme */
.stMultiSelect > div > div > div {
    background-color: #ffffff;
    color: #2d2926;
    border: 1px solid #f0e6d8;
}

/* Radio buttons - Subtle Warm Theme */
.stRadio > div {
    color: #2d2926;
}

/* Expander - Subtle Warm Theme */
.streamlit-expanderHeader {
    background-color: #fefaf7;
    color: #2d2926;
    border: 1px solid #f0e6d8;
}

.streamlit-expanderContent {
    background-color: #ffffff;
    border: 1px solid #f0e6d8;
}

/* Tabs - Subtle Warm Theme */
.stTabs [data-baseweb="tab-list"] {
    background-color: #fefaf7;
}

.stTabs [data-baseweb="tab"] {
    color: #8b7a6b;
    background-color: #fefaf7;
}

.stTabs [aria-selected="true"] {
    color: #d4926f !important;
    background-color: #ffffff !important;
    border-bottom: 2px solid #d4926f !important;
}

/* Sidebar text - Subtle Warm Theme */
.css-1d391kg {
    color: #2d2926;
}

.css-1d391kg .stMarkdown {
    color: #2d2926;
}

.css-1d391kg .stSelectbox label {
    color: #2d2926 !important;
}

/* Enhanced table styling - Subtle Warm Theme */
.enhanced-table {
    font-size: 14px;
    background-color: #ffffff;
    color: #2d2926;
}

.enhanced-table td {
    border-bottom: 1px solid #f0e6d8;
    padding: 0.5rem;
    background-color: #ffffff;
    color: #2d2926;
}

.enhanced-table th {
    background: linear-gradient(45deg, #d4926f, #c8956e);
    color: white;
    font-weight: 600;
}

/* Success messages - Subtle Warm Theme */
.stSuccess {
    background-color: #f0fdf4 !important;
    color: #166534 !important;
    border: 1px solid #22c55e !important;
}

/* Warning messages - Subtle Warm Theme */
.stWarning {
    background-color: #fefce8 !important;
    color: #a16207 !important;
    border: 1px solid #eab308 !important;
}

/* Error messages - Subtle Warm Theme */
.stError {
    background-color: #fef2f2 !important;
    color: #dc2626 !important;
    border: 1px solid #ef4444 !important;
}

/* Info messages - Subtle Warm Theme */
.stInfo {
    background-color: #f0f9ff !important;
    color: #0369a1 !important;
    border: 1px solid #3b82f6 !important;
}

/* Additional subtle warm accents */
.stMetric {
    background: linear-gradient(135deg, #ffffff 0%, #fefaf7 100%);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 6px rgba(212, 146, 111, 0.08);
}

/* Subtle warm gradient backgrounds for sections */
.warm-section {
    background: linear-gradient(135deg, #fefaf7 0%, #f5f1ec 100%);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 3px 10px rgba(212, 146, 111, 0.08);
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

# Initialize session state for page navigation without scroll reset
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Upload & Process"

# JavaScript to prevent scroll reset when switching pages - more robust approach
scroll_js = """
<script>
// Function to get a unique identifier for the current page state
function getPageIdentifier() {
    // Get the current URL path and query parameters
    const path = window.location.pathname;
    const search = window.location.search;
    
    // Get the active tab/page from the DOM
    const activeRadioLabel = document.querySelector('[data-testid="stRadio"] [data-checked="true"]');
    const activePage = activeRadioLabel ? activeRadioLabel.textContent.trim() : '';
    
    // Combine for a unique identifier
    return `${path}${search}_${activePage}`;
}

// Function to save scroll position
function saveScrollPosition() {
    const pageId = getPageIdentifier();
    const scrollPosition = window.scrollY;
    sessionStorage.setItem('scrollPos_' + pageId, scrollPosition.toString());
    console.log('Saved scroll position', pageId, scrollPosition);
}

// Function to restore scroll position
function restoreScrollPosition() {
    const pageId = getPageIdentifier();
    const savedPosition = sessionStorage.getItem('scrollPos_' + pageId);
    
    if (savedPosition) {
        console.log('Restoring scroll to', pageId, savedPosition);
        // Use multiple attempts to ensure it works even after dynamic content loads
        window.scrollTo(0, parseInt(savedPosition));
        
        // Try again after short delays to handle dynamic content
        setTimeout(() => window.scrollTo(0, parseInt(savedPosition)), 100);
        setTimeout(() => window.scrollTo(0, parseInt(savedPosition)), 300);
        setTimeout(() => window.scrollTo(0, parseInt(savedPosition)), 500);
        setTimeout(() => window.scrollTo(0, parseInt(savedPosition)), 1000);
    }
}

// Save position when user scrolls
window.addEventListener('scroll', function() {
    // Use debounce to avoid excessive saves
    clearTimeout(window.scrollSaveTimeout);
    window.scrollSaveTimeout = setTimeout(saveScrollPosition, 100);
});

// Save position before page changes
window.addEventListener('beforeunload', saveScrollPosition);

// Restore position when page loads
window.addEventListener('DOMContentLoaded', function() {
    // Wait a moment for Streamlit to render content
    setTimeout(restoreScrollPosition, 200);
});

// Also watch for Streamlit's own events that might indicate content changes
document.addEventListener('DOMNodeInserted', function(e) {
    if (e.target.tagName === 'IFRAME' || e.target.tagName === 'DIV') {
        // Content might be changing, try to restore scroll again
        setTimeout(restoreScrollPosition, 300);
    }
});

// Force scroll restoration after the page is fully loaded
window.addEventListener('load', function() {
    setTimeout(restoreScrollPosition, 300);
});
</script>
"""



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
        
        # Database actions - styled like other status indicators
        st.sidebar.markdown(f"""
        <div style="background-color: #ffffff; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; box-shadow: 0 1px 4px rgba(212, 146, 111, 0.06); display: flex; align-items: center;">
            <span style="color: #3d3530; margin-right: 0.5rem;">🌐</span>
            <a href="{manager.base_url}" target="_blank" style="color: #3d3530; text-decoration: none; font-weight: 500; flex-grow: 1;">Open Database</a>
        </div>
        """, unsafe_allow_html=True)
        
        # Show configuration status
        config_exists = manager.config_file.exists()
        if config_exists:
            st.sidebar.info("⚙️ Configured")
        else:
            st.sidebar.warning("⚙️ Setup Required")

def main():
    # Inject JavaScript for scroll position preservation
    st.markdown(scroll_js, unsafe_allow_html=True)
    
    # Add sidebar title and styling
    st.sidebar.markdown("""
    <div style="padding: 1rem 0.5rem; margin-bottom: 1rem; border-bottom: 2px solid #e8ddd4;">
        <h3 style="color: #3d3530; margin: 0; font-size: 1.2rem; font-weight: 600;">📊 Navigation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    page = st.sidebar.radio(
        "",
        ["Upload & Process", "Header Mapping", "Master Sheet", "Analytics"],
        label_visibility="collapsed",
        key="page_navigation"
    )
    
    # Update current page in session state
    st.session_state.current_page = page
    
    # Embedded database sidebar
    embedded_database_sidebar()
    
    # Render the selected page
    if page == "Upload & Process":
        upload_and_process_page()
    elif page == "Header Mapping":
        header_mapping_page()
    elif page == "Master Sheet":
        master_sheet_page()
    elif page == "Analytics":
        analytics_page()



def upload_and_process_page():
    # Show main header only on first page
    st.markdown("""
    <div class="main-header">
        <h1>📊 Spreadsheet Consolidator</h1>
        <p>Transform multiple spreadsheets into unified, standardized data with intelligent header mapping</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: #b8956e; margin-top: 0;">📁 Upload & Process Files</h2>
        <p style="color: #8b7a6b; margin-bottom: 0;">Start by uploading your spreadsheet files. Supported formats: CSV, Excel (.xlsx, .xls)</p>
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
        <div style="background: linear-gradient(45deg, #e8ddd4, #f0e6d8); padding: 1rem; border-radius: 8px; margin: 1rem 0; box-shadow: 0 2px 6px rgba(212, 146, 111, 0.08); border: 1px solid #f5f0eb;">
            <h4 style="color: #3d3530; margin: 0;">✨ Successfully uploaded {len(uploaded_files)} files</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display uploaded files in a beautiful card
        with st.expander("📋 View Uploaded Files", expanded=True):
            for file in uploaded_files:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffffff 0%, #fefcfa 100%); padding: 0.8rem; border-radius: 6px; margin: 0.5rem 0; border-left: 3px solid #e8ddd4; color: #3d3530; box-shadow: 0 1px 4px rgba(212, 146, 111, 0.06);">
                    <strong>📄 {file.name}</strong><br>
                    <small style="color: #8b7a6b;">Size: {file.size:,} bytes</small>
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
                        <h3 style="color: #b8956e; margin: 0 0 0.5rem 0;">{result['file_count']}</h3>
                        <p style="margin: 0; color: #8b7a6b;">Files Processed</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h3 style="color: #b8956e; margin: 0 0 0.5rem 0;">{result['total_sheets']}</h3>
                        <p style="margin: 0; color: #8b7a6b;">Total Sheets</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h3 style="color: #b8956e; margin: 0 0 0.5rem 0;">{len(result['headers'])}</h3>
                        <p style="margin: 0; color: #8b7a6b;">Unique Headers</p>
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
        <h2 style="color: #b8956e; margin-top: 0;">🔧 Header Mapping Configuration</h2>
        <p style="color: #8b7a6b; margin-bottom: 0;">Review and adjust header mappings to standardize your data columns</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.processed:
        st.warning("⚠️ Please upload and process files first.")
        return
    
    # Show automatic mappings
    headers = st.session_state.headers
    auto_mappings = st.session_state.auto_mappings
    
    # Create mapping interface without redundant title
    
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
                # Start index from 1 instead of 0
                df_mapping.index = df_mapping.index + 1
                st.dataframe(df_mapping, use_container_width=True)
            
            st.info("👉 Go to 'Master Sheet' to consolidate your data.")


# Export dialog has been removed in favor of direct export
def master_sheet_page():
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: #b8956e; margin-top: 0;">📋 Unified Master Sheet</h2>
        <p style="color: #8b7a6b; margin-bottom: 0;">View, filter, and export your consolidated data</p>
    </div>
    """, unsafe_allow_html=True)

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
        
        # Show summary metrics
        st.subheader("📊 Data Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: #b8956e; margin: 0 0 0.5rem 0;">{summary['total_rows']:,}</h2>
                <p style="margin: 0; color: #8b7a6b; font-weight: 600;">Total Rows</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: #b8956e; margin: 0 0 0.5rem 0;">{summary['total_columns']}</h2>
                <p style="margin: 0; color: #8b7a6b; font-weight: 600;">Total Columns</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: #b8956e; margin: 0 0 0.5rem 0;">{summary['source_files']}</h2>
                <p style="margin: 0; color: #8b7a6b; font-weight: 600;">Source Files</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: #b8956e; margin: 0 0 0.5rem 0;">{summary['source_sheets']}</h2>
                <p style="margin: 0; color: #8b7a6b; font-weight: 600;">Source Sheets</p>
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
        
        # Display data
        st.subheader("📋 Data Preview")
        st.info(f"Showing all {len(filtered_data)} rows")
        
        # Data table view - show all data without restrictions and start index from 1
        st.markdown("**Data Table View:**")
        # Reset index to start from 1 instead of 0
        display_data = filtered_data.copy()
        display_data.index = display_data.index + 1
        st.dataframe(display_data, use_container_width=True, height=600)
        
        # Export section
        st.markdown("<div style='margin: 2rem 0 1rem 0;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Download as Excel", type="secondary"):
                # Use display_data to ensure the order is preserved exactly as shown in the preview
                export_data = filtered_data.copy().reset_index(drop=True)
                excel_data = st.session_state.consolidator.export_data(export_data, 'xlsx')
                st.download_button(
                    label="📥 Download Excel File",
                    data=excel_data,
                    file_name="consolidated_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            if st.button("📝 Download as CSV", type="secondary"):
                # Use filtered_data to ensure the order is preserved exactly as shown in the preview
                export_data = filtered_data.copy().reset_index(drop=True)
                csv_data = st.session_state.consolidator.export_data(export_data, 'csv')
                st.download_button(
                    label="📥 Download CSV File",
                    data=csv_data,
                    file_name="consolidated_data.csv",
                    mime="text/csv"
                )
        
        with col3:
            # Database export to your specific table - direct export without preview
            # Ensure data is exported in the exact same order as shown in the preview
            if st.button("🗑️ Export to Baserow Database", type="primary"):
                if len(filtered_data) > 0:
                    manager = st.session_state.baserow_manager
                    # Direct API export to Baserow without showing preview
                    # Use display_data to ensure the order is preserved exactly as shown in the preview
                    with st.spinner(f"Exporting {len(filtered_data)} rows to Baserow..."):
                        # Reset index to ensure it's exported in the exact same order as displayed
                        export_data = filtered_data.copy().reset_index(drop=True)
                        success = manager.export_data(export_data, clear_existing=False)
                    
                    if success:
                        st.success(f"✅ Successfully exported {len(filtered_data)} rows to Table {manager.table_id}!")
                        st.info(f"🔗 View your data: [Table {manager.table_id}]({manager.base_url}/database/174/table/{manager.table_id})")
                    else:
                        st.error("❌ Export failed. Check your Baserow connection and API token.")
                        st.info(f"🔗 Verify table access: [Table {manager.table_id}]({manager.base_url}/database/174/table/{manager.table_id})")
                        st.info("💡 **Tip**: Ensure your API token has create/update permissions for this table.")
                else:
                    st.error("❌ No data to export")

def analytics_page():
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: #b8956e; margin-top: 0;">📊 Data Analytics</h2>
        <p style="color: #8b7a6b; margin-bottom: 0;">Explore insights and statistics from your consolidated data</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.consolidated:
        st.warning("⚠️ Please consolidate data first.")
        return
    
    master_data = st.session_state.master_data
    
    # Data quality overview with warm theme styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0e3d6 0%, #e8ddd4 100%); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border: 1px solid #f0e6d8; box-shadow: 0 2px 8px rgba(212, 146, 111, 0.1);">
        <h3 style="color: #3d3530; margin: 0; text-align: center;">🔍 Data Quality Analysis</h3>
        <p style="color: #8b7a6b; margin: 0.5rem 0 0 0; text-align: center;">Comprehensive overview of your data completeness</p>
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
    
    # Visualize data completeness with warm theme colors
    fig = px.bar(
        completeness_df,
        x='Column',
        y='Completeness (%)',
        title='Data Completeness by Column',
        color='Completeness (%)',
        color_continuous_scale=['#e8ddd4', '#d4b3a0', '#b8956e']
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Show completeness table with index starting from 1
    completeness_display = completeness_df.copy()
    completeness_display.index = completeness_display.index + 1
    st.dataframe(completeness_display, use_container_width=True)
    
    # Source file distribution with warm theme styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0e3d6 0%, #e8ddd4 100%); padding: 1.5rem; border-radius: 12px; margin: 2rem 0 1rem 0; border: 1px solid #f0e6d8; box-shadow: 0 2px 8px rgba(212, 146, 111, 0.1);">
        <h3 style="color: #3d3530; margin: 0 0 1rem 0; text-align: center;">📈 Source File Distribution</h3>
        <p style="color: #8b7a6b; margin: 0; text-align: center;">Visualize how your data is distributed across source files</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File distribution with warm theme colors - centered, no second pie chart
    file_counts = master_data['source_file'].value_counts()
    fig_files = px.pie(
        values=file_counts.values,
        names=file_counts.index,
        title="Records by Source File",
        color_discrete_sequence=['#e8ddd4', '#d4b3a0', '#b8956e', '#c8a694', '#e0bfa8']
    )
    # Make the chart a bit larger and centered
    fig_files.update_layout(height=500, width=700, margin=dict(l=50, r=50, t=80, b=50))
    st.plotly_chart(fig_files, use_container_width=True)
    
    # Column statistics with warm theme styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0e3d6 0%, #e8ddd4 100%); padding: 1.5rem; border-radius: 12px; margin: 2rem 0 1rem 0; border: 1px solid #f0e6d8; box-shadow: 0 2px 8px rgba(212, 146, 111, 0.1);">
        <h3 style="color: #3d3530; margin: 0 0 1rem 0; text-align: center;">📋 Detailed Column Analysis</h3>
        <p style="color: #8b7a6b; margin: 0; text-align: center;">Deep dive into individual column statistics</p>
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
            
            # Create histogram for numeric data with warm theme colors
            numeric_data = pd.to_numeric(master_data[selected_column], errors='coerce').dropna()
            fig_hist = px.histogram(
                x=numeric_data,
                nbins=30,
                title=f"Distribution of {selected_column}",
                color_discrete_sequence=['#b8956e'],
                opacity=0.8
            )
            fig_hist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#3d3530'
            )
            st.plotly_chart(fig_hist, use_container_width=True)


if __name__ == "__main__":
    main()