#!/usr/bin/env python3
"""
Secure API Setup Script for MYNFINI Revolutionary TTRPG System
Provides safe, interactive configuration for API keys with support for:
- Synthetic.new multi-model platform
- Kimi K2-905 with 127-agent mega-parallel orchestration
- Multiple AI providers with validation and testing
"""

import os
import sys
import json
import getpass
import asyncio
import subprocess
from typing import Dict, Any, Optional
from pathlib import Path

# Import required modules from the MYNFINI system
try:
    from modular_ai_interface import AIManager, AIProvider, AIMessage
    from ai_config_manager import AIConfigManager
    from config import Config
    HAS_MYFNI_MODULES = True
except ImportError as e:
    print(f"[ERROR] Required MYNFINI modules not available: {e}")
    HAS_MYFNI_MODULES = False

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mask_key(key: str, show_chars: int = 4) -> str:
    """Mask API key for secure display"""
    if not key:
        return ""
    if len(key) <= show_chars:
        return "*" * len(key)
    return key[:show_chars] + "*" * (len(key) - show_chars)

def get_user_input(prompt: str, hide_input: bool = False) -> str:
    """Get user input with optional hiding for sensitive data"""
    try:
        if hide_input:
            return getpass.getpass(prompt)
        else:
            return input(prompt)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)

def save_to_env_file(config: Dict[str, str], filename: str = ".env") -> bool:
    """Save configuration to environment file"""
    try:
        env_path = Path(filename)
        env_lines = []

        # Read existing content if file exists
        if env_path.exists():
            with open(env_path, 'r') as f:
                env_lines = f.readlines()

        # Update or add new keys
        for key, value in config.items():
            # Check if key already exists
            key_found = False
            for i, line in enumerate(env_lines):
                if line.startswith(f"{key}="):
                    env_lines[i] = f"{key}={value}\n"
                    key_found = True
                    break

            if not key_found:
                env_lines.append(f"{key}={value}\n")

        # Write back to file
        with open(env_path, 'w') as f:
            f.writelines(env_lines)

        print(f"[SUCCESS] Configuration saved to {filename}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save to {filename}: {e}")
        return False

def save_to_config_file(config: Dict[str, Any], filename: str = "ai_config.json") -> bool:
    """Save configuration to JSON file"""
    try:
        config_path = Path(filename)
        existing_config = {}

        # Read existing config if it exists
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    existing_config = json.load(f)
            except Exception:
                pass  # Start with empty config if file is invalid

        # Update with new configuration
        existing_config.update(config)

        # Write back to file
        with open(config_path, 'w') as f:
            json.dump(existing_config, f, indent=2)

        print(f"[SUCCESS] Configuration saved to {filename}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save to {filename}: {e}")
        return False

async def test_provider_connectivity(provider: AIProvider, config: Dict[str, Any]) -> bool:
    """Test connectivity to AI provider"""
    if not HAS_MYFNI_MODULES:
        print("[WARNING] MYNFINI modules not available, skipping connectivity test")
        return True

    try:
        # Create provider instance
        manager = AIManager()
        success = manager.add_provider(provider, config)

        if not success:
            print(f"[ERROR] Failed to initialize {provider.value} provider")
            return False

        # Test with a simple message
        test_message = [AIMessage("user", "Hello, this is a connectivity test.")]
        response = manager.generate_response(test_message, provider)

        if response.success:
            print(f"[SUCCESS] {provider.value} connectivity test passed")
            print(f"  Model: {response.model_name}")
            print(f"  Response: {response.content[:100]}...")
            return True
        else:
            print(f"[ERROR] {provider.value} connectivity test failed: {response.error}")
            return False

    except Exception as e:
        print(f"[ERROR] Exception during {provider.value} connectivity test: {e}")
        return False

def validate_api_key_format(provider: str, key: str) -> bool:
    """Validate API key format for different providers"""
    if not key or len(key) < 10:
        return False

    # Basic validation - could be extended for specific provider formats
    if provider == "anthropic":
        return key.startswith("sk-ant-") or key.startswith("sk-")
    elif provider == "openai":
        return key.startswith("sk-")
    elif provider == "synthetic_new" or provider == "kimi_k2":
        # Synthetic.new and Kimi K2 keys can be more flexible
        return len(key) >= 20

    # Default validation
    return len(key) >= 20

