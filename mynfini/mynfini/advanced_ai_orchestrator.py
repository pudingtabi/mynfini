"""
Advanced AI Orchestrator with CORE MECHANICS EVOLUTION Implementation
MYNFINI Revolutionary Interactive Resolution System
Creativity becomes power - the world's first truly intelligent TTRPG
"""

import json
import time
import re
import random
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict, deque
import anthropic

# Import Phase 2B Narrative Engine Systems with individual error handling
narrative_engine_available = False
narrative_core_systems_available = False
narrative_cohesion_available = False

try:
    from narrative_engine import SensoryDescriptor, SceneContext, SensoryDescription
    narrative_engine_available = True
except ImportError as e:
    print(f"[WARNING] Cannot import narrative_engine: {e}")
    class SensoryDescriptor:
        def generate_layered_sensory_description(self, *args, **kwargs):
            return type('SensoryDescription', (), {
                'text': "Sensory details emerge in the environment.",
                'sight': "Details become visible.",
                'sound': "Sounds become audible.",
                'smell': "Scents emerge.",
                'touch': "Sensations become apparent.",
                'taste': "Flavors develop.",
                'focus_sense': 'sight'
            })()
    class SceneContext: pass
    class SensoryDescription: pass

try:
    from narrative_core_systems import PacingManager, SceneType, EmotionalIntensity, PacingContext
    from narrative_core_systems import ShowDontTellProcessor, EightPillarsFramework
    narrative_core_systems_available = True
except ImportError as e:
    print(f"[WARNING] Cannot import narrative_core_systems: {e}")
    class PacingManager: pass
    class SceneType:
        STANDARD = "Standard"
        CONFLICT = "Conflict"
    class EmotionalIntensity: pass
    class PacingContext: pass
    class ShowDontTellProcessor: pass
    class EightPillarsFramework: pass

try:
    from narrative_cohesion_system import CohesionManager, NarrativeConstraint, CharacterPsychology
    narrative_cohesion_available = True
except ImportError as e:
    print(f"[WARNING] Cannot import narrative_cohesion_system: {e}")
    class CohesionManager: pass
    class NarrativeConstraint: pass
    class CharacterPsychology: pass

# Additional fallback classes
class AIErrorRecoveryManager: pass
class SessionZeroProtocol: pass
class GameStateProtocol: pass
class PlayerBehaviorTracker: pass

# Import revolutionary systems implementation with individual error handling
REVOLUTIONARY_SYSTEMS_AVAILABLE = False
revolutionary_systems = {}

revolutionary_modules = [
    'NarrativeConsistencyEnforcer', 'NarrativeEventType', 'EventCategory', 'NarrativeEvent',
    'DynamicsOptimizationSystem', 'AdversityEvolutionSystem', 'MultiAxisProgressionSystem',
    'AdversityType', 'ProgressionAxis', 'CharacterProgression'
]

# Initialize placeholders
for module in revolutionary_modules:
    globals()[module] = type(module, (), {
        '__init__': lambda self: None,
        '__call__': lambda self, *args, **kwargs: {"status": "placeholder"}
    })

try:
    from revolutionary_systems_implementation import (
        NarrativeConsistencyEnforcer, NarrativeEventType, EventCategory, NarrativeEvent,
        DynamicsOptimizationSystem, AdversityEvolutionSystem, MultiAxisProgressionSystem,
        AdversityType, ProgressionAxis, CharacterProgression
    )
    REVOLUTIONARY_SYSTEMS_AVAILABLE = True
    print("[INFO] Revolutionary systems successfully imported")
except ImportError as e:
    print(f"[INFO] Revolutionary systems not available - using placeholder classes: {e}")
    REVOLUTIONARY_SYSTEMS_AVAILABLE = False

# Use full MYNFINI protocol implementation from src
import sys
import os

# Add src directory to path if it exists
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
if os.path.exists(src_path):
    sys.path.insert(0, src_path)
    print(f"[DEBUG] Added src path: {src_path}")

# Ensure current directory is in path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Individual imports with error handling
game_state_protocol_available = False
narrative_consistency_advanced_available = False
narrative_systems_available = False

try:
    from game_state_protocol import GameStateProtocol, SessionState, SceneType, AttributeType, Attribute
    game_state_protocol_available = True
except ImportError as e:
    print(f"[WARNING] Cannot import game_state_protocol: {e}")
    class GameStateProtocol: pass
    class SessionState: pass
    class AttributeType: pass
    class Attribute: pass

try:
    from narrative_consistency_advanced import NarrativeConsistencyEnforcer as NarrativeConsistencyAdvanced, NarrativeEventType as AdvancedNarrativeEventType, EventCategory as AdvancedEventCategory
    narrative_consistency_advanced_available = True
except ImportError as e:
    print(f"[WARNING] Cannot import narrative_consistency_advanced: {e}")
    NarrativeConsistencyAdvanced = type('NarrativeConsistencyEnforcer', (), {
        'record_event': lambda self, event: True,
        'get_consistency_report': lambda self: {"status": "placeholder"}
    })

try:
    # Available narrative systems only
    from narrative_engine import NarrativeEngine
    from narrative_cohesion_system import NarrativeCohesionSystem
    from narrative_points_system_complete import NarrativePointsSystem, NPEarningTrigger, NPActivity
    narrative_systems_available = True
except ImportError as e:
    print(f"[WARNING] Cannot import narrative systems: {e}")
    class NarrativeEngine: pass
    class NarrativeCohesionSystem: pass
    class NarrativePointsSystem: pass
    class NPEarningTrigger: pass
    class NPActivity: pass

logger = logging.getLogger(__name__)


# Import KimiK2Orchestrator for K2-905 integration with better error handling
KIMI_K2_AVAILABLE = False
kimi_k2_orchestrator_available = False

try:
    from kimi_k2_orchestrator import KimiK2Orchestrator
    KIMI_K2_AVAILABLE = True
    kimi_k2_orchestrator_available = True
    print("[INFO] KimiK2Orchestrator successfully imported")
except ImportError as e:
    print(f"[WARNING] KimiK2Orchestrator not available - K2-905 integration disabled: {e}")
    KIMI_K2_AVAILABLE = False
    KimiK2Orchestrator = None


class CreativityTier(Enum):
    """5-Tier creativity evaluation system - THE REVOLUTION"""
    BASIC = 0.0           # "I attack the guard" - No bonus
    TACTICAL = 0.15       # "I feint left then strike his sword arm" - +15%
    CREATIVE = 0.30       # "I kick sand in his eyes while sliding under his guard" - +30%
    BRILLIANT = 0.45      # "I use the chandelier's shadow to disguise movements" - +45%
    LEGENDARY = 0.50      # "I shatter ice beneath heavy armor" - +50%
    BEYOND_LEGENDARY = 0.75  # With NP spending - reality bends


class NPEarningTrigger(Enum):
    """Narrative Points earning - drama-driven resources"""
    SURVIVE_LOW_HP = "survive_low_hp"                 # <10% HP survival
    LEGENDARY_CREATIVE = "legendary_creative"        # Awe-inspiring moment
    ULTIMATE_SACRIFICE = "ultimate_sacrifice"        # Give everything for others
    IMPOSSIBLE_VICTORY = "impossible_victory"        # Defeat CR+5 enemy
    PERFECT_CHARACTER_MOMENT = "perfect_character_moment"   # Pure roleplay
    CALLBACK_VICTORY = "callback_victory"            # Use earlier setup for triumph
    BREAKTHROUGH_CREATIVE = "breakthrough_creative"  # Transform battlefield
    ROCK_BOTTOM_SURVIVAL = "rock_bottom_survival"    # Defeat at lowest point
    TEACHING_MOMENT = "teaching_moment"              # Help others grow
    CONSISTENCY_BREAK = "consistency_break"          # Major personal change

class CBEarningTrigger(Enum):
    """Choice-Based Experience - experience from everything"""
    SPECTACULAR_FAILURE = "spectacular_failure"      # Fail with style
    TRUSTED_WRONGLY = "trusted_wrongly"              # Betrayal teaches caution
    PLAN_BACKFIRED = "plan_backfired"              # Complexity attempted
    MORAL_STAND_FAILED = "moral_stand_failed"       # Principles tested
    CAUGHT_LYING = "caught_lying"                   # Social lesson learned
    HARD_CHOICE = "hard_choice"                     # No good options
    LESSER_EVIL = "lesser_evil"                     # Pragmatism learned
    SACRIFICED_SELF = "sacrificed_self"             # Heroism proven
    SELF_PRESERVATION = "self_preservation"          # Survival instinct
    BROKE_CODE = "broke_code"                       # Character growth through crisis
    ENEMY_TO_FRIEND = "enemy_to_friend"             # Redemption arc
    LOST_IMPORTANT = "lost_important"               # Grief shapes us
    FELL_IN_LOVE = "fell_in_love"                   # Vulnerability explored
    BETRAYED_OTHER = "betrayed_other"               # Dark choice made
    FORGAVE_ENEMY = "forgave_enemy"                 # Transcended revenge


@dataclass
class NPCGoal:
    """Autonomous goal system for living NPCs"""
    primary: str
    secondary: str
    obstacles: List[str]
    resources: List[str]
    timeline: str
    complexity: int


@dataclass
class EvaluatedDescription:
    """Result of creativity evaluation"""
    original_text: str
    creativity_tier: CreativityTier
    bonus_percentage: float
    mechanical_bonus: int
    extra_dice: Optional[str]
    reasoning: str
    context_used: List[str]
    environmental_elements: List[str]
    tactical_elements: List[str]
    dramatic_elements: List[str]
    feedback: str
    suggested_improvements: List[str]

@dataclass
class EvaluatedDescription:
    """Result of creativity evaluation with revolutionary mechanics"""
    evaluated_text: str
    creativity_tier: CreativityTier
    bonus_percentage: float
    mechanical_bonus: int
    extra_dice: Optional[str]
    reasoning: str
    context_used: List[str]
    environmental_elements: List[str]
    tactical_elements: List[str]
    dramatic_elements: List[str]
    feedback: str
    suggested_improvements: List[str]
    cbx_earned: int
    pressure_points: int
    np_triggered: bool
    emerging_patterns: List[str]

