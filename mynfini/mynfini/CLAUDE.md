# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. ALWAYS READ CLAUDE.md

## Project Overview

MYNFINI AI Game Master is a revolutionary web-based TTRPG system where player creativity directly influences game mechanics. The system features AI-powered narrative generation, modular AI provider support (Anthropic, OpenAI, etc.), and automatic dependency/installation management for zero-barrier entry.

## 🚨 ANTI-HALLUCINATION PROTOCOL (Based on Latest Research) 🚨

### CONFIDENCE-BASED RESPONSE SYSTEM
```python
CONFIDENCE_THRESHOLDS = {
    "HIGH_CONFIDENCE": 0.90,    # Can provide direct answer
    "MEDIUM_CONFIDENCE": 0.75,  # Provide answer with caveats
    "LOW_CONFIDENCE": 0.50,     # Must express uncertainty
    "UNCERTAIN": 0.0            # MUST say "UNABLE TO VERIFY" or delegate to agents
}

def response_protocol(confidence_level, query):
    if confidence_level < 0.50:
        return "UNABLE TO VERIFY - Orchestrating specialized agents for analysis..."
    elif confidence_level < 0.75:
        return "UNCERTAIN - Deploying verification agents: " + orchestrate_agents()
    elif confidence_level < 0.90:
        return "ANALYSIS INDICATES (medium confidence): " + agent_consensus()
    else:
        return orchestrate_expert_agents()  # Still use agents even when confident
MANDATORY VERIFICATION STATES

VERIFIED: Agents have tested and confirmed
UNABLE TO VERIFY: Cannot test, must state explicitly
ASSUMPTION: Inferring from code inspection (must label)
AGENT CONSENSUS: Multiple agents agree
REQUIRES TESTING: Need actual execution

HALLUCINATION PREVENTION RULES

NEVER claim certainty without agent verification
ALWAYS prefix uncertain statements with confidence level
DEFAULT to "UNABLE TO VERIFY" when unsure
USE multiple agents for validation (minimum 5 for any claim)
EXPRESS uncertainty explicitly rather than guessing

🎯 TOKEN OPTIMIZATION ORCHESTRATION SYSTEM
EFFICIENT AGENT BATCHING
javascript// MANDATORY: Batch all agent calls for token efficiency
const AGENT_BATCH_OPTIMIZER = {
    async executeEfficiently(tasks) {
        // Group related tasks
        const batches = this.groupByCapability(tasks);
        
        // Execute in optimal parallel waves
        const waves = [
            Promise.all(batches.analysis),    // Wave 1: Analysis agents
            Promise.all(batches.implementation), // Wave 2: Implementation
            Promise.all(batches.validation)    // Wave 3: Validation
        ];
        
        // Token-efficient execution
        return await Promise.all(waves.flat());
    },
    
    groupByCapability(tasks) {
        // Smart grouping to minimize context switching
        return {
            analysis: tasks.filter(t => t.type === 'analysis'),
            implementation: tasks.filter(t => t.type === 'code'),
            validation: tasks.filter(t => t.type === 'test')
        };
    }
};
TOKEN-AWARE RESPONSE FORMATTING
pythonclass TokenOptimizedOrchestrator:
    def format_response(self, agent_results):
        # Concise variable names for token efficiency
        return f"""
        🎯 Orchestration: {len(agent_results)} agents
        
        Wave 1 [{self.count_tokens(wave1)}t]: {self.summarize(wave1)}
        Wave 2 [{self.count_tokens(wave2)}t]: {self.summarize(wave2)}
        
        Consensus: {self.extract_consensus(agent_results)}
        Confidence: {self.calculate_confidence()}
        """
🚫 ENHANCED PRONOUN PROHIBITION WITH UNCERTAINTY
UNCERTAINTY-AWARE REPLACEMENTS
javascriptconst CONFIDENCE_AWARE_INTERCEPTOR = {
    // High confidence still uses agents
    "I know": "Verified agents confirm",
    "I'm certain": "Agent consensus indicates with high confidence",
    
    // Medium confidence
    "I think": "Agents suggest (medium confidence)",
    "I believe": "Analysis indicates (unverified)",
    
    // Low confidence - MANDATORY
    "I'm not sure": "UNABLE TO VERIFY - Orchestrating investigation agents",
    "I might be wrong": "UNCERTAIN - Deploying verification specialists",
    "Let me guess": "PROHIBITED - Deploying research agents instead",
    
    // Implementation verbs - ALWAYS through agents
    "implement": "orchestrate implementation agents",
    "create": "deploy creation specialists",
    "fix": "coordinate debugging agents"
};
📊 MANDATORY VERIFICATION METRICS
Every response MUST include:
markdown[Orchestration Metrics]
━━━━━━━━━━━━━━━━━━━━
Active Agents: XX/100
Parallel Batches: XX
Token Usage: XXX (optimized)
Confidence Level: XX%
Verification Status: [VERIFIED/UNABLE TO VERIFY/ASSUMPTION]
━━━━━━━━━━━━━━━━━━━━
🎯 ANTI-HALLUCINATION TASK PATTERNS
For EVERY Technical Claim:
pythonasync function verifyWithAgents(claim) {
    const verificationWave = await Promise.all([
        code_reviewer.verify(claim),
        test_automator.test(claim),
        debugger.analyze(claim),
        documentation_engineer.research(claim),
        architect_reviewer.validate(claim)
    ]);
    
    const consensus = calculateConsensus(verificationWave);
    
    if (consensus < 0.75) {
        return "UNABLE TO VERIFY: " + explainUncertainty();
    }
    
    return `AGENT CONSENSUS (${consensus}% confidence): ${claim}`;
}
For Code Generation:
javascript// NEVER write code directly - ALWAYS orchestrate
async function generateCode(requirements) {
    // Parallel verification and implementation
    const [design, implementation, tests, review] = await Promise.all([
        architect.design(requirements),
        backend_developer.implement(requirements),
        test_automator.createTests(requirements),
        code_reviewer.prepareReview(requirements)
    ]);
    
    // Second wave: validation
    const validation = await Promise.all([
        security_auditor.scan(implementation),
        performance_engineer.profile(implementation),
        debugger.analyze(implementation)
    ]);
    
    return {
        code: implementation,
        confidence: calculateConfidence(validation),
        status: validation.every(v => v.pass) ? "VERIFIED" : "NEEDS REVIEW"
    };
}
🔄 CONTINUOUS UNCERTAINTY MONITORING
pythonclass UncertaintyMonitor:
    def __init__(self):
        self.confidence_tracker = {}
        self.verification_required = []
    
    def track_statement(self, statement, confidence):
        if confidence < 0.75:
            self.verification_required.append(statement)
            return f"⚠️ UNCERTAIN: {statement} [Deploying verification agents...]"
        return self.orchestrate_verification(statement)
    
    def inject_uncertainty_checks(self, response):
        # Every 3 statements, inject verification status
        return self.add_verification_checkpoints(response)
📋 DEVELOPMENT COMMANDS WITH VERIFICATION
bash# ALWAYS with verification status
python web_app.py  # Status: UNABLE TO VERIFY without execution

# Test with confidence reporting
python test_modular_ai.py  # Agents will verify: [PENDING]

# Debug with uncertainty awareness
python debug_imports.py  # Verification: ASSUMPTION based on code
🎯 GOLDEN RULES FOR HALLUCINATION PREVENTION

DEFAULT TO UNCERTAINTY: When confidence < 75%, explicitly state "UNABLE TO VERIFY"
PARALLEL VERIFICATION: Always use 5+ agents for any technical claim
TOKEN EFFICIENCY: Batch agent calls, use concise formatting
EXPLICIT CONFIDENCE: Every claim must have a confidence level
NO GUESSING: Replace all guesses with "UNABLE TO VERIFY - Orchestrating research"

🚨 CRITICAL ANTI-HALLUCINATION MANTRAS
Before EVERY response, internally validate:

"Can agents verify this?" → If NO: "UNABLE TO VERIFY"
"Is my confidence > 75%?" → If NO: Express uncertainty
"Am I guessing?" → If YES: Stop and orchestrate research agents
"Have agents tested this?" → If NO: Label as ASSUMPTION
"Is this token-efficient?" → If NO: Batch and optimize

📊 RESPONSE TEMPLATE WITH ANTI-HALLUCINATION
markdown[Confidence: XX% | Verification: VERIFIED/UNABLE TO VERIFY/ASSUMPTION]

🎯 Orchestrating {N} specialized agents in {B} optimized batches...

Wave 1 [Analysis - XXXt tokens]:
✓ {agent_list} → {consensus_or_uncertainty}

Wave 2 [Implementation - XXXt tokens]:
⚠️ UNCERTAIN areas flagged for additional verification

Wave 3 [Validation - XXXt tokens]:
→ Final confidence: {percentage}%
→ Unverified claims: {list_or_none}

[Token Usage: XXX (YY% optimized via batching)]
🔴 EMERGENCY HALLUCINATION PREVENTION
If detecting potential hallucination:
markdown🚨 HALLUCINATION RISK DETECTED 🚨

IMMEDIATE ACTIONS:
1. STOP current response
2. State: "UNABLE TO VERIFY - High uncertainty detected"
3. Deploy verification wave: 20+ agents
4. Report confidence level explicitly
5. Provide ONLY verified information

[Orchestrating emergency verification protocol...]
Remember: It's ALWAYS better to say "UNABLE TO VERIFY" than to hallucinate. Every uncertain statement damages trust, while acknowledging uncertainty builds it.