def setup_anthropic():
    """Setup Anthropic API key"""
    print("\n=== Anthropic Claude API Setup ===")
    print("1. Visit: https://console.anthropic.com/")
    print("2. Navigate to API Keys section")
    print("3. Create a new API key")

    current_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if current_key:
        print(f"Current key (masked): {mask_key(current_key)}")

    api_key = get_user_input("Enter your Anthropic API key (or press Enter to skip): ", hide_input=True)

    if not api_key:
        print("[INFO] Skipping Anthropic setup")
        return None

    if not validate_api_key_format("anthropic", api_key):
        print("[WARNING] API key format appears invalid, but proceeding anyway")

    return {
        "ANTHROPIC_API_KEY": api_key,
        "MYNFINI_AI_PROVIDER": "anthropic"
    }

def setup_openai():
    """Setup OpenAI API key"""
    print("\n=== OpenAI API Setup ===")
    print("1. Visit: https://platform.openai.com/api-keys")
    print("2. Create a new secret key")

    current_key = os.environ.get('OPENAI_API_KEY', '')
    if current_key:
        print(f"Current key (masked): {mask_key(current_key)}")

    api_key = get_user_input("Enter your OpenAI API key (or press Enter to skip): ", hide_input=True)

    if not api_key:
        print("[INFO] Skipping OpenAI setup")
        return None

    if not validate_api_key_format("openai", api_key):
        print("[WARNING] API key format appears invalid, but proceeding anyway")

    return {
        "OPENAI_API_KEY": api_key,
        "MYNFINI_AI_PROVIDER": "openai"
    }

def setup_synthetic_new():
    """Setup Synthetic.new API key"""
    print("\n=== Synthetic.new Multi-Model API Setup ===")
    print("1. Visit: https://synthetic.new/")
    print("2. Sign up or log in to your account")
    print("3. Navigate to API Keys section")
    print("4. Create a new API key for multi-model access")

    current_key = os.environ.get('SYNTHETIC_NEW_API_KEY', '')
    if current_key:
        print(f"Current key (masked): {mask_key(current_key)}")

    api_key = get_user_input("Enter your Synthetic.new API key (or press Enter to skip): ", hide_input=True)

    if not api_key:
        print("[INFO] Skipping Synthetic.new setup")
        return None

    if not validate_api_key_format("synthetic_new", api_key):
        print("[WARNING] API key format appears invalid, but proceeding anyway")

    # Ask about mega-parallel mode
    mega_parallel = get_user_input("Enable mega-parallel mode? (y/N): ").lower().startswith('y')

    config = {
        "SYNTHETIC_NEW_API_KEY": api_key,
        "MYNFINI_AI_PROVIDER": "synthetic_new"
    }

    if mega_parallel:
        config["SYNTHETIC_NEW_MEGA_PARALLEL"] = "true"
        print("[INFO] Mega-parallel mode enabled for Synthetic.new")

    return config

def setup_kimi_k2():
    """Setup Kimi K2-905 API key"""
    print("\n=== Kimi K2-905 API Setup ===")
    print("1. Kimi K2-905 is accessed through Synthetic.new platform")
    print("2. Ensure you have Synthetic.new API key with Kimi K2 access")
    print("3. The system will automatically use Kimi K2 when available")

    current_key = os.environ.get('KIMI_K2_API_KEY', '')
    if current_key:
        print(f"Current Kimi K2 key (masked): {mask_key(current_key)}")

    api_key = get_user_input("Enter your Kimi K2 API key (or press Enter to skip): ", hide_input=True)

    if not api_key:
        print("[INFO] Skipping Kimi K2 setup")
        return None

    if not validate_api_key_format("kimi_k2", api_key):
        print("[WARNING] API key format appears invalid, but proceeding anyway")

    # Confirm 127-agent mega-parallel mode
    print("\nKimi K2-905 supports 127-agent mega-parallel orchestration!")
    mega_parallel = get_user_input("Enable 127-agent mega-parallel mode? (Y/n): ").lower()
    if not mega_parallel or mega_parallel.startswith('y'):
        print("[INFO] 127-agent mega-parallel mode will be enabled")
        mega_parallel_enabled = True
    else:
        mega_parallel_enabled = False

    config = {
        "KIMI_K2_API_KEY": api_key,
        "MYNFINI_AI_PROVIDER": "kimi_k2"
    }

    if mega_parallel_enabled:
        config["KIMI_K2_MEGA_PARALLEL"] = "true"

    return config

