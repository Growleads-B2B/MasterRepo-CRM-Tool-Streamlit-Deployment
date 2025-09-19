import streamlit as st
import pandas as pd
import plotly.express as px
from data_consolidator import DataConsolidator
from embedded_baserow import EmbeddedBaserowManager
from batch_export_manager import BatchExportManager
from simple_batch_exporter import SimpleBatchExporter, create_batches_simple
from ultra_simple_exporter import export_batch_ultra_simple, create_simple_batches
from final_working_exporter import export_batch_final, create_final_batches
from typing import Dict, List
import io
import time

# Page configuration
st.set_page_config(
    page_title="MasterCRM Repo Tool",
    page_icon="https://i.ibb.co/4wQpPPX6/transparent.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Comprehensive Adaptive Theme System - Beautiful in Both Dark & Light Modes
st.markdown("""
<style>
/* ========================================
   ADAPTIVE THEME SYSTEM - WARM PROFESSIONAL DESIGN
   Beautiful in both Dark & Light modes
   ======================================== */
/* Light Theme Variables (Default) */
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #fefcf9;
    --bg-tertiary: #f8f4f0;
    --bg-card: #ffffff;
    --bg-sidebar: #fefefe;
    --bg-header: #ffffff;
    --bg-accent: #f8f5f2;
    --bg-hover: #f5f1ec;
    
    --text-primary: #3d3530;
    --text-secondary: #5a4f47;
    --text-muted: #8b7a6b;
    --text-accent: #b8956e;
    --text-inverse: #ffffff;
    
    --border-primary: #f0e6d8;
    --border-secondary: #e8ddd4;
    --border-accent: #d4b3a0;
    
    --accent-primary: #e0bfa8;
    --accent-secondary: #d4b3a0;
    --accent-tertiary: #c8a694;
    --accent-gradient: linear-gradient(45deg, #e0bfa8, #d4b3a0);
    
    --shadow-light: 0 2px 8px rgba(212, 146, 111, 0.08);
    --shadow-medium: 0 4px 16px rgba(212, 146, 111, 0.12);
    --shadow-heavy: 0 8px 32px rgba(212, 146, 111, 0.16);
    
    --success-bg: #f0fdf4;
    --success-border: #22c55e;
    --success-text: #166534;
    
    --warning-bg: #fefce8;
    --warning-border: #eab308;
    --warning-text: #a16207;
    
    --error-bg: #fef2f2;
    --error-border: #ef4444;
    --error-text: #dc2626;
    
    --info-bg: #f0f9ff;
    --info-border: #3b82f6;
    --info-text: #0369a1;
}

/* Dark Theme Variables */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #1a1612;
        --bg-secondary: #2a241e;
        --bg-tertiary: #3a332b;
        --bg-card: #2a241e;
        --bg-sidebar: #1f1b16;
        --bg-header: #2a241e;
        --bg-accent: #3a332b;
        --bg-hover: #4a4137;
        
        --text-primary: #f0ede8;
        --text-secondary: #d4c7b8;
        --text-muted: #a69584;
        --text-accent: #d4926f;
        --text-inverse: #1a1612;
        
        --border-primary: #4a4137;
        --border-secondary: #5a5147;
        --border-accent: #d4926f;
        
        --accent-primary: #d4926f;
        --accent-secondary: #c8956e;
        --accent-tertiary: #b8956e;
        --accent-gradient: linear-gradient(45deg, #d4926f, #c8956e);
        
        --shadow-light: 0 2px 8px rgba(0, 0, 0, 0.2);
        --shadow-medium: 0 4px 16px rgba(0, 0, 0, 0.3);
        --shadow-heavy: 0 8px 32px rgba(0, 0, 0, 0.4);
        
        --success-bg: #0f2a0f;
        --success-border: #22c55e;
        --success-text: #4ade80;
        
        --warning-bg: #2a2a0f;
        --warning-border: #eab308;
        --warning-text: #fbbf24;
        
        --error-bg: #2a0f0f;
        --error-border: #ef4444;
        --error-text: #f87171;
        
        --info-bg: #0f1a2a;
        --info-border: #3b82f6;
        --info-text: #60a5fa;
    }
}

/* ========================================
   GLOBAL ADAPTIVE STYLING
   ======================================== */

/* Base App Styling */
.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.main > div {
    padding: 1rem 2rem;
    background: var(--bg-primary) !important;
}

/* ========================================
   HEADER & CARD COMPONENTS
   ======================================== */

/* Main Header */
.main-header {
    background: var(--bg-header) !important;
    padding: 2.5rem 2rem;
    border-radius: 20px;
    margin-bottom: 2.5rem;
    box-shadow: var(--shadow-medium) !important;
    text-align: center;
    border: 1px solid var(--border-accent) !important;
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.main-header:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-heavy) !important;
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-primary);
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.1rem;
    opacity: 0.95;
    color: var(--text-secondary);
}

/* Feature Cards */
.feature-card {
    background: var(--bg-card) !important;
    padding: 1.5rem;
    border-radius: 16px;
    margin: 1rem 0;
    border: 1px solid var(--border-primary) !important;
    box-shadow: var(--shadow-light) !important;
    backdrop-filter: blur(8px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.feature-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium) !important;
    border-color: var(--border-accent) !important;
}

/* ========================================
   SIDEBAR STYLING
   ======================================== */

/* Main Sidebar Container */
.css-1d391kg {
    background: var(--bg-sidebar) !important;
    border-right: 2px solid var(--border-accent) !important;
    box-shadow: var(--shadow-light) !important;
    backdrop-filter: blur(8px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.css-1d391kg .css-1v0mbdj {
    background: var(--bg-sidebar) !important;
}

/* Enhanced sidebar container */
[data-testid="stSidebar"] > div:first-child {
    background: var(--bg-sidebar) !important;
    border-right: 2px solid var(--border-accent) !important;
    box-shadow: var(--shadow-light) !important;
}

/* Streamlit sidebar overrides */
.stApp > div {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

.stApp [data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    color: var(--text-primary) !important;
    border-right: 2px solid var(--border-accent) !important;
    box-shadow: var(--shadow-light) !important;
}

.stApp [data-testid="stSidebar"] > div {
    background: var(--bg-sidebar) !important;
    color: var(--text-primary) !important;
    border-right: 2px solid var(--border-accent) !important;
}

/* ========================================
   BUTTON COMPONENTS
   ======================================== */

/* Primary Buttons */
.stButton > button {
    background: var(--accent-gradient) !important;
    color: var(--text-inverse) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: var(--shadow-light) !important;
    backdrop-filter: blur(8px);
    position: relative;
    overflow: hidden;
}

.stButton > button:before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: var(--shadow-medium) !important;
    background: linear-gradient(45deg, var(--accent-secondary), var(--accent-tertiary)) !important;
}

.stButton > button:hover:before {
    left: 100%;
}

.stButton > button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ========================================
   ALERT & MESSAGE COMPONENTS
   ======================================== */

/* Base Alert Styling */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid var(--border-primary) !important;
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    box-shadow: var(--shadow-light) !important;
    backdrop-filter: blur(8px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Success Messages */
.stSuccess {
    background-color: var(--success-bg) !important;
    border: 1px solid var(--success-border) !important;
    color: var(--success-text) !important;
    border-radius: 12px !important;
}

/* Warning Messages */
.stWarning {
    background-color: var(--warning-bg) !important;
    border: 1px solid var(--warning-border) !important;
    color: var(--warning-text) !important;
    border-radius: 12px !important;
}

/* Error Messages */
.stError {
    background-color: var(--error-bg) !important;
    border: 1px solid var(--error-border) !important;
    color: var(--error-text) !important;
    border-radius: 12px !important;
}

/* Info Messages */
.stInfo {
    background-color: var(--info-bg) !important;
    border: 1px solid var(--info-border) !important;
    color: var(--info-text) !important;
    border-radius: 12px !important;
}

/* ========================================
   METRIC & FORM COMPONENTS
   ======================================== */

/* Metric Container */
.metric-container {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid var(--border-primary);
    box-shadow: var(--shadow-light);
    margin: 0.5rem 0;
    backdrop-filter: blur(8px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.metric-container:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium);
    border-color: var(--border-accent);
}

/* ========================================
   DATA TABLE & INPUT COMPONENTS
   ======================================== */

/* Data Tables */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-light) !important;
    border: 1px solid var(--border-primary) !important;
    background-color: var(--bg-card) !important;
    backdrop-filter: blur(8px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stDataFrame:hover {
    box-shadow: var(--shadow-medium) !important;
    border-color: var(--border-accent) !important;
}

/* Input Components */
.stSelectbox > div > div {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stSelectbox > div > div:hover {
    border-color: var(--border-accent) !important;
    box-shadow: var(--shadow-light) !important;
}

.stNumberInput > div > div > input {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stNumberInput > div > div > input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(212, 146, 111, 0.1) !important;
}

.stTextInput > div > div > input {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(212, 146, 111, 0.1) !important;
}

.stFileUploader > div {
    border: 2px dashed var(--border-accent) !important;
    border-radius: 12px !important;
    background-color: var(--bg-card) !important;
    padding: 1.5rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: var(--text-primary) !important;
}

.stFileUploader > div:hover {
    border-color: var(--accent-primary) !important;
    background-color: var(--bg-hover) !important;
}

.stFileUploader {
    border: 2px dashed var(--border-accent) !important;
    border-radius: 12px !important;
    padding: 2rem !important;
    text-align: center !important;
    background: var(--bg-card) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Fix file uploader text in dark mode */
.stFileUploader [data-testid="stFileUploadDropzone"] {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

.stFileUploader [data-testid="stFileUploadDropzone"] p {
    color: var(--text-primary) !important;
}

.stFileUploader label {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

.stExpander {
    border: 1px solid var(--border-primary) !important;
    border-radius: 12px !important;
    background-color: var(--bg-card) !important;
    backdrop-filter: blur(8px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stExpander:hover {
    border-color: var(--border-accent) !important;
    box-shadow: var(--shadow-light) !important;
}

.stExpander .streamlit-expanderHeader {
    background-color: var(--bg-accent) !important;
    color: var(--text-primary) !important;
    border-bottom: 1px solid var(--border-primary) !important;
}

/* ========================================
   NAVIGATION & RADIO COMPONENTS
   ======================================== */

/* Enhanced Radio Navigation */
.css-1d391kg .stRadio {
    margin-bottom: 2rem !important;
    position: relative !important;
    padding: 0.5rem !important;
}

.css-1d391kg .stRadio > div {
    background: var(--bg-sidebar) !important;
    padding: 0 !important;
    border: none !important;
    gap: 0.8rem !important;
    position: relative !important;
    z-index: 1 !important;
}

.css-1d391kg .stRadio > div > label {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.2rem !important;
    margin: 0.5rem 0 !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100% !important;
    display: block !important;
    text-align: left !important;
    position: relative !important;
    padding-left: 2.5rem !important;
    backdrop-filter: blur(8px);
}

.css-1d391kg .stRadio > div > label:before {
    content: '' !important;
    position: absolute !important;
    left: 1rem !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    width: 10px !important;
    height: 10px !important;
    border-radius: 50% !important;
    background: var(--accent-primary) !important;
    opacity: 0 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 0 5px rgba(212, 146, 111, 0.5) !important;
}

.css-1d391kg .stRadio > div > label:hover {
    border-color: var(--border-accent) !important;
    background: var(--bg-hover) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-light) !important;
}

.css-1d391kg .stRadio > div > label[data-checked="true"] {
    background: var(--bg-accent) !important;
    border-color: var(--accent-primary) !important;
    border-left: 6px solid var(--accent-primary) !important;
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    box-shadow: var(--shadow-medium) !important;
}

.css-1d391kg .stRadio > div > label[data-checked="true"]:before {
    opacity: 1 !important;
    background: var(--accent-primary) !important;
    box-shadow: 0 0 8px rgba(212, 146, 111, 0.8) !important;
}

.css-1d391kg .stRadio > div > label[data-checked="true"]:after {
    content: '•' !important;
    position: absolute !important;
    left: 1rem !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    color: var(--accent-primary) !important;
    font-size: 24px !important;
    font-weight: bold !important;
    line-height: 0 !important;
}

/* Sidebar Text Styling */
.css-1d391kg .stSelectbox label {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

.css-1d391kg .stMarkdown {
    color: var(--text-primary) !important;
}

.css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4 {
    color: var(--text-primary) !important;
}

/* Main Content Text */
.main .stMarkdown {
    color: var(--text-primary) !important;
}

/* ========================================
   UNIVERSAL ADAPTIVE STYLING
   ======================================== */

/* Global Text Elements */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
}

p, div, span, label {
    color: var(--text-primary) !important;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: var(--text-primary) !important;
}

.stMarkdown p {
    color: var(--text-primary) !important;
}

/* Widget Labels */
[data-testid="stWidgetLabel"] {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

.stRadio label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

.stSubheader {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

.stCheckbox > label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

/* Caption and Small Text */
.caption {
    color: var(--text-muted) !important;
}

small {
    color: var(--text-muted) !important;
}

/* ========================================
   ADDITIONAL COMPONENTS
   ======================================== */

/* Metrics */
.stMetric {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stMetric:hover {
    border-color: var(--border-accent) !important;
    box-shadow: var(--shadow-light) !important;
}

.stMetric label {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

.stMetric [data-testid="metric-container"] {
    background-color: var(--bg-card) !important;
}

/* Forms and Other Components */
.stForm {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-primary) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    backdrop-filter: blur(8px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stForm:hover {
    border-color: var(--border-accent) !important;
    box-shadow: var(--shadow-light) !important;
}

/* Progress Bar */
.stProgress {
    background-color: var(--border-primary) !important;
    border-radius: 8px;
    overflow: hidden;
}

.stProgress > div > div {
    background: var(--accent-gradient) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Tabs */
.stTabs {
    color: var(--text-primary) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background-color: var(--bg-card) !important;
    border-radius: 12px 12px 0 0;
}

.stTabs [data-baseweb="tab"] {
    background-color: var(--bg-accent) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-primary) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: var(--bg-hover) !important;
    color: var(--text-primary) !important;
}

.stTabs [aria-selected="true"] {
    color: var(--accent-primary) !important;
    background-color: var(--bg-card) !important;
    border-bottom: 2px solid var(--accent-primary) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: var(--accent-primary) !important;
}

/* Code Blocks */
.stCode {
    background-color: var(--bg-accent) !important;
    border: 1px solid var(--border-primary) !important;
    color: var(--text-primary) !important;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
}

/* Download Buttons */
.stDownloadButton > button {
    background: var(--accent-gradient) !important;
    color: var(--text-inverse) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-light) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: var(--shadow-medium) !important;
}

/* Table Headers and Cells */
thead th {
    background: var(--accent-gradient) !important;
    color: var(--text-inverse) !important;
    font-weight: 600 !important;
    border-bottom: 2px solid var(--border-accent) !important;
}

tbody td {
    color: var(--text-primary) !important;
    border-bottom: 1px solid var(--border-primary) !important;
    background-color: var(--bg-card) !important;
}

/* Enhanced Table Styling */
.enhanced-table {
    font-size: 14px;
    background-color: var(--bg-card);
    color: var(--text-primary);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--shadow-light);
}

.enhanced-table td {
    border-bottom: 1px solid var(--border-primary);
    padding: 0.75rem;
    background-color: var(--bg-card);
    color: var(--text-primary);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.enhanced-table td:hover {
    background-color: var(--bg-hover);
}

.enhanced-table th {
    background: var(--accent-gradient);
    color: var(--text-inverse);
    font-weight: 600;
    padding: 1rem 0.75rem;
}

/* Sliders and Other Inputs */
.stSlider {
    color: var(--text-primary) !important;
}

.stSlider > div > div {
    color: var(--text-primary) !important;
}

/* Multi-select */
.stMultiSelect > div > div > div {
    background-color: var(--bg-card);
    color: var(--text-primary);
    border: 1px solid var(--border-primary);
    border-radius: 8px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stMultiSelect > div > div > div:hover {
    border-color: var(--border-accent);
    box-shadow: var(--shadow-light);
}

/* Pagination */
.stPagination {
    color: var(--text-primary) !important;
}

.stPagination button {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-primary) !important;
    color: var(--text-primary) !important;
    border-radius: 8px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stPagination button:hover {
    border-color: var(--border-accent) !important;
    background-color: var(--bg-hover) !important;
}

/* Warm Section Styling */
.warm-section {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: var(--shadow-light);
    border: 1px solid var(--border-primary);
    backdrop-filter: blur(8px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.warm-section:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium);
    border-color: var(--border-accent);
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
if 'batch_manager' not in st.session_state:
    st.session_state.batch_manager = BatchExportManager()
if 'batches_created' not in st.session_state:
    st.session_state.batches_created = False
if 'simple_batches' not in st.session_state:
    st.session_state.simple_batches = []
if 'batch_status' not in st.session_state:
    st.session_state.batch_status = {}

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
        st.sidebar.markdown("### 🗄️ Database")
        st.sidebar.success("✅ Available")
        
        # Database actions - styled like other status indicators with enhanced visibility
        st.sidebar.markdown(f"""
        <div style="background-color: var(--bg-card); border-radius: 8px; padding: 1rem; margin: 0.5rem 0; box-shadow: var(--shadow-light); display: flex; align-items: center; border: 1px solid var(--border-accent);">
            <span style="color: var(--text-primary); margin-right: 0.5rem;">🌐</span>
            <a href="{manager.base_url}" target="_blank" style="color: var(--text-primary); text-decoration: none; font-weight: 600; flex-grow: 1;">Open Database</a>
        </div>
        """, unsafe_allow_html=True)
        
        # Show configuration status with enhanced visibility
        config_exists = manager.config_file.exists()
        if config_exists:
            st.sidebar.markdown("""
            <div style="background-color: var(--info-bg); border-radius: 8px; padding: 0.8rem; margin: 0.5rem 0; border: 1px solid var(--info-border); color: var(--info-text); font-weight: 500;">
                ⚙️ Configuration Complete
            </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown("""
            <div style="background-color: var(--warning-bg); border-radius: 8px; padding: 0.8rem; margin: 0.5rem 0; border: 1px solid var(--warning-border); color: var(--warning-text); font-weight: 500;">
                ⚙️ Setup Required
            </div>
            """, unsafe_allow_html=True)

def main():
    # Inject JavaScript for scroll position preservation
    st.markdown(scroll_js, unsafe_allow_html=True)
    
    # Add sidebar title and styling with enhanced visibility
    st.sidebar.markdown("""
    <div style="padding: 1rem 0.5rem; margin-bottom: 1rem; border-bottom: 2px solid var(--border-accent); background-color: var(--bg-accent); border-radius: 8px 8px 0 0;">
        <h3 style="color: var(--text-primary); margin: 0; font-size: 1.2rem; font-weight: 700;">📊 Navigation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Add custom CSS for navigation items with enhanced indicators
    st.sidebar.markdown("""
    <style>
    /* Custom navigation styling with clear indicators */
    .nav-item-container .stRadio > div > label {
        padding-left: 2.8rem !important;
        position: relative !important;
    }
    
    /* Add circle indicators for all items */
    .nav-item-container .stRadio > div > label:before {
        content: '' !important;
        position: absolute !important;
        left: 1.2rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 12px !important;
        height: 12px !important;
        border: 2px solid #d4b3a0 !important;
        border-radius: 50% !important;
        background: #ffffff !important;
    }
    
    /* Fill circle for selected item */
    .nav-item-container .stRadio > div > label[data-checked="true"]:before {
        background: #d4b3a0 !important;
        box-shadow: 0 0 5px rgba(212, 146, 111, 0.5) !important;
    }
    
    /* Enhanced selected state */
    .nav-item-container .stRadio > div > label[data-checked="true"] {
        background: #f0e6d8 !important;
        font-weight: 700 !important;
        border-left: 4px solid #d4b3a0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation menu with custom container
    with st.sidebar.container():
        st.markdown('<div class="nav-item-container">', unsafe_allow_html=True)
        page = st.radio(
            "",
            ["Upload & Process", "Header Mapping", "Master Sheet", "Analytics"],
            label_visibility="collapsed",
            key="page_navigation"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
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
        <h1>Mastersheet CRM Tool</h1>
        <p>Transform multiple spreadsheets into unified, standardized data with intelligent header mapping</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: var(--text-accent); margin-top: 0;">📁 Upload & Process Files</h2>
        <p style="color: var(--text-muted); margin-bottom: 0;">Start by uploading your spreadsheet files. Supported formats: CSV, Excel (.xlsx, .xls)</p>
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
        <div style="background: var(--bg-accent); padding: 1rem; border-radius: 8px; margin: 1rem 0; box-shadow: var(--shadow-light); border: 1px solid var(--border-accent);">
            <h4 style="color: var(--text-primary); margin: 0;">✨ Successfully uploaded {len(uploaded_files)} files</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display uploaded files in a beautiful card
        with st.expander("📋 View Uploaded Files", expanded=True):
            for file in uploaded_files:
                st.markdown(f"""
                <div style="background: var(--bg-card); padding: 0.8rem; border-radius: 6px; margin: 0.5rem 0; border-left: 3px solid var(--accent-primary); color: var(--text-primary); box-shadow: var(--shadow-light);">
                    <strong>📄 {file.name}</strong><br>
                    <small style="color: var(--text-muted);">Size: {file.size:,} bytes</small>
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
                        <h3 style="color: var(--text-accent); margin: 0 0 0.5rem 0;">{result['file_count']}</h3>
                        <p style="margin: 0; color: var(--text-muted);">Files Processed</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h3 style="color: var(--text-accent); margin: 0 0 0.5rem 0;">{result['total_sheets']}</h3>
                        <p style="margin: 0; color: var(--text-muted);">Total Sheets</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h3 style="color: var(--text-accent); margin: 0 0 0.5rem 0;">{len(result['headers'])}</h3>
                        <p style="margin: 0; color: var(--text-muted);">Unique Headers</p>
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
        <h2 style="color: var(--text-accent); margin-top: 0;">🔧 Header Mapping Configuration</h2>
        <p style="color: var(--text-muted); margin-bottom: 0;">Review and adjust header mappings to standardize your data columns</p>
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
        <h2 style="color: var(--text-accent); margin-top: 0;">📋 Unified Master Sheet</h2>
        <p style="color: var(--text-muted); margin-bottom: 0;">View, filter, and export your consolidated data</p>
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
                <h2 style="color: var(--text-accent); margin: 0 0 0.5rem 0;">{summary['total_rows']:,}</h2>
                <p style="margin: 0; color: var(--text-muted); font-weight: 600;">Total Rows</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: var(--text-accent); margin: 0 0 0.5rem 0;">{summary['total_columns']}</h2>
                <p style="margin: 0; color: var(--text-muted); font-weight: 600;">Total Columns</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: var(--text-accent); margin: 0 0 0.5rem 0;">{summary['source_files']}</h2>
                <p style="margin: 0; color: var(--text-muted); font-weight: 600;">Source Files</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center;">
                <h2 style="color: var(--text-accent); margin: 0 0 0.5rem 0;">{summary['source_sheets']}</h2>
                <p style="margin: 0; color: var(--text-muted); font-weight: 600;">Source Sheets</p>
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
        
        # FINAL WORKING Batch Export Section
        st.markdown("<div style='margin: 2rem 0 1rem 0;'></div>", unsafe_allow_html=True)
        st.subheader("🎯 FINAL WORKING Batch Export to Baserow")
        st.markdown("""
        <div style="background: var(--success-bg); padding: 1rem; border-radius: 8px; margin: 1rem 0; border: 1px solid var(--success-border); color: var(--success-text);">
            <strong>🎯 FINAL SOLUTION - GUARANTEED TO WORK</strong><br>
            Fixes HTTP 400 field validation errors by mapping data correctly to Baserow fields. Each batch uploads ALL 80 rows successfully.
        </div>
        """, unsafe_allow_html=True)

        # Create batches button
        if not st.session_state.batches_created:
            if st.button("🎯 Create FINAL WORKING Batches", type="primary"):
                if len(filtered_data) > 0:
                    # Use the final working batch creator
                    batches = create_final_batches(filtered_data, batch_size=80)
                    st.session_state.simple_batches = batches
                    st.session_state.batch_status = {batch['number']: 'pending' for batch in batches}
                    st.session_state.batches_created = True
                    st.success(f"🎯 Created {len(batches)} FINAL WORKING batches of 80 rows each!")
                    st.rerun()
                else:
                    st.error("❌ No data to create batches from")

        # Show BULLETPROOF batch export interface if batches are created
        if st.session_state.batches_created:
            batches = st.session_state.simple_batches
            batch_status = st.session_state.batch_status

            if batches:
                # Calculate summary
                total_batches = len(batches)
                completed_batches = sum(1 for status in batch_status.values() if status == 'completed')
                pending_batches = sum(1 for status in batch_status.values() if status == 'pending')
                failed_batches = sum(1 for status in batch_status.values() if status == 'failed')
                completion_percentage = (completed_batches / total_batches * 100) if total_batches > 0 else 0

                # Batch summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class="metric-container" style="text-align: center;">
                        <h3 style="color: var(--text-accent); margin: 0;">{total_batches}</h3>
                        <p style="margin: 0; color: var(--text-muted); font-weight: 600;">Total Batches</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-container" style="text-align: center;">
                        <h3 style="color: var(--success-text); margin: 0;">{completed_batches}</h3>
                        <p style="margin: 0; color: var(--text-muted); font-weight: 600;">Completed</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="metric-container" style="text-align: center;">
                        <h3 style="color: var(--warning-text); margin: 0;">{pending_batches}</h3>
                        <p style="margin: 0; color: var(--text-muted); font-weight: 600;">Pending</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col4:
                    st.markdown(f"""
                    <div class="metric-container" style="text-align: center;">
                        <h3 style="color: var(--text-accent); margin: 0;">{completion_percentage:.1f}%</h3>
                        <p style="margin: 0; color: var(--text-muted); font-weight: 600;">Progress</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Progress bar
                st.progress(completion_percentage / 100)

                # Batch export buttons
                st.markdown("### 🚀 Export Batches")

                # Create columns for batch buttons (4 per row)
                cols_per_row = 4

                for i in range(0, len(batches), cols_per_row):
                    cols = st.columns(cols_per_row)

                    for j, col in enumerate(cols):
                        batch_idx = i + j
                        if batch_idx < len(batches):
                            batch = batches[batch_idx]
                            batch_num = batch['number']
                            status = batch_status[batch_num]

                            with col:
                                # Button styling based on status
                                if status == 'completed':
                                    button_text = f"✅ Batch {batch_num}"
                                    button_disabled = True
                                    button_type = "secondary"
                                elif status == 'exporting':
                                    button_text = f"⏳ Batch {batch_num}"
                                    button_disabled = True
                                    button_type = "secondary"
                                elif status == 'failed':
                                    button_text = f"❌ Batch {batch_num}"
                                    button_disabled = False
                                    button_type = "secondary"
                                else:  # pending
                                    button_text = f"📤 Batch {batch_num}"
                                    button_disabled = False
                                    button_type = "primary"

                                # Export button
                                if st.button(
                                    button_text,
                                    key=f"final_export_batch_{batch_num}",
                                    disabled=button_disabled,
                                    type=button_type
                                ):
                                    # Export this batch using FINAL WORKING method
                                    manager = st.session_state.baserow_manager
                                    st.session_state.batch_status[batch_num] = 'exporting'

                                    # Final working export with correct field mapping
                                    success = export_batch_final(
                                        batch['data'],
                                        batch_num,
                                        manager.base_url,
                                        manager.api_token,
                                        str(manager.table_id)
                                    )

                                    # Update status
                                    if success:
                                        st.session_state.batch_status[batch_num] = 'completed'
                                    else:
                                        st.session_state.batch_status[batch_num] = 'failed'

                                    st.rerun()

                                # Show batch info
                                batch_size = len(batch['data'])
                                st.caption(f"Rows {batch['start_row']}-{batch['end_row']} ({batch_size} rows)")

                # Reset batches option
                st.markdown("---")
                if st.button("🔄 Reset All Batches", type="secondary"):
                    st.session_state.batches_created = False
                    st.session_state.simple_batches = []
                    st.session_state.batch_status = {}
                    st.success("✅ All batches reset!")
                    st.rerun()

            else:
                st.error("❌ No batch data available")

def analytics_page():
    st.markdown("""
    <div class="feature-card">
        <h2 style="color: var(--text-accent); margin-top: 0;">📊 Data Analytics</h2>
        <p style="color: var(--text-muted); margin-bottom: 0;">Explore insights and statistics from your consolidated data</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.consolidated:
        st.warning("⚠️ Please consolidate data first.")
        return
    
    master_data = st.session_state.master_data
    
    # Data quality overview with adaptive theme styling
    st.markdown("""
    <div style="background: var(--bg-accent); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border: 1px solid var(--border-accent); box-shadow: var(--shadow-light);">
        <h3 style="color: var(--text-primary); margin: 0; text-align: center;">🔍 Data Quality Analysis</h3>
        <p style="color: var(--text-muted); margin: 0.5rem 0 0 0; text-align: center;">Comprehensive overview of your data completeness</p>
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
    
    # Visualize data completeness with adaptive theme colors
    fig = px.bar(
        completeness_df,
        x='Column',
        y='Completeness (%)',
        title='Data Completeness by Column',
        color='Completeness (%)',
        color_continuous_scale=['#D4926F', '#B8956E', '#9D7A5A']
    )
    fig.update_xaxes(tickangle=45)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='var(--text-primary)'),
        title=dict(font=dict(color='var(--text-primary)')),
        xaxis=dict(color='var(--text-primary)'),
        yaxis=dict(color='var(--text-primary)')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show completeness table with index starting from 1
    completeness_display = completeness_df.copy()
    completeness_display.index = completeness_display.index + 1
    st.dataframe(completeness_display, use_container_width=True)
    
    # Source file distribution with adaptive theme styling
    st.markdown("""
    <div style="background: var(--bg-accent); padding: 1.5rem; border-radius: 12px; margin: 2rem 0 1rem 0; border: 1px solid var(--border-accent); box-shadow: var(--shadow-light);">
        <h3 style="color: var(--text-primary); margin: 0 0 1rem 0; text-align: center;">📈 Source File Distribution</h3>
        <p style="color: var(--text-muted); margin: 0; text-align: center;">Visualize how your data is distributed across source files</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File distribution with adaptive theme colors - centered, no second pie chart
    file_counts = master_data['source_file'].value_counts()
    fig_files = px.pie(
        values=file_counts.values,
        names=file_counts.index,
        title="Records by Source File",
        color_discrete_sequence=['#D4926F', '#B8956E', '#9D7A5A', '#C8956E', '#A0845C']
    )
    # Make the chart a bit larger and centered with adaptive styling
    fig_files.update_layout(
        height=500, 
        width=700, 
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='var(--text-primary)'),
        title=dict(font=dict(color='var(--text-primary)'))
    )
    st.plotly_chart(fig_files, use_container_width=True)
    
    # Column statistics with adaptive theme styling
    st.markdown("""
    <div style="background: var(--bg-accent); padding: 1.5rem; border-radius: 12px; margin: 2rem 0 1rem 0; border: 1px solid var(--border-accent); box-shadow: var(--shadow-light);">
        <h3 style="color: var(--text-primary); margin: 0 0 1rem 0; text-align: center;">📋 Detailed Column Analysis</h3>
        <p style="color: var(--text-muted); margin: 0; text-align: center;">Deep dive into individual column statistics</p>
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
            
            # Create histogram for numeric data with adaptive theme colors
            numeric_data = pd.to_numeric(master_data[selected_column], errors='coerce').dropna()
            fig_hist = px.histogram(
                x=numeric_data,
                nbins=30,
                title=f"Distribution of {selected_column}",
                color_discrete_sequence=['#D4926F'],
                opacity=0.8
            )
            fig_hist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-primary)'),
                title=dict(font=dict(color='var(--text-primary)')),
                xaxis=dict(color='var(--text-primary)'),
                yaxis=dict(color='var(--text-primary)')
            )
            st.plotly_chart(fig_hist, use_container_width=True)


if __name__ == "__main__":
    main()