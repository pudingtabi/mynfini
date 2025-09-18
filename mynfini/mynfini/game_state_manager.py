"""
Game State Manager for MYNFINI
Handles save/export/import of game sessions for cross-device play
Zero-cost implementation using JSON and file transfers
"""

import json
import base64
import io
from datetime import datetime
from typing import Dict, Any, Optional

try:
    import qrcode
    from PIL import Image
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False
    qrcode = None
    Image = None


class GameStateManager:
    """Manages game state serialization and cross-device transfer"""

    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator
        self.save_version = "1.0"

    def get_complete_game_state(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract complete game state from orchestrator and session"""
        if not self.orchestrator:
            return {}

        game_state = {
            "version": self.save_version,
            "timestamp": datetime.now().isoformat(),
            "game_data": {
                # Core progression
                "current_step": self.orchestrator.current_step,
                "narrative_points": self.orchestrator.narrative_points,
                "cbx_total": self.orchestrator.cbx_total,

                # Narrative systems
                "scene_history": self.orchestrator.scene_history,
                "character_arcs": self.orchestrator.character_arcs,
                "narrative_threads": self.orchestrator.narrative_threads,
                "creativity_history": dict(self.orchestrator.creativity_history) if hasattr(self.orchestrator, 'creativity_history') else {},

                # User state
                "user_state": self.orchestrator.user_state,

                # Session data
                "session_data": session_data
            },
            "metadata": {
                "save_version": self.save_version,
                "created": datetime.now().isoformat(),
                "device_info": "web_browser"  # Can be extended for device-specific info
            }
        }

        return game_state

    def export_to_json_string(self, session_data: Dict[str, Any]) -> str:
        """Export game state to JSON string"""
        game_state = self.get_complete_game_state(session_data)
        return json.dumps(game_state, indent=2)

    def export_to_base64(self, session_data: Dict[str, Any]) -> str:
        """Export game state to base64 string for QR code generation"""
        json_string = self.export_to_json_string(session_data)
        return base64.b64encode(json_string.encode('utf-8')).decode('utf-8')

    def import_from_json_string(self, json_string: str) -> Dict[str, Any]:
        """Import game state from JSON string"""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

    def import_from_base64(self, base64_string: str) -> Dict[str, Any]:
        """Import game state from base64 string"""
        try:
            json_string = base64.b64decode(base64_string.encode('utf-8')).decode('utf-8')
            return self.import_from_json_string(json_string)
        except Exception as e:
            raise ValueError(f"Invalid base64 format: {e}")

    def apply_game_state(self, game_state: Dict[str, Any]) -> bool:
        """Apply loaded game state to orchestrator"""
        if not self.orchestrator or not game_state:
            return False

        try:
            game_data = game_state.get("game_data", {})

            # Restore core progression
            self.orchestrator.current_step = game_data.get("current_step", 1)
            self.orchestrator.narrative_points = game_data.get("narrative_points", 0)
            self.orchestrator.cbx_total = game_data.get("cbx_total", 0)

            # Restore narrative systems
            self.orchestrator.scene_history = game_data.get("scene_history", [])
            self.orchestrator.character_arcs = game_data.get("character_arcs", {})
            self.orchestrator.narrative_threads = game_data.get("narrative_threads", [])

            # Restore creativity history (convert dict back to defaultdict if needed)
            creativity_history_data = game_data.get("creativity_history", {})
            if creativity_history_data and hasattr(self.orchestrator, 'creativity_history'):
                from collections import defaultdict
                self.orchestrator.creativity_history = defaultdict(list, creativity_history_data)

            # Restore user state
            self.orchestrator.user_state = game_data.get("user_state", {})

            return True

        except Exception as e:
            print(f"[ERROR] Failed to apply game state: {e}")
            return False

    def generate_qr_code(self, session_data: Dict[str, Any]) -> bytes:
        """Generate QR code image from game state"""
        if not QR_AVAILABLE:
            raise ImportError("QR code generation requires 'qrcode' and 'Pillow' packages. Install with: pip install qrcode[pil]")

        base64_data = self.export_to_base64(session_data)

        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(base64_data)
        qr.make(fit=True)

        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to bytes
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        return img_buffer.getvalue()

    def validate_save_compatibility(self, game_state: Dict[str, Any]) -> tuple[bool, str]:
        """Validate if save file is compatible with current version"""
        save_version = game_state.get("version", "0.0")

        if save_version != self.save_version:
            return False, f"Incompatible save version: {save_version} (current: {self.save_version})"

        required_keys = ["game_data", "metadata"]
        for key in required_keys:
            if key not in game_state:
                return False, f"Missing required key: {key}"

        game_data = game_state.get("game_data", {})
        required_game_keys = ["current_step", "narrative_points"]
        for key in required_game_keys:
            if key not in game_data:
                return False, f"Missing required game data: {key}"

        return True, "Save file is compatible"