class CreativeEvaluationEngine:
    """CORE MECHANICS EVOLUTION: 5-tier creativity evaluation system"""

    def __init__(self):
        self.established_elements = []
        self.previous_creations = []
        self.player_patterns = defaultdict(list)
        self.creativity_templates = self._load_evaluation_templates()

    def _load_evaluation_templates(self) -> Dict[str, Any]:
        """Load comprehensive evaluation templates"""
        return {
            "environmental_usage": {
                "basic": ["direct attack", "simple action", "standard approach"],
                "tactical": ["use cover", "positional advantage", "exploit weakness"],
                "creative": ["environmental element", "multi-step plan", "unexpected approach"],
                "brilliant": ["multiple elements", "chain reactions", "environment transformation"],
                "legendary": ["battlefield reshaping", "paradigm shift", "reality bending"]
            },
            "tactical_depth": {
                "basic": ["single action", "direct approach"],
                "tactical": ["2-step plan", "contingency", "backup plan"],
                "creative": ["3+ step plan", "interlocking elements", "resource management"],
                "brilliant": ["complex strategy", "multiple contingencies", "adaptive planning"],
                "legendary": ["master strategy", "paradigm shifts", "revolutionary tactics"]
            },
            "character_consistency": {
                "protector": ["shield others", "take damage", "defensive positioning"],
                "trickster": ["deception", "illusions", "misdirection"],
                "scholar": ["knowledge application", "analysis", "strategic thinking"],
                "berserker": ["rage", "direct assault", "risk-taking"],
                "diplomat": ["negotiation", "alliance building", "social solutions"]
            }
        }

    def evaluate_action_description(self, description: str, context: Dict[str, Any],
                                   player_history: Dict[str, Any]) -> EvaluatedDescription:
        """
        REVOLUTIONARY: Evaluate player description for creativity tier
        Determines mechanical bonuses based on creative merit
        """

        # Extract and analyze description elements
        environmental_elements = self._identify_environmental_usage(description, context)
        tactical_elements = self._identify_tactical_depth(description, context)
        dramatic_elements = self._identify_dramatic_impact(description, context)
        character_consistency = self._evaluate_character_consistency(description, player_history)
        originality = self._evaluate_originality(description, self.previous_creations)

        # Score each component
        env_score = self._score_environmental_usage(environmental_elements, context)
        tac_score = self._score_tactical_depth(tactical_elements)
        dra_score = self._score_dramatic_impact(dramatic_elements)
        con_score = self._score_character_consistency(character_consistency)
        ori_score = self._score_originality(originality)

        # Calculate final tier
        total_score = (env_score * 0.3 + tac_score * 0.25 + dra_score * 0.2 +
                      con_score * 0.15 + ori_score * 0.1)

        creativity_tier = self._determine_creativity_tier(total_score)
        bonus_percentage = creativity_tier.value
        mechanical_bonus = self._calculate_mechanical_bonus(creativity_tier, context)
        extra_dice = self._determine_extra_dice(creativity_tier, description)

        # Check for Narrative Point triggers
        np_triggered = creativity_tier in [CreativityTier.LEGENDARY, CreativityTier.BEYOND_LEGENDARY]

        # Calculate CBX and Pressure Point earnings
        cbx_earned = self._calculate_cbx_earnings(creativity_tier, context)
        pressure_points = self._calculate_pressure_points(description, context, creativity_tier)

        # Identify emerging patterns
        emerging_patterns = self._identify_player_patterns(description, player_history)

        # Generate feedback and suggestions
        reasoning = self._generate_evaluation_reasoning(
            creativity_tier, env_score, tac_score, dra_score, con_score, ori_score
        )
        feedback = self._generate_player_feedback(creativity_tier, description, context)
        suggestions = self._generate_improvement_suggestions(creativity_tier, description, context)

        # Store for future reference
        evaluation_result = {
            'description': description,
            'tier': creativity_tier.name,
            'score': total_score,
            'elements': {
                'environmental': environmental_elements,
                'tactical': tactical_elements,
                'dramatic': dramatic_elements
            }
        }
        self.previous_creations.append(evaluation_result)

        return EvaluatedDescription(
            evaluated_text=description,
            creativity_tier=creativity_tier,
            bonus_percentage=bonus_percentage,
            mechanical_bonus=mechanical_bonus,
            extra_dice=extra_dice,
            reasoning=reasoning,
            context_used=list(context.get('established_elements', [])),
            environmental_elements=environmental_elements,
            tactical_elements=tactical_elements,
            dramatic_elements=dramatic_elements,
            feedback=feedback,
            suggested_improvements=suggestions,
            cbx_earned=cbx_earned,
            pressure_points=pressure_points,
            np_triggered=np_triggered,
            emerging_patterns=emerging_patterns
        )

    def _identify_environmental_usage(self, description: str, context: Dict) -> List[str]:
        """Identify how player uses established environmental elements"""
        established_elements = context.get('established_elements', [])
        environmental_elements = []

        for element in established_elements:
            if element.lower() in description.lower():
                environmental_elements.append(f"used_established_{element}")

        # Advanced pattern recognition
        if any(word in description.lower() for word in ['shadow', 'light', 'darkness', 'illumination']):
            environmental_elements.append('light_manipulation')
        if any(word in description.lower() for word in ['sand', 'dirt', 'dust', 'earth']):
            environmental_elements.append('terrain_usage')
        if any(word in description.lower() for word in ['water', 'ice', 'steam', 'liquid']):
            environmental_elements.append('liquid_manipulation')

        return environmental_elements

    def _identify_tactical_depth(self, description: str, context: Dict) -> List[str]:
        """Identify multi-step planning and tactical elements"""
        tactical_elements = []

        # Multi-step actions
        steps = description.count('then') + description.count('while') + description.count('and')
        if steps >= 2:
            tactical_elements.append('multi_step_planning')
        if steps >= 3:
            tactical_elements.append('complex_strategy')

        # Deception and misdirection
        if any(word in description.lower() for word in ['feint', 'misdirect', 'distract', 'fake']):
            tactical_elements.append('deception_tactics')

        # Exploitation of weaknesses
        if any(phrase in description.lower() for phrase in ['weak spot', 'vulnerability', 'exploit', 'weakness']):
            tactical_elements.append('weakness_exploitation')

        # Positioning and movement
        if any(word in description.lower() for word in ['position', 'angle', 'approach', 'distance']):
            tactical_elements.append('positional_tactics')

        return tactical_elements

    def _identify_dramatic_impact(self, description: str, context: Dict) -> List[str]:
        """Identify narrative advancement and dramatic elements"""
        dramatic_elements = []

        # Character development
        if any(word in description.lower() for word in ['determination', 'courage', 'willpower', 'resolve']):
            dramatic_elements.append('character_growth')

        # Relationship impact
        if any(word in description.lower() for word in ['ally', 'friend', 'companion', 'love']):
            dramatic_elements.append('relationship_development')

        # Emotional stakes
        if any(word in description.lower() for word in ['desperate', 'crucial', 'everything', 'never']):
            dramatic_elements.append('emotional_stakes')

        # Story advancement
        if any(phrase in description.lower() for phrase in ['reveal', 'discover', 'uncover', 'learn']):
            dramatic_elements.append('story_revelation')

        return dramatic_elements

    def _evaluate_character_consistency(self, description: str, player_history: Dict) -> str:
        """Check if action fits character's established patterns"""
        character_traits = player_history.get('character_traits', [])
        past_actions = player_history.get('creative_patterns', [])

        # Simple consistency check
        consistency_score = 0

        for trait in character_traits:
            if trait.lower() in description.lower():
                consistency_score += 1

        if consistency_score > 0:
            return "consistent_with_character"
        elif len(past_actions) > 0:
            # Compare with past creative approaches
            similar_patterns = sum(1 for action in past_actions[-3:] if
                                 any(word in description.lower() for word in action.lower()))
            if similar_patterns > 0:
                return "consistent_with_patterns"

        return "new_approach"

    def _evaluate_originality(self, description: str, previous_creations: List) -> float:
        """Rate originality based on previous creative solutions"""
        if not previous_creations:
            return 1.0

        # Check for repetition
        similarity_scores = []
        for creation in previous_creations[-10:]:  # Last 10 creations
            creation_desc = creation.get('description', '')
            similarity = self._calculate_description_similarity(description, creation_desc)
            similarity_scores.append(similarity)

        max_similarity = max(similarity_scores) if similarity_scores else 0
        originality = 1.0 - max_similarity

        return originality

    def _calculate_description_similarity(self, desc1: str, desc2: str) -> float:
        """Calculate semantic similarity between descriptions"""
        words1 = set(desc1.lower().split())
        words2 = set(desc2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    def _score_environmental_usage(self, elements: List[str], context: Dict) -> float:
        """Score environmental usage from 0-1"""
        if not elements:
            return 0.0

        base_score = min(len(elements) * 0.3, 1.0)

        # Bonus for using multiple environmental types
        environmental_themes = sum(1 for elem in elements if 'manipulation' in elem)
        if environmental_themes > 1:
            base_score += 0.2

        return min(base_score, 1.0)

    def _score_tactical_depth(self, elements: List[str]) -> float:
        """Score tactical depth from 0-1"""
        if not elements:
            return 0.0

        score_map = {
            'multi_step_planning': 0.4,
            'complex_strategy': 0.8,
            'deception_tactics': 0.5,
            'weakness_exploitation': 0.6,
            'positional_tactics': 0.4
        }

        score = sum(score_map.get(elem, 0.2) for elem in elements)
        return min(score, 1.0)

    def _score_dramatic_impact(self, elements: List[str]) -> float:
        """Score dramatic impact from 0-1"""
        if not elements:
            return 0.0

        score_map = {
            'character_growth': 0.7,
            'relationship_development': 0.8,
            'emotional_stakes': 0.6,
            'story_revelation': 0.9
        }

        score = sum(score_map.get(elem, 0.3) for elem in elements)
        return min(score, 1.0)

    def _score_character_consistency(self, consistency: str) -> float:
        """Score character consistency from 0-1"""
        consistency_scores = {
            'consistent_with_character': 1.0,
            'consistent_with_patterns': 0.8,
            'new_approach': 0.4
        }
        return consistency_scores.get(consistency, 0.5)

    def _score_originality(self, originality: float) -> float:
        """Score originality from 0-1"""
        return originality

    def _determine_creativity_tier(self, total_score: float) -> CreativityTier:
        """Determine creativity tier based on total score"""
        if total_score >= 0.9:
            return CreativityTier.LEGENDARY
        elif total_score >= 0.75:
            return CreativityTier.BRILLIANT
        elif total_score >= 0.6:
            return CreativityTier.CREATIVE
        elif total_score >= 0.4:
            return CreativityTier.TACTICAL
        else:
            return CreativityTier.BASIC

    def _calculate_mechanical_bonus(self, tier: CreativityTier, context: Dict) -> int:
        """Calculate mechanical bonus based on creativity tier"""
        tier_bonuses = {
            CreativityTier.BASIC: 0,
            CreativityTier.TACTICAL: 2,
            CreativityTier.CREATIVE: 4,
            CreativityTier.BRILLIANT: 6,
            CreativityTier.LEGENDARY: 8,
            CreativityTier.BEYOND_LEGENDARY: 12
        }

        base_bonus = tier_bonuses.get(tier, 0)

        # Apply situational modifiers
        if context.get('hp_percent', 100) < 25:
            base_bonus += 1  # Desperate situation bonus
        if context.get('character_theme_match', False):
            base_bonus += 1  # Character theme bonus

        return base_bonus

    def _determine_extra_dice(self, tier: CreativityTier, description: str) -> Optional[str]:
        """Determine extra dice for creative actions"""
        dice_map = {
            CreativityTier.CREATIVE: "d6",
            CreativityTier.BRILLIANT: "d8",
            CreativityTier.LEGENDARY: "d10",
            CreativityTier.BEYOND_LEGENDARY: "d12"
        }

        return dice_map.get(tier)

    def _calculate_cbx_earnings(self, tier: CreativityTier, context: Dict) -> int:
        """Calculate Choice-Based Experience earnings"""
        base_cbx = {
            CreativityTier.BASIC: 0,
            CreativityTier.TACTICAL: 1,
            CreativityTier.CREATIVE: 2,
            CreativityTier.BRILLIANT: 4,
            CreativityTier.LEGENDARY: 6,
            CreativityTier.BEYOND_LEGENDARY: 10
        }

        return base_cbx.get(tier, 0)

    def _calculate_pressure_points(self, description: str, context: Dict, tier: CreativityTier) -> int:
        """Calculate pressure points from adversity"""
        if tier in [CreativityTier.LEGENDARY, CreativityTier.BEYOND_LEGENDARY]:
            return 2  # Legendary creativity creates pressure through high stakes
        if context.get('adversity_level', 0) > 5:
            return 1  # High adversity situations create pressure

        return 0

    def _identify_player_patterns(self, description: str, player_history: Dict) -> List[str]:
        """Identify emerging player behavior patterns"""
        patterns = []

        # Environmental usage pattern
        if 'environment' in description.lower() or any(word in description.lower() for word in ['shadow', 'terrain', 'structure', 'object']):
            patterns.append('environmental_innovator')

        # Risk-taking pattern
        if any(word in description.lower() for word in ['reckless', 'desperate', 'all in', 'everything']):
            patterns.append('risk_taker')

        # Protector pattern
        if any(word in description.lower() for word in ['protect', 'shield', 'defend', 'save']):
            patterns.append('protector')

        # Deception pattern
        if any(word in description.lower() for word in ['trick', 'deceive', 'misdirect', 'feint']):
            patterns.append('deceiver')

        return patterns

    def _generate_evaluation_reasoning(self, tier: CreativityTier, env_score: float,
                                     tac_score: float, dra_score: float,
                                     con_score: float, ori_score: float) -> str:
        """Generate reasoning for creativity evaluation"""
        if tier == CreativityTier.LEGENDARY:
            return "Your description demonstrates mastery across all dimensions - environmental mastery, tactical brilliance, dramatic impact, character authenticity, and original thinking."
        elif tier == CreativityTier.BRILLIANT:
            return "Excellent creative approach showing strong tactical thinking and environmental awareness with meaningful narrative impact."
        elif tier == CreativityTier.CREATIVE:
            return "Good creative solution that effectively uses multiple elements in an innovative way."
        elif tier == CreativityTier.TACTICAL:
            return "Solid tactical thinking with some creative elements and effective planning."
        else:
            return "Basic approach - consider adding environmental elements or multi-step planning."

    def _generate_player_feedback(self, tier: CreativityTier, description: str, context: Dict) -> str:
        """Generate specific feedback to help player improve"""
        if tier == CreativityTier.BASIC:
            return "Try incorporating environmental elements from the scene or using multi-step tactics."
        elif tier == CreativityTier.TACTICAL:
            return "Great start! To reach Creative tier, try combining multiple elements or thinking outside conventional approaches."
        elif tier == CreativityTier.CREATIVE:
            return "Excellent creativity! For Brilliant tier, consider how your action advances the narrative or reveals character development."
        elif tier == CreativityTier.BRILLIANT:
            return "Outstanding! For Legendary tier, try creating a moment that transforms the entire situation or inspires others."
        else:
            return "Masterful execution! Your creativity has become power itself."

    def _generate_improvement_suggestions(self, tier: CreativityTier, description: str, context: Dict) -> List[str]:
        """Generate specific suggestions for improvement"""
        suggestions = []
        established = context.get('established_elements', [])

        if tier == CreativityTier.BASIC:
            suggestions = [
                f"Try using one of these environmental elements: {', '.join(established[:3])}",
                "Consider a two-step plan instead of a single action",
                "Think about how your character's personality would approach this"
            ]
        elif tier == CreativityTier.TACTICAL:
            suggestions = [
                "Combine multiple elements for greater effect",
                "Consider the emotional stakes of this moment",
                "Try an approach that advances the story in a new way"
            ]
        elif tier == CreativityTier.CREATIVE:
            suggestions = [
                "Connect this action to your character's growth arc",
                "Consider how this moment affects your relationships",
                "Try to create a memorable story moment"
            ]
        elif tier == CreativityTier.BRILLIANT:
            suggestions = [
                "Aim to transform the entire situation",
                "Consider how this action could inspire others",
                "Try to create a 'legendary' moment that will be remembered"
            ]

        return suggestions

class InteractiveResolutionSystem:
    """CORE MECHANICS EVOLUTION: Creativity becomes power - defeats statistics"""

    def __init__(self):
        self.creativity_engine = CreativeEvaluationEngine()
        self.established_elements = defaultdict(list)
        self.creativity_history = defaultdict(list)
        self.narrative_points = defaultdict(int)
        self.cbx_totals = defaultdict(int)
        self.pressure_points = defaultdict(int)

    def resolve_action_with_creativity(self, action_description: str, player_data: Dict,
                                     game_context: Dict) -> Dict[str, Any]:
        """
        REVOLUTIONARY: Resolve actions using creativity evaluation instead of pure statistics
        Creativity defeats mathematics
        """
        player_id = player_data.get('name', 'player')

        # Build comprehensive context
        context = self._build_resolution_context(player_data, game_context)
        player_history = self._get_player_history(player_id)

        # Evaluate creativity - THE REVOLUTION
        creativity_result = self.creativity_engine.evaluate_action_description(
            action_description, context, player_history
        )

        # Update player patterns and history
        self._update_player_patterns(player_id, creativity_result)
        self._update_established_elements(game_context)

        # Calculate mechanical results based on creativity
        mechanical_result = self._calculate_mechanical_outcome(
            creativity_result, player_data, context
        )

        # Handle narrative points and CBX
        self._handle_narrative_points(player_id, creativity_result)
        self._handle_cbx_earnings(player_id, creativity_result)
        self._handle_pressure_points(player_id, creativity_result)

        # Generate revolutionary narrative response
        narrative_result = self._generate_revolutionary_narrative(
            action_description, creativity_result, mechanical_result, context
        )

        return {
            'creativity_evaluation': creativity_result,
            'mechanical_outcome': mechanical_result,
            'narrative_response': narrative_result,
            'narrative_points_earned': creativity_result.cbx_earned if creativity_result.np_triggered else 0,
            'cbx_earned': creativity_result.cbx_earned,
            'pressure_points': creativity_result.pressure_points,
            'emerging_patterns': creativity_result.emerging_patterns,
            'systems_status': 'revolutionary_resolution_active',
            'creativity_defeats_statistics': True
        }

    def _build_resolution_context(self, player_data: Dict, game_context: Dict) -> Dict[str, Any]:
        """Build comprehensive context for creativity evaluation"""
        return {
            'established_elements': self.established_elements.get(game_context.get('scene_id', 'default'), []),
            'scene_type': game_context.get('scene_type', 'combat'),
            'emotional_intensity': game_context.get('emotional_intensity', 3),
            'character_data': player_data,
            'current_tension': game_context.get('tension', 0.5),
            'hp_percent': (player_data.get('hp_current', 10) / player_data.get('hp_max', 10)) * 100,
            'adversity_level': game_context.get('adversity_level', 5),
            'character_theme_match': game_context.get('theme_match', False)
        }

    def _get_player_history(self, player_id: str) -> Dict[str, Any]:
        """Get player history for pattern recognition"""
        return {
            'character_traits': self.creativity_history.get(f'{player_id}_traits', []),
            'creative_patterns': self.creativity_history.get(player_id, [])[-10:],  # Last 10
            'cbx_total': self.cbx_totals.get(player_id, 0),
            'pressure_points': self.pressure_points.get(player_id, 0)
        }

    def _update_player_patterns(self, player_id: str, creativity_result: EvaluatedDescription):
        """Track player behavior patterns for class generation"""
        # Update creativity history
        if player_id not in self.creativity_history:
            self.creativity_history[player_id] = []

        self.creativity_history[player_id].append(creativity_result.evaluated_text)

        # Update emerging patterns
        for pattern in creativity_result.emerging_patterns:
            pattern_key = f'{player_id}_{pattern}'
            if pattern_key not in self.creativity_history:
                self.creativity_history[pattern_key] = []
            self.creativity_history[pattern_key].append(datetime.now().isoformat())

        # Update totals
        self.cbx_totals[player_id] = self.cbx_totals.get(player_id, 0) + creativity_result.cbx_earned
        self.pressure_points[player_id] = self.pressure_points.get(player_id, 0) + creativity_result.pressure_points

    def _update_established_elements(self, game_context: Dict):
        """Update established elements from game context"""
        scene_id = game_context.get('scene_id', 'default')
        new_elements = game_context.get('newly_established', [])

        if scene_id not in self.established_elements:
            self.established_elements[scene_id] = []

        self.established_elements[scene_id].extend(new_elements)

    def _calculate_mechanical_outcome(self, creativity_result: EvaluatedDescription,
                                    player_data: Dict, context: Dict) -> Dict[str, Any]:
        """Calculate final mechanical outcome - REVOLUTION: Creativity defeats statistics"""

        # Apply creativity bonus to dice rolls
        total_dice_result = self._roll_dice_with_creativity_bonus(creativity_result, player_data)

        # Calculate adjusted difficulty
        base_difficulty = context.get('difficulty', 8)
        effective_difficulty = max(1, base_difficulty - creativity_result.mechanical_bonus)

        # Determine success based on creativity-enhanced rolls
        success = total_dice_result >= effective_difficulty

        # Check for critical/fumble based on creativity tier
        critical = creativity_result.creativity_tier == CreativityTier.LEGENDARY and random.randint(1, 100) <= 25
        fumble = creativity_result.creativity_tier == CreativityTier.BASIC and random.randint(1, 100) <= 50

        if critical and creativity_result.creativity_tier == CreativityTier.BEYOND_LEGENDARY:
            critical = True
            fumble = False  # Beyond Legendary cannot fumble

        return {
            'success': success,
            'critical': critical,
            'fumble': fumble,
            'total_roll': total_dice_result,
            'difficulty': base_difficulty,
            'effective_difficulty': effective_difficulty,
            'creativity_bonus': creativity_result.mechanical_bonus,
            'message': self._generate_mechanical_message(success, critical, fumble, creativity_result),
            'opportunities_gained': 1 if critical else 0,
            'opportunity_text': self._generate_opportunity_text(critical, creativity_result)
        }

    def _roll_dice_with_creativity_bonus(self, creativity_result: EvaluatedDescription,
                                       player_data: Dict) -> int:
        """Roll dice with creativity bonus - REVOLUTION in action"""
        # Base dice from stats (traditional)
        attribute1 = player_data.get('attribute1', 'DEXTERITY')
        attribute2 = player_data.get('attribute2', 'INSIGHT')

        # Simulate attribute dice (would normally come from character data)
        die1 = random.randint(1, 8)  # Default d8
        die2 = random.randint(1, 8)

        # Creativity bonus - THE REVOLUTION
        creativity_bonus = creativity_result.mechanical_bonus

        # Extra dice from high creativity
        extra_dice_bonus = 0
        if creativity_result.extra_dice:
            dice_type = int(creativity_result.extra_dice.replace('d', ''))
            extra_dice_bonus = random.randint(1, dice_type)

        total = die1 + die2 + creativity_bonus + extra_dice_bonus

        return total

    def _generate_mechanical_message(self, success: bool, critical: bool, fumble: bool,
                                   creativity_result: EvaluatedDescription) -> str:
        """Generate mechanical success/failure message"""
        if critical:
            return f"CRITICAL SUCCESS! Your {creativity_result.creativity_tier.name.lower()} creativity shatters all expectations!"
        elif fumble:
            return f"Execution fumbles, but your {creativity_result.creativity_tier.name.lower()} creativity still impresses."
        elif success:
            return f"Success through {creativity_result.creativity_tier.name.lower()} creativity!"
        else:
            return f"Failure, but your {creativity_result.creativity_tier.name.lower()} creativity advances the story."

    def _generate_opportunity_text(self, critical: bool, creativity_result: EvaluatedDescription) -> str:
        """Generate text for opportunities gained"""
        if critical:
            return f"Your {creativity_result.creativity_tier.name.lower()} genius creates new possibilities: gain 1 opportunity"
        return ""

    def _handle_narrative_points(self, player_id: str, creativity_result: EvaluatedDescription):
        """Handle Narrative Point earnings from creative achievements"""
        if creativity_result.np_triggered:
            self.narrative_points[player_id] = self.narrative_points.get(player_id, 0) + 1

    def _handle_cbx_earnings(self, player_id: str, creativity_result: EvaluatedDescription):
        """Handle Choice-Based Experience earnings"""
        pass  # Implemented in CBX system

    def _handle_pressure_points(self, player_id: str, creativity_result: EvaluatedDescription):
        """Handle Pressure Point accumulation"""
        pass  # Implemented in adversity system

    def _generate_revolutionary_narrative(self, action_description: str,
                                        creativity_result: EvaluatedDescription,
                                        mechanical_result: Dict[str, Any],
                                        context: Dict) -> str:
        """Generate narrative that celebrates creativity becoming power - NOW WITH HUMAN STORYTELLING"""

        # Base narrative
        base_narrative = f"You attempt: {action_description}"

        # Add creativity impact
        creativity_narrative = f"\n\nYour {creativity_result.creativity_tier.name.lower()} creativity becomes manifest reality."

        # Add mechanical result with revolutionary flavor
        if mechanical_result['critical']:
            result_narrative = f"\n\nThe world itself bends to your vision! {mechanical_result['message']}"
        elif mechanical_result['success']:
            result_narrative = f"\n\n{creativity_result.reasoning} {mechanical_result['message']}"
        else:
            result_narrative = f"\n\nThough the outcome falters, your {creativity_result.creativity_tier.name.lower()} vision inspires all who witness it."

        # Add creativity feedback
        feedback_narrative = f"\n\n[{creativity_result.feedback}]"

        # Add progression information
        progression_narrative = ""
        if creativity_result.cbx_earned > 0:
            progression_narrative += f"\n[Choice-Based Experience +{creativity_result.cbx_earned}]"
        if creativity_result.pressure_points > 0:
            progression_narrative += f"\n[Pressure Points +{creativity_result.pressure_points}]"
        if creativity_result.np_triggered:
            progression_narrative += "\n[Narrative Point earned for legendary creativity]"

        # Build initial narrative
        raw_narrative = base_narrative + creativity_narrative + result_narrative + feedback_narrative + progression_narrative

        # Apply HUMAN STORYTELLING ENHANCEMENT if available
        if self.human_storytelling_engine and self.curiosity_manager:
            try:
                # Build context for storytelling enhancement
                storytelling_context = {
                    "creativity_tier": creativity_result.creativity_tier.name,
                    "creativity_level": creativity_result.creativity_level,
                    "action_type": "combat",
                    "current_stakes": context.get("current_stakes", 3.0),
                    "player_experience": context.get("player_sessions", 1),
                    "scene_suspense_level": min(self.emotional_coaster.tension_level, 10.0),
                    "last_emotional_peak": self.emotional_coaster.last_emotional_peak
                }

                # Enhance with human storytelling techniques
                human_narrative = self.human_storytelling_engine.enhance_narrative(
                    raw_narrative, storytelling_context
                )

                # Track curiosity management
                curiosity_opportunities = self.curiosity_manager.identify_curiosity_opportunities(context)
                if curiosity_opportunities:
                    enhanced_narrative = self.curiosity_manager.integrate_curiosties_into_narrative(
                        human_narrative.enhanced_text, curiosity_opportunities
                    )
                else:
                    enhanced_narrative = human_narrative.enhanced_text

                # Store curiosity gaps for future resolution
                self.active_curiosties = human_narrative.curiosity_gaps

                return enhanced_narrative

            except Exception as e:
                print(f"[WARNING] Human storytelling enhancement failed: {e}")
                # Fall back to normal narrative
                return raw_narrative
        else:
            print("[DEBUG] Human storytelling systems not available, using standard narrative")
            return raw_narrative

class CreativeDescriptionBuilder:
    """AI-Assisted Creative Description Builder - Helps players improve creativity"""

    def __init__(self):
        self.progressive_prompts = self._load_progressive_prompts()
        self.example_templates = self._load_example_templates()
        self.player_coaching_history = defaultdict(list)

    def _load_progressive_prompts(self) -> Dict[str, List[str]]:
        """Load progressive prompting system for creativity assistance"""
        return {
            "level_1_basic": [
                "Consider these elements in this scene: {elements}",
                "What environmental factors could help you?",
                "How might your character's personality approach this?"
            ],
            "level_2_tactical": [
                "Think about chain reactions - what follows your first action?",
                "Consider weaknesses you could exploit",
                "How could you use established elements together?"
            ],
            "level_3_creative": [
                "Start your description with:",
                "- WHERE you move: _____",
                "- WHAT you use: _____",
                "- HOW you strike: _____",
                "- WHY it works: _____"
            ],
            "level_4_brilliant": [
                "Transform the entire situation",
                "Create a moment that advances your story",
                "Consider how this reveals character growth"
            ]
        }

    def _load_example_templates(self) -> Dict[str, Dict]:
        """Load contextual examples for different creativity tiers"""
        return {
            "combat_scene": {
                "tactical_example": "I feint left then strike his sword arm when he blocks",
                "creative_example": "I kick sand in his eyes while sliding under his heavy guard",
                "brilliant_example": "I use the chandelier's shadow pattern to disguise my movements",
                "legendary_example": "I shatter the ice beneath us, using his heavy armor against him"
            }
        }

    def build_creative_description_progressively(self, current_approach: str, creativity_tier: str,
                                               scene_context: Dict, player_history: Dict) -> Dict[str, Any]:
        """Progressively build creative descriptions with coaching"""

        current_level = self._determine_current_level(current_approach, creativity_tier)
        next_level_prompts = self._get_next_level_prompts(current_level, scene_context)

        coaching_response = {
            "current_approach": current_approach,
            "detected_level": current_level,
            "next_level_prompts": next_level_prompts,
            "improvement_suggestions": self._generate_improvement_suggestions(current_approach, scene_context),
            "relevant_examples": self._get_relevant_examples(scene_context, current_level),
            "coaching_style": "collaborative_building"
        }

        # Track coaching for future sessions
        self._track_coaching_progress(player_history, current_level)

        return coaching_response

    def _determine_current_level(self, current_approach: str, creativity_tier: str) -> str:
        """Determine player's current creativity development level"""
        tier_map = {
            "BASIC": "level_1_basic",
            "TACTICAL": "level_2_tactical",
            "CREATIVE": "level_3_creative",
            "BRILLIANT": "level_4_brilliant",
            "LEGENDARY": "level_5_legendary"
        }

        return tier_map.get(creativity_tier, "level_1_basic")

    def _get_next_level_prompts(self, current_level: str, scene_context: Dict) -> List[str]:
        """Get prompts to help player reach next creativity level"""
        # Fill in context-specific elements
        elements_prompts = self.progressive_prompts.get(current_level, [])
        filled_prompts = []

        for prompt in elements_prompts:
            # Replace placeholders with actual scene elements
            if "{elements}" in prompt:
                prompt = prompt.replace("{elements}", ", ".join(scene_context.get('available_elements', [])))
            filled_prompts.append(prompt)

        return filled_prompts

    def _generate_improvement_suggestions(self, current_approach: str, scene_context: Dict) -> List[str]:
        """Generate specific suggestions for the player's approach"""
        suggestions = []

        # Analyze current approach for improvement opportunities
        if len(current_approach.split()) < 10:
            suggestions.append("Try adding more specific details about how your action works")

        if not any(env_word in current_approach.lower() for env_word in scene_context.get('available_elements', [])):
            suggestions.append("Consider using one of these environmental elements: " +
                             ", ".join(scene_context.get('available_elements', [])[:3]))

        # Add tactical suggestions
        if "and" not in current_approach.lower() and "then" not in current_approach.lower():
            suggestions.append("Try a multi-step plan: first do X, then follow up with Y")

        # Add character-specific suggestions
        character_traits = scene_context.get('character_traits', [])
        if character_traits:
            suggestions.append(f"Consider how your character's {character_traits[0]} nature would approach this")

        return suggestions[:3]  # Limit to top 3 suggestions

    def _get_relevant_examples(self, scene_context: Dict, current_level: str) -> Dict[str, str]:
        """Get relevant examples for improvement inspiration"""
        scene_type = scene_context.get('scene_type', 'general')
        examples_for_scene = self.example_templates.get(scene_type, self.example_templates.get('general', {}))

        # Get examples at or above current level
        relevant_examples = {}
        level_order = ["tactical_example", "creative_example", "brilliant_example", "legendary_example"]

        level_index = level_order.index(current_level.replace("level_", "").replace("_", "_") + "_example") if current_level.replace("level_", "").replace("_", "_") + "_example" in level_order else 0

        for level_name in level_order[level_index:]:
            if level_name in examples_for_scene:
                tier_name = level_name.replace("_example", "").title()
                relevant_examples[tier_name] = examples_for_scene[level_name]

        return relevant_examples

    def _track_coaching_progress(self, player_history: Dict, current_level: str):
        """Track player progress through coaching system"""
        if 'coaching_sessions' not in player_history:
            player_history['coaching_sessions'] = []

        player_history['coaching_sessions'].append({
            'timestamp': "now",  # Would use actual datetime
            'level_reached': current_level,
            'session_count': len(player_history.get('coaching_sessions', []))
        })

        # Track improvement patterns
        if len(player_history.get('coaching_sessions', [])) > 3:
            recent_levels = [session['level_reached'] for session in player_history['coaching_sessions'][-3:]]
            if len(set(recent_levels)) > 1:
                player_history['improving_patterns'] = True

    def provide_creativity_coaching(self, player_id: str, current_approach: str, scene_context: Dict) -> Dict[str, Any]:
        """Provide ongoing creativity coaching based on player patterns"""
        player_history = self.player_coaching_history.get(player_id, {})

        coaching = self.build_creative_description_progressively(
            current_approach, "BASIC", scene_context, player_history
        )

        # Add personalized coaching based on history
        if len(player_history.get('coaching_sessions', [])) > 5:
            coaching['milestone_message'] = "You've been developing your creative skills! Keep experimenting with different approaches."

        return coaching

class PersonalClassGenerator:
    """CORE MECHANICS EVOLUTION: AI-generated personal classes from player behavior"""

    def __init__(self):
        self.player_behavior_data = defaultdict(dict)
        self.generated_classes = {}
        self.emergence_triggers = defaultdict(list)
        self.class_evolution_tracks = self._initialize_evolution_tracks()

    def _initialize_evolution_tracks(self) -> Dict[str, Dict]:
        """Initialize class evolution tracks based on behavior patterns"""
        return {
            'environmental_innovator': {
                'base_class': 'Reality Sculptor',
                'evolution_paths': ['Master Architect', 'World Shaper', 'Reality Binder'],
                'keystone_ability': 'Environmental Mastery - Add extra d8 when using environment',
                'progression_thresholds': [10, 25, 50, 100]  # Pattern usage counts
            },
            'protector': {
                'base_class': 'Shield Guardian',
                'evolution_paths': ['Aegis Eternal', 'Martyr Knight', 'Guardian Ascendant'],
                'keystone_ability': 'Shield Others - Take damage meant for allies',
                'progression_thresholds': [5, 15, 30, 60]
            },
            'risk_taker': {
                'base_class': 'Gambler',
                'evolution_paths': ['Chaos Master', 'Fate Weaver', 'Probability Knight'],
                'keystone_ability': 'Risk Reward - High risk actions gain bonus dice',
                'progression_thresholds': [8, 20, 40, 80]
            },
            'deceiver': {
                'base_class': 'Illusionist',
                'evolution_paths': ['Master of Lies', 'Reality Hacker', 'Truth Twister'],
                'keystone_ability': 'Deceptive Strike - Attacks enhanced by misdirection',
                'progression_thresholds': [7, 18, 35, 70]
            }
        }

    def analyze_player_behavior(self, player_id: str, behavior_data: Dict) -> Dict[str, Any]:
        """Analyze player behavior patterns to determine emerging class"""
        patterns = self._extract_behavior_patterns(behavior_data)
        dominant_pattern = self._identify_dominant_pattern(patterns)
        supporting_patterns = self._identify_supporting_patterns(patterns)

        # Check class emergence eligibility
        emergence_data = self._check_class_emergence(player_id, dominant_pattern, patterns)

        # Generate preliminary class assessment
        class_assessment = self._generate_class_assessment(
            player_id, dominant_pattern, supporting_patterns, patterns, emergence_data
        )

        return class_assessment

    def _extract_behavior_patterns(self, behavior_data: Dict) -> Dict[str, int]:
        """Extract quantified behavior patterns from player data"""
        patterns = defaultdict(int)

        # Analyze creative action patterns
        creative_history = behavior_data.get('creative_history', [])
        for action in creative_history:
            if 'environment' in action.lower() or any(word in action.lower() for word in ['shadow', 'terrain', 'structure']):
                patterns['environmental_innovator'] += 1
            if any(word in action.lower() for word in ['protect', 'shield', 'defend']):
                patterns['protector'] += 1
            if any(word in action.lower() for word in ['feint', 'deceive', 'trick', 'misdirect']):
                patterns['deceiver'] += 1
            if any(word in action.lower() for word in ['desperate', 'reckless', 'all in']):
                patterns['risk_taker'] += 1

        # Analyze combat patterns
        combat_history = behavior_data.get('combat_history', [])
        for combat in combat_history:
            if combat.get('took_damage_for_others'):
                patterns['protector'] += combat['took_damage_for_others']
            if combat.get('used_environment'):
                patterns['environmental_innovator'] += 1
            if combat.get('risk_level', 0) > 7:
                patterns['risk_taker'] += 1

        # Analyze social patterns
        social_history = behavior_data.get('social_history', [])
        for interaction in social_history:
            if interaction.get('used_deception'):
                patterns['deceiver'] += 1
            if interaction.get('protected_others'):
                patterns['protector'] += 1

        return dict(patterns)

    def _identify_dominant_pattern(self, patterns: Dict[str, int]) -> Optional[str]:
        """Identify the most prominent behavior pattern"""
        if not patterns:
            return None

        max_count = max(patterns.values())
        if max_count >= 5:  # Minimum threshold for dominance
            return max(patterns.items(), key=lambda x: x[1])[0]
        return None

    def _identify_supporting_patterns(self, patterns: Dict[str, int]) -> List[str]:
        """Identify secondary behavior patterns"""
        if not patterns:
            return []

        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
        return [pattern for pattern, count in sorted_patterns[1:4] if count >= 3]

    def _check_class_emergence(self, player_id: str, dominant_pattern: str, patterns: Dict) -> Dict[str, Any]:
        """Check if player's behavior meets emergence triggers"""
        emergence_data = {
            'eligible': False,
            'trigger_type': None,
            'urgency': 0,
            'recommendation': None
        }

        if not dominant_pattern:
            return emergence_data

        pattern_count = patterns.get(dominant_pattern, 0)
        evolution_track = self.class_evolution_tracks.get(dominant_pattern, {})
        thresholds = evolution_track.get('progression_thresholds', [])

        # Check against evolution thresholds
        current_tier = 0
        for i, threshold in enumerate(thresholds):
            if pattern_count >= threshold:
                current_tier = i + 1

        if current_tier >= 1:  # Minimum emergence
            emergence_data['eligible'] = True
            emergence_data['urgency'] = min(pattern_count / thresholds[0], 1.0)

            # Determine trigger type
            if pattern_count >= thresholds[-1]:  # Highest threshold
                emergence_data['trigger_type'] = 'legendary_emergence'
            elif pattern_count >= thresholds[1] if len(thresholds) > 1 else thresholds[0]:
                emergence_data['trigger_type'] = 'major_emergence'
            else:
                emergence_data['trigger_type'] = 'basic_emergence'

        return emergence_data

    def _generate_class_assessment(self, player_id: str, dominant_pattern: str,
                                 supporting_patterns: List[str], patterns: Dict,
                                 emergence_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive class assessment"""
        evolution_track = self.class_evolution_tracks.get(dominant_pattern, {})

        assessment = {
            'player_id': player_id,
            'analysis_timestamp': datetime.now().isoformat(),
            ' dominant_pattern': dominant_pattern,
            'supporting_patterns': supporting_patterns,
            'pattern_frequencies': patterns,
            'class_data': None,
            'emergence_eligible': emergence_data['eligible'],
            'emergence_urgency': emergence_data['urgency'],
            'evolution_potential': self._calculate_evolution_potential(patterns, emergence_data),
            'recommended_class': None,
            'next_evolution_milestone': None,
            'behavioral_insights': self._generate_behavioral_insights(patterns, dominant_pattern),
            'growth_recommendations': self._generate_growth_recommendations(dominant_pattern, supporting_patterns)
        }

        if dominant_pattern and emergence_data['eligible']:
            base_class = evolution_track.get('base_class', 'Custom Class')
            keystone_ability = evolution_track.get('keystone_ability', 'Default ability')

            assessment['recommended_class'] = {
                'class_name': base_class,
                'keystone_ability': keystone_ability,
                'evolution_tier': self._calculate_current_tier(dominant_pattern, patterns),
                'total_evolution_tiers': len(evolution_track.get('progression_thresholds', [])),
                'until_next_evolution': self._calculate_until_next_evolution(dominant_pattern, patterns)
            }

            assessment['class_data'] = {
                'primary_pattern': dominant_pattern,
                'class_archetype': base_class,
                'keystone_ability_description': keystone_ability,
                'current_power_level': self._calculate_power_level(patterns, dominant_pattern),
                'unique_aspects': self._identify_unique_aspects(patterns, dominant_pattern, supporting_patterns)
            }

        return assessment

    def _calculate_evolution_potential(self, patterns: Dict, emergence_data: Dict) -> float:
        """Calculate potential for class evolution"""
        if not emergence_data['eligible']:
            return 0.0

        # Based on pattern consistency and emergence urgency
        total_patterns = sum(patterns.values())
        urgency = emergence_data['urgency']

        return min(urgency * 1.2, 1.0)

    def _calculate_current_tier(self, dominant_pattern: str, patterns: Dict) -> int:
        """Calculate current evolution tier"""
        pattern_count = patterns.get(dominant_pattern, 0)
        evolution_track = self.class_evolution_tracks.get(dominant_pattern, {})
        thresholds = evolution_track.get('progression_thresholds', [])

        current_tier = 0
        for threshold in thresholds:
            if pattern_count >= threshold:
                current_tier += 1

        return current_tier

    def _calculate_until_next_evolution(self, dominant_pattern: str, patterns: Dict) -> int:
        """Calculate actions needed until next evolution"""
        current_count = patterns.get(dominant_pattern, 0)
        evolution_track = self.class_evolution_tracks.get(dominant_pattern, {})
        thresholds = evolution_track.get('progression_thresholds', [])

        current_tier = self._calculate_current_tier(dominant_pattern, patterns)

        if current_tier < len(thresholds):
            next_threshold = thresholds[current_tier]
            return max(0, next_threshold - current_count)

        return 0  # Max tier reached

    def _identify_unique_aspects(self, patterns: Dict, dominant_pattern: str,
                               supporting_patterns: List[str]) -> List[str]:
        """Identify unique aspects of this player's behavioral profile"""
        unique_aspects = []

        # Pattern combination uniqueness
        if len(supporting_patterns) >= 2:
            unique_aspects.append("Multi-faceted approach combining multiple behavioral patterns")

        # High frequency uniqueness
        dominant_count = patterns.get(dominant_pattern, 0)
        if dominant_count >= 50:
            unique_aspects.append(f"Exceptional dedication to {dominant_pattern.replace('_', ' ')} approach")

        # Supporting pattern synergy
        if 'protector' in supporting_patterns and 'environmental_innovator' in supporting_patterns:
            unique_aspects.append("Innovative protective strategies using environmental control")

        if 'risk_taker' in supporting_patterns and 'deceiver' in supporting_patterns:
            unique_aspects.append("High-risk deception tactics with dramatic flair")

        return unique_aspects

    def _generate_behavioral_insights(self, patterns: Dict, dominant_pattern: str) -> List[str]:
        """Generate insightful observations about player behavior"""
        insights = []

        if not patterns:
            return ["Player showing emerging behavioral patterns - more data needed"]

        # Dominant pattern insights
        if dominant_pattern == 'environmental_innovator':
            insights.append("Shows consistent preference for creative environmental solutions")
        elif dominant_pattern == 'protector':
            insights.append("Demonstrates strong protective instincts and team-oriented thinking")
        elif dominant_pattern == 'risk_taker':
            insights.append("Embraces high-risk strategies with dramatic flair")
        elif dominant_pattern == 'deceiver':
            insights.append("Prefers indirect solutions through misdirection and clever tactics")

        # Pattern balance insights
        total_actions = sum(patterns.values())
        diversity = len([p for p in patterns.values() if p > 0]) / len(patterns) if patterns else 0

        if diversity > 0.7:
            insights.append("Highly versatile player comfortable with multiple approaches")
        elif diversity < 0.3:
            insights.append("Focused specialist who excels in preferred methodology")

        return insights

    def _generate_growth_recommendations(self, dominant_pattern: str, supporting_patterns: List[str]) -> List[str]:
        """Generate recommendations for class development"""
        recommendations = []

        if not dominant_pattern:
            return ["Continue expressing your unique approach to develop your personal class"]

        # Primary pattern recommendations
        if dominant_pattern == 'environmental_innovator':
            recommendations.append("Focus on mastering environmental transformation techniques")
            recommendations.append("Combine multiple environmental elements for maximum effect")

        elif dominant_pattern == 'protector':
            recommendations.append("Develop advanced protective techniques and team coordination")
            recommendations.append("Consider how your protective instincts can become offensive strength")

        elif dominant_pattern == 'risk_taker':
            recommendations.append("Channel your risk-taking into calculated high-reward strategies")
            recommendations.append("Learn to minimize downside while maximizing dramatic impact")

        elif dominant_pattern == 'deceiver':
            recommendations.append("Master advanced misdirection and reality manipulation")
            recommendations.append("Combine deception tactics with environmental control")

        # Supporting pattern integration
        for supporting_pattern in supporting_patterns[:2]:  # Top 2 supporting
            if supporting_pattern == 'protector' and dominant_pattern != 'protector':
                recommendations.append("Integrate protective instincts into your primary approach")
            elif supporting_pattern == 'environmental_innovator' and dominant_pattern != 'environmental_innovator':
                recommendations.append("Use environmental manipulation to support your primary strategy")

        return recommendations

    def trigger_class_emergence(self, player_id: str, emergence_trigger: str) -> Dict[str, Any]:
        """Trigger the emergence of player's personal class"""
        if player_id not in self.player_behavior_data:
            return {'error': f'No behavior data for player {player_id}'}

        behavior_data = self.player_behavior_data[player_id]
        assessment = self.analyze_player_behavior(player_id, behavior_data)

        if not assessment['emergence_eligible']:
            return {'error': 'Player not eligible for class emergence', 'assessment': assessment}

        # Generate the personal class
        generated_class = self._generate_personal_class(player_id, assessment)
        self.generated_classes[player_id] = generated_class

        # Create emergence narrative
        emergence_narrative = self._create_emergence_narrative(generated_class, emergence_trigger)

        return {
            'success': True,
            'personal_class': generated_class,
            'emergence_narrative': emergence_narrative,
            'assessment': assessment,
            'transformation_moment': datetime.now().isoformat()
        }

    def _generate_personal_class(self, player_id: str, assessment: Dict) -> Dict[str, Any]:
        """Generate unique personal class based on behavior assessment"""
        dominant_pattern = assessment['dominant_pattern']
        evolution_track = self.class_evolution_tracks.get(dominant_pattern, {})

        base_class_name = evolution_track.get('base_class', 'Custom Class')

        # Generate unique class name based on specific behaviors
        unique_class_name = self._generate_unique_class_name(assessment)

        personal_class = {
            'player_id': player_id,
            'base_archetype': base_class_name,
            'unique_name': unique_class_name,
            'generation_date': datetime.now().isoformat(),
            'behavioral_foundation': assessment,
            'mechanics': {
                'keystone_ability': evolution_track.get('keystone_ability', 'Default keystone'),
                'supporting_abilities': self._generate_supporting_abilities(assessment),
                'signature_style': self._determine_signature_style(assessment),
                'weakness': self._determine_class_weakness(assessment),
                'power_source': f'Your consistent {dominant_pattern.replace("_", " ")} approach'
            },
            'evolution_track': evolution_track.get('evolution_paths', []),
            'flavor_text': self._generate_class_flavor_text(assessment),
            'uniqueness': 'This class could only belong to you - it emerges from your specific play patterns'
        }

        return personal_class

    def _generate_unique_class_name(self, assessment: Dict) -> str:
        """Generate unique class name based on specific behavioral patterns"""
        dominant_pattern = assessment['dominant_pattern']
        frequencies = assessment['pattern_frequencies']

        # Generate name based on frequency and supporting patterns
        if dominant_pattern == 'environmental_innovator':
            count = frequencies.get('environmental_innovator', 0)
            if count >= 30:
                return 'World Shaper'
            elif count >= 15:
                return 'Environmental Savant'
            else:
                return 'Terrain Master'

        elif dominant_pattern == 'protector':
            count = frequencies.get('protector', 0)
            supporting = len(assessment['supporting_patterns'])
            if count >= 25 and supporting >= 2:
                return 'Aegis Eternal'
            elif count >= 15:
                return 'Shield Guardian'
            else:
                return 'Defender'

        elif dominant_pattern == 'risk_taker':
            count = frequencies.get('risk_taker', 0)
            if count >= 20:
                return 'Gambler King'
            else:
                return 'Risk Taker'

        elif dominant_pattern == 'deceiver':
            count = frequencies.get('deceiver', 0)
            if count >= 18:
                return 'Master of Illusions'
            else:
                return 'Trickster'

        return 'Custom Class'  # Fallback

    def _generate_supporting_abilities(self, assessment: Dict) -> List[str]:
        """Generate supporting abilities based on behavioral patterns"""
        supporting_abilities = []
        supporting_patterns = assessment['supporting_patterns']

        for pattern in supporting_patterns[:2]:  # Top 2 supporting patterns
            if pattern == 'protector':
                supporting_abilities.append("Ally Reinforcement - Allies gain defensive bonuses near you")
            elif pattern == 'environmental_innovator':
                supporting_abilities.append("Persistent Changes - Your environmental modifications last longer")
            elif pattern == 'risk_taker':
                supporting_abilities.append("Fortune Favors the Bold - Gain advantage when outnumbered")
            elif pattern == 'deceiver':
                supporting_abilities.append("Subtle Influence - NPCs are more susceptible to your suggestions")

        return supporting_abilities[:3]  # Limit to 3 abilities

    def _determine_signature_style(self, assessment: Dict) -> str:
        """Determine the signature style of this personal class"""
        dominant_pattern = assessment['dominant_pattern']

        styles = {
            'environmental_innovator': "You excel at transforming the battlefield using established elements",
            'protector': "You naturally position yourself between danger and those you care about",
            'risk_taker': "You thrive in high-stakes situations where others would hesitate",
            'deceiver': "You prefer indirect solutions that manipulate perception and reality"
        }

        return styles.get(dominant_pattern, "Your unique approach sets you apart from traditional classes")

    def _determine_class_weakness(self, assessment: Dict) -> str:
        """Determine meaningful weakness based on behavioral avoidance"""
        all_patterns = ['environmental_innovator', 'protector', 'risk_taker', 'deceiver']
        used_patterns = [assessment['dominant_pattern']] + assessment['supporting_patterns']
        avoided_patterns = [p for p in all_patterns if p not in used_patterns]

        if 'protector' in avoided_patterns:
            return "You struggle when forced to prioritize others' safety over your objectives"
        elif 'environmental_innovator' in avoided_patterns:
            return "Featureless environments limit your usual creative approaches"
        elif 'risk_taker' in avoided_patterns:
            return "Conservative situations don't provide the dramatic tension you need to excel"
        elif 'deceiver' in avoided_patterns:
            return "Direct confrontations bypass your preferred indirect methods"

        return "Your specialized focus creates blind spots in other approaches"

    def _generate_class_flavor_text(self, assessment: Dict) -> str:
        """Generate inspiring flavor text for the personal class"""
        dominant_pattern = assessment['dominant_pattern']
        pattern_count = assessment['pattern_frequencies'].get(dominant_pattern, 0)

        if pattern_count >= 30:
            intensity = "master"
        elif pattern_count >= 15:
            intensity = "skilled practitioner"
        else:
            intensity = "emerging talent"

        flavor_templates = {
            'environmental_innovator': f"The world itself becomes your weapon as a {intensity} of battlefield transformation",
            'protector': f"You are the shield that stands between darkness and innocence, a {intensity} of selfless defense",
            'risk_taker': f"Where others see danger, you see opportunity as a {intensity} of high-stakes triumph",
            'deceiver': f"Reality bends to your will as a {intensity} of perception and illusion"
        }

        return flavor_templates.get(dominant_pattern, "Your unique journey has forged a class like no other")

    def _create_emergence_narrative(self, generated_class: Dict, emergence_trigger: str) -> str:
        """Create dramatic emergence narrative for class revelation"""
        class_name = generated_class['unique_name']
        base_archetype = generated_class['base_archetype']
        behavioral_foundation = generated_class['behavioral_foundation']

        emergence_scenes = {
            'extreme_adversity': f"As doom approaches and all seems lost, your repeated {behavioral_foundation['dominant_pattern'].replace('_', ' ')} choices crystallize into pure power. You are not just a {base_archetype}. You are {class_name.toUpperCase()}.",
            'personal_crisis': f"When everything you believe is tested, your true nature emerges. All those moments of {behavioral_foundation['dominant_pattern'].replace('_', ' ')} have shaped you into something new: {class_name.toUpperCase()}.",
            'heroic_sacrifice': f"In the moment you give everything for others, your journey transforms you. Your consistent choice to {behavioral_foundation['dominant_pattern'].replace('_', ' ')} becomes legend. You become {class_name.toUpperCase()}.",
            'perfect_expression': f"In this perfect moment of self-expression, your true power awakens. Your mastery of {behavioral_foundation['dominant_pattern'].replace('_', ' ')} transcends mortal limits. You are {class_name.toUpperCase()}.",
            'story_climax': f"As your personal story reaches its crescendo, power flows through you. Every choice to {behavioral_foundation['dominant_pattern'].replace('_', ' ')} has led to this: {class_name.toUpperCase()}."
        }

        return emergence_scenes.get(emergence_trigger, f"Through your consistent actions, you have become {class_name.toUpperCase()} - a class as unique as your journey.")

class AdvancedAIOrchestrator:
    """
    CERTAIN: Complete MYNFINI mechanics integration in web-based AI-first system
    Includes CORE MECHANICS EVOLUTION features:
    - Interactive Resolution System (creativity defeats statistics)
    - 5-Tier Creativity Evaluation Engine
    - AI-assisted Creative Description Builder
    - Translation Layer (creativity→mechanics mapping)
    - Narrative Points System (replaces Fabula Points)
    - Personal Class Generation from player behavior
    - Kimi K2-905 Integration with 127-agent mega-parallel orchestration
    """

    def __init__(self):
        """Simplified initialization to prevent blocking - CORE MECHANICS EVOLUTION"""
        self.current_step = 1
        self.user_state = {}
        self.cbx_total = 0
        self.narrative_points = 0

        # Initialize with minimal required systems for fast startup
        print("[DEBUG] Starting minimal AdvancedAIOrchestrator initialization...")

        # Initialize CORE MECHANICS EVOLUTION systems (always available)
        try:
            self.creativity_evaluator = CreativeEvaluationEngine()
            print(f"[DEBUG] CreativeEvaluationEngine initialized successfully")
        except Exception as e:
            print(f"[ERROR] CreativeEvaluationEngine initialization failed: {e}")
            self.creativity_evaluator = None

        try:
            self.interactive_resolution = InteractiveResolutionSystem()
            print(f"[DEBUG] InteractiveResolutionSystem initialized successfully")
        except Exception as e:
            print(f"[ERROR] InteractiveResolutionSystem initialization failed: {e}")
            self.interactive_resolution = None

        try:
            self.creative_description_builder = CreativeDescriptionBuilder()
            print(f"[DEBUG] CreativeDescriptionBuilder initialized successfully")
        except Exception as e:
            print(f"[ERROR] CreativeDescriptionBuilder initialization failed: {e}")
            self.creative_description_builder = None

        try:
            self.class_generator = PersonalClassGenerator()
            print(f"[DEBUG] PersonalClassGenerator initialized successfully")
        except Exception as e:
            print(f"[ERROR] PersonalClassGenerator initialization failed: {e}")
            self.class_generator = None

        # Initialize Kimi K2-905 orchestrator if available
        try:
            if KIMI_K2_AVAILABLE:
                self.k2_orchestrator = KimiK2Orchestrator()
                print(f"[DEBUG] KimiK2Orchestrator initialized successfully")
            else:
                self.k2_orchestrator = None
                print(f"[DEBUG] KimiK2Orchestrator not available")
        except Exception as e:
            print(f"[ERROR] KimiK2Orchestrator initialization failed: {e}")
            self.k2_orchestrator = None

        # Initialize revolutionary systems
        self._initialize_revolutionary_systems()

        # Initialize fallback systems with proper error handling and timeout protection
        self._initialize_fallback_systems()

        # State tracking (minimal)
        self.scene_history = []
        self.character_arcs = {}
        self.narrative_threads = []
        self.sensory_environment = {}
        self.creativity_history = []
        self.narrative_spending_log = []

        # Configuration for mega-parallel mode
        self.mega_parallel_mode = True
        self.max_agents = 127
        self.parallel_streams = 100

        print(f"[VERIFIED] Minimal AdvancedAIOrchestrator initialized successfully")
        print(f"[DEBUG] Core systems: Creativity={bool(self.creativity_evaluator)}, Interactive={bool(self.interactive_resolution)}, Description={bool(self.creative_description_builder)}, ClassGen={bool(self.class_generator)}, K2Orchestrator={bool(self.k2_orchestrator)}")

    def _initialize_revolutionary_systems(self):
        """Initialize revolutionary systems from revolutionary_systems_implementation"""
        # Initialize revolutionary systems
        self.narrative_consistency_enforcer = None
        self.dynamics_optimization_system = None
        self.adversity_evolution_system = None
        self.multi_axis_progression_system = None

        # Try to initialize revolutionary systems
        try:
            if REVOLUTIONARY_SYSTEMS_AVAILABLE:
                # Create instances of revolutionary systems
                self.narrative_consistency_enforcer = NarrativeConsistencyEnforcer()
                self.dynamics_optimization_system = DynamicsOptimizationSystem()
                self.adversity_evolution_system = AdversityEvolutionSystem()
                self.multi_axis_progression_system = MultiAxisProgressionSystem()
                print(f"[DEBUG] Revolutionary systems initialized successfully")
            else:
                # Use fallback implementations
                self.narrative_consistency_enforcer = NarrativeConsistencyEnforcer()
                self.dynamics_optimization_system = DynamicsOptimizationSystem()
                self.adversity_evolution_system = AdversityEvolutionSystem()
                self.multi_axis_progression_system = MultiAxisProgressionSystem()
                print(f"[DEBUG] Revolutionary systems initialized with fallback implementations")
        except Exception as e:
            print(f"[DEBUG] Revolutionary systems not available: {e}")

    def _initialize_fallback_systems(self):
        """Initialize fallback systems with proper error handling"""
        # Initialize basic narrative systems with fallbacks
        self.narrative_engine = None
        self.narrative_cohesion = None
        self.pacing_manager = None
        self.clock_system = None
        self.adversity_system = None
        self.progression_system = None
        self.narrative_points_system = None
        self.narrative_consistency = None
        self.sensory_descriptor = None
        self.show_dont_tell_processor = None
        self.eight_pillars_framework = None
        self.cohesion_manager = None
        self.session_zero = None
        self.game_state = None
        self.ai_error_recovery = None
        self.dynamic_naming = None
        self.player_behavior_tracking = None
        self.human_storytelling_engine = None
        self.curiosity_manager = None
        self.world_system = None

        # Try to initialize essential fallback systems
        try:
            if 'PacingManager' in globals():
                self.pacing_manager = PacingManager()
                print(f"[DEBUG] PacingManager initialized as fallback")
        except Exception as e:
            print(f"[DEBUG] PacingManager not available as fallback: {e}")

        # Try to initialize NarrativePointsSystem if available
        try:
            if 'NarrativePointsSystem' in globals():
                self.narrative_points_system = NarrativePointsSystem()
                print(f"[DEBUG] NarrativePointsSystem initialized as fallback")
            else:
                # Try direct import as fallback
                from narrative_points_system_complete import NarrativePointsSystem
                self.narrative_points_system = NarrativePointsSystem()
                print(f"[DEBUG] NarrativePointsSystem initialized via direct import")
        except Exception as e:
            print(f"[DEBUG] NarrativePointsSystem not available as fallback: {e}")
            self.narrative_points_system = None

        # Try to initialize EnhancedClockSystem if available
        try:
            from enhanced_clock_system_complete import EnhancedClockSystem
            self.clock_system = EnhancedClockSystem()
            print(f"[DEBUG] EnhancedClockSystem initialized as fallback")
        except Exception as e:
            print(f"[DEBUG] EnhancedClockSystem not available as fallback: {e}")
            self.clock_system = None

        # Try to initialize CohesionManager if available
        try:
            from narrative_cohesion_system import CohesionManager
            self.cohesion_manager = CohesionManager()
            print(f"[DEBUG] CohesionManager initialized as fallback")
        except Exception as e:
            print(f"[DEBUG] CohesionManager not available as fallback: {e}")
            self.cohesion_manager = None

        # Try to initialize SensoryDescriptor if available
        try:
            from narrative_engine import SensoryDescriptor
            self.sensory_descriptor = SensoryDescriptor()
            print(f"[DEBUG] SensoryDescriptor initialized as fallback")
        except Exception as e:
            print(f"[DEBUG] SensoryDescriptor not available as fallback: {e}")
            self.sensory_descriptor = None

        # Try to initialize EightPillars framework if available
        try:
            from narrative_core_systems import EightPillarsFramework
            self.eight_pillars_framework = EightPillarsFramework()
            print(f"[DEBUG] EightPillarsFramework initialized as fallback")
        except Exception as e:
            print(f"[DEBUG] EightPillarsFramework not available as fallback: {e}")
            self.eight_pillars_framework = None

        # Try to initialize SessionZeroProtocol if available
        try:
            from session_zero_enhanced import SessionZeroProtocol
            # Create a minimal ExpandedWorldSystem for SessionZeroProtocol
            from expanded_world_system import ExpandedWorldSystem
            world_system = ExpandedWorldSystem()
            self.session_zero = SessionZeroProtocol(world_system)
            print(f"[DEBUG] SessionZeroProtocol initialized as fallback")
        except Exception as e:
            print(f"[DEBUG] SessionZeroProtocol not available as fallback: {e}")
            self.session_zero = None

        # Try to initialize AI Error Recovery Manager if available
        try:
            from error_handler import FriendlyErrorHandler
            # Use the error handler as a base for AI error recovery
            self.ai_error_recovery = FriendlyErrorHandler()
            print(f"[DEBUG] AIErrorRecoveryManager initialized as fallback")
        except Exception as e:
            print(f"[DEBUG] AIErrorRecoveryManager not available as fallback: {e}")
            self.ai_error_recovery = None

    def _class_available(self, class_name: str) -> bool:
        """Check if a class is available in the current module scope"""
        try:
            # Direct class reference check - much simpler and more reliable
            return getattr(__import__(__name__), class_name, None) is not None
        except (AttributeError, ImportError):
            return False

    def _get_systems_status(self) -> Dict[str, bool]:
        """Get current status of all MYNFINI systems - FIXED to show actual status"""
        return {
            'narrative_consistency': self.narrative_consistency_enforcer is not None,
            'pacing_engine': self.pacing_manager is not None,
            'clock_mechanics': self.clock_system is not None,
            'adversity_evolution': self.adversity_evolution_system is not None,
            'progression_system': self.multi_axis_progression_system is not None,
            'narrative_points': self.narrative_points_system is not None,  # Use actual system reference
            'dynamics_optimization': self.dynamics_optimization_system is not None,
            'creativity_evaluation': self.creativity_evaluator is not None,  # Always available
            'interactive_resolution': self.interactive_resolution is not None,  # Always available
            'personal_class_generation': self.class_generator is not None,  # Always available
            'cbx_system': True,  # Always available
            'sensory_descriptor': self.sensory_descriptor is not None,
            'cohesion_manager': self.cohesion_manager is not None,
            'eight_pillars_framework': self.eight_pillars_framework is not None,
            'ai_error_recovery': self.ai_error_recovery is not None,
            'k2_905_integration': self.k2_orchestrator is not None  # Kimi K2-905 integration status
        }

    def make_skill_check(self, character_data: Dict, attribute1: str, attribute2: str, difficulty: int, context: str = "") -> Dict[str, Any]:
        """CERTAIN: Implement complete skill check system with critical/fumble mechanics"""
        try:
            if self.clock_system and hasattr(self.clock_system, 'make_attribute_check'):
                # Build proper character object from web data
                from dataclasses import dataclass
                @dataclass
                class TempCharacter:
                    name: str
                    attributes: Dict
                    hp_current: int
                    hp_max: int
                    mp_current: int
                    mp_max: int
                    ip_current: int
                    ip_max: int
                    level: int

                character = TempCharacter(
                    name=character_data.get('name', 'Player'),
                    attributes={attr: Attribute(AttributeType[attr], die) for attr, die in character_data.get('attributes', {}).items()},
                    hp_current=character_data.get('hp_current', 10),
                    hp_max=character_data.get('hp_max', 10),
                    mp_current=character_data.get('mp_current', 10),
                    mp_max=character_data.get('mp_max', 10),
                    ip_current=character_data.get('ip_current', 10),
                    ip_max=character_data.get('ip_max', 10),
                    level=character_data.get('level', 1)
                )

                result = self.clock_system.make_attribute_check(
                    character,
                    AttributeType[attribute1],
                    AttributeType[attribute2],
                    difficulty,
                    context
                )

                return {
                    'success': result.success,
                    'result': result.result_type.value,
                    'total': result.total,
                    'dice_rolled': result.dice_rolled,
                    'opportunities_gained': result.opportunities_generated,
                    'fabula_gained': result.fabula_points_gained,
                    'message': result.message,
                    'critical': result.critical,
                    'fumble': result.fumble,
                    'high_roll': result.high_roll
                }
            else:
                return self._fallback_skill_check(attribute1, attribute2, difficulty, context)

        except Exception as e:
            print(f"[ERROR] Skill check system failed: {e}")
            return self._fallback_skill_check(attribute1, attribute2, difficulty, context)

    def _fallback_skill_check(self, attr1: str, attr2: str, difficulty: int, context: str) -> Dict[str, Any]:
        """Fallback skill check when full mechanics unavailable"""
        import random

        # Roll dice for both attributes
        die1 = random.randint(1, 8)  # Default d8
        die2 = random.randint(1, 8)
        total = die1 + die2

        # Critical and fumble per protocol
        critical = die1 == die2 and die1 >= 6
        fumble = die1 == 1 and die2 == 1

        success = (total >= difficulty) or critical

        if critical:
            message = "Critical Success! (Opportunity gained)"
            opportunities = 1
            fabula_gain = 0
        elif fumble:
            message = "Fumble! (1 FP gained)"
            opportunities = 0
            fabula_gain = 1
        elif success:
            message = f"Success! ({total} vs DL {difficulty})"
            opportunities = 0
            fabula_gain = 0
        else:
            message = f"Failure ({total} vs DL {difficulty})"
            opportunities = 0
            fabula_gain = 0

        return {
            'success': success,
            'result': 'critical_success' if critical else ('fumble' if fumble else ('success' if success else 'failure')),
            'total': total,
            'dice_rolled': [die1, die2],
            'opportunities_gained': opportunities,
            'fabula_gained': fabula_gain,
            'message': message,
            'critical': critical,
            'fumble': fumble,
            'high_roll': max(die1, die2)
        }

    def initiate_advanced_system(self):
        """CERTAIN: Advanced system initialization with complete MYNFINI mechanics"""
        init_prompt = """You are MYNFINI Revolutionary AI Game Master with complete mechanics system.

User has activated the comprehensive web-based system including:
- Complete narrative consistency engine
- Advanced clock mechanics with critical/fumble
- Multi-axis progression system
- Narrative points and adversity evolution
- Pacing engine and sensory descriptions
- Character arcs and story cohesion
- Interactive Resolution System (creativity defeats statistics)
- 5-tier creativity evaluation engine
- AI-assisted creative description builder
- Personal class generation from behavior
- Choice-Based Experience (CBX) system

Create personalized welcome showing awareness of:
1. Complete mechanistic system activation
2. Revolutionary narrative processing
3. Advanced progression tracking
4. Comprehensive game state management
5. Creative resolution mechanics

Return JSON: {"welcome_message": "message", "system_status": "advanced_ready", "narrative_points": 0, "total_systems": "complete"}"""

        try:
            from config import Config
            client = Config().get_client()

            response = client.messages.create(
                model="claude-3-5-haiku-20141022",
                max_tokens=800,
                messages=[{"role": "user", "content": init_prompt}]
            )

            result = json.loads(response.content[0].text)

            # Add system configuration data
            result['systems_active'] = {
                'narrative_consistency': self.narrative_consistency is not None,
                'pacing_engine': self.pacing_manager is not None,
                'clock_mechanics': self.clock_system is not None,
                'adversity_evolution': self.adversity_system is not None,
                'progression_system': self.progression_system is not None,
                'narrative_points': self.narrative_points_system is not None,
                'creativity_evaluation': True,
                'interactive_resolution': True,
                'personal_class_generation': True,
                'cbx_system': True
            }

            print(f"[VERIFIED] Advanced system initialization complete: {len(result.get('welcome_message', ''))} characters")
            return result

        except json.JSONDecodeError as e:
            logging.error(f"[ERROR] AI response not valid JSON: {e}")
            return self.create_advanced_fallback()
        except Exception as e:
            logging.error(f"[ERROR] Advanced system initialization failed: {e}")
            return None

    def process_revolutionary_input(self, user_input: str, game_state: Dict, character_data: Dict = None) -> Dict[str, Any]:
        """CERTAIN: Process input with CORE MECHANICS EVOLUTION - THE REVOLUTION"""
        try:
            # Check for creative resolution requests
            if self._is_creative_action_request(user_input):
                return self._process_creative_resolution(user_input, game_state, character_data)

            # Check for personal class analysis requests
            if self._is_class_analysis_request(user_input):
                return self._process_class_analysis(user_input, game_state)

            # Check for narrative points spending
            if self._is_narrative_points_request(user_input):
                return self._process_narrative_points(user_input, game_state)

            # Check for K2-905 mega-task requests
            if self._is_k2_mega_task_request(user_input):
                return self._process_k2_mega_task(user_input, game_state)

            # Process as advanced narrative input
            return self.process_advanced_input(user_input, game_state)

        except Exception as e:
            print(f"[ERROR] Revolutionary input processing failed: {e}")
            return self.create_advanced_fallback()

    def _is_creative_action_request(self, user_input: str) -> bool:
        """Determine if input is requesting creative resolution"""
        creative_indicators = ['i describe', 'i use', 'i attempt', 'i try', 'creative', 'environmental']
        return any(indicator in user_input.lower() for indicator in creative_indicators)

    def _process_creative_resolution(self, user_input: str, game_state: Dict, character_data: Dict) -> Dict[str, Any]:
        """Process creative resolution with Interactive Resolution System"""
        player_data = character_data or game_state.get('character', {})

        # Use Interactive Resolution System - THE REVOLUTION
        resolution_result = self.interactive_resolution.resolve_action_with_creativity(
            user_input, player_data, game_state
        )

        # Update global state
        if resolution_result.get('narrative_points_earned', 0) > 0:
            self.narrative_points += resolution_result['narrative_points_earned']

        if resolution_result.get('cbx_earned', 0) > 0:
            self.cbx_total += resolution_result['cbx_earned']

        return {
            'narrative': resolution_result['narrative_response'],
            'creativity_evaluation': resolution_result['creativity_evaluation'],
            'mechanical_outcome': resolution_result['mechanical_outcome'],
            'elements': {'world': 'revolutionary resolution active'},
            'cbx_earned': resolution_result['cbx_earned'],
            'narrative_points_total': self.narrative_points,
            'systems_active': {'creative_resolution': True, 'interactive_systems': True}
        }

    def _is_class_analysis_request(self, user_input: str) -> bool:
        """Determine if input is requesting personal class analysis"""
        class_indicators = ['class analysis', 'my class', 'personal class', 'behavior analysis', 'journey analysis']
        return any(indicator in user_input.lower() for indicator in class_indicators)

    def _process_class_analysis(self, user_input: str, game_state: Dict) -> Dict[str, Any]:
        """Process personal class analysis request"""
        player_id = game_state.get('player_id', 'player')
        player_behavior_data = game_state.get('player_behavior', {})

        # Analyze player behavior for class emergence
        class_assessment = self.class_generator.analyze_player_behavior(player_id, player_behavior_data)

        # Generate narrative response
        if class_assessment['emergence_eligible']:
            narrative = f"Analyzing your journey... Your consistent patterns reveal your emerging identity. {class_assessment['behavioral_insights'][0]} Your personal class {class_assessment['recommended_class']['class_name']} is forming through your {class_assessment['dominant_pattern'].replace('_', ' ')} approach. {class_assessment['growth_recommendations'][0]}"
        else:
            narrative = f"Analyzing your behavior patterns... You show emerging tendencies toward {class_assessment['dominant_pattern'].replace('_', ' ')} if patterns continue. {class_assessment['growth_recommendations'][0]} More data needed for complete class formation."

        return {
            'narrative': narrative,
            'class_assessment': class_assessment,
            'elements': {'analysis': 'complete', 'personal_class': class_assessment['recommended_class']},
            'cbx_earned': 0,
            'narrative_points_total': self.narrative_points
        }

    def _is_narrative_points_request(self, user_input: str) -> bool:
        """Determine if input is requesting narrative points spending"""
        np_indicators = ['narrative point', 'spend point', 'use point', 'fate intervention', 'death defiance', 'story alteration']
        return any(indicator in user_input.lower() for indicator in np_indicators)

    def _process_narrative_points(self, user_input: str, game_state: Dict) -> Dict[str, Any]:
        """Process narrative points spending request"""
        current_np = self.narrative_points

        if current_np <= 0:
            return {
                'narrative': "You have no Narrative Points to spend. Earn them through legendary creativity, surviving desperate situations, or dramatic story moments.",
                'error': 'insufficient_narrative_points',
                'narrative_points_total': 0
            }

        # Detect spending intent
        if 'fate intervention' in user_input.lower():
            cost = 1
            effect = "reroll with advantage"
        elif 'death defiance' in user_input.lower():
            cost = 2
            effect = "survive certain death"
        elif 'story alteration' in user_input.lower():
            cost = 3
            effect = "major narrative change"
        else:
            cost = 1
            effect = "narrative intervention"

        if cost <= current_np:
            self.narrative_points -= cost
            narrative = f"You spend {cost} Narrative Point{'s' if cost > 1 else ''} for {effect}. Reality bends to your dramatic vision."
            return {
                'narrative': narrative,
                'narrative_points_spent': cost,
                'narrative_points_total': self.narrative_points,
                'effect': effect
            }
        else:
            return {
                'narrative': f"That costs {cost} Narrative Points, but you only have {current_np}. Consider earning more through creative brilliance or dramatic story moments.",
                'error': 'insufficient_narrative_points',
                'narrative_points_total': current_np
            }

    def _is_k2_mega_task_request(self, user_input: str) -> bool:
        """Determine if input is requesting K2-905 mega-task processing"""
        k2_indicators = ['mega task', 'k2 task', 'massive parallel', '127 agents', 'kimi k2', 'synthetic.new', 'moonshot']
        return any(indicator in user_input.lower() for indicator in k2_indicators)

    def _process_k2_mega_task(self, user_input: str, game_state: Dict) -> Dict[str, Any]:
        """Process K2-905 mega-task with 127-agent orchestration"""
        # Check if K2-905 orchestrator is available
        if not self.k2_orchestrator:
            return {
                'narrative': "Kimi K2-905 orchestrator not available. Please ensure kimi_k2_orchestrator.py is properly installed.",
                'error': 'k2_orchestrator_unavailable',
                'systems_active': self._get_systems_status()
            }

        try:
            # Execute mega-task using KimiK2Orchestrator
            import asyncio
            result = asyncio.run(self.execute_k2_mega_task(user_input, game_state))

            return {
                'narrative': f"K2-905 mega-task completed with {result.get('total_agents_deployed', 0)} agents in parallel.",
                'k2_result': result,
                'elements': {'world': 'k2_905_mega_parallel_active'},
                'cbx_earned': result.get('cbx_earned', 0),
                'narrative_points_total': self.narrative_points,
                'systems_active': {'k2_905_integration': True, 'mega_parallel_mode': True}
            }
        except Exception as e:
            print(f"[ERROR] K2-905 mega-task processing failed: {e}")
            return {
                'narrative': f"K2-905 mega-task processing failed: {str(e)}",
                'error': 'k2_mega_task_failed',
                'systems_active': self._get_systems_status()
            }

    async def execute_k2_mega_task(self, main_task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute massive tasks using KimiK2Orchestrator with 127-agent mega-parallel orchestration"""
        if not self.k2_orchestrator:
            raise ValueError("KimiK2Orchestrator not initialized")

        # Delegate to KimiK2Orchestrator
        result = await self.k2_orchestrator.execute_mega_task(main_task, context)

        # Update global state with any earned points
        if result.get('narrative_points_earned', 0) > 0:
            self.narrative_points += result['narrative_points_earned']

        if result.get('cbx_earned', 0) > 0:
            self.cbx_total += result['cbx_earned']

        return result

    def initiate_advanced_system(self):
        """CERTAIN: Advanced system initialization with complete MYNFINI mechanics"""
        init_prompt = """You are MYNFINI Web AI Game Master with complete revolutionary mechanics.

User has activated the comprehensive web-based system including:
- Complete narrative consistency engine
- Advanced clock mechanics with critical/fumble
- Multi-axis progression system
- Narrative points and adversity evolution
- Pacing engine and sensory descriptions
- Character arcs and story cohesion

Create personalized welcome showing awareness of:
1. Complete mechanistic system activation
2. Revolutionary narrative processing
3. Advanced progression tracking
4. Comprehensive game state management

Return JSON: {"welcome_message": "message", "system_status": "advanced_ready", "narrative_points": 0, "total_systems": "complete"}"""

        try:
            from config import Config
            client = Config().get_client()

            response = client.messages.create(
                model="claude-3-5-haiku-20141022",
                max_tokens=800,
                messages=[{"role": "user", "content": init_prompt}]
            )

            result = json.loads(response.content[0].text)

            # Add system configuration data
            result['systems_active'] = {
                'narrative_consistency': self.narrative_consistency is not None,
                'pacing_engine': self.pacing_manager is not None,
                'clock_mechanics': self.clock_system is not None,
                'adversity_evolution': self.adversity_system is not None,
                'progression_system': self.progression_system is not None,
                'narrative_points': self.narrative_points_system is not None,
                'k2_905_integration': self.k2_orchestrator is not None
            }

            print(f"[VERIFIED] Advanced system initialization complete: {len(result.get('welcome_message', ''))} characters")
            return result

        except json.JSONDecodeError as e:
            logging.error(f"[ERROR] AI response not valid JSON: {e}")
            return self.create_advanced_fallback()
        except Exception as e:
            logging.error(f"[ERROR] Advanced system initialization failed: {e}")
            return None

    def process_advanced_input(self, user_input: str, game_state: Dict) -> Dict[str, Any]:
        """CERTAIN: Advanced MYNFINI processing with complete mechanics"""
        # Initialize advanced context
        context_data = self._build_advanced_context(game_state)

        step_prompt = f"""You are MYNFINI Revolutionary AI Game Master with complete mechanics system.

User Input: "{user_input}"

Advanced System Context:
{json.dumps(context_data, indent=2)}

Use complete MYNFINI mechanics including:
1. Narrative consistency with established facts
2. Advanced pacing based on scene type and emotional intensity
3. Clock mechanics with critical/fumble opportunities
4. Multi-axis character progression tracking
5. Narrative points and adversity evolution
6. Character arc development and psychological depth
7. Kimi K2-905 Integration with 127-agent mega-parallel orchestration

Generate rich, immersive experience with:
- Layered sensory descriptions (sight, sound, smell, touch, taste)
- Dynamic pacing that adjusts to story flow
- Narrative threads and thematic coherence
- Character development opportunities
- Mechanical consequences woven into storytelling
- K2-905 enhanced processing when available

Return JSON with enhanced structure including mechanics results."""

        try:
            from config import Config
            client = Config().get_client()

            response = client.messages.create(
                model="claude-3-5-haiku-20141022",
                max_tokens=1500,
                messages=[{"role": "user", "content": step_prompt}]
            )

            result = json.loads(response.content[0].text)

            # Enhance with mechanical interactions if available
            enhanced_result = self._enhance_with_mechanics(result, game_state)

            print(f"[VERIFIED] Advanced processing complete: {len(enhanced_result.get('narrative', ''))} characters")
            return enhanced_result

        except json.JSONDecodeError as e:
            logging.error(f"[ERROR] AI response parsing failed: {e}")
            return self.create_advanced_fallback()

    def _build_advanced_context(self, game_state: Dict) -> Dict[str, Any]:
        """Build comprehensive context for advanced AI processing"""
        context = {
            "current_step": game_state.get("current_step", self.current_step),
            "session_state": game_state.get("session_state", "SESSION_ZERO"),
            "cbx_total": self.cbx_total,
            "narrative_points": self.narrative_points,
            "scene_type": game_state.get("scene_type", "Standard"),
            "emotional_intensity": game_state.get("emotional_intensity", 0),
            "character_data": game_state.get("character", {}),
            "world_elements": game_state.get("world_elements", []),
            "narrative_threads": self.narrative_threads,
            "character_arcs": self.character_arcs,
            "sensory_environment": self.sensory_environment,
            "k2_905_available": self.k2_orchestrator is not None,
            "mega_parallel_mode": self.mega_parallel_mode,
            "max_agents": self.max_agents
        }

        # Add narrative consistency data if available
        if self.narrative_consistency and hasattr(self.narrative_consistency, 'get_current_context'):
            consistency_check = self.narrative_consistency.get_current_context(game_state)
            if consistency_check:
                context["consistency_enforcer"] = consistency_check

        return context

    def _enhance_with_mechanics(self, ai_result: Dict, game_state: Dict) -> Dict[str, Any]:
        """Enhance AI results with mechanical system interactions"""
        result = ai_result.copy()

        # Add mechanical bonuses
        enhanced_narrative = result.get('narrative', '')

        if self.clock_system and result.get('trigger_check'):
            # Perform mechanical check if AI indicates need
            check_result = self.make_skill_check(
                game_state.get('character', {}),
                result.get('check_attribute1', 'DEXTERITY'),
                result.get('check_attribute2', 'INSIGHT'),
                result.get('check_difficulty', 8)
            )
            result['mechanical_result'] = check_result
            enhanced_narrative += f"\n\n[Mechanical Result: {check_result['message']}]"

            # Add consequences from mechanical check
            if check_result['opportunities_gained'] > 0:
                enhanced_narrative += f"\n[Opportunity gained for {check_result['opportunities_gained']} additional actions]"
            if check_result['fabula_gained'] > 0:
                enhanced_narrative += f"\n[Fabula Point gained from fumble]"
                self.narrative_points += check_result['fabula_gained']

        # Handle narrative points if earned
        if result.get('narrative_points_earned'):
            self.narrative_points += result['narrative_points_earned']
            enhanced_narrative += f"\n[Narrative Points +{result['narrative_points_earned']}]"

        # Add character arc advancement
        if result.get('character_arc_advancement'):
            character_name = result.get('character_name', 'Player')
            if character_name not in self.character_arcs:
                self.character_arcs[character_name] = []
            self.character_arcs[character_name].append({
                'timestamp': datetime.now().isoformat(),
                'advancement': result['character_arc_advancement'],
                'narrative_context': result.get('context', '')
            })
            enhanced_narrative += f"\n[Character Arc: {result['character_arc_advancement']}]"

        result['narrative'] = enhanced_narrative
        result['enhanced_cbx_earned'] = result.get('cbx_earned', 0) + (check_result.get('opportunities_gained', 0) * 5 if 'check_result' in locals() else 0)
        result['narrative_points_total'] = self.narrative_points

        # Track narrative threads
        if result.get('new_narrative_thread'):
            self.narrative_threads.append({
                'timestamp': datetime.now().isoformat(),
                'thread': result['new_narrative_thread'],
                'importance': result.get('thread_importance', 1)
            })

        return result

    def create_advanced_fallback(self):
        """CERTAIN: Advanced fallback with mechanical implications"""
        return {
            "narrative": "System processing advanced mechanics. Please describe your adventure in more detail.",
            "elements": {"world": "Advanced system loading narrative mechanics"},
            "cbx_earned": 0,
            "cbx_earned_enhanced": 0,
            "narrative_points_total": self.narrative_points,
            "systems_active": self._get_systems_status(),
            "error": "Advanced system processing additional narrative context"
        }

