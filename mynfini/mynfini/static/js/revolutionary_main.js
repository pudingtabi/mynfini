/**
 * Revolutionary MYNFINI Web Interface Controller
 * Complete mechanics integration for web-based AI Game Master
 */

class RevolutionaryAIGameInterface {
    constructor() {
        this.currentStep = 1;
        this.cbxTotal = 0;
        this.narrativePoints = 0;
        this.gameState = {};
        this.actionType = 'basic_narrative';
        this.previousInputs = [];
        this.characterProfile = {};
        this.isLoading = false;
        this.systemsStatus = {};

        this.initializeInterface();
        console.log('[VERIFIED] Revolutionary MYNFINI interface initialized with advanced mechanics');
    }

    initializeInterface() {
        // Set up event listeners
        this.setupEventListeners();

        // Initialize UI elements
        this.updateStepIndicator();
        this.initializeMetricsDisplay();

        // Auto-focus on input
        document.getElementById('user-input').focus();

        // Load any saved character profile
        this.loadCharacterProfile();
    }

    setupEventListeners() {
        const inputElement = document.getElementById('user-input');

        // Handle enter key for submission
        inputElement.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Real-time action type detection
        inputElement.addEventListener('input', (e) => {
            this.detectActionType(e.target.value);
        });

        // Loading state management
        inputElement.addEventListener('focus', this.onInputFocus.bind(this));
        inputElement.addEventListener('blur', this.onInputBlur.bind(this));
    }

    detectActionType(text) {
        const lowerText = text.toLowerCase();

        // Clean previous highlights
        this.clearActionButtonHighlights();

        if (lowerText.includes('perform check') || lowerText.includes('roll') ||
            lowerText.includes('skill check') || this.hasAttributeMentions(lowerText)) {
            this.setActionType('mechanical_check');
            document.getElementById('mech-btn').classList.add('active');
        }
        else if (lowerText.includes('narrative point') || lowerText.includes('dramatic moment') ||
                 lowerText.includes('divine intervention') || lowerText.includes('breakthrough')) {
            this.setActionType('narrative_points');
            document.getElementById('np-btn').classList.add('active');
        }
        else if (lowerText.includes('character development') || lowerText.includes('advance') ||
                 lowerText.includes('progress') || lowerText.includes('level up')) {
            this.setActionType('character_progression');
            document.getElementById('progress-btn').classList.add('active');
        }
        else {
            this.setActionType('basic_narrative');
        }
    }

    hasAttributeMentions(text) {
        const attributes = ['dexterity', 'insight', 'might', 'willpower', 'dex', 'ins', 'mig', 'wlp'];
        return attributes.some(attr => text.includes(attr));
    }

    clearActionButtonHighlights() {
        const buttons = document.querySelectorAll('.action-btn');
        buttons.forEach(btn => btn.classList.remove('active'));
    }

    setActionType(actionType) {
        this.actionType = actionType;
        console.log(`[ACTION TYPE SET]: ${actionType}`);
    }

    onInputFocus() {
        document.getElementById('user-input').classList.add('focused');
    }

    onInputBlur() {
        document.getElementById('user-input').classList.remove('focused');
    }

    async sendMessage() {
        if (this.isLoading) return;

        const input = document.getElementById('user-input').value.trim();
        if (!input) {
            this.displayError('Please enter a description of your action or world creation.');
            return;
        }

        try {
            this.setLoadingState(true);
            this.clearError();

            // Prepare character data from profile
            const characterData = this.buildCharacterProfile();

            // Build comprehensive game state
            const gameState = this.buildAdvancedGameState(input);

            console.log(`[SENDING REQUEST]: Action type: ${this.actionType}, Input: "${input}"`);

            const response = await fetch('/play', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Advanced-Mechanics': 'enabled'
                },
                body: JSON.stringify({
                    input: input,
                    character: characterData,
                    state: gameState,
                    action_type: this.actionType
                })
            });

            const data = await response.json();

            if (data.error) {
                console.error('[SYSTEM ERROR]', data.error);
                this.displayError(data.error, data.debug);
                return;
            }

            console.log('[RESPONSE RECEIVED]', {
                responseLength: data.response?.length || 0,
                cbxEarned: data.cbx_earned,
                narrativePoints: data.narrative_points_total,
                hasMechanicalResult: !!data.check_result
            });

            // Display advanced response
            this.displayAdvancedResponse(data);

            // Update game metrics
            this.updateAdvancedMetrics(data);

            // Handle mechanical results
            if (data.check_result) {
                this.displayMechanicalResults(data.check_result);
            }

            // Process opportunities
            if (data.opportunities_available && data.opportunities_available.length > 0) {
                this.displayOpportunities(data.opportunities_available);
            }

