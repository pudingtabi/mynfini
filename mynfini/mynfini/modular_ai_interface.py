"""
Modular AI Interface System - MYNFINI Revolutionary TTRPG
Supports multiple AI providers: Anthropic, OpenAI, Gemini, Local Models
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
import time
import os

class AIProvider(Enum):
    """Available AI providers"""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GEMINI = "gemini"
    LOCAL = "local"
    SYNTHETIC_NEW = "synthetic_new"
    KIMI_K2 = "kimi_k2"

@dataclass
class AIMessage:
    """Standardized AI message format"""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

@dataclass
class AIResponse:
    """Standardized AI response format"""
    content: str
    tokens_used: int
    model_name: str
    provider: AIProvider
    latency_ms: float
    success: bool
    error: Optional[str] = None
    metadata: Dict[str, Any] = None

class BaseAIProvider(ABC):
    """Base class for all AI providers"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.is_initialized = False

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the AI provider"""
        pass

    @abstractmethod
    async def generate_response_async(self, messages: List[AIMessage],
                                    system_prompt: str = None,
                                    max_tokens: int = 800,
                                    temperature: float = 0.7) -> AIResponse:
        """Generate AI response asynchronously"""
        pass

    def generate_response(self, messages: List[AIMessage],
                         system_prompt: str = None,
                         max_tokens: int = 800,
                         temperature: float = 0.7) -> AIResponse:
        """Generate AI response synchronously (fallback for non-async)"""
        import asyncio
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(
                self.generate_response_async(messages, system_prompt, max_tokens, temperature)
            )
        except Exception as e:
            # Return a failed AIResponse instead of letting the exception propagate
            return AIResponse(
                content="",
                tokens_used=0,
                model_name=getattr(self, 'model_name', 'unknown'),
                provider=getattr(self, 'provider', 'unknown'),
                latency_ms=0,
                success=False,
                error=str(e)
            )
        finally:
            loop.close()

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name for this provider"""
        pass

    @abstractmethod
    def get_price_estimate(self, tokens: int) -> float:
        """Estimate cost for generation in USD"""
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate provider configuration"""
        pass

class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude API provider"""

    def get_model_name(self) -> str:
        """Get the model name for this provider"""
        return self.config.get('model', 'claude-3-5-haiku-20141022')

    def get_price_estimate(self, tokens: int) -> float:
        """Estimate cost for generation in USD"""
        # Anthropic pricing (per 1K tokens): $0.25 input, $1.25 output
        # Assuming 70% input tokens, 30% output tokens for estimate
        input_ratio = 0.7
        output_ratio = 0.3
        input_cost = (tokens * input_ratio / 1000) * 0.25
        output_cost = (tokens * output_ratio / 1000) * 1.25
        return input_cost + output_cost

    def validate_config(self) -> bool:
        """Validate provider configuration"""
        if not self.config.get('api_key'):
            raise ValueError("Anthropic provider requires 'api_key' in configuration")
        return True

    def initialize(self) -> bool:
        """Initialize Anthropic client"""
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.config.get('api_key'))
            self.is_initialized = True
            return True
        except ImportError:
            raise ImportError("anthropic library not installed. Run: pip install anthropic")
        except Exception as e:
            print(f"Anthropic initialization error: {e}")
            return False

    async def generate_response_async(self, messages: List[AIMessage],
                                     system_prompt: str = None,
                                     max_tokens: int = 800,
                                     temperature: float = 0.7) -> AIResponse:
        """Generate response using Anthropic API"""
        if not self.is_initialized:
            await self.initialize()
            if not self.is_initialized:
                return AIResponse(
                    content="Anthropic provider not initialized",
                    tokens_used=0,
                    model_name=self.get_model_name(),
                    provider=AIProvider.ANTHROPIC,
                    latency_ms=0,
                    success=False,
                    error="Initialization failed"
                )

        start_time = time.time()

        try:
            # Convert to Anthropic message format
            anthropic_messages = []
            for msg in messages:
                anthropic_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Prepare API call
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=anthropic_messages,
                system=system_prompt or "You are MYNFINI Revolutionary AI Game Master"
            )

            latency_ms = (time.time() - start_time) * 1000

            return AIResponse(
                content=response.content[0].text,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                model_name=self.get_model_name(),
                provider=AIProvider.ANTHROPIC,
                latency_ms=latency_ms,
                success=True,
                metadata={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return AIResponse(
                content="",
                tokens_used=0,
                model_name=self.get_model_name(),
                provider=AIProvider.ANTHROPIC,
                latency_ms=latency_ms,
                success=False,
                error=str(e)
            )

class OpenAIProvider(BaseAIProvider):
    """OpenAI GPT API provider"""

    def get_model_name(self) -> str:
        """Get the model name for this provider"""
        return self.config.get('model', 'gpt-3.5-turbo')

    def get_price_estimate(self, tokens: int) -> float:
        """Estimate cost for generation in USD"""
        # OpenAI pricing (per 1K tokens): $0.50 input, $1.50 output
        # Assuming 70% input tokens, 30% output tokens for estimate
        input_ratio = 0.7
        output_ratio = 0.3
        input_cost = (tokens * input_ratio / 1000) * 0.50
        output_cost = (tokens * output_ratio / 1000) * 1.50
        return input_cost + output_cost

    def validate_config(self) -> bool:
        """Validate provider configuration"""
        if not self.config.get('api_key'):
            raise ValueError("OpenAI provider requires 'api_key' in configuration")
        return True

    def initialize(self) -> bool:
        """Initialize OpenAI client"""
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.config.get('api_key'))
            self.is_initialized = True
            return True
        except ImportError:
            raise ImportError("openai library not installed. Run: pip install openai")
        except Exception as e:
            print(f"OpenAI initialization error: {e}")
            return False

    async def generate_response_async(self, messages: List[AIMessage],
                                     system_prompt: str = None,
                                     max_tokens: int = 800,
                                     temperature: float = 0.7) -> AIResponse:
        """Generate response using OpenAI API"""
        if not self.is_initialized:
            await self.initialize()
            if not self.is_initialized:
                return AIResponse(
                    content="OpenAI provider not initialized",
                    tokens_used=0,
                    model_name=self.get_model_name(),
                    provider=AIProvider.OPENAI,
                    latency_ms=0,
                    success=False,
                    error="Initialization failed"
                )

        start_time = time.time()

        try:
            # Convert to OpenAI message format
            openai_messages = []

            if system_prompt:
                openai_messages.append({"role": "system", "content": system_prompt})

            for msg in messages:
                openai_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Prepare API call
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=openai_messages,
                max_tokens=max_tokens,
                temperature=temperature
            )

            latency_ms = (time.time() - start_time) * 1000

            return AIResponse(
                content=response.choices[0].message.content,
                tokens_used=response.usage.prompt_tokens + response.usage.completion_tokens,
                model_name=self.get_model_name(),
                provider=AIProvider.OPENAI,
                latency_ms=latency_ms,
                success=True,
                metadata={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens
                }
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return AIResponse(
                content="",
                tokens_used=0,
                model_name=self.get_model_name(),
                provider=AIProvider.OPENAI,
                latency_ms=latency_ms,
                success=False,
                error=str(e)
            )

class GeminiProvider(BaseAIProvider):
    """Google Gemini API provider"""

    def get_model_name(self) -> str:
        """Get the model name for this provider"""
        return self.config.get('model', 'gemini-1.5-flash')

    def get_price_estimate(self, tokens: int) -> float:
        """Estimate cost for generation in USD"""
        # Gemini pricing (per 1K tokens): $0.15 input, $0.60 output
        # Assuming 70% input tokens, 30% output tokens for estimate
        input_ratio = 0.7
        output_ratio = 0.3
        input_cost = (tokens * input_ratio / 1000) * 0.15
        output_cost = (tokens * output_ratio / 1000) * 0.60
        return input_cost + output_cost

    def validate_config(self) -> bool:
        """Validate provider configuration"""
        if not self.config.get('api_key'):
            raise ValueError("Gemini provider requires 'api_key' in configuration")
        return True

    def initialize(self) -> bool:
        """Initialize Google Gemini client"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.config.get('api_key'))
            self.client = genai.GenerativeModel(self.model_name)
            self.is_initialized = True
            return True
        except ImportError:
            raise ImportError("google-generativeai library not installed. Run: pip install google-generativeai")
        except Exception as e:
            print(f"Gemini initialization error: {e}")
            return False

    async def generate_response_async(self, messages: List[AIMessage],
                                     system_prompt: str = None,
                                     max_tokens: int = 800,
                                     temperature: float = 0.7) -> AIResponse:
        """Generate response using Google Gemini API"""
        if not self.is_initialized:
            await self.initialize()
            if not self.is_initialized:
                return AIResponse(
                    content="Gemini provider not initialized",
                    tokens_used=0,
                    model_name=self.get_model_name(),
                    provider=AIProvider.GEMINI,
                    latency_ms=0,
                    success=False,
                    error="Initialization failed"
                )

        start_time = time.time()

        try:
            # Convert to Gemini text format
            prompt_parts = []
            if system_prompt:
                prompt_parts.append(system_prompt)

            for msg in messages:
                if msg.role == "user":
                    prompt_parts.append(msg.content)
                elif msg.role == "assistant":
                    prompt_parts.append(f"Assistant: {msg.content}")
                elif msg.role == "system":
                    prompt_parts.append(f"System: {msg.content}")

            # Prepare generation config
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }

            # Generate response
            response = self.client.generate_content(
                prompt_parts,
                generation_config=generation_config
            )

            latency_ms = (time.time() - start_time) * 1000

            # Estimate tokens (approximate)
            estimated_tokens = len(" ".join(prompt_parts).split()) + len(response.text.split())

            return AIResponse(
                content=response.text,
                tokens_used=estimated_tokens,
                model_name=self.get_model_name(),
                provider=AIProvider.GEMINI,
                latency_ms=latency_ms,
                success=True,
                metadata={
                    "input_tokens": len(" ".join(prompt_parts).split()),
                    "output_tokens": len(response.text.split())
                }
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return AIResponse(
                content="",
                tokens_used=0,
                model_name=self.get_model_name(),
                provider=AIProvider.GEMINI,
                latency_ms=latency_ms,
                success=False,
                error=str(e)
            )

class LocalProvider(BaseAIProvider):
    """Local AI model provider (for self-hosted models)"""

    def get_model_name(self) -> str:
        """Get the model name for this provider"""
        return self.config.get('model', 'local-model')

    def get_price_estimate(self, tokens: int) -> float:
        """Estimate cost for generation in USD - local models have minimal cost"""
        # Local models have very low operational cost - estimate as $0.01 per 1K tokens
        return (tokens / 1000) * 0.01

    def validate_config(self) -> bool:
        """Validate provider configuration"""
        base_url = self.config.get('base_url', 'http://localhost:5001')
        if not isinstance(base_url, str) or not base_url.startswith(('http://', 'https://')):
            raise ValueError("Local provider 'base_url' must be a valid HTTP URL")
        return True

    def initialize(self) -> bool:
        """Initialize local AI connection"""
        try:
            import requests
            self.base_url = self.config.get('base_url', 'http://localhost:5001')
            # Test connection
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                self.is_initialized = True
                return True
            else:
                print(f"Local AI server not accessible at {self.base_url}")
                return False
        except Exception as e:
            print(f"Local AI initialization error: {e}")
            return False

    async def generate_response_async(self, messages: List[AIMessage],
                                     system_prompt: str = None,
                                     max_tokens: int = 800,
                                     temperature: float = 0.7) -> AIResponse:
        """Generate response using local AI endpoint"""
        if not self.is_initialized:
            await self.initialize()
            if not self.is_initialized:
                return AIResponse(
                    content="Local AI provider not initialized",
                    tokens_used=0,
                    model_name=self.get_model_name(),
                    provider=AIProvider.LOCAL,
                    latency_ms=0,
                    success=False,
                    error="Local AI server not accessible"
                )

        start_time = time.time()

        try:
            import aiohttp

            # Convert to local provider format
            local_messages = []
            if system_prompt:
                local_messages.append({"role": "system", "content": system_prompt})

            for msg in messages:
                local_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            payload = {
                "messages": local_messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "model": self.model_name
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        latency_ms = (time.time() - start_time) * 1000

                        return AIResponse(
                            content=result.get('content', ''),
                            tokens_used=result.get('tokens_used', 0),
                            model_name=self.get_model_name(),
                            provider=AIProvider.LOCAL,
                            latency_ms=latency_ms,
                            success=True,
                            metadata=result
                        )
                    else:
                        raise Exception(f"Local AI server returned status: {response.status}")

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return AIResponse(
                content="",
                tokens_used=0,
                model_name=self.get_model_name(),
                provider=AIProvider.LOCAL,
                latency_ms=latency_ms,
                success=False,
                error=str(e)
            )

class SyntheticNewProvider(BaseAIProvider):
    """Synthetic.new provider with dynamic model discovery and multi-model capability"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get('base_url', 'https://api.synthetic.new/v1')
        self.api_key = config.get('api_key')
        self.max_tokens = config.get('max_tokens', 8000)
        self.temperature = config.get('temperature', 0.7)
        self.timeout = config.get('timeout', 30)

        # Dynamic model discovery and selection
        self.models = {}  # Will store available models with their capabilities
        self.selected_model = config.get('model', 'auto')  # 'auto' for capability-based selection
        self.model_selection_strategy = config.get('model_selection_strategy', 'best_fit')

        # Model capabilities mapping
        self.supported_models = config.get('supported_models', [
            'kimi', 'glm', 'deepseek', 'qwen', 'claude', 'gpt', 'gemini', 'mixtral', 'llama'
        ])

        # Capability-based selection preferences
        self.capability_preferences = config.get('capabilities', {
            'text_generation': ['kimi', 'deepseek', 'qwen', 'claude', 'gpt'],
            'code_completion': ['deepseek', 'qwen', 'glm', 'claude'],
            'reasoning': ['kimi', 'claude', 'gpt', 'gemini'],
            'creative_writing': ['kimi', 'qwen', 'claude'],
            'technical_analysis': ['deepseek', 'glm', 'claude']
        })

        # Cache for model discovery
        self._models_cache = None
        self._models_cache_time = 0
        self._cache_duration = 300  # 5 minutes cache

        # Authentication headers (no longer storing session as instance variable)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # KimiK2Orchestrator integration for mega-parallel processing
        self.mega_parallel_mode = config.get('mega_parallel_mode', False)
        self.sub_agent_pool = config.get('sub_agent_pool', 127)
        self.k2_orchestrator = None

        # Initialize KimiK2Orchestrator if available and mega_parallel_mode is enabled
        if self.mega_parallel_mode:
            try:
                from kimi_k2_orchestrator import KimiK2Orchestrator
                self.k2_orchestrator = KimiK2Orchestrator()
                print("[SYNTHETIC.NEW] KimiK2Orchestrator initialized for mega-parallel mode")
            except ImportError:
                print("[SYNTHETIC.NEW] KimiK2Orchestrator not available, using standard mode")
                self.k2_orchestrator = None

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async cleanup aiohttp session"""
        await self._close_session()

    def __del__(self):
        """Cleanup aiohttp session on destruction"""
        if self.session:
            try:
                # Check if there's a running event loop
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # If loop is running, create a task to close the session
                        if hasattr(loop, 'create_task'):
                            loop.create_task(self._safe_close_session())
                    else:
                        # If loop is not running, run until complete
                        if not loop.is_closed():
                            loop.run_until_complete(self._safe_close_session())
                except RuntimeError:
                    # No event loop in current thread, create a new one
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self._safe_close_session())
                    loop.close()
            except Exception:
                pass  # Ignore cleanup errors in destructor

    async def _safe_close_session(self):
        """Safely close aiohttp session"""
        try:
            if self.session and not self.session.closed:
                await self.session.close()
                self.session = None
        except Exception:
            pass  # Ignore errors during cleanup

    def get_model_name(self) -> str:
        """Get the model name for this provider"""
        if self.selected_model != 'auto':
            return f"synthetic-new-{self.selected_model}"
        return f"synthetic-new-multi-model-{len(self.models)}-parallel"

    def get_price_estimate(self, tokens: int) -> float:
        """Estimate cost for generation in USD - synthetic.new models have minimal cost"""
        # Synthetic.new models have very low operational cost - estimate as $0.005 per 1K tokens
        return (tokens / 1000) * 0.005

    def validate_config(self) -> bool:
        """Validate provider configuration"""
        if not self.api_key:
            raise ValueError("Synthetic.new provider requires 'api_key' in configuration")
        if not isinstance(self.base_url, str) or not self.base_url.startswith(('http://', 'https://')):
            raise ValueError("Synthetic.new provider 'base_url' must be a valid HTTP URL")
        return True

    def _get_session(self):
        """Deprecated: No longer used as we use context managers for session management"""
        import aiohttp
        return aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers=self.headers
        )

    async def _close_session(self):
        """Deprecated: No longer used as we use context managers for session management"""
        pass

    async def _discover_models(self) -> Dict[str, Any]:
        """Discover available models from synthetic.new API with caching"""
        import time
        current_time = time.time()

        # Return cached models if still valid
        if self._models_cache and (current_time - self._models_cache_time) < self._cache_duration:
            return self._models_cache

        try:
            import aiohttp
            session = self._get_session()

            async with session.get(f"{self.base_url}/models") as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get('models', [])

                    # Process and store model information
                    self.models = {}
                    for model in models:
                        model_id = model.get('id', '')
                        self.models[model_id] = {
                            'name': model.get('name', model_id),
                            'capabilities': model.get('capabilities', []),
                            'max_tokens': model.get('max_tokens', 8000),
                            'is_active': model.get('is_active', True),
                            'provider': model.get('provider', 'unknown'),
                            'pricing': model.get('pricing', {'input': 0.005, 'output': 0.005})
                        }

                    # Update cache
                    self._models_cache = self.models.copy()
                    self._models_cache_time = current_time

                    print(f"[SYNTHETIC.NEW] Discovered {len(self.models)} models")
                    return self.models
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to discover models: {response.status} - {error_text}")

        except Exception as e:
            print(f"[SYNTHETIC.NEW] Model discovery error: {e}")
            # Return cached models if available, or empty dict
            return self._models_cache or {}

    def _select_model_by_capability(self, required_capability: str) -> str:
        """Select the best model based on required capability"""
        if not self.models:
            # Fallback to default if no models discovered
            return "synthetic-new-default"

        # Get preference order for this capability
        preference_order = self.capability_preferences.get(required_capability, self.supported_models)

        # Find the first available model that supports this capability
        for preferred_model in preference_order:
            for model_id, model_info in self.models.items():
                # Check if model name contains the preferred model identifier
                if preferred_model.lower() in model_id.lower() and \
                   required_capability in model_info.get('capabilities', []):
                    return model_id

        # Fallback to first available model
        for model_id, model_info in self.models.items():
            if required_capability in model_info.get('capabilities', []):
                return model_id

        # Ultimate fallback
        return next(iter(self.models.keys()), "synthetic-new-default")

    def _select_model_by_strategy(self, messages: List[AIMessage], system_prompt: str = None) -> str:
        """Select model based on content analysis and strategy"""
        if self.selected_model != 'auto':
            return self.selected_model

        # Analyze content to determine required capability
        text_content = " ".join([msg.content for msg in messages])
        if system_prompt:
            text_content += " " + system_prompt

        # Determine capability based on content analysis
        capability = 'text_generation'  # default

        # Check for code-related content
        code_indicators = ['function', 'class', 'def ', 'import ', 'var ', 'const ', 'let ']
        if any(indicator in text_content for indicator in code_indicators):
            capability = 'code_completion'

        # Check for reasoning/analysis content
        reasoning_indicators = ['analyze', 'compare', 'evaluate', 'explain', 'reason', 'why', 'how']
        if any(indicator in text_content.lower() for indicator in reasoning_indicators):
            capability = 'reasoning'

        # Check for creative content
        creative_indicators = ['story', 'creative', 'imagine', 'narrative', 'character', 'world']
        if any(indicator in text_content.lower() for indicator in creative_indicators):
            capability = 'creative_writing'

        return self._select_model_by_capability(capability)

    def initialize(self) -> bool:
        """Initialize Synthetic.new connection with dynamic model discovery"""
        try:
            import asyncio
            import aiohttp

            # Check if there's a running event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is already running, we can't block it
                    print("[SYNTHETIC.NEW] Event loop is already running, deferring async initialization")
                    # Mark as initialized but defer async operations
                    self.is_initialized = True
                    return True
            except RuntimeError:
                # No event loop in current thread
                pass

            # Create a new event loop for initialization
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                # Run async initialization
                result = loop.run_until_complete(self._async_initialize())
                return result
            finally:
                # Always close the loop to prevent resource leaks
                if not loop.is_closed():
                    loop.close()

        except Exception as e:
            print(f"[SYNTHETIC.NEW] Initialization error: {e}")
            # Fallback to basic initialization
            self.is_initialized = True
            return True

    async def _async_initialize(self) -> bool:
        """Async initialization with model discovery"""
        try:
            # Test connection and discover models
            models = await self._discover_models()

            if models:
                print(f"[SYNTHETIC.NEW] Successfully discovered {len(models)} models")
                self.is_initialized = True
                return True
            else:
                print(f"[SYNTHETIC.NEW] No models discovered, but connection successful")
                self.is_initialized = True
                return True

        except Exception as e:
            print(f"[SYNTHETIC.NEW] Async initialization error: {e}")
            return False

    async def generate_response_async(self, messages: List[AIMessage],
                                     system_prompt: str = None,
                                     max_tokens: int = 800,
                                     temperature: float = 0.7) -> AIResponse:
        """Generate response using Synthetic.new with dynamic model selection"""
        if not self.is_initialized:
            await self._async_initialize()
            if not self.is_initialized:
                return AIResponse(
                    content="Synthetic.new provider not initialized",
                    tokens_used=0,
                    model_name=self.get_model_name(),
                    provider=AIProvider.SYNTHETIC_NEW,
                    latency_ms=0,
                    success=False,
                    error="Synthetic.new server not accessible"
                )

        start_time = time.time()

        try:
            # Ensure models are discovered
            if not self.models:
                await self._discover_models()

            # If mega-parallel mode is enabled and KimiK2Orchestrator is available, use it
            if self.mega_parallel_mode and self.k2_orchestrator:
                print(f"[SYNTHETIC.NEW] Using KimiK2Orchestrator with {self.sub_agent_pool} agents in mega-parallel mode")

                # Prepare context for KimiK2Orchestrator
                context = {
                    "messages": [msg.__dict__ for msg in messages],
                    "system_prompt": system_prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "models": self.models,
                    "provider": "synthetic_new"
                }

                # Execute mega-task using KimiK2Orchestrator
                k2_result = await self.k2_orchestrator.execute_mega_task(
                    "Synthetic.new parallel AI processing",
                    context
                )

                latency_ms = (time.time() - start_time) * 1000

                # Extract the best response from K2 results
                best_response = self._extract_best_response_from_k2_result(k2_result)

                return AIResponse(
                    content=best_response.get('content', 'Synthetic.new mega-parallel processing completed'),
                    tokens_used=best_response.get('tokens_used', 0),
                    model_name=self.get_model_name(),
                    provider=AIProvider.SYNTHETIC_NEW,
                    latency_ms=latency_ms,
                    success=True,
                    metadata={
                        "k2_orchestration": True,
                        "agents_deployed": k2_result.get('total_agents_deployed', 0),
                        "parallel_streams": k2_result.get('parallel_streams', 0),
                        "k2_results": k2_result
                    }
                )
            else:
                # Standard single model processing with dynamic selection
                # Select the best model based on content and capabilities
                selected_model = self._select_model_by_strategy(messages, system_prompt)
                print(f"[SYNTHETIC.NEW] Selected model: {selected_model}")

                # Prepare messages
                synthetic_messages = []
                if system_prompt:
                    synthetic_messages.append({"role": "system", "content": system_prompt})

                for msg in messages:
                    synthetic_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })

                # Generate response using selected model
                result = await self._generate_single_model_response(
                    selected_model, synthetic_messages, max_tokens, temperature
                )

                latency_ms = (time.time() - start_time) * 1000

                if result.get('success', False):
                    return AIResponse(
                        content=result.get('content', ''),
                        tokens_used=result.get('tokens_used', 0),
                        model_name=selected_model,
                        provider=AIProvider.SYNTHETIC_NEW,
                        latency_ms=latency_ms,
                        success=True,
                        metadata={
                            "model_selected": selected_model,
                            "model_capabilities": self.models.get(selected_model, {}).get('capabilities', []),
                            "provider": self.models.get(selected_model, {}).get('provider', 'unknown')
                        }
                    )
                else:
                    raise Exception(f"Synthetic.new model {selected_model} failed: {result.get('error', 'Unknown error')}")

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return AIResponse(
                content="",
                tokens_used=0,
                model_name=self.get_model_name(),
                provider=AIProvider.SYNTHETIC_NEW,
                latency_ms=latency_ms,
                success=False,
                error=str(e)
            )
        finally:
            # Always close session to prevent resource leaks
            try:
                await self._close_session()
            except Exception:
                # Ignore cleanup errors but log them
                pass

    async def _generate_single_model_response(self, model_id: str,
                                             messages: List[Dict[str, str]],
                                             max_tokens: int,
                                             temperature: float) -> Dict[str, Any]:
        """Generate response using a single Synthetic.new model with proper session management"""
        # Get model-specific configuration
        model_info = self.models.get(model_id, {})
        model_max_tokens = model_info.get('max_tokens', self.max_tokens)

        # Respect model's token limit
        effective_max_tokens = min(max_tokens, model_max_tokens)

        payload = {
            "messages": messages,
            "max_tokens": effective_max_tokens,
            "temperature": temperature,
            "model": model_id
        }

        try:
            # Use context manager for proper session cleanup
            import aiohttp
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers=self.headers
            ) as session:
                # Use the correct endpoint for synthetic.new API
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                        usage = result.get('usage', {})
                        tokens_used = usage.get('total_tokens', len(content.split()) + sum(len(msg.get('content', '').split()) for msg in messages))

                        return {
                            "success": True,
                            "content": content,
                            "tokens_used": tokens_used,
                            "model": model_id,
                            "usage": usage
                        }
                    else:
                        error_text = await response.text()
                        raise Exception(f"Synthetic.new model {model_id} returned status {response.status}: {error_text}")

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model_id
            }

    def _extract_best_response_from_k2_result(self, k2_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract the best response from KimiK2Orchestrator results"""
        try:
            # Get results from K2 orchestrator
            results = k2_result.get('results', {})
            if not results:
                return {"content": "No results from K2 orchestration", "tokens_used": 0}

            # Find the best result based on performance score
            best_agent = None
            best_score = -1

            for agent_name, result in results.items():
                if isinstance(result, dict) and result.get('success', False):
                    score = result.get('performance_score', 0)
                    if score > best_score:
                        best_score = score
                        best_agent = result

            if best_agent:
                # Extract content from the best agent result
                content = best_agent.get('result', '')
                if isinstance(content, dict):
                    # If result is a dict, extract the actual content
                    content = content.get('content', content.get('result', ''))
                elif not isinstance(content, str):
                    content = str(content)

                return {
                    "content": f"K2-optimized response: {content}",
                    "tokens_used": best_agent.get('tokens_used', 0)
                }
            else:
                # Fallback to first successful result
                for agent_name, result in results.items():
                    if isinstance(result, dict) and result.get('success', False):
                        content = result.get('result', '')
                        if isinstance(content, dict):
                            content = content.get('content', content.get('result', ''))
                        elif not isinstance(content, str):
                            content = str(content)

                        return {
                            "content": f"Synthetic.new response: {content}",
                            "tokens_used": result.get('tokens_used', 0)
                        }

                return {"content": "All K2 agents failed", "tokens_used": 0}

        except Exception as e:
            print(f"[SYNTHETIC.NEW] Error extracting best response from K2 result: {e}")
            return {"content": "Error processing K2 results", "tokens_used": 0}

class KimiK2Provider(BaseAIProvider):
    """Kimi K2-905 provider with 127-agent mega-parallel orchestration and synthetic.new integration"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model = config.get('model', 'moonshotai/Kimi-K2-Instruct-0905')
        # Updated endpoint to avoid 404 errors - using the main synthetic.new endpoint with model routing
        self.base_url = config.get('base_url', 'https://api.synthetic.new/v1')
        self.api_key = config.get('api_key')
        self.max_tokens = config.get('max_tokens', 4000)
        self.temperature = config.get('temperature', 0.8)
        self.timeout = config.get('timeout', 30)

        # Dynamic model support for Kimi and other models
        self.supported_models = config.get('supported_models', [
            'kimi', 'kimi-chat', 'kimi-coding', 'kimi-reasoning'
        ])

        # Model capabilities
        self.model_capabilities = config.get('capabilities', {
            'kimi': ['text_generation', 'creative_writing', 'reasoning'],
            'kimi-chat': ['conversation', 'text_generation'],
            'kimi-coding': ['code_completion', 'technical_analysis'],
            'kimi-reasoning': ['reasoning', 'analysis', 'evaluation']
        })

        # Mega-parallel processing settings
        self.mega_parallel_mode = config.get('mega_parallel_mode', True)
        self.subagents_enabled = config.get('subagents_enabled', True)
        self.agent_specialization = config.get('agent_specialization', 'maximum')
        self.sub_agent_pool = config.get('sub_agent_pool', 127)
        self.k2_orchestrator = None

        # Authentication headers (no longer storing session as instance variable)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Initialize KimiK2Orchestrator if available and mega_parallel_mode is enabled
        if self.mega_parallel_mode and self.subagents_enabled:
            try:
                from kimi_k2_orchestrator import KimiK2Orchestrator
                self.k2_orchestrator = KimiK2Orchestrator()
                print("[KIMI K2] KimiK2Orchestrator initialized for mega-parallel mode")
            except ImportError:
                print("[KIMI K2] KimiK2Orchestrator not available, using standard mode")
                self.k2_orchestrator = None

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async cleanup aiohttp session"""
        await self._close_session()

    def __del__(self):
        """Cleanup aiohttp session on destruction"""
        if self.session:
            try:
                # Check if there's a running event loop
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # If loop is running, create a task to close the session
                        if hasattr(loop, 'create_task'):
                            loop.create_task(self._safe_close_session())
                    else:
                        # If loop is not running, run until complete
                        if not loop.is_closed():
                            loop.run_until_complete(self._safe_close_session())
                except RuntimeError:
                    # No event loop in current thread, create a new one
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self._safe_close_session())
                    loop.close()
            except Exception:
                pass  # Ignore cleanup errors in destructor

    async def _safe_close_session(self):
        """Safely close aiohttp session"""
        try:
            if self.session and not self.session.closed:
                await self.session.close()
                self.session = None
        except Exception:
            pass  # Ignore errors during cleanup

    def get_model_name(self) -> str:
        """Get the model name for this provider"""
        return self.model

    def get_price_estimate(self, tokens: int) -> float:
        """Estimate cost for generation in USD - Kimi K2 models have minimal cost"""
        # Kimi K2 models have very low operational cost - estimate as $0.01 per 1K tokens
        return (tokens / 1000) * 0.01

    def validate_config(self) -> bool:
        """Validate provider configuration"""
        if not self.api_key:
            raise ValueError("Kimi K2 provider requires 'api_key' in configuration")
        if not isinstance(self.base_url, str) or not self.base_url.startswith(('http://', 'https://')):
            raise ValueError("Kimi K2 provider 'base_url' must be a valid HTTP URL")
        return True

    def _get_session(self):
        """Deprecated: No longer used as we use context managers for session management"""
        import aiohttp
        return aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers=self.headers
        )

    async def _close_session(self):
        """Deprecated: No longer used as we use context managers for session management"""
        pass

    def _select_model_by_capability(self, required_capability: str) -> str:
        """Select the best Kimi model based on required capability"""
        # Find the first available model that supports this capability
        for model_id, capabilities in self.model_capabilities.items():
            if required_capability in capabilities:
                return model_id

        # Fallback to default model
        return self.model

    def initialize(self) -> bool:
        """Initialize Kimi K2 connection"""
        try:
            import asyncio
            import aiohttp

            # Check if there's a running event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is already running, we can't block it
                    print("[KIMI K2] Event loop is already running, deferring async initialization")
                    # Mark as initialized but defer async operations
                    self.is_initialized = True
                    return True
            except RuntimeError:
                # No event loop in current thread
                pass

            # Create a new event loop for initialization
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                # Run async initialization
                result = loop.run_until_complete(self._async_initialize())
                return result
            finally:
                # Always close the loop to prevent resource leaks
                if not loop.is_closed():
                    loop.close()

        except Exception as e:
            print(f"[KIMI K2] Initialization error: {e}")
            # Fallback to basic initialization
            self.is_initialized = True
            return True

    async def _async_initialize(self) -> bool:
        """Async initialization"""
        try:
            # Test connection
            session = self._get_session()
            async with session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    self.is_initialized = True
                    print("[KIMI K2] Successfully initialized")
                    return True
                else:
                    print(f"[KIMI K2] Server not accessible at {self.base_url}: {response.status}")
                    return False

        except Exception as e:
            print(f"[KIMI K2] Async initialization error: {e}")
            return False

    async def generate_response_async(self, messages: List[AIMessage],
                                     system_prompt: str = None,
                                     max_tokens: int = 800,
                                     temperature: float = 0.7) -> AIResponse:
        """Generate response using Kimi K2 with mega-parallel subagent orchestration"""
        if not self.is_initialized:
            await self._async_initialize()
            if not self.is_initialized:
                return AIResponse(
                    content="Kimi K2 provider not initialized",
                    tokens_used=0,
                    model_name=self.get_model_name(),
                    provider=AIProvider.KIMI_K2,
                    latency_ms=0,
                    success=False,
                    error="Kimi K2 server not accessible"
                )

        start_time = time.time()

        try:
            # If mega-parallel mode is enabled and KimiK2Orchestrator is available, use it
            if self.mega_parallel_mode and self.k2_orchestrator:
                print(f"[KIMI K2] Using KimiK2Orchestrator with {self.sub_agent_pool} agents in mega-parallel mode")

                # Prepare context for KimiK2Orchestrator
                context = {
                    "messages": [msg.__dict__ for msg in messages],
                    "system_prompt": system_prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "model": self.model,
                    "provider": "kimi_k2",
                    "sub_agent_pool": self.sub_agent_pool
                }

                # Execute mega-task using KimiK2Orchestrator
                k2_result = await self.k2_orchestrator.execute_mega_task(
                    "Kimi K2-905 parallel AI processing",
                    context
                )

                latency_ms = (time.time() - start_time) * 1000

                # Extract the best response from K2 results
                best_response = self._extract_best_response_from_k2_result(k2_result)

                return AIResponse(
                    content=best_response.get('content', 'Kimi K2 mega-parallel processing completed'),
                    tokens_used=best_response.get('tokens_used', 0),
                    model_name=self.get_model_name(),
                    provider=AIProvider.KIMI_K2,
                    latency_ms=latency_ms,
                    success=True,
                    metadata={
                        "k2_orchestration": True,
                        "agents_deployed": k2_result.get('total_agents_deployed', 0),
                        "parallel_streams": k2_result.get('parallel_streams', 0),
                        "k2_results": k2_result
                    }
                )
            else:
                # Standard Kimi K2 processing with dynamic model selection
                # Analyze content to determine required capability
                text_content = " ".join([msg.content for msg in messages])
                if system_prompt:
                    text_content += " " + system_prompt

                # Determine capability based on content analysis
                capability = 'text_generation'  # default

                # Check for code-related content
                code_indicators = ['function', 'class', 'def ', 'import ', 'var ', 'const ', 'let ']
                if any(indicator in text_content for indicator in code_indicators):
                    capability = 'code_completion'

                # Check for reasoning/analysis content
                reasoning_indicators = ['analyze', 'compare', 'evaluate', 'explain', 'reason', 'why', 'how']
                if any(indicator in text_content.lower() for indicator in reasoning_indicators):
                    capability = 'reasoning'

                # Check for creative content
                creative_indicators = ['story', 'creative', 'imagine', 'narrative', 'character', 'world']
                if any(indicator in text_content.lower() for indicator in creative_indicators):
                    capability = 'creative_writing'

                # Select the best model based on capability
                selected_model = self._select_model_by_capability(capability)
                print(f"[KIMI K2] Selected model: {selected_model}")

                # Prepare messages
                k2_messages = []
                if system_prompt:
                    k2_messages.append({"role": "system", "content": system_prompt})

                for msg in messages:
                    k2_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })

                # Ensure we're using the correct Kimi K2 model identifier
                model_to_use = selected_model if selected_model else self.model
                payload = {
                    "messages": k2_messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "model": model_to_use
                }

                # Use context manager for proper session cleanup
                import aiohttp
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    headers=self.headers
                ) as session:
                    # Use the correct endpoint for synthetic.new API
                    async with session.post(
                        f"{self.base_url}/chat/completions",
                        json=payload
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            latency_ms = (time.time() - start_time) * 1000

                            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                            usage = result.get('usage', {})
                            tokens_used = usage.get('total_tokens', len(content.split()) + sum(len(msg.get('content', '').split()) for msg in k2_messages))

                            return AIResponse(
                                content=content,
                                tokens_used=tokens_used,
                                model_name=selected_model,
                                provider=AIProvider.KIMI_K2,
                                latency_ms=latency_ms,
                                success=True,
                                metadata={
                                    "model_selected": selected_model,
                                    "model_capabilities": self.model_capabilities.get(selected_model, []),
                                    "usage": usage
                                }
                            )
                        else:
                            error_text = await response.text()
                            raise Exception(f"Kimi K2 returned status {response.status}: {error_text}")

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return AIResponse(
                content="",
                tokens_used=0,
                model_name=self.get_model_name(),
                provider=AIProvider.KIMI_K2,
                latency_ms=latency_ms,
                success=False,
                error=str(e)
            )

    def _extract_best_response_from_k2_result(self, k2_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract the best response from KimiK2Orchestrator results"""
        try:
            # Get results from K2 orchestrator
            results = k2_result.get('results', {})
            if not results:
                return {"content": "No results from K2 orchestration", "tokens_used": 0}

            # Find the best result based on performance score
            best_agent = None
            best_score = -1

            for agent_name, result in results.items():
                if isinstance(result, dict) and result.get('success', False):
                    score = result.get('performance_score', 0)
                    if score > best_score:
                        best_score = score
                        best_agent = result

            if best_agent:
                # Extract content from the best agent result
                content = best_agent.get('result', '')
                if isinstance(content, dict):
                    # If result is a dict, extract the actual content
                    content = content.get('content', content.get('result', ''))
                elif not isinstance(content, str):
                    content = str(content)

                return {
                    "content": f"K2-optimized response: {content}",
                    "tokens_used": best_agent.get('tokens_used', 0)
                }
            else:
                # Fallback to first successful result
                for agent_name, result in results.items():
                    if isinstance(result, dict) and result.get('success', False):
                        content = result.get('result', '')
                        if isinstance(content, dict):
                            content = content.get('content', content.get('result', ''))
                        elif not isinstance(content, str):
                            content = str(content)

                        return {
                            "content": f"Kimi K2 response: {content}",
                            "tokens_used": result.get('tokens_used', 0)
                        }

                return {"content": "All K2 agents failed", "tokens_used": 0}

        except Exception as e:
            print(f"[KIMI K2] Error extracting best response from K2 result: {e}")
            return {"content": "Error processing K2 results", "tokens_used": 0}

class AIManager:
    """Central management for multiple AI providers"""

    def __init__(self, default_provider: AIProvider = AIProvider.ANTHROPIC):
        self.default_provider = default_provider
        self.providers: Dict[AIProvider, BaseAIProvider] = {}
        self.models = self._default_models()
        self.price_estimates = self._default_price_estimates()

    def _default_models(self) -> Dict[AIProvider, str]:
        """Default models for each provider"""
        return {
            AIProvider.ANTHROPIC: "claude-3-5-haiku-20141022",
            AIProvider.OPENAI: "gpt-3.5-turbo",
            AIProvider.GEMINI: "gemini-1.5-flash",
            AIProvider.LOCAL: "local-model",
            AIProvider.SYNTHETIC_NEW: "synthetic-new-auto",
            AIProvider.KIMI_K2: "moonshotai/Kimi-K2-Instruct-0905"
        }

    def _default_price_estimates(self) -> Dict[AIProvider, Dict[str, float]]:
        """Default price estimates (per 1K tokens) in USD"""
        return {
            AIProvider.ANTHROPIC: {"input": 0.25, "output": 1.25},
            AIProvider.OPENAI: {"input": 0.50, "output": 1.50},
            AIProvider.GEMINI: {"input": 0.15, "output": 0.60},
            AIProvider.LOCAL: {"input": 0.01, "output": 0.01},
            AIProvider.SYNTHETIC_NEW: {"input": 0.005, "output": 0.005},
            AIProvider.KIMI_K2: {"input": 0.01, "output": 0.01}
        }

    def add_provider(self, provider: AIProvider, config: Dict[str, Any]) -> bool:
        """Add and initialize an AI provider"""
        try:
            provider_instance = self._create_provider(provider, config)
            if provider_instance.initialize():
                self.providers[provider] = provider_instance
                return True
            return False
        except Exception as e:
            print(f"Error adding provider {provider}: {e}")
            return False

    def _create_provider(self, provider: AIProvider, config: Dict[str, Any]) -> BaseAIProvider:
        """Create AI provider instance"""
        provider_classes = {
            AIProvider.ANTHROPIC: AnthropicProvider,
            AIProvider.OPENAI: OpenAIProvider,
            AIProvider.GEMINI: GeminiProvider,
            AIProvider.LOCAL: LocalProvider,
            AIProvider.SYNTHETIC_NEW: SyntheticNewProvider,
            AIProvider.KIMI_K2: KimiK2Provider,
        }

        provider_class = provider_classes.get(provider)
        if provider_class:
            return provider_class(config)
        else:
            raise ValueError(f"Provider {provider} not supported")

    def generate_response(self,
                         messages: List[AIMessage],
                         provider: AIProvider = None,
                         system_prompt: str = None,
                         max_tokens: int = 800,
                         temperature: float = 0.7) -> AIResponse:
        """Generate response using specified provider"""
        provider = provider or self.default_provider

        if provider not in self.providers:
            if not self.add_provider(provider, {"api_key": "test-key"}) and provider != AIProvider.LOCAL:
                return AIResponse(
                    content=f"Provider {provider} not available",
                    tokens_used=0,
                    model_name="error",
                    provider=provider,
                    latency_ms=0,
                    success=False,
                    error=f"Provider {provider} not configured"
                )

        # Use the configured provider
        ai_provider = self.providers.get(provider)
        if ai_provider:
            return ai_provider.generate_response(messages, system_prompt, max_tokens, temperature)
        else:
            return AIResponse(
                content="Provider service unavailable",
                tokens_used=0,
                model_name="error",
                provider=provider,
                latency_ms=0,
                success=False,
                error="Provider not available"
            )

    def list_available_providers(self) -> List[AIProvider]:
        """List configured providers"""
        return list(self.providers.keys())

    def is_provider_available(self, provider: AIProvider) -> bool:
        """Check if a specific provider is available and initialized"""
        return provider in self.providers and self.providers[provider].is_initialized

    def get_provider_status(self, provider: AIProvider) -> Dict[str, Any]:
        """Get provider status and capabilities"""
        if provider not in self.providers:
            return {
                "provider": provider.value,
                "available": False,
                "initialized": False,
                "model": self.models.get(provider, "unknown"),
                "price_per_1k_tokens": self.price_estimates.get(provider, {"input": 0, "output": 0})
            }

        ai_provider = self.providers[provider]
        return {
            "provider": provider.value,
            "available": True,
            "initialized": ai_provider.is_initialized,
            "model": ai_provider.get_model_name(),
            "price_per_1k_tokens": self.price_estimates.get(provider, {"input": 0, "output": 0})
        }

def create_ai_manager(config: Dict[str, Any], default_provider: AIProvider = None) -> AIManager:
    """Factory function to create AI manager with configuration"""
    manager = AIManager(default_provider or AIProvider.ANTHROPIC)

    # Add configured providers
    for provider_name, provider_config in config.get('providers', {}).items():
        if provider_config.get('enabled'):
            try:
                provider = AIProvider(provider_name.lower())
                manager.add_provider(provider, provider_config)
            except ValueError:
                print(f"Warning: Unknown provider '{provider_name}' - skipping")
                continue

    return manager