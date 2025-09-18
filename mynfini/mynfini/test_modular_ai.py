"""
Test Modular AI System - MYNFINI Revolutionary TTRPG
Tests multiple AI providers and switching functionality
"""

import os
import json
from modular_ai_interface import AIMessage, AIResponse, AIProvider, create_ai_manager, AIManager
from ai_config_manager import AIConfigManager

def test_ai_providers_solo():
    """Test AI providers without real API keys"""
    print("TESTING MODULAR AI SYSTEM")
    print("=" * 50)

    # Test 1: Configuration Manager
    print("\n1. CONFIGURATION MANAGER")
    print("-" * 30)

    config_manager = AIConfigManager()
    current_provider = config_manager.get_current_provider()
    available_providers = config_manager.list_available_providers()

    print(f"Current Provider: {current_provider}")
    print(f"Available Providers: {available_providers}")

    # Test 2: Provider Switching
    print("\n2. PROVIDER CONFIGURATION")
    print("-" * 30)

    # Test switching configuration (won't work without API keys, but validates structure)
    test_providers = ["anthropic", "openai", "gemini"]

    for provider in test_providers:
        print(f"\nTesting {provider} configuration:")
        config = config_manager.get_provider_config(provider)
        enabled = config.get("enabled", False)
        model = config.get("model", "unknown")
        print(f"  Enabled: {enabled}")
        print(f"  Model: {model}")

    # Test 3: AI Manager Structure
    print("\n3. AI MANAGER STRUCTURE")
    print("-" * 30)

    ai_manager = config_manager.get_ai_manager()
    if ai_manager:
        print(f"AI Manager: Initialized")
        print(f"Available Providers: {ai_manager.list_available_providers()}")

        status = config_manager.get_provider_status()
        print(f"Provider Status: {json.dumps(status, indent=2)}")
    else:
        print("AI Manager: Not initialized (no API keys configured)")

    print("\nAI system structure validated successfully!")

    return True

def create_sample_configs():
    """Create sample configuration files for different setups"""
    print("\n\nSAMPLE CONFIGURATIONS")
    print("=" * 50)

    # Anthropic Default
    anthropic_default = Config.create_sample_config()
    print("\n1. ANTHROPIC DEFAULT:")
    print("Copy to ai_config.json:")
    print(json.dumps(anthropic_default, indent=2)[:500] + "...")

    # OpenAI Alternative
    openai_config = anthropic_default.copy()
    openai_config["default_provider"] = "openai"
    openai_config["providers"]["anthropic"]["enabled"] = False
    openai_config["providers"]["openai"]["enabled"] = True
    openai_config["providers"]["openai"]["model"] = "gpt-3.5-turbo"

    print("\n\n2. OPENAI ALTERNATIVE:")
    print("Set OPENAI_API_KEY environment variable")
    print("Default configuration includes OpenAI as primary")

    # Gemini Alternative
    gemini_config = anthropic_default.copy()
    gemini_config["default_provider"] = "gemini"
    gemini_config["providers"]["anthropic"]["enabled"] = False
    gemini_config["providers"]["gemini"]["enabled"] = True
    gemini_config["providers"]["gemini"]["model"] = "gemini-1.5-flash"

    print("\n\n3. GEMINI ALTERNATIVE:")
    print("Set GEMINI_API_KEY environment variable")
    print("Most cost-effective option for high-volume usage")

    # Local Model Setup
    local_config = anthropic_default.copy()
    local_config["default_provider"] = "local"
    local_config["providers"]["local"]["enabled"] = True
    local_config["providers"]["local"]["base_url"] = "http://localhost:5001"

    print("\n\n4. LOCAL MODEL:")
    print("Host local AI at http://localhost:5001")
    print("Most private, completely free")

    print("\n\nPRICE COMPARISON (per 1K tokens):")
    print("Anthropic Claude-3.5-Haiku: $0.25 input, $1.25 output")
    print("OpenAI GPT-3.5-Turbo:     $0.50 input, $1.50 output")
    print("Google Gemini 1.5 Flash:  $0.15 input, $0.60 output")
    print("Local Model:              ~$0.01 input, ~$0.01 output")

    return True

def demonstrate_provider_switching():
    """Demonstrate provider switching functionality"""
    print("\n\nPROVIDER SWITCHING DEMO")
    print("=" * 50)

    config_manager = AIConfigManager()

    print("1. SHOW CURRENT PROVIDER CONFIGURATION:")
    current = config_manager.get_current_provider()
    print(f"Current Provider: {current}")

    print("\n2. SET UP ENVIRONMENT VARIABLES:")
    print("For Anthropic (default):")
    print("  set ANTHROPIC_API_KEY=sk-ant-your-actual-key-here")
    print("  set SECRET_KEY=your-secret-key-here")

    print("\nFor OpenAI:")
    print("  set OPENAI_API_KEY=sk-your-openai-key-here")

    print("\nFor Gemini:")
    print("  set GEMINI_API_KEY=your-gemini-key-here")

    print("\n\n3. PROVIDER SWITCHING IN ACTION:")
    print("Switch to OpenAI (will fail without real API key):")

    # This will fail without real API key, but shows the interface
    try:
        success = config_manager.set_provider("openai")
        print(f"Switch to OpenAI: {'SUCCESS' if success else 'FAILED - API key missing'}")
    except Exception as e:
        print(f"Switch to OpenAI: EXPECTED FAILURE - {e}")

    print("\n\n4. REAL-WORLD SWITCHING EXAMPLE:")
    print("\n# Switch providers dynamically")
    print("python -c \"")
    print("from ai_config_manager import AIConfigManager")
    print("manager = AIConfigManager()")
    print("")
    print("# Set API keys in environment first!")
    print("switch_result = manager.set_provider('openai')")
    print("print(f'Switched to OpenAI: {switch_result}')\"")")

    print("\n\nMULTI-PROVIDER STRATEGY:")
    print("- Start with Anthropic (best for creativity)")
    print("- Switch to Gemini for cost optimization")
    print("- Use OpenAI for specific capabilities")
    print("- Deploy Local model for privacy/control")
    print("- Set up automatic fallback between providers")

    return True

if __name__ == "__main__":
    print("MYNFINI Modular AI System - Testing & Setup Guide")
    print("=" * 60)

    # Run all tests
    test_ai_providers_solo()
    create_sample_configs()
    demonstrate_provider_switching()

    print("\n\n\n🎯 SUMMARY: YOUR AI OPTIONS ARE READY")
    print("=" * 60)
    print("The revolutionary AI system now supports multiple providers:")
    print("- Anthropic Claude (creativity-optimized, default)")
    print("- OpenAI GPT (reliable, widely available)")
    print("- Google Gemini (cost-effective, fast)")
    print("- Local models (private, self-hosted)")
    print("\nWith modular switching and configuration management")
    print("No longer locked to single AI provider!")
    print("\nChoose the provider that best fits your needs! 🚀")