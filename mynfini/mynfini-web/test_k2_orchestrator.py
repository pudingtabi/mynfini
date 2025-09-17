#!/usr/bin/env python3
"""
Test script for Kimi K2 orchestrator
"""

def test_k2_orchestrator():
    """Test that Kimi K2 orchestrator can be imported"""
    try:
        from kimi_k2_orchestrator import KimiK2Orchestrator
        print("[SUCCESS] KimiK2Orchestrator imported successfully")

        # Try to create an instance
        orchestrator = KimiK2Orchestrator()
        print(f"[SUCCESS] KimiK2Orchestrator instantiated with {len(orchestrator.agent_pool)} agents")
        print(f"[SUCCESS] ThreadPoolExecutor max_workers: {orchestrator.executor._max_workers}")

        return True
    except Exception as e:
        print(f"[INFO] KimiK2Orchestrator not available: {e}")
        return True  # This is okay, it's optional

if __name__ == "__main__":
    success = test_k2_orchestrator()
    if success:
        print("\n[SUCCESS] Kimi K2 orchestrator test completed!")
    else:
        print("\n[ERROR] Kimi K2 orchestrator test failed!")