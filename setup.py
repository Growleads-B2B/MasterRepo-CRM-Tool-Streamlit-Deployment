#!/usr/bin/env python3
"""
Setup script for Spreadsheet Consolidator
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def verify_installation():
    """Verify that all packages were installed correctly"""
    print("🔍 Verifying installation...")
    
    required_packages = [
        'pandas',
        'openpyxl', 
        'xlrd',
        'streamlit',
        'fuzzywuzzy',
        'plotly'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            failed_imports.append(package)
            print(f"❌ {package}")
    
    if failed_imports:
        print(f"\n❌ Failed to import: {failed_imports}")
        return False
    else:
        print("\n✅ All packages verified!")
        return True

def main():
    print("🚀 Spreadsheet Consolidator Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found. Please run this script from the project directory.")
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Verify installation
    if not verify_installation():
        print("\n🔧 Some packages failed to install. Try installing manually:")
        print("pip install pandas openpyxl xlrd streamlit fuzzywuzzy python-levenshtein plotly")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo start the application, run:")
    print("    streamlit run app.py")
    print("\nThen open your browser to the displayed URL (usually http://localhost:8501)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)