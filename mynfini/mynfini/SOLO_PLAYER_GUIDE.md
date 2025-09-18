# MYNFINI Solo/Private Group TTRPG Setup & Play Guide

## 🎯 QUICK START (5 minutes to activation)

### **1. Get Your API Key**
```bash
# Sign up at https://console.anthropic.com
# Copy your API key (starts with sk-ant)
```

### **2. Set Environment Variables (Windows)**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-actual-key-here-12345
set SECRET_KEY=my-solo-rpg-secret-key-12345
```

### **3. Start the Server**
```cmd
cd C:\Users\mrcpe\OneDrive\Documents\Obsidian Vault\TTRPG\mynfini\mynfini-web
python complete_revolutionary_system.py
```

### **4. Test Your Setup**
```bash
# Check systems status (should show all ACTIVE)
curl http://localhost:5000/api/systems/status

# Test creativity evaluation
curl -X POST http://localhost:5000/revolution/creativity/evaluate \
  -H "Content-Type: application/json" \
  -d '{"description": "I use the shadows to hide my attack"}'
```

---

## 🎭 THE REVOLUTION - HOW IT WORKS

**Traditional TTRPG:** "I attack" → Roll dice → Success/Failure

**MYNFINI Revolution:** "I describe creatively" → AI evaluates → Creativity DEFEATS statistics

### **5-Tier Creativity System**
1. **BASIC** (+0) - Simple actions
2. **TACTICAL** (+2) - Multi-step planning
3. **CREATIVE** (+4 + extra die) - Environmental innovation
4. **BRILLIANT** (+6 + extra die) - Multi-element mastery
5. **LEGENDARY** (+8 + narrative points) - Reality-bending creativity

### **Revolutionary Mechanics**
- **Personal Classes**: Your behavior creates unique classes
- **Choice-Based XP**: Failure teaches more than success
- **Narrative Points**: Drama becomes power
- **Pressure Systems**: Adversity fuels growth
- **Multi-Axis Progression**: Six simultaneous development paths

---

## 🎮 SOLO GAMEPLAY FLOW

### **Session Setup**
1. Start server with your API key
2. Create character using class analysis
3. Set initial scene context
4. Begin interactive play

### **The Solo Cycle**
```
1. PLAYER describes creative action

2. SYSTEM evaluates creativity tier

3. MECHANICS apply bonuses/penalties

4. AI generates narrative outcome

5. SYSTEM tracks behavioral patterns

6. PROGRESSION advances multiple axes

7. REPEAT with new dramatic situations
```

### **Example Solo Session**

**Scene**: You face the Bandit Lord in a candlelit hall

**Your Turn**: "I grab the candelabra and swing it while the hot wax splatters across his face"

**System Response**: *"CRATIVITY EVALUATION: CREATIVE tier achieved (+4 mechanical bonus + d6 extra)... [AI generates narrative describing your tactical brilliance]"*

**Player Response**: "I capitalize on his blindness by using the polished floor to slide under his wild swing"

**System Response**: *"BRILLIANT execution! Your creative momentum builds toward a Legendary moment..."*

---

## 🛠️ ADVANCED COMMANDS

### **Character Development**
```bash
# Analyze your play patterns
python api_testing_templates.py

# Test class emergence
curl -X POST http://localhost:5000/revolution/class/analyze \
  -d '{"player_behavior": {"creative_history": ["used_environment", "creative_solution"]}, "player_id": "my_character"}'
```

### **Creativity Experiments**
```bash
# Compare different approaches to same action
curl -X POST http://localhost:5000/revolution/creativity/evaluate -d '{"description": "I attack"}'
curl -X POST http://localhost:5000/revolution/creativity/evaluate -d '{"description": "I use the shadows to strike"}'
curl -X POST http://localhost:5000/revolution/creativity/evaluate -d '{"description": "I manipulate the chandelier shadows to blind him while striking from darkness"}'
```

### **Adversity Testing**
```bash
# Record dramatic failure
curl -X POST http://localhost:5000/revolution/adversity/record \
  -d '{"character_id": "hero", "adversity_type": "combat_failure", "severity": 8, "description": "Defeated due to overconfidence", "lessons_learned": [\"should_have_retreated\", \"plan_better_next_time\"]}'
```

---

## 🎲 GAME MASTER AI PROMPTS

### **For Combat Scenes**
"Generate a dramatic combat encounter where environmental elements become weapons through creative description"

### **For Social Scenes**
"Create a tense negotiation where the player must use environmental context and creative rhetoric to succeed"

### **For Exploration Scenes**
"Describe a mysterious location where understanding the environment leads to creative solutions"

### **For Character Moments**
"Show how the player's previous creative choices have shaped their personal destiny"

---

## 📊 TRACKING YOUR PROGRESS

### **Create Progress Log**
```json
{
  "session_date": "2025-01-20",
  "total_cbx_earned": 45,
  "narrative_points_earned": 3,
  "creativity_breakdown": {
    "basic": 12, "tactical": 8, "creative": 5, "brilliant": 2, "legendary": 0
  },
  "adversity_events": 8,
  "wisdom_points_gained": 16,
  "emerging_class": "Environmental Innovator",
  "favorite_tactics": ["shadow_manipulation", "environmental_repurposing"]
}
```

### **Behavioral Pattern Analysis**
- Track descriptive complexity over time
- Note environmental element usage frequency
- Record multi-step thinking strategies
- Monitor character consistency themes
- Document creative breakthrough moments

---

## 🔧 TROUBLESHOOTING COMMON ISSUES

### **"API Key Invalid" Error**
- Verify key starts with `sk-ant-`
- Check key copied correctly (no spaces)
- Try regenerating key at console.anthropic.com
**Test**: `echo %ANTHROPIC_API_KEY%` should show your key

### **"Connection Refused" Error**
- Ensure server is running: `tasklist | findstr python`
- Check port 5000 not occupied: `netstat -ano | findstr 5000`
- Verify Windows Firewall allows localhost connections
- Try browser at http://localhost:5000/api/systems/status

### **"Unicode Error" in Commands**
- Use ASCII characters only in descriptions
- Avoid special characters in JSON payloads
- Use escape characters for quotes: `\"`
- Test basic commands first, then add complexity

### **"System Not Found" Error**
- Verify all Python files in directory
- Check imports work: `python -c "import advanced_ai_orchestrator"`
- Ensure revolutionary_systems_implementation.py exists
- Verify working directory is mynfini-web

### **"Creativity Evaluation Failed"**
- Test with simpler descriptions first
- Ensure context contains established elements
- Gradually increase complexity
- Check API rate limits aren't exceeded

---

## 🎯 SOLO PLAY TIPS

### **Start Simple**
- Begin with basic actions to understand tiers
- Practice environmental creativity gradually
- Build up to multi-step complex descriptions

### **Environmental Focus**
- Always note established scene elements
- Think "How can I use what's here?"
- Combine multiple elements for higher tiers

### **Dramatic Timing**
- Describe actions at emotional peaks
- Use character motivation in descriptions
- Connect to previous story moments

### **Pattern Development**
- Be consistent with your approach style
- Let character personality shape creativity
- Track what works for higher tiers

### **Fail Forward**
- Embrace failure as character growth
- Use adversity to develop Wisdom/Scars
- Let setbacks become story fuel

---

## 🌟 THE SOLO REVOLUTION

You're not just playing a game - you're experiencing the world's first AI-augmented TTRPG where:

- **Your creativity becomes power**
- **Your failures foster growth**
- **Your descriptions shape destiny**
- **Your choices create unique classes**
- **Your stories generate mechanical advantage**

Enjoy your solo revolutionary journey! 🚀