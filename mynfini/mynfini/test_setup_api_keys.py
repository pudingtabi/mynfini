#!/usr/bin/env python3
"""
Test script for setup_api_keys.py
Verifies that the setup script can be imported and has the expected functions.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_setup_script():
    """Test that the setup script can be imported and has required functions"""
    try:
        import setup_api_keys
        print("[SUCCESS] setup_api_keys.py imported successfully")

        # Check for key functions
        required_functions = [
            'mask_key',
            'save_to_env_file',
            'save_to_config_file',
            'validate_api_key_format'
        ]

        for func_name in required_functions:
            if hasattr(setup_api_keys, func_name):
                print(f"[SUCCESS] Function {func_name} found")
            else:
                print(f"[ERROR] Function {func_name} not found")
                return False

        print("[SUCCESS] All required functions present")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to import setup_api_keys.py: {e}")
        return False

if __name__ == "__main__":
    success = test_setup_script()
    if success:
        print("\n[SUCCESS] setup_api_keys.py validation passed!")
        sys.exit(0)
    else:
        print("\n[ERROR] setup_api_keys.py validation failed!")
        sys.exit(1)