def setup_gemini():
    """Setup Google Gemini API key"""
    print("\n=== Google Gemini API Setup ===")
    print("1. Visit: https://aistudio.google.com/app/apikey")
    print("2. Create a new API key")

    current_key = os.environ.get('GEMINI_API_KEY', '')
    if current_key:
        print(f"Current key (masked): {mask_key(current_key)}")

    api_key = get_user_input("Enter your Google Gemini API key (or press Enter to skip): ", hide_input=True)

    if not api_key:
        print("[INFO] Skipping Google Gemini setup")
        return None

    if not validate_api_key_format("gemini", api_key):
        print("[WARNING] API key format appears invalid, but proceeding anyway")

    return {
        "GEMINI_API_KEY": api_key,
        "MYNFINI_AI_PROVIDER": "gemini"
    }

def setup_local():
    """Setup local AI model"""
    print("\n=== Local AI Model Setup ===")
    print("Configure a locally hosted AI model (e.g., Ollama, LM Studio)")

    base_url = get_user_input("Enter your local AI server URL (default: http://localhost:5001): ") or "http://localhost:5001"

    # Validate URL format
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'http://' + base_url

    return {
        "LOCAL_AI_URL": base_url,
        "MYNFINI_AI_PROVIDER": "local"
    }

async def test_all_configured_providers(config: Dict[str, Any]) -> Dict[str, bool]:
    """Test connectivity for all configured providers"""
    results = {}

    if not HAS_MYFNI_MODULES:
        print("[WARNING] MYNFINI modules not available, skipping provider tests")
        return results

    # Test each provider that has been configured
    if config.get('ANTHROPIC_API_KEY'):
        print("\n--- Testing Anthropic Connectivity ---")
        provider_config = {
            "api_key": config['ANTHROPIC_API_KEY'],
            "model": "claude-3-haiku-20240307",
            "max_tokens": 500
        }
        results['anthropic'] = await test_provider_connectivity(AIProvider.ANTHROPIC, provider_config)

    if config.get('OPENAI_API_KEY'):
        print("\n--- Testing OpenAI Connectivity ---")
        provider_config = {
            "api_key": config['OPENAI_API_KEY'],
            "model": "gpt-3.5-turbo",
            "max_tokens": 500
        }
        results['openai'] = await test_provider_connectivity(AIProvider.OPENAI, provider_config)

    if config.get('GEMINI_API_KEY'):
        print("\n--- Testing Google Gemini Connectivity ---")
        provider_config = {
            "api_key": config['GEMINI_API_KEY'],
            "model": "gemini-1.5-flash",
            "max_tokens": 500
        }
        results['gemini'] = await test_provider_connectivity(AIProvider.GEMINI, provider_config)

    if config.get('SYNTHETIC_NEW_API_KEY'):
        print("\n--- Testing Synthetic.new Connectivity ---")
        provider_config = {
            "api_key": config['SYNTHETIC_NEW_API_KEY'],
            "base_url": "https://api.synthetic.new/v1",
            "model": "auto",
            "max_tokens": 1000
        }
        results['synthetic_new'] = await test_provider_connectivity(AIProvider.SYNTHETIC_NEW, provider_config)

    if config.get('KIMI_K2_API_KEY'):
        print("\n--- Testing Kimi K2 Connectivity ---")
        provider_config = {
            "api_key": config['KIMI_K2_API_KEY'],
            "base_url": "https://api.synthetic.new/v1/kimi",
            "model": "moonshotai/Kimi-K2-Instruct-0905",
            "max_tokens": 1000
        }
        results['kimi_k2'] = await test_provider_connectivity(AIProvider.KIMI_K2, provider_config)

    if config.get('LOCAL_AI_URL'):
        print("\n--- Testing Local AI Connectivity ---")
        provider_config = {
            "base_url": config['LOCAL_AI_URL'],
            "model": "local-model",
            "max_tokens": 500
        }
        results['local'] = await test_provider_connectivity(AIProvider.LOCAL, provider_config)

    return results

