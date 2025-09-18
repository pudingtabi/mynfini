# API Connection Test Script

## Overview
This script provides comprehensive testing of all configured API providers in the MYNFINI Revolutionary TTRPG system, with special focus on:
- synthetic.new multi-model API access
- Kimi K2-905 mega-parallel functionality
- Provider switching and fallback mechanisms

## Features Tested
1. Environment variable validation for all API keys
2. Configuration loading and validation
3. AI configuration manager functionality
4. Modular AI interface testing
5. synthetic.new connectivity and multi-model access
6. Kimi K2-905 mega-parallel orchestration
7. Provider switching capabilities
8. Fallback mechanism testing
9. Safe API call validation

## Usage
Run the test script directly:

```bash
python test_api_connection.py
```

## Expected Output
The script will provide detailed status reports for:
- Found and missing API keys
- Configuration loading status
- Provider availability and initialization status
- Connectivity test results
- Recommendations for configuration improvements

## Configuration Requirements
To fully test all providers, set the following environment variables:

```bash
# Anthropic (default provider)
ANTHROPIC_API_KEY=your-anthropic-api-key

# OpenAI alternative
OPENAI_API_KEY=your-openai-api-key

# Google Gemini alternative
GEMINI_API_KEY=your-gemini-api-key

# synthetic.new multi-model access
SYNTHETIC_NEW_API_KEY=your-synthetic-new-api-key

# Kimi K2-905 mega-parallel access
KIMI_K2_API_KEY=your-kimi-k2-api-key

# Web application security
SECRET_KEY=your-secret-key
```

## Safe Testing
The script performs safe connectivity tests that:
- Check configuration without making actual API calls where possible
- Validate provider interfaces and configurations
- Test initialization without consuming API credits
- Provide detailed status without exposing sensitive information

## Output Interpretation
- `[OK]` - Test passed successfully
- `[INFO]` - Informational message, not an error
- `[WARNING]` - Non-critical issue that may affect functionality
- `[ERROR]` - Critical issue requiring attention

The final status report will indicate:
- `[SUCCESS]` - All systems operational
- `[WARNING]` - Most systems working, some configuration needed
- `[ERROR]` - Significant configuration required