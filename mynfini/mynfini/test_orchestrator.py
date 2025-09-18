#!/usr/bin/env python3
"""
Test script to check AdvancedAIOrchestrator initialization
"""

import sys
import os
import traceback
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print("=== AdvancedAIOrchestrator Test ===")
print(f"Current directory: {current_dir}")
print(f"Python path: {sys.path[:5]}...")

# Set environment variables for testing
os.environ['ANTHROPIC_API_KEY'] = 'test-key'
os.environ['SECRET_KEY'] = 'test-secret-key'

print("\n1. Testing imports...")
try:
    print("   Importing AdvancedAIOrchestrator...")
    from advanced_ai_orchestrator import AdvancedAIOrchestrator
    print("[OK] AdvancedAIOrchestrator imported successfully")

except Exception as e:
    print(f"[ERROR] AdvancedAIOrchestrator import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n2. Testing initialization...")
try:
    print("   Creating AdvancedAIOrchestrator instance...")
    ai_system = AdvancedAIOrchestrator()
    print("[OK] AdvancedAIOrchestrator created successfully")

    print("   Checking system status...")
    if hasattr(ai_system, '_get_systems_status'):
        status = ai_system._get_systems_status()
        print(f"[OK] System status: {status}")
        working_systems = sum(status.values())
        total_systems = len(status)
        print(f"   Systems active: {working_systems}/{total_systems}")
    else:
        print("[ERROR] _get_systems_status method not found")

except Exception as e:
    print(f"[ERROR] AdvancedAIOrchestrator initialization failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n3. Testing basic methods...")
try:
    if hasattr(ai_system, 'creativity_evaluator'):
        print("[OK] Creativity evaluator available")
    else:
        print("[ERROR] Creativity evaluator not available")

    if hasattr(ai_system, 'class_generator'):
        print("[OK] Class generator available")
    else:
        print("[ERROR] Class generator not available")

except Exception as e:
    print(f"[ERROR] Method testing failed: {e}")
    traceback.print_exc()

print("\n=== Test Complete ===")