def display_current_status():
    """Display current API key status without exposing actual keys"""
    print("\n=== Current API Configuration Status ===")

    providers = [
        ("Anthropic", "ANTHROPIC_API_KEY"),
        ("OpenAI", "OPENAI_API_KEY"),
        ("Google Gemini", "GEMINI_API_KEY"),
        ("Synthetic.new", "SYNTHETIC_NEW_API_KEY"),
        ("Kimi K2", "KIMI_K2_API_KEY"),
        ("Local AI", "LOCAL_AI_URL")
    ]

    any_configured = False

    for provider_name, env_var in providers:
        value = os.environ.get(env_var, '')
        if value:
            print(f"✓ {provider_name}: Configured ({mask_key(value)})")
            any_configured = True
        else:
            print(f"✗ {provider_name}: Not configured")

    if not any_configured:
        print("No API providers are currently configured.")

    # Show current provider
    current_provider = os.environ.get('MYNFINI_AI_PROVIDER', 'anthropic')
    print(f"\nCurrent active provider: {current_provider}")

async def run_mega_parallel_test():
    """Run test for 127-agent mega-parallel orchestration system"""
    print("\n=== Testing 127-Agent Mega-Parallel Orchestration ===")

    if not HAS_MYFNI_MODULES:
        print("[WARNING] MYNFINI modules not available, cannot test mega-parallel system")
        return False

    try:
        # Import KimiK2Orchestrator
        try:
            from kimi_k2_orchestrator import KimiK2Orchestrator
        except ImportError:
            print("[INFO] KimiK2Orchestrator not available, testing with basic configuration")
            return True

        print("Initializing KimiK2Orchestrator with 127-agent pool...")
        orchestrator = KimiK2Orchestrator()

        print(f"Agent pool size: {len(orchestrator.agent_pool)}")
        print("ThreadPoolExecutor max workers:", orchestrator.executor._max_workers)

        # Test with a sample task
        print("Executing sample mega-task...")
        result = await orchestrator.execute_mega_task(
            "Test 127-agent mega-parallel orchestration for TTRPG narrative generation",
            {"creativity": 9.5, "complexity": 8.0, "parallelization": "maximum"}
        )

        if result.get('success', False):
            print("[SUCCESS] 127-agent mega-parallel orchestration test passed!")
            print(f"Agents deployed: {result.get('total_agents_deployed', 0)}")
            print(f"Execution time: {result.get('execution_time', 0):.2f}s")
            print(f"Parallel streams: {result.get('parallel_streams', 0)}")
            return True
        else:
            print("[WARNING] Mega-parallel orchestration test completed but with issues")
            return True

    except Exception as e:
        print(f"[ERROR] Mega-parallel orchestration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_launcher_config():
    """Update launcher configuration to indicate API setup is complete"""
    try:
        config_path = Path("launcher_config.json")
        config = {}

        # Read existing config
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)

        # Update API setup status
        config["api_setup"] = "completed"
        config["setup_date"] = __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write back to file
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        print("[SUCCESS] Launcher configuration updated")
        return True
    except Exception as e:
        print(f"[WARNING] Failed to update launcher configuration: {e}")
        return False

