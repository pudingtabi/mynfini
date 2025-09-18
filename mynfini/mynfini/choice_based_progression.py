"""
CHOICE-BASED PROGRESSION SYSTEM FOR MYNFINI
Grows characters through consequences - failures teach more than success
Based on "Growth Through Adversity" from CORE MECHANICS EVOLUTION
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict


class ChoiceCategory(Enum):
    ETHICAL_DILEMMA = "ethical_dilemma"
    SACRIFICE_CHOICE = "sacrifice_choice"
    FAILURE_CHOICE = "failure_choice"
    TRUST_CHOICE = "trust_choice"
    IDENTITY_CHOICE = "identity_choice"
    RELATIONSHIP_CHOICE = "relationship_choice"


class ChoiceConsequence(Enum):
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"
    PERMANENT = "permanent"


class FailureType(Enum):
    SPECTACULAR_FAILURE = "spectacular_failure"
    BETRAYAL_FAILURE = "betrayal_failure"
    MORAL_COMPROMISE_FAILURE = "moral_compromise_failure"
    TRAGIC_FAILURE = "tragic_failure"
    HUMILIATING_FAILURE = "humiliating_failure"


@dataclass
class CharacterChoice:
    id: str
    description: str
    category: ChoiceCategory
    no_good_options: bool
    consequences: Dict[str, List[Dict[str, Any]]]
    emotional_weight: float  # 0.0 - 10.0
    moral_complexity: float  # 0.0 - 10.0
    stakes_level: float  # 0.0 - 10.0
    failure_probability: float  # 0.0 - 1.0
    revelation_potential: float  # how much about character it reveals


@dataclass
class CBXPRecord:
    amount: int
    category: str
    choice_id: str
    timestamp: datetime
    consequence: ChoiceConsequence
    failure_type: Optional[FailureType] = None


@dataclass
class ScarRecord:
    scar_type: str  # "physical", "emotional", "moral", "social"
    description: str
    mechanical_effect: Dict[str, Any]
    origin_chapter: str
    revelation_required: bool = False
    current_story_weight: float = 0.0  # 0.0 - 10.0
    player_acceptance: float = 0.0  # 0.0 - 10.0


@dataclass
class FailureTransformation:
    failure_type: FailureType
    failure_magnitude: float  # 0.0 - 10.0
    lessons_learned: List[str]
    abilities_gained: List[Dict[str, Any]]
    character_development: Dict[str, Any]
    available_progressions: List[str]
    narrative_importance: float  # how central to character arc


class ChoiceBasedProgressionSystem:
    """Grows characters through meaningful choices - failures teach more than success"""

    def __init__(self):
        self.choice_db = self._build_choice_database()
        self.cbx_records = []  # Choice-Based Experience
        self.scar_records = []
        self.failure_transformations = []
        self.wisdom_points = 0  # Separate from CBX - earned only through suffering
        self.choice_history = []
        self.character_progressions = defaultdict(list)

    def evaluate_player_choice(self, player_input: str, context: Dict[str, Any], character_data: Dict[str, Any]) -> Tuple[CharacterChoice, float, Optional[FailureType]]:
        """Determine the choice the player faces and its consequences"""

        # Analyze player input for choice patterns
        choice_patterns = self._identify_choice_patterns(player_input, context)

        # Match to appropriate choice category
        choice_category = self._determine_choice_category(player_input, context, character_data)

        # Generate appropriate choice based on situation
        available_choices = self._get_appropriate_choices(context, choice_category, character_data)

        if len(available_choices) == 0:
            # No choice situation - create one based on patterns
            choice = self._generate_emergent_choice(player_input, context, character_data, choice_patterns)
        else:
            choice = random.choice(available_choices)

        # Calculate choice weight and outcome
        cbx_gain = self._calculate_cbx_gain(choice, context, player_input)
        possible_failure = self._calculate_failure_probability(choice, context)

        return choice, cbx_gain, possible_failure

    def process_choice_and_consequences(self, choice: CharacterChoice, player_decision: str, character_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute choice consequences and character growth"""

        # Record the choice forever
        self._record_player_choice(choice, player_decision, context)

        # Determine short-term consequences
        immediate_result = self._resolve_immediate_consequences(choice, player_decision, context)

        # Check for failure (and the growth that comes with it)
        failure_type = self._check_if_failure_should_occur(choice, context, immediate_result)

        # Calculate CBX (Choice-Based Experience) - often higher for "bad" choices
        cbx_e = self._calculate_cbx_gain(choice, context, player_decision)
        if failure_type:
            cbx_e *= 1.5  # Failure teaches more
            if failure_type == FailureType.SPECTACULAR_FAILURE:
                cbx_e *= 1.5  # Spectacular failure = maximum learning

        # Process failure transformation if failure occurred
        if failure_type:
            failure_result = self._process_failure_transformation(failure_type, choice, character_data, context)
            self._create_scar_from_failure(failure_type, choice, context)
        else:
            failure_result = {"type": None, "magnitude": 0}

        # Calculate wisdom points (earned ONLY through suffering/painful lessons)
        wisdom_gain = self._calculate_wisdom_points(choice, character_data, immediate_result, failure_type)

        # Update character progression arcs
        self._update_character_development(character_data, choice, immediate_result, failure_type)

        # Schedule consequence timeline
        consequences_schedule = self._build_consequence_timeline(choice, player_decision, context)

        return {
            "immediate_result": immediate_result,
            "cbx_gained": cbx_e,
            "wisdom_points": wisdom_gain,
            "failure_transformation": failure_result,
            "scheduled_consequences": consequences_schedule,
            "character_growth": self._get_current_character_growth_progression(character_data),
            "choice_recorded": True
        }

    def _calculate_cbx_gain(self, choice: CharacterChoice, context: Dict[str, Any], player_input: str = "") -> int:
        """Calculate Choice-Based Experience - failures teach more than success"""

        base_cbx = choice.emotional_weight + choice.moral_complexity

        # Multipliers based on choice type (failures give more)
        if choice.category == ChoiceCategory.FAILURE_CHOICE:
            multiplier = 2.0
        elif choice.no_good_options:
            multiplier = 1.5
        elif choice.emotional_weight >= 5.0 and choice.no_good_options:
            multiplier = 1.8
        else:
            multiplier = 1.0

        # Additional factors
        additional_sources = 0

        # "Bad" choices often teach more
        if self._is_morally_complex_choice(choice, player_input):
            additional_sources += 1

        # High stakes teach more
        if choice.stakes_level >= 7.0:
            additional_sources += 2

        # Emotional investment teaches more
        if choice.revelation_potential >= 6.0:
            additional_sources += 1

        total_cbx = int((base_cbx * multiplier) + additional_sources)

        # Store the record
        cbx_record = CBXPRecord(
            amount=total_cbx,
            category=choice.category.value,
            choice_id=choice.id,
            timestamp=datetime.now(),
            consequence=ChoiceConsequence.SHORT_TERM  # Immediate consequence
        )
        self.cbx_records.append(cbx_record)

        return total_cbx

    def process_failure_transformation(self, failure_result: Dict[str, Any], character_data: Dict[str, Any]) -> FailureTransformation:
        """Transform failure into character growth and unique abilities"""

        failure_type = failure_result["failure_type"]
        failure_magnitude = failure_result["magnitude"]

        # Calculate specific transformations based on failure
        lessons_learned = self._extract_lessons_from_failure(failure_type, failure_magnitude)
        abilities_gained = self._generate_failure-based_abilities(failure_type, failure_magnitude, character_data)
        character_development = self._track_character_growth(failure_type, failure_magnitude)

        # Calculate available progression paths
        progressions = self._determine_failure_progressions(failure_type, failure_magnitude, character_data)

        transformation = FailureTransformation(
            failure_type=failure_type,
            failure_magnitude=failure_magnitude,
            lessons_learned=lessons_learned,
            abilities_gained=abilities_gained,
            character_development=character_development,
            available_progressions=progressions,
            narrative_importance=self._calculate_failure_narrative_importance(failure_type, failure_magnitude)
        )

        # Wisdom points only from true suffering/learning
        if failure_magnitude >= 7.0:
            self.wisdom_points += int(failure_magnitude / 2)

        self.failure_transformations.append(transformation)

        return transformation

    def _create_scar_from_failure(self, failure_type: FailureType, choice: CharacterChoice, context: Dict[str, Any]) -> None:
        """Create character scars that provide both disadvantage and unique abilities"""

        scar_type = self._determine_scar_type(failure_type)
        severity = self._calculate_scar_severity(failure_type, choice.emotional_weight)

        scar = ScarRecord(
            scar_type=scar_type,
            description=self._describe_scar(failure_type, choice),
            mechanical_effect=self._calculate_mechanical_effect(failure_type, severity),
            origin_chapter=context.get("current_chapter", "unknown"),
            current_story_weight=severity,
            player_acceptance=self._calculate_player_acceptance(context, scar_type)
        )

        self.scar_records.append(scar)

    def _build_choice_database(self) -> Dict[ChoiceCategory, List[CharacterChoice]]:
        """Build database of meaningful choices that force growth through consequences"""

        return {
            ChoiceCategory.FAILURE_CHOICE: [
                CharacterChoice(
                    id="spectacular_failure_1",
                    description="Attempt the impossible to save everyone, knowing you might fail tragically",
                    category=ChoiceCategory.FAILURE_CHOICE,
                    no_good_options=True,
                    consequences={
                        "failure": [{"type": "spectacular_failure", "magnitude": 9.0, "wisdom_gained": 4}],
                        "critical_success": [{"type": "legendary_achievement", "magnitude": 8.0}],
                        "partial_failure": [{"type": "bittersweet_victory", "magnitude": 6.0}]
                    },
                    emotional_weight=9.0,
                    moral_complexity=8.0,
                    stakes_level=10.0,
                    failure_probability=0.75,  # Very likely to fail, but teaches so much
                    revelation_potential=10.0
                ),
                CharacterChoice(
                    id="humiliating_failure_1",
                    description="Admit your limitations publicly, opening yourself to ridicule but gaining wisdom",
                    category=ChoiceCategory.FAILURE_CHOICE,
                    no_good_options=True,
                    consequences={
                        "failure": [{"type": "humiliation", "magnitude": 7.0, "wisdom_gained": 3, "character_growth": "humility"}],
                        "success": [{"type": "respect_gained", "magnitude": 5.0, "character_growth": "authenticity"}]
                    },
                    emotional_weight=7.0,
                    moral_complexity=6.0,
                    stakes_level=8.0,
                    failure_probability=0.60,
                    revelation_potential=8.0
                )
            ],
            ChoiceCategory.ETHICAL_DILEMMA: [
                CharacterChoice(
                    id="lesser_evil_1",
                    description="Choose between betraying a friend or allowing an evil to go unchecked",
                    category=ChoiceCategory.ETHICAL_DILEMMA,
                    no_good_options=True,
                    consequences={
                        "betray_f": [{"type": "friendship_damage", "magnitude": 8.0}, {"type": "evil_prevented", "magnitude": 7.0}],
                        "allow_evil": [{"type": "moral_cowardice", "magnitude": 6.0}, {"type": "guilt", "magnitude": 7.0}]
                    },
                    emotional_weight=9.0,
                    moral_complexity=9.0,
                    stakes_level=9.0,
                    failure_probability=0.00,  # No clear "failure" - just different failures
                    revelation_potential=9.0
                )
            ],
            ChoiceCategory.SACRIFICE_CHOICE: [
                CharacterChoice(
                    id="heroic_sacrifice_1",
                    description="Offer your well-being to save someone else, knowing it might not work and cost you everything",
                    category=ChoiceCategory.SACRIFICE_CHOICE,
                    no_good_options=True,
                    consequences={
                        "successful_sacrifice": [{"type": "permanent_damage", "magnitude": 9.0, "character_growth": "heroism"}],
                        "failed_sacrifice": [{"type": "wasted_suffering", "magnitude": 8.0, "emotional_scarring": True}],
                        "partial_sacrifice": [{"type": "shared_burden", "magnitude": 6.0}]
                    },
                    emotional_weight=10.0,
                    moral_complexity=9.0,
                    stakes_level=10.0,
                    failure_probability=0.50,  # 50% chance of total failure
                    revelation_potential=10.0
                )
            ]
        }

    # Additional helper methods would continue...

    def _is_morally_complex_choice(self, choice: CharacterChoice, player_input: str) -> bool:
        """Determine if choice involves moral complexity"""
        return choice.moral_complexity >= 7.0 or "moral" in player_input.lower()

    def _get_current_character_growth_progression(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate current character development progression"""

        num_choices = len([r for r in self.cbx_records if r.category != "routine"])
        num_scars = len(self.scar_records)
        avg_cbx_per_choice = sum(r.amount for r in self.cbx_records) / max(len(self.cbx_records), 1)

        return {
            "choice_experience": num_choices,
            "scars_accumulated": num_scars,
            "wisdom_points": self.wisdom_points,
            "average_cbx_per_moment": avg_cbx_per_choice,
            "scar_weight_total": sum(s.current_story_weight for s in self.scar_records),
            "failure_transformation_stage": len(self.failure_transformations),
            "character_arc_phase": self._determine_character_arc_phase()
        }

    def _determine_character_arc_phase(self) -> str:
        """Determine current phase of character development arc"""
        total_pressure = sum(r.amount for r in self.cbx_records) + len(self.scar_records) * 5

        if total_pressure < 25:
            return "emergence"
        elif total_pressure < 50:
            return "testing"
        elif total_pressure < 100:
            return "transformation"
        elif total_pressure < 200:
            return "revelation"
        else:
            return "transcendence"