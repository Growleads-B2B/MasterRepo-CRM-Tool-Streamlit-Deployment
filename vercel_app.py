import streamlit as st
import os

# Redirect to the main app
if __name__ == "__main__":
    # This is a simple entry point for Vercel
    os.system("streamlit run app.py --server.port=$PORT --server.headless=true --server.enableCORS=false")
