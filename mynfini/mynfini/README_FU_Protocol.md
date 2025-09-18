# Fabula Ultima AI Game Master Protocol v6.7.2

## 🎯 Overview

Enhanced modular protocol system for running Fabula Ultima TTRPG campaigns with AI Game Masters. Features improved error handling, standardized variable syntax, and flexible deployment options.

## 📁 File Structure

### 🔧 Modular Components
- **`FU_Core.json`** - Essential AI directives, error handling, and core protocols
- **`FU_ClassSkills.json`** - Complete class definitions and skill systems  
- **`FU_WorldData.json`** - World building tools, bestiary, and GM guidance
- **`combine_fu_files.py`** - Script to generate different protocol versions

### 📦 Generated Versions
- **`FU_AI_GM_CORE.json`** (~5K tokens) - Essential directives only
- **`FU_AI_GM_STANDARD.json`** (~8K tokens) - Core + key mechanics  
- **`FU_AI_GM_COMPLETE.json`** (~13K tokens) - Full protocol with all systems

## 🚀 Quick Start

1. **Choose your version** based on AI platform:
   - **GPT-4**: Use Core version
   - **Claude/ChatGPT Plus**: Use Standard version
   - **Development/High Context**: Use Complete version

2. **Upload to your AI platform** by copying the JSON content

3. **Start gaming** with `!start` command

## 🛠 Key Improvements

### ✅ Fixed Issues
- **Variable Syntax**: Unified to `${{{variable}}}` format throughout
- **Error Handling**: Comprehensive fallback system for undefined variables
- **Template Processing**: Clear validation and substitution rules
- **Role Clarity**: Defined boundaries between storytelling and mechanics

### 🎯 Enhanced Features
- **Modular Architecture**: Easy to maintain and customize
- **Token Optimization**: Multiple versions for different context limits
- **Better Error Recovery**: Graceful handling of common failure modes
- **Improved AI Instructions**: Clearer, more actionable directives

## 🎮 Platform Compatibility

| Platform | Recommended Version | Context Limit | Performance |
|----------|-------------------|---------------|-------------|
| GPT-4 | Core | ~8K | Excellent |
| Claude | Standard/Complete | ~200K | Excellent |
| ChatGPT Plus | Standard | ~32K | Very Good |
| Gemini | Standard | ~32K | Good |

## 📋 Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `!start` | Begin new session | `!start` |
| `!save` | Create checkpoint | `!save` |
| `!status` | Show character info | `!status` |
| `!hp +10` | Adjust health | `!hp +10` |
| `!scene conflict` | Change scene type | `!scene conflict` |
| `!help` | Show all commands | `!help` |

## 🔄 Updating Protocol

1. **Edit modular files** (FU_Core.json, etc.)
2. **Run combination script**: `python combine_fu_files.py`
3. **Deploy new version** to your AI platform

## 📊 Version Comparison

### Core Version (5K tokens)
- ✅ Essential AI directives
- ✅ Error handling
- ✅ Basic commands
- ❌ Class skills
- ❌ World building tools

### Standard Version (8K tokens)  
- ✅ Everything from Core
- ✅ Essential world mechanics
- ✅ Simplified crafting
- ✅ GM tools basics
- ❌ Complete class definitions

### Complete Version (13K tokens)
- ✅ Everything from Standard
- ✅ All 15 class skill trees
- ✅ Full world building system
- ✅ Complete bestiary tools
- ✅ Advanced GM guidance

## 🔧 Customization

Edit the modular files to customize:
- **AI behavior** (FU_Core.json)
- **Class balance** (FU_ClassSkills.json)  
- **World content** (FU_WorldData.json)

Then regenerate versions with the combination script.

## 🐛 Troubleshooting

### Common Issues:
- **Template variables showing**: Check `${{{variable}}}` syntax
- **File too large**: Use Core or Standard version
- **Inconsistent rulings**: Verify Chain of Verification Protocol is active

### Error Recovery:
- Use `!help` for command assistance
- Check variable fallback values in template config
- Refer to error recovery protocols in Core module

---

*Protocol developed for enhanced AI Game Master experiences in Fabula Ultima campaigns.*