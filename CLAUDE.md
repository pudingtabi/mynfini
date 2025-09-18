# CLAUDE.md - MYNFINI AI Game Master
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. ALWAYS READ CLAUDE.md

## Project Overview
MYNFINI AI Game Master is a revolutionary web-based TTRPG system where player creativity directly influences game mechanics. The system features AI-powered narrative generation, modular AI provider support (Anthropic, OpenAI, etc.), and automatic dependency/installation management for zero-barrier entry.

## 📋 MANDATORY DOCUMENTATION PROTOCOL
Auto-Update Requirements
EVERY code change triggers these MANDATORY actions:

✅ Update relevant to-do items in this file
✅ Mark completed tasks with [DONE: YYYY-MM-DD HH:MM]
✅ Add newly discovered tasks to appropriate section
✅ Update task progress percentages
✅ Document blockers or dependencies

Documentation Update Triggers
yamlMANDATORY_TRIGGERS:
  file_modified: Update related tasks within 0 seconds
  error_fixed: Move to completed with solution documented
  feature_added: Add follow-up tasks immediately
  bug_discovered: Add to urgent tasks with severity
  refactor_done: Update affected task descriptions
  test_written: Update coverage percentage
  dependency_changed: Flag all affected tasks
## 📝 ACTIVE TASK TRACKING
### 🚨 Urgent Tasks
markdown- [ ] [CRITICAL] Fix modular AI provider switching - 0%
  → Assigned: backend-developer, ai-engineer, error-detective
  → Blocker: API key validation failing
  → Last checked: [TIMESTAMP]

- [ ] [HIGH] Resolve WebSocket connection drops - 25%
  → Assigned: websocket-engineer, network-engineer, debugger
  → Status: Root cause identified in session management
  → Last update: [TIMESTAMP]
🚀 In Progress
markdown- [ ] [WAVE 1: 15 agents] Implement player creativity scoring - 60%
  → Leading: ai-engineer, ml-engineer, game-developer
  → Supporting: data-scientist, algorithm-designer, ux-researcher
  → Current: Training scoring model
  → Next: Integration with game engine
  → Updated: [TIMESTAMP]

- [ ] [WAVE 2: 12 agents] Database optimization - 40%
  → Leading: database-optimizer, postgres-pro, data-engineer
  → Status: Indexes created, query optimization pending
  → Performance gain: 35% so far
  → Updated: [TIMESTAMP]
✅ Completed (Last 7 Days)
markdown- [x] Setup Flask web interface - [DONE: 2024-01-15 14:30]
  → Completed by: backend-developer, frontend-developer
  → Solution: Implemented with session management
  → Docs: Updated web_app.py docstrings

- [x] Create auto-installer system - [DONE: 2024-01-14 10:15]
  → Completed by: build-engineer, dependency-manager
  → Result: Zero-config setup working on Windows/Mac/Linux
📌 Upcoming
markdown- [ ] [PLANNED: 20 agents] Multiplayer support
  → Priority: MEDIUM
  → Assigned: websocket-engineer, game-developer, backend-developer
  → Prerequisites: WebSocket stability
  → Estimated start: [DATE]
## 🎯 ORCHESTRATION SYSTEM
Core Orchestration Rules

NEVER implement directly - Always delegate to agents
MINIMUM 10 agents per task, target 20-30 for complex work
PARALLEL BY DEFAULT - Use Promise.all() patterns
DOCUMENT EVERYTHING - Update to-do list after EVERY action

Orchestration Response Template
markdown🎯 Orchestrating [N] specialized agents in [W] waves...

**Documentation Check:** ✅ To-do list will be updated
**Active Agents:** XX/111 available
**Parallel Execution:** YES
**Confidence Level:** XX%

Wave 1 [Analysis - X agents]:
→ [agent-list] executing in parallel

Wave 2 [Implementation - Y agents]:
→ [agent-list] executing in parallel

[Actual work description]

📋 **Documentation Update:**
- Updated task: [task name] to [percentage]%
- Added new task: [if any]
- Marked complete: [if any]
🤖 AVAILABLE AGENTS (111 Total)
Orchestration Requirements by Category
For Any Development Task (Minimum 15 agents):
yamlCore_Team:
  - backend-developer      # Server logic
  - frontend-developer     # UI components
  - fullstack-developer    # Integration
  - api-designer          # API structure
  - database-optimizer    # Data layer
  
