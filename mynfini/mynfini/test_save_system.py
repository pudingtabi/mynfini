#!/usr/bin/env python3
"""
Test script for MYNFINI cross-device save functionality
Verifies save export/import system works correctly
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_state_manager import GameStateManager
from advanced_ai_orchestrator import AdvancedAIOrchestrator


def test_save_system():
    """Test the complete save system functionality"""
    print("Testing MYNFINI Cross-Device Save System")
    print("=" * 50)

    # Test 1: Initialize systems
    print("\n1. Initializing AI Orchestrator...")
    try:
        orchestrator = AdvancedAIOrchestrator()
        print("SUCCESS: AI Orchestrator initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize orchestrator: {e}")
        return False

    # Test 2: Initialize Game State Manager
    print("\n2. Initializing Game State Manager...")
    try:
        save_manager = GameStateManager(orchestrator)
        print("✅ Game State Manager initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize game state manager: {e}")
        return False

    # Test 3: Add some test data
    print("\n3. Adding test game data...")
    try:
        # Simulate some game progress
        orchestrator.current_step = 5
        orchestrator.narrative_points = 150
        orchestrator.cbx_total = 75

        # Add some test scene history
        orchestrator.scene_history.append({
            'scene': 'Test Scene Entry',
            'timestamp': '2025-01-17T12:00:00Z',
            'narrative_points_earned': 10
        })

        # Add some test character arcs
        orchestrator.character_arcs['TestPlayer'] = [
            {
                'archetype': 'Seeker',
                'level': 3,
                'discoveries': 5
            }
        ]

        # Add test narrative threads
        orchestrator.narrative_threads.append({
            'id': 'test_thread_1',
            'title': 'The Great Adventure',
            'status': 'active'
        })

        print("✅ Test data added successfully")
    except Exception as e:
        print(f"❌ Failed to add test data: {e}")
        return False

    # Test 4: Export game state
    print("\n4. Testing save export...")
    try:
        session_data = {
            'narrative_points': 150,
            'mynfini_systems': {'test_system': True},
            'current_step': 5,
            'previous_inputs': ['Test input 1', 'Test input 2']
        }

        # Test JSON export
        json_export = save_manager.export_to_json_string(session_data)
        parsed = json.loads(json_export)

        print(f"✅ JSON export successful - size: {len(json_export)} bytes")
        print(f"   - Version: {parsed.get('version', 'N/A')}")
        print(f"   - Contains game_data: {'game_data' in parsed}")
        print(f"   - Current step: {parsed.get('game_data', {}).get('current_step', 'N/A')}")
        print(f"   - Narrative points: {parsed.get('game_data', {}).get('narrative_points', 'N/A')}")

        # Test base64 export
        base64_export = save_manager.export_to_base64(session_data)
        print(f"✅ Base64 export successful - size: {len(base64_export)} characters")

    except Exception as e:
        print(f"❌ Export failed: {e}")
        return False

    # Test 5: QR code generation
    print("\n5. Testing QR code generation...")
    try:
        qr_bytes = save_manager.generate_qr_code(session_data)
        print(f"✅ QR code generated successfully - size: {len(qr_bytes)} bytes")
    except Exception as e:
        print(f"❌ QR code generation failed: {e}")
        return False

    # Test 6: Import validation
    print("\n6. Testing save import validation...")
    try:
        # Validate the exported data
        game_state = json.loads(json_export)
        is_valid, message = save_manager.validate_save_compatibility(game_state)

        if is_valid:
            print(f"✅ Save validation passed: {message}")
        else:
            print(f"❌ Save validation failed: {message}")
            return False

    except Exception as e:
        print(f"❌ Save validation failed: {e}")
        return False

    # Test 7: Import functionality
    print("\n7. Testing import from base64...")
    try:
        # Import the base64 data
        imported_state = save_manager.import_from_base64(base64_export)
        game_data = imported_state.get('game_data', {})

        print(f"✅ Import successful")
        print(f"   - Imported step: {game_data.get('current_step', 'N/A')}")
        print(f"   - Imported narrative points: {game_data.get('narrative_points', 'N/A')}")
        print(f"   - Character arcs: {len(game_data.get('character_arcs', {}))}")
        print(f"   - Scene history: {len(game_data.get('scene_history', []))}")

    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

    # Test 8: Apply game state
    print("\n8. Testing game state application...")
    try:
        # Reset orchestrator state
        orchestrator.current_step = 1
        orchestrator.narrative_points = 0
        orchestrator.scene_history = []
        orchestrator.character_arcs = {}
        orchestrator.narrative_threads = []

        # Apply the imported state
        success = save_manager.apply_game_state(imported_state)

        if success:
            print(f"✅ Game state applied successfully")
            print(f"   - Current step: {orchestrator.current_step}")
            print(f"   - Narrative points: {orchestrator.narrative_points}")
            print(f"   - Scene history count: {len(orchestrator.scene_history)}")
            print(f"   - Character arcs: {len(orchestrator.character_arcs)}")
        else:
            print(f"❌ Failed to apply game state")
            return False

    except Exception as e:
        print(f"❌ Game state application failed: {e}")
        return False

    print("\n" + "=" * 50)
    print("✅ All tests passed! Cross-device save system is working correctly.")
    print("\n📱 Usage Instructions:")
    print("1. Click '💾 Export Save' to download save file")
    print("2. Click '📱 QR Transfer' to generate QR code for mobile scanning")
    print("3. Click '📋 Copy Save' to get base64 data for copy/paste")
    print("4. Click '📥 Import Save' to load save from file/paste")
    print("\n💡 Transfer saves between devices using any of these methods!")

    return True


if __name__ == '__main__':
    success = test_save_system()
    sys.exit(0 if success else 1)