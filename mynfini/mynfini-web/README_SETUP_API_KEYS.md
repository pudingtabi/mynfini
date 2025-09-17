# MYNFINI AI Game Master - Secure API Setup

## Overview
This secure API setup script provides a safe, interactive way to configure API keys for the MYNFINI Revolutionary TTRPG system. The script supports multiple AI providers with validation and testing capabilities.

## Supported AI Providers
1. **Anthropic Claude** - Default provider with advanced reasoning capabilities
2. **OpenAI GPT** - Alternative provider with extensive model selection
3. **Google Gemini** - Google's advanced AI models
4. **Synthetic.new Multi-Model** - Platform supporting 100+ AI models with dynamic selection
5. **Kimi K2-905** - Moonshot AI's advanced model with 127-agent mega-parallel orchestration
6. **Local AI Models** - Self-hosted models for privacy-focused usage

## Features
- 🔐 Secure API key handling with masking
- 🧪 Connectivity testing for all providers
- 📋 Interactive menu-driven setup
- 💾 Multiple storage options (.env file, JSON config)
- ✅ API key format validation
- 🚀 Support for 127-agent mega-parallel orchestration
- 🔄 Provider switching capabilities
- 📊 Real-time status reporting

## Usage

### Interactive Setup
Run the setup script directly:

```bash
python setup_api_keys.py
```

The script will guide you through:
1. Checking current API key status
2. Setting up each provider interactively
3. Validating API key formats
4. Testing connectivity to configured providers
5. Testing 127-agent mega-parallel orchestration (if applicable)
6. Saving configuration securely

### Automated Testing
Test the setup script functionality:

```bash
python test_setup_api_keys.py
```

## Configuration Storage Options
1. **Environment File (.env)** - Recommended for development
2. **JSON Config (ai_config.json)** - For persistent configuration
3. **System Environment Variables** - For production deployments

## Security Features
- API keys are masked in all displays
- Secure input handling with hidden password fields
- No plaintext key storage in logs or outputs
- Configuration files are created with appropriate permissions
- Keys are validated without exposing sensitive information

## Mega-Parallel Orchestration
When configured with Kimi K2-905 or Synthetic.new:
- Supports 127-agent mega-parallel processing
- Automatic task distribution across agent pool
- Real-time performance monitoring
- Error handling and recovery mechanisms

## Environment Variables
The setup script configures the following environment variables:

```bash
# Core Providers
ANTHROPIC_API_KEY=your-anthropic-api-key
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key

# Advanced Providers
SYNTHETIC_NEW_API_KEY=your-synthetic-new-api-key
KIMI_K2_API_KEY=your-kimi-k2-api-key

# Local Models
LOCAL_AI_URL=http://localhost:5001

# System Configuration
MYNFINI_AI_PROVIDER=anthropic  # Default provider
```

## Troubleshooting
Common issues and solutions:

1. **Import Errors**: Ensure all dependencies are installed
2. **Connectivity Failures**: Verify API keys and network access
3. **Permission Errors**: Run with appropriate file permissions
4. **Mega-Parallel Issues**: Ensure sufficient system resources

## Integration with Launcher
The MYNFINI launcher now includes an "Advanced Setup" option that directly invokes this script for users who want to configure multiple AI providers.

## Output Interpretation
- `[SUCCESS]` - Operation completed successfully
- `[INFO]` - Informational message
- `[WARNING]` - Non-critical issue
- `[ERROR]` - Critical issue requiring attention

## Starting Your Adventure
After successful setup, start the MYNFINI system:

```bash
python web_app.py
```

Or use the launcher:

```bash
python launcher.py
```