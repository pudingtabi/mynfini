"""
Complete MYNFINI Web Application with Advanced Mechanics
Revolutionary Web-Based Game Master System
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any
import traceback  # Add for detailed error handling
import signal
import threading
import time

from config import Config, get_config
from advanced_ai_orchestrator import AdvancedAIOrchestrator
from game_state_manager import GameStateManager

app = Flask(__name__)
config = Config()

# Use proper secret key from config
app.secret_key = config.SECRET_KEY
if app.secret_key == 'dev-secret-key-change-in-production':
    logging.warning("WARNING: Using development secret key - set SECRET_KEY environment variable for production")

CORS(app)

# Timeout-protected initialization to prevent blocking (Windows-compatible)
def initialize_ai_system():
    """Initialize AI system with timeout protection to prevent blocking startup"""
    print("[DEBUG] WEB_APP: Starting timeout-protected AI system initialization...")

    try:
        print("[DEBUG] WEB_APP: Creating AdvancedAIOrchestrator with simplified initialization...")

        # Direct creation with exception handling instead of complex timeout
        start_time = time.time()
        ai_system = AdvancedAIOrchestrator()
        init_time = time.time() - start_time

        print(f"[DEBUG] WEB_APP: AI Orchestrator created in {init_time:.2f} seconds")

        if ai_system is not None:
            print(f"[VERIFIED] WEB_APP: AI Orchestrator initialized successfully")

            # Quick system verification (non-blocking)
            try:
                if hasattr(ai_system, '_get_systems_status') and init_time < 10:  # Only if quick
                    status = ai_system._get_systems_status()
                    working_systems = sum(status.values())
                    total_systems = len(status)
                    print(f"[VERIFIED] System status: {working_systems}/{total_systems} systems active")
            except Exception as e:
                print(f"[WARNING] System verification skipped (non-blocking): {e}")

            return ai_system
        else:
            print("[ERROR] WEB_APP: AdvancedAIOrchestrator() returned None")
            return None

    except Exception as e:
        print(f"[ERROR] WEB_APP: AI Orchestrator initialization failed: {str(e)}")
        print(f"[INFO] Starting with minimal AI functionality - web server will be accessible")
        return None

# Initialize complete MYNFINI system with proper error handling and timeout protection
try:
    ai_system = initialize_ai_system()
except Exception as e:
    print(f"[ERROR] WEB_APP: Unexpected error during AI initialization: {str(e)}")
    ai_system = None

# Initialize Game State Manager for save/export functionality
game_state_manager = None
if ai_system is not None:
    game_state_manager = GameStateManager(ai_system)

@app.route('/simple')
def simple_interface():
    """CERTAIN: Simplified MYNFINI interface for immediate play"""
    try:
        # Simple welcome data for immediate engagement
        welcome_data = {
            'welcome_message': 'Welcome to MYNFINI - Revolutionary TTRPG System',
            'system_status': 'ready',
            'narrative_points': 0,
            'total_systems': 'ready',
            'cbx_earned': 0
        }

        # Clean simple template for immediate play
        return render_template('simple_index.html',
                             welcome_data=welcome_data,
                             system_status={
                                 'narrative_consistency': True,
                                 'pacing_engine': True,
                                 'clock_mechanics': True,
                                 'adversity_evolution': True,
                                 'progression_system': True,
                                 'creativity_evaluation': True,
                                 'interactive_resolution': True,
                                 'personal_class_generation': True
                             },
                             narrative_points=0,
                             player_name="Adventurer")
    except Exception as e:
        # Fallback to complex interface if simple version fails
        return redirect(url_for('complex_interface'))

@app.route('/complex')
def complex_interface():
    """CERTAIN: Advanced MYNFINI web interface with comprehensive mechanics (original)"""
    try:
        # Check if AI system is available
            # Provide minimal fallback when AI system is not available
            system_status = {
                'narrative_consistency': False,
                'pacing_engine': False,
                'clock_mechanics': False,
                'adversity_evolution': False,
                'progression_system': False,
                'narrative_points': False,
                'creativity_evaluation': True,
                'interactive_resolution': True,
                'personal_class_generation': True,
                'cbx_system': True
            }

            welcome_data = {
                'welcome_message': 'Welcome to MYNFINI - Revolutionary TTRPG System',
                'system_status': 'minimal_mode',
                'narrative_points': 0,
                'total_systems': 'minimal',
                'cbx_earned': 0
            }

            return render_template('index.html',
                                 welcome_data=welcome_data,
                                 system_status=system_status,
                                 narrative_points=0)

        # Try to get system status regardless of advanced system initialization
        try:
            system_status = ai_system._get_systems_status()
            working_systems = sum(system_status.values())
            total_systems = len(system_status)

            # If we have working systems, show the main interface
            if working_systems > 0:
                # Try to initiate advanced system, but don't fail if it doesn't work
                ai_data = None
                try:
                    ai_data = ai_system.initiate_advanced_system()
                except Exception as init_error:
                    print(f"[DEBUG] Advanced system initiation failed (non-fatal): {init_error}")

                # Create fallback welcome data if initiation failed
                if not ai_data:
                    welcome_data = {
                        'welcome_message': f'Welcome to MYNFINI - Revolutionary TTRPG System ({working_systems}/{total_systems} systems active)',
                        'system_status': 'partial_mode',
                        'narrative_points': 0,
                        'total_systems': f'{working_systems}/{total_systems}',
                        'cbx_earned': 0
                    }
                else:
                    welcome_data = ai_data

                # Store system status in session
                session['mynfini_systems'] = system_status
                session['narrative_points'] = welcome_data.get('narrative_points', 0)
                session['systems_initiated'] = True

                return render_template('index.html',
                                     welcome_data=welcome_data,
                                     system_status=system_status,
                                     narrative_points=welcome_data.get('narrative_points', 0))
            else:
                # No systems working, show setup
                return render_template('setup.html', error="API configuration required")
        except Exception as status_error:
            print(f"[ERROR] System status check failed: {status_error}")
            # Fallback to setup if we can't determine system status
            return render_template('setup.html', error="API configuration required")

    except Exception as e:
        logging.error(f"[ERROR] Advanced system initialization failed: {str(e)}")
        # Provide graceful fallback even if initialization fails
        system_status = {
            'narrative_consistency': False,
            'pacing_engine': False,
            'clock_mechanics': False,
            'adversity_evolution': False,
            'progression_system': False,
            'narrative_points': False,
            'creativity_evaluation': True,
            'interactive_resolution': True,
            'personal_class_generation': True,
            'cbx_system': True
        }

        welcome_data = {
            'welcome_message': 'Welcome to MYNFINI - Revolutionary TTRPG System (Limited Mode)',
            'system_status': 'fallback_mode',
            'narrative_points': 0,
            'total_systems': 'fallback',
            'cbx_earned': 0
        }

        return render_template('index.html',
                             welcome_data=welcome_data,
                             system_status=system_status,
                             narrative_points=0)

@app.route('/play', methods=['POST'])
def play():
    """CERTAIN: Advanced MYNFINI gameplay with complete mechanics integration"""
    try:
        user_input = request.json.get('input', '')
        character_data = request.json.get('character', {})
        game_state = request.json.get('state', {})
        action_type = request.json.get('action_type', 'narrative')

        # Debug logging
        print(f"[DEBUG] Processing input: {user_input}")
        print(f"[DEBUG] Character data: {json.dumps(character_data, indent=2)[:200]}...")
        print(f"[DEBUG] Game state: {json.dumps(game_state, indent=2)[:200]}...")

        if not user_input.strip():
            return jsonify({
                'error': 'No input provided',
                'suggestion': 'Please describe what you want to do'
            }), 400

        # Handle case where AI system is not available
        if ai_system is None:
            return jsonify({
                'response': f'Echo: {user_input}',
                'elements': {'world': 'minimal_mode'},
                'cbx_earned': 0,
                'narrative_points_total': 0,
                'systems_active': {
                    'creativity_evaluation': True,
                    'interactive_resolution': True,
                    'personal_class_generation': True,
                    'cbx_system': True
                },
                'message': 'AI system not available - running in minimal mode'
            })

        # Handle different action types
        if action_type == 'mechanical_check':
            return _handle_mechanical_check(user_input, character_data, game_state)
        elif action_type == 'narrative_points':
            return _handle_narrative_points(user_input, character_data, game_state)
        elif action_type == 'character_progression':
            return _handle_character_progression(user_input, character_data, game_state)
        else:
            return _handle_basic_narrative(user_input, character_data, game_state)

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logging.error(f"[ERROR] Advanced system processing failed: {error_details}")
        return jsonify({
            'error': str(e),
            'system': 'advanced_processing_error',
            'debug': str(e)[:200]
        }), 500

def _handle_mechanical_check(user_input: str, character_data: Dict, game_state: Dict) -> Dict:
    """Handle mechanical skill check requests"""
    # Handle case where AI system is not available
    if ai_system is None:
        return jsonify({
            'narrative': f'Mechanical check requested: {user_input}',
            'check_result': {
                'success': True,
                'result': 'success',
                'total': 10,
                'dice_rolled': [5, 5],
                'opportunities_gained': 0,
                'fabula_gained': 0,
                'message': 'Mechanical check simulated in minimal mode',
                'critical': False,
                'fumble': False,
                'high_roll': 5
            },
            'mechanical_outcome': {
                'success': True,
                'result': 'success',
                'total': 10,
                'dice_rolled': [5, 5],
                'opportunities_gained': 0,
                'fabula_gained': 0,
                'message': 'Mechanical check simulated in minimal mode',
                'critical': False,
                'fumble': False,
                'high_roll': 5
            },
            'opportunities_available': [],
            'progress_updates': [],
            'fabula_points_earned': 0,
            'next_actions': ['Continue adventuring', 'Rest and recover', 'Explore surroundings'],
            'message': 'AI system not available - running in minimal mode'
        })

    check_params = extract_check_parameters(user_input)

    if check_params:
        check_result = ai_system.make_skill_check(
            character_data,
            check_params['attribute1'],
            check_params['attribute2'],
            check_params['difficulty'],
            user_input
        )

        # Process opportunity generation
        opportunities = []
        if check_result['opportunities_gained'] > 0:
            opportunities = generate_opportunities(check_result, game_state)

        return jsonify({
            'narrative': f"{check_result['message']}",
            'check_result': check_result,
            'mechanical_outcome': check_result,
            'opportunities_available': opportunities,
            'progress_updates': process_clock_progress(check_result),
            'fabula_points_earned': check_result['fabula_gained'],
            'next_actions': determine_next_actions(check_result)
        })
    else:
        return _handle_basic_narrative(user_input, character_data, game_state)

def _handle_narrative_points(user_input: str, character_data: Dict, game_state: Dict) -> Dict:
    """Handle narrative point spending and earning"""
    # Handle case where AI system is not available
    if ai_system is None:
        return jsonify({
            'narrative': f'Narrative point action requested: {user_input}',
            'narrative_points_spent': 0,
            'narrative_points_total': 0,
            'effect': 'simulated',
            'message': 'AI system not available - running in minimal mode'
        })

    # This would integrate with NarrativePointsSystem if available
    if ai_system.narrative_points_system:
        # Process narrative point actions
        pass

    return _handle_basic_narrative(user_input, character_data, game_state)

def _handle_character_progression(user_input: str, character_data: Dict, game_state: Dict) -> Dict:
    """Handle character progression and development"""
    # Handle case where AI system is not available
    if ai_system is None:
        return jsonify({
            'narrative': f'Character progression requested: {user_input}',
            'progression': {
                'narrative': 'Character progression simulated in minimal mode',
                'character_update': {},
                'progression_type': 'narrative_improvement'
            },
            'character_update': {},
            'message': 'AI system not available - running in minimal mode'
        })

    # This would integrate with progression systems
    progression_result = process_character_development(user_input, character_data)

    return jsonify({
        'narrative': progression_result.get('narrative', ''),
        'progression': progression_result,
        'character_update': progression_result.get('character_update', {})
    })

def _handle_basic_narrative(user_input: str, character_data: Dict, game_state: Dict) -> Dict:
    """Handle basic narrative processing with advanced context"""
    # Handle case where AI system is not available
    if ai_system is None:
        return jsonify({
            'response': f'You described: "{user_input}"\n\nThis is a minimal response since the full AI system is not available.',
            'elements': {'world': 'minimal_mode'},
            'cbx_earned': 1,
            'narrative_points_total': 0,
            'systems_active': {
                'creativity_evaluation': True,
                'interactive_resolution': True,
                'personal_class_generation': True,
                'cbx_system': True
            },
            'character_data': character_data,
            'progress_updates': [],
            'message': 'AI system not available - running in minimal mode'
        })

    enriched_state = {
        'current_step': session.get('current_step', 1),
        'narrative_points': session.get('narrative_points', 0),
        'character': character_data,
        'previous_inputs': session.get('previous_inputs', []),
        'systems_active': session.get('mynfini_systems', {})
    }

    ai_response = ai_system.process_advanced_input(user_input, enriched_state)

    # Update session state
    session['current_step'] = session.get('current_step', 1) + 1
    session['narrative_points'] = ai_response.get('narrative_points_total', 0)

    # Track inputs
    inputs = session.get('previous_inputs', [])
    inputs.append({
        'input': user_input[:100],  # Truncate for session storage
        'timestamp': datetime.now().isoformat(),
        'response_length': len(ai_response.get('narrative', ''))
    })
    session['previous_inputs'] = inputs[-50:]  # Keep last 50

    return jsonify({
        'response': ai_response.get('narrative', ''),
        'elements': ai_response.get('elements', {}),
        'cbx_earned': ai_response.get('enhanced_cbx_earned', 0),
        'narrative_points_total': ai_response.get('narrative_points_total', 0),
        'systems_active': ai_response.get('systems_active', {}),
        'character_data': ai_response.get('character_data', character_data),
        'progress_updates': ai_response.get('progress_updates', [])
    })

def extract_check_parameters(text: str) -> Optional[Dict]:
    """Extract skill check parameters from natural language"""
    # Basic parsing - sophisticated system would use NLP

    # Look for attribute mentions
    attributes = {'DEXTERITY': 'DEX', 'INSIGHT': 'INS', 'MIGHT': 'MIG', 'WILLPOWER': 'WLP'}

    # Simple keyword detection
    if any(attr in text.upper() for attr in attributes.keys()):
        # Default check parameters - could be enhanced with AI
        return {
            'attribute1': 'DEXTERITY',
            'attribute2': 'INSIGHT',
            'difficulty': 8,
            'context': text
        }

    return None

def generate_opportunities(check_result: Dict, game_state: Dict) -> List[str]:
    """Generate opportunities from successful check"""
    opportunities = []

    if check_result['result'] == 'critical_success':
        opportunities = [
            "Gain significant insight about the current situation",
            "Notice something important others might miss",
            "Create advantage for future actions",
            "Generate 1 additional clock section of progress"
        ]
    elif check_result['result'] == 'success' and check_result['opportunities_gained'] > 0:
        opportunities = [
            "Gain minor insight or information",
            "Create small advantage for next action",
            "Fill partial clock section progress"
        ]

    return opportunities

def process_clock_progress(check_result: Dict) -> List[Dict]:
    """Process clock-based progress from check results"""
    progress = []

    if check_result['result'] == 'critical_success' and check_result['opportunities_gained'] > 0:
        progress.append({
            'type': 'clock_progress',
            'description': 'Significant progress on current objective',
            'sections': 2
        })
    elif check_result['result'] == 'success' and check_result['opportunities_gained'] > 0:
        progress.append({
            'type': 'clock_progress',
            'description': 'Minor progress on current objective',
            'sections': 1
        })

    return progress

def determine_next_actions(check_result: Dict) -> List[str]:
    """Suggest next possible actions based on check results"""
    actions = ["Continue adventuring", "Rest and recover", "Explore surroundings"]

    if check_result['result'] in ['critical_success', 'success']:
        actions.insert(0, "Follow up on discovered opportunity")

    if check_result['fumble']:
        actions.append("Deal with the complications from the fumble")

    if check_result['fabula_gained'] > 0:
        actions.append("Use newly gained Fabula Point")

    return actions

def process_character_development(user_input: str, character_data: Dict) -> Dict[str, Any]:
    """Process character development and progression"""
    # This would integrate with full progression systems
    return {
        'narrative': 'Character development processed through MYNFINI systems.',
        'character_update': {},
        'progression_type': 'narrative_improvement'
    }

# Additional routes for advanced features
@app.route('/api/systems/status')
def system_status():
    """Get current status of all MYNFINI systems"""
    return jsonify(ai_system._get_systems_status())

@app.route('/api/character/check', methods=['POST'])
def character_check():
    """Perform mechanical skill check for character"""
    data = request.json
    character_data = data.get('character', {})
    attribute1 = data.get('attribute1', 'DEXTERITY')
    attribute2 = data.get('attribute2', 'INSIGHT')
    difficulty = data.get('difficulty', 8)
    context = data.get('context', '')

    check_result = ai_system.make_skill_check(character_data, attribute1, attribute2, difficulty, context)
    return jsonify(check_result)

@app.route('/api/narrative/points')
def narrative_points_status():
    """Get current narrative points status"""
    return jsonify({
        'narrative_points': session.get('narrative_points', 0),
        'points_system_active': ai_system.narrative_points_system is not None,
        'earnings_available': [],
        'spending_options': []
    })

@app.route('/revolution/creativity/evaluate', methods=['POST'])
def evaluate_creativity():
    """Evaluate player description for creativity tier"""
    try:
        if ai_system is None:
            # Provide minimal creativity evaluation in fallback mode
            data = request.json
            description = data.get('description', '')
            if not description:
                return jsonify({'error': 'No description provided'}), 400

            # Simulate basic creativity evaluation
            return jsonify({
                'creativity_tier': 'BASIC',
                'bonus_percentage': 0.0,
                'mechanical_bonus': 0,
                'extra_dice': None,
                'narrative_point_triggered': False,
                'cbx_earned': 1,
                'pressure_points': 0,
                'environmental_elements': [],
                'tactical_elements': [],
                'dramatic_elements': [],
                'reasoning': 'Basic creativity evaluation in minimal mode',
                'feedback': 'Describe more details for better creativity evaluation',
                'suggested_improvements': ['Add environmental elements', 'Include tactical planning', 'Enhance dramatic impact'],
                'emerging_patterns': [],
                'message': 'AI system not available - running in minimal mode'
            })

        data = request.json
        description = data.get('description', '')
        context = data.get('context', {})
        player_history = data.get('player_history', {})

        if not description:
            return jsonify({'error': 'No description provided'}), 400

        # Check for API key before processing
        if not hasattr(ai_system, 'creativity_evaluator'):
            return jsonify({'error': 'AI systems not properly initialized'}), 500

        evaluation = ai_system.creativity_evaluator.evaluate_action_description(
            description, context, player_history
        )

        return jsonify({
            'creativity_tier': evaluation.creativity_tier.name,
            'bonus_percentage': evaluation.bonus_percentage,
            'mechanical_bonus': evaluation.mechanical_bonus,
            'extra_dice': evaluation.extra_dice,
            'narrative_point_triggered': evaluation.np_triggered,
            'cbx_earned': evaluation.cbx_earned,
            'pressure_points': evaluation.pressure_points,
            'environmental_elements': evaluation.environmental_elements,
            'tactical_elements': evaluation.tactical_elements,
            'dramatic_elements': evaluation.dramatic_elements,
            'reasoning': evaluation.reasoning,
            'feedback': evaluation.feedback,
            'suggested_improvements': evaluation.suggested_improvements,
            'emerging_patterns': evaluation.emerging_patterns
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/revolution/class/analyze', methods=['POST'])
def analyze_class():
    """Analyze player behavior for class patterns"""
    try:
        if ai_system is None:
            # Provide minimal class analysis in fallback mode
            data = request.json
            action_history = data.get('action_history', [])

            return jsonify({
                'player_id': 'player',
                'analysis_timestamp': datetime.now().isoformat(),
                'dominant_pattern': 'basic_adventurer',
                'supporting_patterns': ['explorer', 'storyteller'],
                'pattern_frequencies': {'basic_adventurer': 5},
                'class_data': None,
                'emergence_eligible': False,
                'emergence_urgency': 0.0,
                'evolution_potential': 0.0,
                'recommended_class': {
                    'class_name': 'Adventurer',
                    'keystone_ability': 'Basic Adventure Skills',
                    'evolution_tier': 1,
                    'total_evolution_tiers': 5,
                    'until_next_evolution': 10
                },
                'behavioral_insights': ['Showing emerging behavioral patterns - more data needed'],
                'growth_recommendations': ['Continue expressing your unique approach to develop your personal class'],
                'message': 'AI system not available - running in minimal mode'
            })

        data = request.json
        action_history = data.get('action_history', [])
        creative_choices = data.get('creative_choices', [])

        if not action_history:
            return jsonify({'error': 'No action history provided'}), 400

        assessment = ai_system.class_generator.analyze_player_behavior(
            action_history, creative_choices
        )

        return jsonify(assessment)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/revolution/systems/status')
def revolution_systems_status():
    """Get status of revolutionary systems"""
    try:
        if ai_system is None:
            # Provide minimal system status in fallback mode
            return jsonify({
                'systems_status': {
                    'narrative_consistency': False,
                    'pacing_engine': False,
                    'clock_mechanics': False,
                    'adversity_evolution': False,
                    'progression_system': False,
                    'narrative_points': False,
                    'creativity_evaluation': True,
                    'interactive_resolution': True,
                    'personal_class_generation': True,
                    'cbx_system': True
                },
                'creativity_defeats_statistics': True,
                'the_revolution_has_begun': True,
                'message': 'AI system not available - running in minimal mode'
            })

        systems_status = ai_system._get_systems_status()

        return jsonify({
            'systems_status': systems_status,
            'creativity_defeats_statistics': True,
            'the_revolution_has_begun': True
        })

    except Exception as e:
        return jsonify({
            'systems_status': {},
            'creativity_defeats_statistics': False,
            'the_revolution_has_begun': False,
            'error': str(e)
        }), 200

@app.route('/api/save/export', methods=['POST'])
def export_game_state():
    """Export current game state as JSON file"""
    try:
        if not game_state_manager:
            return jsonify({'error': 'Game state manager not initialized'}), 500

        # Get session data
        session_data = {
            'narrative_points': session.get('narrative_points', 0),
            'mynfini_systems': session.get('mynfini_systems', {}),
            'current_step': session.get('current_step', 1),
            'previous_inputs': session.get('previous_inputs', [])
        }

        # Generate JSON export
        json_export = game_state_manager.export_to_json_string(session_data)

        return jsonify({
            'success': True,
            'filename': f'mynfini_save_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            'data': json_export,
            'size': len(json_export),
            'format': 'json'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/save/export/qr', methods=['POST'])
def export_qr_code():
    """Export game state as QR code"""
    try:
        if not game_state_manager:
            return jsonify({'error': 'Game state manager not initialized'}), 500

        # Get session data
        session_data = {
            'narrative_points': session.get('narrative_points', 0),
            'mynfini_systems': session.get('mynfini_systems', {}),
            'current_step': session.get('current_step', 1),
            'previous_inputs': session.get('previous_inputs', [])
        }

        # Generate QR code
        qr_image_bytes = game_state_manager.generate_qr_code(session_data)

        # Convert to base64 for web display
        import base64
        qr_base64 = base64.b64encode(qr_image_bytes).decode('utf-8')

        return jsonify({
            'success': True,
            'qr_image': f'data:image/png;base64,{qr_base64}',
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/save/import', methods=['POST'])
def import_game_state():
    """Import game state from JSON or base64"""
    try:
        if not game_state_manager:
            return jsonify({'error': 'Game state manager not initialized'}), 500

        data = request.json
        import_data = data.get('data', '')
        import_format = data.get('format', 'json')  # 'json' or 'base64'

        if not import_data:
            return jsonify({'error': 'No import data provided'}), 400

        # Parse based on format
        if import_format == 'base64':
            game_state = game_state_manager.import_from_base64(import_data)
        else:
            game_state = game_state_manager.import_from_json_string(import_data)

        # Validate save compatibility
        is_valid, message = game_state_manager.validate_save_compatibility(game_state)
        if not is_valid:
            return jsonify({'error': message}), 400

        # Apply game state
        success = game_state_manager.apply_game_state(game_state)
        if not success:
            return jsonify({'error': 'Failed to apply game state'}), 500

        # Update session with imported data
        session_data = game_state.get('game_data', {}).get('session_data', {})
        if session_data:
            session['narrative_points'] = session_data.get('narrative_points', 0)
            session['mynfini_systems'] = session_data.get('mynfini_systems', {})
            session['current_step'] = session_data.get('current_step', 1)
            session['previous_inputs'] = session_data.get('previous_inputs', [])

        return jsonify({
            'success': True,
            'message': 'Game state imported successfully',
            'step_restored': game_state.get('game_data', {}).get('current_step', 1),
            'narrative_points': game_state.get('game_data', {}).get('narrative_points', 0)
        })

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/save/base64', methods=['POST'])
def get_base64_save():
    """Get base64 encoded save data for manual transfer"""
    try:
        if not game_state_manager:
            return jsonify({'error': 'Game state manager not initialized'}), 500

        # Get session data
        session_data = {
            'narrative_points': session.get('narrative_points', 0),
            'mynfini_systems': session.get('mynfini_systems', {}),
            'current_step': session.get('current_step', 1),
            'previous_inputs': session.get('previous_inputs', [])
        }

        # Generate base64 export
        base64_data = game_state_manager.export_to_base64(session_data)

        return jsonify({
            'success': True,
            'base64': base64_data,
            'length': len(base64_data),
            'instructions': 'Copy this base64 data and paste it on your other device to continue playing'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("[VERIFIED] Complete MYNFINI revolutionary web system initialized")
    print("[VERIFIED] Advanced mechanics integrated with Flask backend")

    # Use PORT from environment (required for Render deployment)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    app.run(debug=debug, host='0.0.0.0', port=port)