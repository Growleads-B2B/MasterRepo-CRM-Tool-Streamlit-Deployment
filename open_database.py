#!/usr/bin/env python3
import os
import webbrowser
import sys
from pathlib import Path

def open_database():
    """Open the database access page in the default web browser"""
    # Get the directory where this script is located
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Path to the HTML file
    html_path = script_dir / "open_database.html"
    
    # Check if the HTML file exists
    if not html_path.exists():
        print("Error: Database access file not found.")
        return False
    
    # Convert to URL format
    url = f"file://{html_path.absolute()}"
    
    # Open in browser
    print("Opening database access page...")
    webbrowser.open(url)
    print("If the browser doesn't open automatically, you can access the database at:")
    print("http://localhost:8080")
    
    return True

if __name__ == "__main__":
    open_database()