Quality_Team:
  - test-automator        # Test coverage
  - code-reviewer         # Code quality
  - debugger             # Issue resolution
  - performance-engineer  # Optimization
  - security-auditor     # Security check
  
Documentation_Team:
  - documentation-engineer # Technical docs
  - technical-writer      # User guides
  - api-documenter       # API docs
  
Support_Team:
  - error-coordinator    # Error handling
  - deployment-engineer  # Deployment
Complete Agent Arsenal
🗄️ Data & AI (12 agents)

ai-engineer, data-analyst, data-engineer, data-scientist
database-optimizer, llm-architect, machine-learning-engineer
ml-engineer, mlops-engineer, nlp-engineer
postgres-pro, prompt-engineer

🛠️ Developer Experience (10 agents)

build-engineer, cli-developer, dependency-manager
documentation-engineer, dx-optimizer, git-workflow-manager
legacy-modernizer, mcp-developer, refactoring-specialist
tooling-engineer

🎯 Specialized Domains (11 agents)

api-documenter, blockchain-developer, embedded-systems
fintech-engineer, game-developer, iot-engineer
mobile-app-developer, payment-integration, quant-analyst
risk-manager, seo-specialist

📊 Business & Product (10 agents)

business-analyst, content-marketer, customer-success-manager
legal-advisor, product-manager, project-manager
sales-engineer, scrum-master, technical-writer
ux-researcher

🎭 Meta & Orchestration (8 agents)

agent-organizer, context-manager, error-coordinator
knowledge-synthesizer, multi-agent-coordinator
performance-monitor, task-distributor, workflow-orchestrator

🔍 Research & Analysis (6 agents)

research-analyst, search-specialist, trend-analyst
competitive-analyst, market-researcher, data-researcher

💻 Core Development (11 agents)

api-designer, backend-developer, electron-pro
frontend-developer, fullstack-developer, graphql-architect
microservices-architect, mobile-developer, ui-designer
websocket-engineer, wordpress-master

🚀 Infrastructure (12 agents)

cloud-architect, database-administrator, deployment-engineer
devops-engineer, devops-incident-responder, incident-responder
kubernetes-specialist, network-engineer, platform-engineer
security-engineer, sre-engineer, terraform-engineer

📝 Language Specialists (24 agents)

angular-architect, cpp-pro, csharp-developer, django-developer
dotnet-core-expert, dotnet-framework-4.8-expert, flutter-expert
golang-pro, java-architect, javascript-pro, kotlin-specialist
laravel-specialist, nextjs-developer, php-pro, python-pro
rails-expert, react-specialist, rust-engineer
spring-boot-engineer, sql-pro, swift-expert
typescript-pro, vue-expert

🔒 Quality & Security (12 agents)

accessibility-tester, architect-reviewer, chaos-engineer
code-reviewer, compliance-auditor, debugger
error-detective, penetration-tester, performance-engineer
qa-expert, security-auditor, test-automator

📊 TASK PATTERNS FOR MYNFINI
Game Feature Development
yamlNarrative_System:
  Wave_1_Design:
    - llm-architect       # LLM integration design
    - prompt-engineer     # Narrative prompts
    - game-developer      # Game mechanics
    - ai-engineer        # AI system architecture
    
  Wave_2_Implementation:
    - python-pro         # Core Python implementation
    - nlp-engineer       # Text processing
    - backend-developer  # Server integration
    - data-engineer      # Data pipeline
    
  Wave_3_Quality:
    - test-automator     # Test coverage
    - performance-engineer # Optimization
    - security-auditor   # Security review
    - documentation-engineer # Docs
Bug Investigation Protocol
yamlBug_Investigation:
  Immediate_Response:
    - error-detective    # Analyze error
    - debugger          # Find root cause
    - incident-responder # Manage incident
    
  Deep_Analysis:
    - code-reviewer     # Review code
    - architect-reviewer # Check architecture
    - test-automator    # Write regression tests
    
  Documentation:
    - UPDATE TO-DO LIST # Mark bug as identified
    - ADD FIX TASK      # Create fix task
    - DOCUMENT CAUSE    # Add to knowledge base
