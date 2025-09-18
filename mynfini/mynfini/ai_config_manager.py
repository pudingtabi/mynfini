"""
AI Configuration Manager - Modular AI System for MYNFINI
Manages multiple AI providers with switching capabilities
"""

import os
import json
from typing import Dict, Any
from modular_ai_interface import AIManager, AIProvider, create_ai_manager

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("[DEBUG] Loaded environment variables using dotenv")
except ImportError:
    # dotenv not available, try manual loading
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"[DEBUG] Loading environment variables from {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        os.environ[key] = value
                        print(f"[DEBUG] Loaded {key}={value[:10]}...")

class AIConfigManager:
    """Configuration manager for modular AI systems"""

    def __init__(self):
        self.config = self._load_config()
        self.ai_manager = None
        self._initialize_ai_manager()

    def _load_config(self) -> Dict[str, Any]:
        """Load AI configuration from environment and defaults"""

        # Default configuration for all providers
        default_config = {
            "default_provider": "synthetic_new",
            "max_retries": 3,
            "retry_delay": 1.0,
            "fallback_enabled": True,
            "providers": {
                "anthropic": {
                    "enabled": True,
                    "model": "claude-3-5-haiku-20141022",
                    "api_key": os.environ.get('ANTHROPIC_API_KEY', ''),
                    "max_tokens": 800,
                    "temperature": 0.7
                },
                "openai": {
                    "enabled": False,
                    "model": "gpt-3.5-turbo",
                    "api_key": os.environ.get('OPENAI_API_KEY', ''),
                    "max_tokens": 800,
                    "temperature": 0.7
                },
                "gemini": {
                    "enabled": False,
                    "model": "gemini-1.5-flash",
                    "api_key": os.environ.get('GEMINI_API_KEY', ''),
                    "max_tokens": 800,
                    "temperature": 0.7
                },
                "local": {
                    "enabled": False,
                    "model": "local-model",
                    "base_url": os.environ.get('LOCAL_AI_URL', 'http://localhost:5001'),
                    "max_tokens": 800,
                    "temperature": 0.7
                },
                "synthetic_new": {
                    "enabled": True,
                    "model": "synthetic-new-auto",
                    "api_key": os.environ.get('SYNTHETIC_NEW_API_KEY', ''),
                    "base_url": os.environ.get('SYNTHETIC_NEW_URL', 'https://api.synthetic.new/v1'),
                    "max_tokens": 8000,
                    "temperature": 0.7,
                    "mega_parallel_mode": True
                },
                "kimi_k2": {
                    "enabled": True,
                    "model": "moonshotai/Kimi-K2-Instruct-0905",
                    "api_key": os.environ.get('KIMI_K2_API_KEY', ''),
                    "base_url": os.environ.get('KIMI_K2_URL', 'https://api.synthetic.new/v1'),
                    "max_tokens": 4000,
                    "temperature": 0.8,
                    "mega_parallel_mode": True,
                    "sub_agent_pool": 127
                }
            }
        }

        # Load from environment file if exists
        config_file = os.environ.get('AI_CONFIG_FILE', 'ai_config.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    default_config.update(file_config)
            except Exception as e:
                print(f"Warning: Could not load AI config from {config_file}: {e}")

        # Override with environment variables
        env_provider = os.environ.get('MYNFINI_AI_PROVIDER')
        if env_provider:
            default_config["default_provider"] = env_provider.lower()

        return default_config

    def _initialize_ai_manager(self):
        """Initialize the AI manager with configured providers"""
        try:
            self.ai_manager = create_ai_manager(self.config)
            print(f"AI Manager initialized with providers: {self.get_available_providers()}")
        except Exception as e:
            print(f"Warning: AI Manager initialization failed: {e}")
            self.ai_manager = None

    def get_current_provider(self) -> str:
        """Get the currently active AI provider"""
        return self.config.get("default_provider", "anthropic")

    def set_provider(self, provider_name: str) -> bool:
        """Switch to a different AI provider"""
        if provider_name not in self.config.get("providers", {}):
            print(f"Provider '{provider_name}' not configured")
            return False

        # Verify provider is enabled
        provider_config = self.config["providers"][provider_name]
        if not provider_config.get("enabled", False):
            print(f"Provider '{provider_name}' is disabled")
            return False

        # Validate configuration
        if not self._validate_provider_config(provider_name, provider_config):
            return False

        self.config["default_provider"] = provider_name.lower()
        self._update_ai_manager(provider_name, provider_config)
        print(f"Switched to AI provider: {provider_name}")
        return True

    def _validate_provider_config(self, provider_name: str, config: Dict[str, Any]) -> bool:
        """Validate provider configuration"""
        required_fields = {
            "anthropic": ["api_key"],
            "openai": ["api_key"],
            "gemini": ["api_key"],
            "local": ["base_url"],
            "synthetic_new": ["api_key"],
            "kimi_k2": ["api_key"]
        }

        required = required_fields.get(provider_name, ["api_key"])
        missing = [field for field in required if not config.get(field)]

        if missing:
            print(f"Provider '{provider_name}' missing required fields: {missing}")
            return False

        return True

    def _update_ai_manager(self, provider_name: str, provider_config: Dict[str, Any]):
        """Update AI manager with new provider configuration"""
        if self.ai_manager:
            provider_enum = AIProvider(provider_name.lower())
            if self.ai_manager.add_provider(provider_enum, provider_config):
                print(f"Provider '{provider_name}' added successfully")
            else:
                print(f"Provider '{provider_name}' initialization failed")

    def get_available_providers(self) -> list:
        """Get list of available/configured providers"""
        if not self.ai_manager:
            return []
        return [p.value for p in self.ai_manager.list_available_providers()]

    def list_available_providers(self) -> list:
        """Alias for get_available_providers for backward compatibility"""
        return self.get_available_providers()

    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all AI providers"""
        if not self.ai_manager:
            return {"error": "AI Manager not initialized"}

        status = {
            "current_provider": self.get_current_provider(),
            "providers": {}
        }

        for provider_name in ["anthropic", "openai", "gemini", "local", "synthetic_new", "kimi_k2"]:
            try:
                provider_enum = AIProvider(provider_name.lower())
                status["providers"][provider_name] = self.ai_manager.get_provider_status(provider_enum)
            except ValueError:
                # Provider not supported in current AIProvider enum
                status["providers"][provider_name] = {
                    "provider": provider_name,
                    "available": False,
                    "initialized": False,
                    "model": "unknown",
                    "price_per_1k_tokens": {"input": 0, "output": 0}
                }

        return status

    def get_provider_config(self, provider_name: str = None) -> Dict[str, Any]:
        """Get configuration for specific provider or current provider"""
        provider_name = provider_name or self.get_current_provider()
        return self.config.get("providers", {}).get(provider_name, {})

    def get_ai_manager(self) -> AIManager:
        """Get the configured AI manager instance"""
        return self.ai_manager

    def is_provider_available(self, provider_name: str) -> bool:
        """Check if specific provider is available"""
        if not self.ai_manager:
            return False
        provider_enum = AIProvider(provider_name.lower())
        return provider_enum in self.ai_manager.list_available_providers()

    def get_fallback_provider(self, preferred_provider: str) -> str:
        """Get fallback provider if preferred is unavailable"""
        if self.is_provider_available(preferred_provider):
            return preferred_provider

        # Fallback sequence
        fallback_sequence = ["anthropic", "openai", "gemini", "local"]
        if preferred_provider in fallback_sequence:
            fallback_sequence.remove(preferred_provider)

        for fallback in fallback_sequence:
            if self.is_provider_available(fallback):
                return fallback

        return None

    def get_usage_costs(self) -> Dict[str, float]:
        """Get current usage costs based on provider"""
        if not self.ai_manager:
            return {"total_input_cost": 0, "total_output_cost": 0}

        # This would integrate with actual usage tracking
        # For now, return estimated costs based on provider rates
        provider = self.get_current_provider()
        price_estimates = self.ai_manager.price_estimates.get(AIProvider(provider), {"input": 0, "output": 0})

        return {
            "per_1k_input_tokens": price_estimates.get("input", 0),
            "per_1k_output_tokens": price_estimates.get("output", 0)
        }

def create_ai_config_manager() -> AIConfigManager:
    """Factory function to create AI configuration manager"""
    return AIConfigManager()

# Global AI config manager instance
ai_config_manager = create_ai_config_manager()

# For backward compatibility
Config = ai_config_manager  # Replace the old Config class