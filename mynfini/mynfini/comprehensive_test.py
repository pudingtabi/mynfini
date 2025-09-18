#!/usr/bin/env python3
"""
Comprehensive test to reproduce the DynamicsOptimizationSystem NameError
"""

import sys
import os
import traceback
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set environment variables for testing
os.environ['ANTHROPIC_API_KEY'] = 'test-key'
os.environ['SECRET_KEY'] = 'test-secret-key'

print("=== Comprehensive Test to Reproduce DynamicsOptimizationSystem NameError ===")

def test_scenario(name, test_func):
    """Run a test scenario and report results"""
    print(f"\n--- Testing Scenario: {name} ---")
    try:
        result = test_func()
        print(f"[OK] {name}: {result}")
        return True
    except Exception as e:
        print(f"[ERROR] {name}: {e}")
        traceback.print_exc()
        return False

def test_direct_import():
    """Test direct import of the class"""
    from advanced_ai_orchestrator import DynamicsOptimizationSystem
    instance = DynamicsOptimizationSystem()
    return f"Instance created: {type(instance).__name__}"

def test_ai_orchestrator_creation():
    """Test AI orchestrator creation"""
    from advanced_ai_orchestrator import AdvancedAIOrchestrator
    ai_system = AdvancedAIOrchestrator()
    return f"Created successfully with {sum(ai_system._get_systems_status().values())}/7 systems active"

def test_systems_status():
    """Test systems status method"""
    from advanced_ai_orchestrator import AdvancedAIOrchestrator
    ai_system = AdvancedAIOrchestrator()
    status = ai_system._get_systems_status()
    return f"Status: {status}"

def test_all_methods():
    """Test all methods that might reference the system"""
    from advanced_ai_orchestrator import AdvancedAIOrchestrator
    ai_system = AdvancedAIOrchestrator()

    # Test all methods that might reference systems
    methods = [method_name for method_name in dir(ai_system)
               if method_name.startswith('_get_systems_status') and callable(getattr(ai_system, method_name))]

    results = []
    for method_name in methods:
        method = getattr(ai_system, method_name)
        status = method()
        results.append(f"{method_name}: {sum(status.values())}/7 systems")

    return "; ".join(results) if results else "No _get_systems_status methods found"

def test_web_app_import():
    """Test importing web_app which might trigger the error"""
    import web_app
    return "Web app imported successfully"

# Run all test scenarios
scenarios = [
    ("Direct Import", test_direct_import),
    ("AI Orchestrator Creation", test_ai_orchestrator_creation),
    ("Systems Status", test_systems_status),
    ("All Methods", test_all_methods),
    ("Web App Import", test_web_app_import),
]

results = []
for name, test_func in scenarios:
    success = test_scenario(name, test_func)
    results.append((name, success))

print(f"\n=== Test Summary ===")
for name, success in results:
    status = "PASS" if success else "FAIL"
    print(f"{status}: {name}")

failed_tests = [name for name, success in results if not success]
if failed_tests:
    print(f"\nFailed tests: {', '.join(failed_tests)}")
    sys.exit(1)
else:
    print("\nAll tests passed!")
    sys.exit(0)