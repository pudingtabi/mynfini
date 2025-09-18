"""
Modular AI Configuration - MYNFINI Revolutionary TTRPG
Updated config system supporting multiple AI providers
Replaces hardcoded Anthropic dependency with modular AI interface
"""

from modular_ai_interface import AIManager, AIProvider, create_ai_manager
from ai_config_manager import AIConfigManager
from typing import Dict, Any
import os

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

class Config:
    """Updated configuration manager using modular AI system"""

    def __init__(self):
        # Initialize AI configuration manager
        self.ai_config_manager = AIConfigManager()

        # Create fallback AI manager for backward compatibility
        self._initialize_fallback()

        # Web environment settings
        self.SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
        self.DEBUG = True
        self.JSON_AS_ASCII = False  # UTF-8 JSON responses
        self.JSONIFY_PRETTYPRINT_REGULAR = False

    def _initialize_fallback(self):
        """Initialize fallback AI manager for backward compatibility"""
        try:
            # Use the modular AI manager
            ai_manager = self.ai_config_manager.get_ai_manager()
            if ai_manager and ai_manager.is_provider_available(AIProvider.ANTHROPIC):
                self.modular_manager = ai_manager
                print("[OK] Using modular AI system")
                return
        except Exception as e:
            print(f"Modular AI system not available: {e}")

        # Fallback to basic Anthropic setup for backward compatibility
        print("[WARN] Falling back to basic Anthropic setup")
        from modular_ai_interface import AnthropicProvider

        fallback_config = {
            "enabled": True,
            "model": "claude-3-5-haiku-20141022",
            "api_key": os.environ.get('ANTHROPIC_API_KEY', None),
            "max_tokens": 800,
            "temperature": 0.7
        }

        try:
            if fallback_config.get('api_key'):
                self.modular_manager = AIManager(default_provider=AIProvider.ANTHROPIC)
                self.modular_manager.add_provider(AIProvider.ANTHROPIC, fallback_config)
            else:
                self.modular_manager = None
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        except Exception as e:
            print(f"Basic Anthropic setup failed: {e}")
            self.modular_manager = None

    def get_client(self):
        """Get AI client - now uses modular system"""
        if not self.ai_config_manager.ai_manager:
            raise ValueError("AI Manager not initialized - set appropriate API keys")

        return self.ai_config_manager

    def get_ai_manager(self):
        """Get the modular AI manager instance"""
        return self.ai_config_manager.ai_manager

    def get_current_ai_provider(self) -> str:
        """Get currently active AI provider"""
        return self.ai_config_manager.get_current_provider()

    def get_ai_status(self) -> Dict[str, Any]:
        """Get AI system status and available providers"""
        return self.ai_config_manager.get_provider_status()

    def switch_ai_provider(self, provider_name: str) -> bool:
        """Switch to different AI provider"""
        return self.ai_config_manager.set_provider(provider_name)

    def list_available_providers(self) -> list:
        """List available AI providers"""
        return self.ai_config_manager.get_available_providers()

    def generate_response_template(self, prompt: str, system_prompt: str = None, max_tokens: int = 800) -> str:
        """Template method for AI response generation"""
        if not self.ai_config_manager.ai_manager:
            raise ValueError("AI system not available")

        from modular_ai_interface import AIMessage

        messages = [AIMessage("user", prompt)]
        response = self.ai_config_manager.ai_manager.generate_response(
            messages, system_prompt, max_tokens
        )

        return response.content

    @staticmethod
    def get_supported_providers() -> list:
        """List all supported AI providers"""
        return ["anthropic", "openai", "gemini", "local", "bedrock", "huggingface", "synthetic_new", "kimi_k2"]

    @staticmethod
    def create_sample_config() -> Dict[str, Any]:
        """Create sample configuration for multiple providers"""
        return {
            "default_provider": "anthropic",
            "max_retries": 3,
            "fallback_enabled": True,
            "providers": {
                "anthropic": {
                    "enabled": True,
                    "model": "claude-3-5-haiku-20141022",
                    "api_key": os.environ.get('ANTHROPIC_API_KEY', 'your-api-key-here'),
                    "max_tokens": 800,
                    "temperature": 0.7,
                    "price_estimate": {"input": 0.25, "output": 1.25}  # per 1K tokens
                },
                "openai": {
                    "enabled": False,
                    "model": "gpt-3.5-turbo",
                    "api_key": os.environ.get('OPENAI_API_KEY', 'your-openai-key'),
                    "max_tokens": 800,
                    "temperature": 0.7,
                    "price_estimate": {"input": 0.50, "output": 1.50}
                },
                "gemini": {
                    "enabled": False,
                    "model": "gemini-1.5-flash",
                    "api_key": os.environ.get('GEMINI_API_KEY', 'your-gemini-key'),
                    "max_tokens": 800,
                    "temperature": 0.7,
                    "price_estimate": {"input": 0.15, "output": 0.60}
                },
                "local": {
                    "enabled": False,
                    "model": "local-model",
                    "base_url": os.environ.get('LOCAL_AI_URL', 'http://localhost:5001'),
                    "max_tokens": 800,
                    "temperature": 0.7,
                    "price_estimate": {"input": 0.01, "output": 0.01}
                },
                "synthetic_new": {
                    "enabled": False,
                    "model": "synthetic-new-auto",
                    "api_key": os.environ.get('SYNTHETIC_NEW_API_KEY', 'your-synthetic-new-key'),
                    "base_url": os.environ.get('SYNTHETIC_NEW_URL', 'https://api.synthetic.new/v1'),
                    "max_tokens": 8000,
                    "temperature": 0.7,
                    "mega_parallel_mode": False,
                    "supported_models": ["kimi", "glm", "deepseek", "qwen", "claude", "gpt", "gemini", "mixtral", "llama"],
                    "capabilities": {
                        "text_generation": ["kimi", "deepseek", "qwen", "claude", "gpt"],
                        "code_completion": ["deepseek", "qwen", "glm", "claude"],
                        "reasoning": ["kimi", "claude", "gpt", "gemini"],
                        "creative_writing": ["kimi", "qwen", "claude"],
                        "technical_analysis": ["deepseek", "glm", "claude"]
                    },
                    "price_estimate": {"input": 0.005, "output": 0.005}
                },
                "kimi_k2": {
                    "enabled": False,
                    "model": "moonshotai/Kimi-K2-Instruct-0905",
                    "api_key": os.environ.get('KIMI_K2_API_KEY', 'your-kimi-k2-key'),
                    "base_url": os.environ.get('KIMI_K2_URL', 'https://api.synthetic.new/v1'),
                    "max_tokens": 4000,
                    "temperature": 0.8,
                    "mega_parallel_mode": True,
                    "sub_agent_pool": 127,
                    "supported_models": ["kimi", "kimi-chat", "kimi-coding", "kimi-reasoning"],
                    "capabilities": {
                        "text_generation": ["kimi", "kimi-chat"],
                        "code_completion": ["kimi-coding"],
                        "reasoning": ["kimi-reasoning", "kimi"],
                        "creative_writing": ["kimi"],
                        "technical_analysis": ["kimi-coding", "kimi-reasoning"]
                    },
                    "price_estimate": {"input": 0.01, "output": 0.01}
                }
            }
        }

# Global configuration instance for backward compatibility
config_instance = Config()

# For backward compatibility - provide both class and instance access
def get_config():
    """Get the global configuration instance"""
    return config_instance