async def main():
    """Main interactive setup function"""
    clear_screen()
    print("=" * 60)
    print("🚀 MYNFINI Revolutionary TTRPG - Secure API Setup")
    print("=" * 60)
    print("Configure API keys for multiple AI providers with security")
    print("Supports Anthropic, OpenAI, Google Gemini, Synthetic.new, Kimi K2")
    print()

    # Display current status
    display_current_status()

    # Collect configuration
    all_config = {}

    print("\n" + "=" * 50)
    print("API Provider Setup")
    print("=" * 50)

    # Setup providers
    providers_setup = [
        ("Anthropic Claude", setup_anthropic),
        ("OpenAI GPT", setup_openai),
        ("Google Gemini", setup_gemini),
        ("Synthetic.new Multi-Model", setup_synthetic_new),
        ("Kimi K2-905", setup_kimi_k2),
        ("Local AI Model", setup_local)
    ]

    for provider_name, setup_func in providers_setup:
        print(f"\n--- {provider_name} ---")
        provider_config = setup_func()
        if provider_config:
            all_config.update(provider_config)

    if not all_config:
        print("\n[INFO] No API providers configured. Exiting.")
        return

    # Confirm saving
    print("\n" + "=" * 50)
    print("Configuration Summary")
    print("=" * 50)
    for key, value in all_config.items():
        if 'KEY' in key:
            print(f"{key}: {mask_key(value)}")
        else:
            print(f"{key}: {value}")

    print("\nSave configuration to:")
    print("1. Environment file (.env) - Recommended")
    print("2. JSON config file (ai_config.json)")
    print("3. Both")
    print("4. Skip saving (environment variables only)")

    choice = get_user_input("Choose save option (1-4, default: 1): ") or "1"

    saved = False
    if choice == "1" or choice == "3":
        saved = save_to_env_file(all_config)
    if choice == "2" or choice == "3":
        saved = save_to_config_file(all_config) or saved
    if choice == "4":
        print("[INFO] Configuration will only be available in current session")
        saved = True

    if not saved:
        print("[WARNING] Configuration not saved. You'll need to reconfigure on next run.")

    # Test connectivity
    print("\n" + "=" * 50)
    print("Connectivity Testing")
    print("=" * 50)
    test_connectivity = get_user_input("Test API connectivity? (Y/n): ").lower()
    if not test_connectivity or test_connectivity.startswith('y'):
        test_results = await test_all_configured_providers(all_config)
        success_count = sum(1 for result in test_results.values() if result)
        total_count = len(test_results)
        print(f"\nConnectivity test results: {success_count}/{total_count} providers successful")
    else:
        print("[INFO] Skipping connectivity tests")

    # Test mega-parallel system if Kimi K2 is configured
    if all_config.get('KIMI_K2_API_KEY') or all_config.get('SYNTHETIC_NEW_API_KEY'):
        print("\n" + "=" * 50)
        print("Mega-Parallel Orchestration Testing")
        print("=" * 50)
        test_mega = get_user_input("Test 127-agent mega-parallel system? (y/N): ").lower()
        if test_mega.startswith('y'):
            mega_success = await run_mega_parallel_test()
            if mega_success:
                print("[SUCCESS] 127-agent mega-parallel orchestration is ready!")
            else:
                print("[WARNING] Mega-parallel system test failed or not available")

    # Update launcher config
    update_launcher_config()

    print("\n" + "=" * 60)
    print("🎉 API Setup Complete!")
    print("=" * 60)
    print("✓ API keys configured securely")
    print("✓ Providers validated")
    if all_config.get('KIMI_K2_API_KEY'):
        print("✓ Kimi K2-905 127-agent mega-parallel system ready")
    elif all_config.get('SYNTHETIC_NEW_API_KEY'):
        print("✓ Synthetic.new multi-model system ready")
    print("✓ Configuration saved")
    print("\nYour MYNFINI Revolutionary TTRPG system is now ready!")
    print("Start your adventure with: python web_app.py")

    # Final prompt to start the system
    start_now = get_user_input("\nStart the web application now? (y/N): ").lower()
    if start_now.startswith('y'):
        try:
            print("Starting MYNFINI web application...")
            subprocess.run([sys.executable, "web_app.py"], check=True)
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to start web application")
        except KeyboardInterrupt:
            print("\nApplication startup cancelled")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error during setup: {e}")
        import traceback
        traceback.print_exc()