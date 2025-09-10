#!/usr/bin/env python3
"""
Basic test script to verify code structure without external dependencies
"""

import sys
import os
from pathlib import Path

def test_file_structure():
    """Test that all required files exist"""
    required_files = [
        'app.py',
        'header_mapper.py', 
        'spreadsheet_processor.py',
        'data_consolidator.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_imports():
    """Test Python imports without external dependencies"""
    try:
        import re
        from typing import Dict, List, Tuple, Any, Optional
        import logging
        from pathlib import Path
        print("✅ Standard library imports working")
        return True
    except ImportError as e:
        print(f"❌ Standard library import error: {e}")
        return False

def test_code_syntax():
    """Test that Python files have valid syntax"""
    python_files = ['header_mapper.py', 'spreadsheet_processor.py', 'data_consolidator.py', 'app.py']
    
    for file in python_files:
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print(f"✅ {file} has valid syntax")
        except SyntaxError as e:
            print(f"❌ Syntax error in {file}: {e}")
            return False
        except Exception as e:
            print(f"❌ Error checking {file}: {e}")
            return False
    
    return True

def main():
    print("Running basic tests...")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Standard Imports", test_imports), 
        ("Code Syntax", test_code_syntax)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}:")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    all_passed = all(results)
    
    if all_passed:
        print("✅ All basic tests passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the application: streamlit run app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)