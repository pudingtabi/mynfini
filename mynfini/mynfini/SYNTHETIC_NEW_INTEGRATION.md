# Synthetic.new and Kimi K2 Provider Integration

This document explains the enhanced multi-model support for synthetic.new and Kimi K2 providers in the MYNFINI AI system.

## Overview

The enhanced implementation provides:

1. **Dynamic Model Discovery** - Automatically discovers available models from synthetic.new API
2. **Capability-Based Selection** - Selects models based on task requirements (text generation, code completion, reasoning)
3. **Unified Authentication** - Single API key for access to multiple models
4. **Model-Specific Configuration** - Handles different capabilities and token limits per model
5. **Mega-Parallel Processing** - Integration with KimiK2Orchestrator for massive parallel execution

## Key Features

### Dynamic Model Discovery

The system automatically discovers available models from the synthetic.new API:

```python
# Models are automatically discovered at initialization
provider = SyntheticNewProvider(config)
await provider._discover_models()  # Returns dict of available models with capabilities
```

### Capability-Based Model Selection

Models are selected based on the content and requirements:

```python
# Automatic capability detection
capability = 'text_generation'  # default
if 'function' in content:
    capability = 'code_completion'
elif 'analyze' in content.lower():
    capability = 'reasoning'
elif 'story' in content.lower():
    capability = 'creative_writing'

# Select best model for capability
selected_model = provider._select_model_by_capability(capability)
```

### Supported Models

The system supports these models through synthetic.new:

- **Kimi** - Advanced reasoning and creative writing
- **GLM** - Technical analysis and reasoning
- **DeepSeek** - Code completion and technical tasks
- **QWEN** - General purpose with strong coding capabilities
- **Claude** - Conversation and reasoning
- **GPT** - General purpose text generation
- **Gemini** - Technical and analytical tasks
- **Mixtral** - General purpose with good multilingual support
- **LLaMA** - Open source general purpose models

### Configuration Options

#### Synthetic.new Provider Configuration

```python
config = {
    "api_key": "your-api-key",
    "base_url": "https://api.synthetic.new/v1",
    "model": "auto",  # or specific model name
    "max_tokens": 8000,
    "temperature": 0.7,
    "mega_parallel_mode": False,
    "supported_models": ["kimi", "glm", "deepseek", "qwen"],
    "capabilities": {
        "text_generation": ["kimi", "deepseek", "qwen"],
        "code_completion": ["deepseek", "qwen"],
        "reasoning": ["kimi", "glm"],
        "creative_writing": ["kimi"],
        "technical_analysis": ["deepseek", "glm"]
    }
}
```

#### Kimi K2 Provider Configuration

```python
config = {
    "api_key": "your-api-key",
    "base_url": "https://api.synthetic.new/v1/kimi",
    "model": "moonshotai/Kimi-K2-Instruct-0905",
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
    }
}
```

## Integration with KimiK2Orchestrator

When mega-parallel mode is enabled, the providers integrate with the KimiK2Orchestrator for massive parallel processing:

```python
# In provider initialization
if self.mega_parallel_mode:
    try:
        from kimi_k2_orchestrator import KimiK2Orchestrator
        self.k2_orchestrator = KimiK2Orchestrator()
    except ImportError:
        self.k2_orchestrator = None
```

## Usage Examples

### Basic Usage

```python
from modular_ai_interface import AIManager, AIProvider, AIMessage

# Configure providers
config = {
    "providers": {
        "synthetic_new": {
            "enabled": True,
            "api_key": "your-synthetic-new-key",
            "model": "auto"
        }
    }
}

# Create manager
manager = AIManager()
manager.add_provider(AIProvider.SYNTHETIC_NEW, config["providers"]["synthetic_new"])

# Generate response
messages = [AIMessage("user", "Explain quantum computing in simple terms")]
response = manager.generate_response(messages, AIProvider.SYNTHETIC_NEW)

print(response.content)
```

### Advanced Usage with Capability Selection

```python
# Code completion request
messages = [AIMessage("user", "Write a Python function to calculate fibonacci numbers")]

# The system will automatically select a code-capable model
response = manager.generate_response(messages, AIProvider.SYNTHETIC_NEW)
# Likely selects DeepSeek or QWEN based on content analysis
```

## Model Capabilities Matrix

| Model | Text Generation | Code Completion | Reasoning | Creative Writing | Technical Analysis |
|-------|----------------|-----------------|-----------|------------------|-------------------|
| Kimi | ✓ | ✓ | ✓ | ✓ | ✓ |
| GLM | ✓ | ✓ | ✓ | ○ | ✓ |
| DeepSeek | ✓ | ✓ | ○ | ○ | ✓ |
| QWEN | ✓ | ✓ | ○ | ○ | ✓ |
| Claude | ✓ | ○ | ✓ | ✓ | ○ |
| GPT | ✓ | ○ | ✓ | ✓ | ○ |
| Gemini | ✓ | ○ | ✓ | ○ | ✓ |
| Mixtral | ✓ | ○ | ○ | ✓ | ○ |
| LLaMA | ✓ | ○ | ○ | ○ | ○ |

✓ = Strong capability
○ = Basic capability

## Performance Considerations

1. **Model Caching** - Discovered models are cached for 5 minutes to reduce API calls
2. **Token Limits** - Respects per-model token limits automatically
3. **Session Reuse** - Reuses HTTP sessions for better performance
4. **Async Operations** - All network operations are asynchronous

## Error Handling

The system provides comprehensive error handling:

```python
try:
    response = await provider.generate_response_async(messages)
    if not response.success:
        print(f"Error: {response.error}")
except Exception as e:
    print(f"Exception: {e}")
```

## Testing

Run the test suite:

```bash
python test_synthetic_new.py
```

## Environment Variables

Set these environment variables for configuration:

```bash
SYNTHETIC_NEW_API_KEY=your-api-key
KIMI_K2_API_KEY=your-kimi-k2-key
```