            // Save input for history
            this.saveToHistory(input, data.response);

            // Clear input field
            document.getElementById('user-input').value = '';
            document.getElementById('user-input').focus();

        } catch (error) {
            console.error('[NETWORK FAILURE]', error);
            this.displayError('Network connection failed. Check API key configuration.', error.message);
        } finally {
            this.setLoadingState(false);
        }
    }

    buildCharacterProfile() {
        const defaultCharacter = {
            name: 'Player',
            level: 1,
            hp_current: 10,
            hp_max: 10,
            mp_current: 10,
            mp_max: 10,
            ip_current: 10,
            ip_max: 10,
            attributes: {
                'DEXTERITY': 'd8',
                'INSIGHT': 'd8',
                'MIGHT': 'd8',
                'WILLPOWER': 'd8'
            },
            skills: {},
            bonds: [],
            traits: [],
            narrative_points: this.narrativePoints,
            adversity_level: 1,
            character_arc: 'seeking'
        };

        return Object.assign({}, defaultCharacter, this.characterProfile);
    }

    buildAdvancedGameState(inputText) {
        const currentEmotionIntensity = this.estimateEmotionIntensity(inputText);
        const detectedSceneType = this.detectSceneType(inputText);

        return {
            current_step: this.currentStep,
            session_state: this.currentStep <= 5 ? 'SESSION_ZERO' : 'ACTIVE_GAMEPLAY',
            scene_type: detectedSceneType,
            emotional_intensity: currentEmotionIntensity,
            total_inputs: this.previousInputs.length,
            previous_mechanical_results: this.getRecentMechanicalResults(),
            narrative_context: this.buildNarrativeContext(),
            sensory_environment: this.buildSensoryEnvironment(),
            character_arcs: this.characterProfile.character_arcs || {},
            active_clock_projects: this.getActiveClockProjects(),
            adversity_context: this.buildAdversityContext()
        };
    }

    estimateEmotionIntensity(text) {
        const intensity_keywords = {
            high: ['dramatic', 'intense', 'critical', 'urgent', 'desperate', 'epic', 'legendary'],
            medium: ['important', 'significant', 'challenging', 'difficult', 'crucial'],
            low: ['normal', 'casual', 'relaxed', 'exploring', 'inquiring']
        };

        const textLower = text.toLowerCase();
        let intensity = 0;

        Object.entries(intensity_keywords).forEach(([level, keywords]) => {
            keywords.forEach(keyword => {
                if (textLower.includes(keyword)) {
                    intensity += level === 'high' ? 3 : (level === 'medium' ? 2 : 1);
                }
            });
        });

        return Math.min(intensity, 10);
    }

    detectSceneType(text) {
        const textLower = text.toLowerCase();

        if (textLower.includes('combat') || textLower.includes('fight') || textLower.includes('battle') ||
            textLower.includes('conflict') || textLower.includes('challenge')) {
            return 'Conflict';
        }
        else if (textLower.includes('rest') || textLower.includes('recover') || textLower.includes('heal') ||
                 textLower.includes('talk') || textLower.includes('discuss')) {
            return 'Interlude';
        }
        else if (textLower.includes('investigate') || textLower.includes('explore') ||
                 textLower.includes('search') || textLower.includes('analyze')) {
            return 'GM';
        }
        else {
            return 'Standard';
        }
    }

    displayAdvancedResponse(data) {
        const responseContainer = document.getElementById('ai-response');
        let enhancedNarrative = data.response || data.narrative || '';

        if (data.check_result) {
            enhancedNarrative = this.formatMechanicalNarrative(enhancedNarrative, data.check_result);
        }

        responseContainer.innerHTML = enhancedNarrative;
        responseContainer.classList.add('show');
    }

    formatMechanicalNarrative(narrative, checkResult) {
        let enhanced = narrative;

        if (checkResult.critical) {
            enhanced = `**CRITICAL SUCCESS**\n\n${enhanced}\n\n*This exceptional performance grants additional opportunities for advancement.*`;
        } else if (checkResult.fumble) {
            enhanced = `**FUMBLE**\n\n${enhanced}\n\n*Despite the setback, you gain 1 Fabula Point for dealing with complications creatively.*`;
        }

        return enhanced;
    }

    displayMechanicalResults(checkResult) {
        const resultsDiv = document.createElement('div');
        resultsDiv.className = 'mechanical-results';
        resultsDiv.innerHTML = `
            <h4>🎲 Mechanical Results</h4>
            <div><strong>Outcome:</strong> ${checkResult.message}</div>
            <div><strong>Roll:</strong> ${checkResult.dice_rolled.join(' + ')} = ${checkResult.total}</div>
            ${checkResult.opportunities_gained > 0 ? `<div><strong>Opportunities Gained:</strong> ${checkResult.opportunities_gained}</div>` : ''}
            ${checkResult.fabula_gained > 0 ? `<div><strong>Fabula Points Earned:</strong> ${checkResult.fabula_gained}</div>` : ''}
        `;

        const responseContainer = document.getElementById('ai-response');
        responseContainer.appendChild(resultsDiv);
    }

    displayOpportunities(opportunities) {
        const opportunitiesDiv = document.createElement('div');
        opportunitiesDiv.className = 'opportunities-display';
        opportunitiesDiv.innerHTML = `
            <h4>⚡ Available Opportunities</h4>
            <ul class="opportunity-list">
                ${opportunities.map(opp => `<li class="opportunity-item">${opp}</li>`).join('')}
            </ul>
        `;

        const responseContainer = document.getElementById('ai-response');
        responseContainer.appendChild(opportunitiesDiv);
    }

    updateAdvancedMetrics(data) {
        if (data.cbx_earned !== undefined) {
            this.cbxTotal += data.cbx_earned;
            this.animateMetricUpdate('cbx-total', this.cbxTotal);
        }

        if (data.narrative_points_total !== undefined) {
            this.narrativePoints = data.narrative_points_total;
            this.animateMetricUpdate('narrative-points', this.narrativePoints);
        }

        if (this.actionType !== 'mechanical_check' && data.response) {
            this.currentStep++;
            this.updateStepIndicator();
            this.animateMetricUpdate('session-step', this.currentStep);
        }
    }

    animateMetricUpdate(elementId, newValue) {
        const element = document.getElementById(elementId);
        if (!element) return;

        element.style.color = '#00FF00';
        element.style.transform = 'scale(1.1)';
        element.textContent = newValue;

        setTimeout(() => {
            element.style.color = '#FFD700';
            element.style.transform = 'scale(1.0)';
        }, 500);
    }

    updateStepIndicator() {
        for (let i = 1; i <= 5; i++) {
            const stepElement = document.getElementById(`step-${i}`);
            if (stepElement) {
                stepElement.classList.toggle('active', i <= this.currentStep);
            }
        }

        const currentStepElement = document.getElementById('current-step');
        if (currentStepElement) {
            currentStepElement.textContent = Math.min(this.currentStep, 5);
        }
    }

    setLoadingState(show) {
        this.isLoading = show;

        const loadingState = document.getElementById('loading-state');
        const sendBtn = document.getElementById('send-btn');
        const actionButtons = document.querySelectorAll('.action-btn');

        if (show) {
            loadingState.style.display = 'flex';
            sendBtn.disabled = true;
            sendBtn.innerHTML = '<div class="spinner"></div><span>Processing...</span>';
            actionButtons.forEach(btn => btn.disabled = true);
        } else {
            loadingState.style.display = 'none';
            sendBtn.disabled = false;
            sendBtn.innerHTML = '<span>🌍 Send to AI</span>';
            actionButtons.forEach(btn => btn.disabled = false);
        }
    }

    displayError(message, details = '') {
        const errorDiv = document.getElementById('error-display');
        const errorMessage = document.getElementById('error-message');

        errorMessage.innerHTML = `
            <strong>Error:</strong> ${message}
            ${details ? `<br><small style="color: #ff8a80;">Details: ${details}</small>` : ''}
        `;

        errorDiv.classList.add('show');
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        setTimeout(() => {
            errorDiv.classList.remove('show');
        }, 5000);
    }

    clearError() {
        document.getElementById('error-display').classList.remove('show');
    }

    saveToHistory(input, output) {
        const entry = {
            timestamp: new Date().toISOString(),
            input: input,
            output: output.substring(0, 500),
            actionType: this.actionType,
            step: this.currentStep
        };

        this.previousInputs.push(entry);
        localStorage.setItem('mynfini_input_history', JSON.stringify(this.previousInputs.slice(-20)));
    }

    loadCharacterProfile() {
        const saved = localStorage.getItem('mynfini_character_profile');
        if (saved) {
            try {
                this.characterProfile = JSON.parse(saved);
                console.log('[CHARACTER PROFILE LOADED]', this.characterProfile.name);
            } catch (e) {
                console.warn('[CHARACTER PROFILE ERR]', e);
            }
        }
    }

    initializeMetricsDisplay() {
        const style = document.createElement('style');
        style.textContent = `
            .action-btn.active {
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1) !important;
                border: 2px solid #4CAF50 !important;
            }
        `;
        document.head.appendChild(style);
    }
}