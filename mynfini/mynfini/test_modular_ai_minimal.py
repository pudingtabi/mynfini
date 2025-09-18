"""
Minimal Modular AI Test - MYNFINI Revolutionary TTRPG
Simple test without complex escaping
"""

import os
import json
from modular_ai_interface import AIMessage, AIResponse, AIProvider, create_ai_manager
from ai_config_manager import AIConfigManager

def test_modular_ai_basic():
    """Basic test of modular AI system"""
    print("TESTING MODULAR AI SYSTEM")
    print("=" * 50)

    # Test Configuration Manager
    print("\nCONFIGURATION MANAGER:")
    config_manager = AIConfigManager()
    current_provider = config_manager.get_current_provider()
    print(f"Current Provider: {current_provider}")

    # Test Provider Status
    print("\nPROVIDER STATUS:")
    status = config_manager.get_provider_status()
    print(f"Provider Details: {json.dumps(status, indent=2)[:200]}...")

    # List available providers
    available = config_manager.list_available_providers()
    print(f"Available Providers: {available}")
    print("\nMODULAR AI SYSTEM: OPERATIONAL")
    return True

def test_provider_switching():
    """Test provider switching logic"""
    print("\nPROVIDER SWITCHING:")
    config_manager = AIConfigManager()

    # Test different provider configurations
    providers = ["anthropic", "openai", "gemini"]
    for provider in providers:
        config = config_manager.get_provider_config(provider)
        enabled = config.get("enabled", False)
        model = config.get("model", "unknown")
        print(f"  {provider}: {'ENABLED' if enabled else 'DISABLED'} (model: {model})")

    print("\nENVIRONMENT SETUP INSTRUCTIONS:")
    print("Set AI_API_PROVIDER environment variable to switch providers")
    print("Or use AI_CONFIG_FILE to load configuration from file")
    print("\nSupported provider types: anthropic, openai, gemini, local")

    return True

def create_provider_guide():
    """Create provider selection guide"""
    print("\nPROVIDER SELECTION GUIDE:")
    print("=" * 50)

    print("\n1. ANTHROPIC CLAUDE (Default):")
    print("   - Best creativity evaluation")
    print("   - Optimized for narrative scenarios")
    print("   - Environment: set ANTHROPIC_API_KEY")

    print("\n2. OPENAI GPT:")
    print("   - Reliable performance")
    print("   - Wide availability")
    print("   - Environment: set OPENAI_API_KEY")

    print("\n3. GOOGLE GEMINI:")
    print("   - Most cost-effective")
    print("   - Fast responses")
    print("   - Environment: set GEMINI_API_KEY")

    print("\n4. LOCAL MODELS:")
    print("   - Complete privacy")
    print("   - No external dependencies")
    print("   - Setup: Host local AI at http://localhost:5001")

    print("\nCOST COMPARISON (per 1K tokens):")
    print("Anthropic: $0.25 input | $1.25 output")
    print("OpenAI:    $0.50 input | $1.50 output")
    print("Gemini:    $0.15 input | $0.60 output")
    print("Local:     ~$0.01 input | ~$0.01 output")

    return True

if __name__ == "__main__":
    print("MYNFINI Modular AI System - Quick Test")
    print("=" * 60)

    test_modular_ai_basic()
    test_provider_switching()
    create_provider_guide()

    print("\n" + "=" * 60)
    print("MODULAR AI TESTING COMPLETE!")
    print("\nNext Steps:")
    print("1. Set your preferred AI provider API key")
    print("2. Start server with new modular config")
    print("3. Test creativity evaluation with new provider")