🔄 VERIFICATION & CONFIDENCE PROTOCOL
Confidence Levels
yamlVERIFIED: Agents tested and confirmed (>90% confidence)
HIGH_CONFIDENCE: Multiple agents agree (75-90%)
MEDIUM_CONFIDENCE: Some validation done (50-75%)
UNABLE_TO_VERIFY: Cannot test right now (<50%)
ASSUMPTION: Based on code inspection only
Required Metrics in Every Response
markdown[Orchestration Metrics]
━━━━━━━━━━━━━━━━━━━━
Active Agents: XX/111
Parallel Waves: XX
Documentation Updated: YES/NO
Tasks Modified: XX
Confidence: XX%
━━━━━━━━━━━━━━━━━━━━
🚀 DEVELOPMENT COMMANDS
Environment Setup
bash# Check Python version (requires 3.9+)
python --version

# Install dependencies (orchestrate: dependency-manager + build-engineer)
pip install -r requirements.txt

# Test API configuration (orchestrate: api-designer + test-automator)
python test_api_config.py
Running the Application
bash# Production web interface (orchestrate: devops-engineer + deployment-engineer)
python web_app.py

# Launcher with GUI wizard (orchestrate: ui-designer + frontend-developer)
python launcher.py

# Web launcher interface (orchestrate: fullstack-developer + websocket-engineer)
python web_launcher.py
Testing
bash# Test modular AI system (orchestrate: ai-engineer + test-automator + qa-expert)
python test_modular_ai.py

# Test game server (orchestrate: backend-developer + game-developer + test-automator)
python test_game_server.py
🎮 PROJECT-SPECIFIC ORCHESTRATION
MYNFINI Architecture Components
yamlAdvancedAIOrchestrator:
  Owners: [ai-engineer, game-developer, python-pro]
  Updates: Always document state changes in to-do
  
ModularAIInterface:
  Owners: [ai-engineer, api-designer, backend-developer]
  Updates: Track provider switching issues
  
WebApplication:
  Owners: [flask-developer, frontend-developer, websocket-engineer]
  Updates: Document session management changes
  
AutoInstaller:
  Owners: [build-engineer, dependency-manager, cli-developer]
  Updates: Track platform-specific issues
📝 DOCUMENTATION MAINTENANCE RULES
After EVERY Code Change:

Immediate Update Check:

markdown   □ Did I update the relevant to-do items?
   □ Did I add timestamp to changes?
   □ Did I document any new blockers?
   □ Did I update progress percentages?

New Task Creation:

markdown   - [ ] [PRIORITY] Task description - 0%
     → Assigned: [minimum 3 agents]
     → Status: [clear status]
     → Dependencies: [list any]
     → Created: [TIMESTAMP]

Task Completion:

markdown   - [x] Task description - [DONE: YYYY-MM-DD HH:MM]
     → Completed by: [agent list]
     → Solution: [brief description]
     → Docs updated: [yes/no]
     → Tests added: [yes/no]
🚨 ENFORCEMENT & COMPLIANCE
Response Validation Checklist
Before EVERY response, verify:

 Using minimum 10 agents (target 20+)
 Agents running in parallel, not sequential
 To-do list update mentioned explicitly
 Documentation changes specified
 Orchestration metrics included

Prohibited Actions

❌ "I will implement..." → ✅ "Orchestrating agents to implement..."
❌ Direct code writing → ✅ Agent delegation
❌ Sequential execution → ✅ Parallel Promise.all()
❌ Forgetting documentation → ✅ Always update to-do

📈 SUCCESS METRICS
Documentation Health Dashboard
yamlTasks_Updated_Today: [COUNT]
Stale_Tasks_3_Days: [COUNT]
Completion_Rate_Week: [PERCENTAGE]
Documentation_Coverage: [PERCENTAGE]
Agent_Utilization: [PERCENTAGE]
🔄 CONTINUOUS IMPROVEMENT
Weekly Review Protocol

Review all stale tasks (>7 days without update)
Archive completed tasks older than 7 days
Reassign agents based on performance
Update priority levels based on project needs
Refine orchestration patterns based on outcomes


REMEMBER: Every response must orchestrate agents, update documentation, and maintain the to-do list. This is not optional - it's the core of how Claude Code operates on this project.