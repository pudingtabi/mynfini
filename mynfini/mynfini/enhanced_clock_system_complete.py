"""
COMPLETE Enhanced Clock Mechanics System - MYNFINI Revolutionary Implementation
Advanced clock-based mechanical system for TTRPG timing, critical/fumble mechanics, and progress tracking
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any
import json
import random
from datetime import datetime, timedelta
from collections import deque, defaultdict

class OpportunityType(Enum):
    """Types of opportunities created by clock mechanics"""
    INFORMATION_GAIN = "information_gain"
    POSITIONAL_ADVANTAGE = "positional_advantage"
    RESOURCE_CREATION = "resource_creation"
    RELATIONSHIP_DEVELOPMENT = "relationship_development"
    TIMING_ADVANTAGE = "timing_advantage"
    REVELATION = "revelation"

class ClockFillResult(Enum):
    """Results of filling clock sections"""
    PARTIAL_FILL = "partial_fill"
    COMPLETE_FILL = "complete_fill"
    OVERFILL = "overfill"
    CRITICAL_COMPLETE = "critical_complete"

@dataclass
class CheckResult:
    """Complete result of a skill check with enhanced mechanics"""
    success: bool
    result: str
    opportunities_gained: int
    fabula_gained: int
    fumble: bool
    critical_success: bool
    mechanical_advantage: bool
    detailed_description: str
    context_impact: Dict[str, Any]

@dataclass
class EnhancementContext:
    """Context for mechanical enhancements"""
    environmental_elements: List[str]
    tactical_factors: List[str]
    narrative_weight: float
    scene_type: str
    time_pressure: float
    risk_level: float

class EnhancedClockSystem:
    """
    COMPLETE Enhanced Clock Mechanics System
    Revolutionary clock-based mechanical system for TTRPG timing, critical/fumble mechanics, and progress tracking
    """

    def __init__(self):
        self.active_clocks = {}
        self.completed_clocks = {}
        self.global_opportunities = deque(maxlen=10)
        self.critical_failures = deque(maxlen=20)
        self.system_status = {
            "total_clocks_created": 0,
            "total_clocks_completed": 0,
            "critical_successes": 0,
            "fumbles_occurred": 0,
            "opportunities_generated": 0
        }

        # Mechanical enhancement matrices
        self.enhancement_multipliers = {
            "environmental": {
                "basic": 1.1,
                "creative": 1.3,
                "brilliant": 1.5,
                "legendary": 2.0
            },
            "tactical": {
                "basic": 1.0,
                "coordinated": 1.2,
                "complex": 1.4,
                "masterful": 1.7
            },
            "narrative": {
                "low": 1.0,
                "medium": 1.2,
                "high": 1.5,
                "epic": 2.0
            }
        }

        # Critical and fumble tables for enhanced outcomes
        self.critical_outcomes = {
            "combat": [
                "Devastating blow that changes the battlefield",
                "Perfect execution that inspires allies",
                "Critical insight reveals enemy weakness",
                "Legendary maneuver becomes instant legend"
            ],
            "social": [
                "Brilliant oration sways entire crowd",
                "Perfect timing creates lasting alliance",
                "Insightful words resolve deep conflict",
                "Charismatic display earns lifelong loyalty"
            ],
            "exploration": [
                "Discovery reveals hidden pathway",
                "Perfect navigation saves massive time",
                "Environmental mastery unlocks secrets",
                "Intuitive understanding reveals treasure"
            ]
        }

        self.fumble_outcomes = {
            "combat": [
                "Weapon jam/break at critical moment",
                "Attack leaves you exposed and vulnerable",
                "Misfire hits unintended target",
                "Momentum carries you into danger"
            ],
            "social": [
                "Words accidentally deeply offend",
                "Misunderstanding creates lasting grudge",
                "Attempted charm becomes mockery",
                "Timing couldn't be worse"
            ],
            "exploration": [
                "Careless step triggers hidden trap",
                "Wrong turn leads to dangerous area",
                "Missed clue causes major setback",
                "Equipment failure at worst moment"
            ]
        }

    def make_attribute_check(self, attribute_value: int, target_difficulty: int,
                           context: EnhancementContext, creativity_description: str = None) -> CheckResult:
        """
        Revolutionary attribute check system that incorporates creativity and narrative weight
        """
        # Base mechanics from Fabula Ultima
        base_roll = random.randint(1, attribute_value)
        success_threshold = target_difficulty

        # Calculate enhancement multipliers based on creativity
        creativity_bonus = self._calculate_creativity_bonus(creativity_description, context)
        environmental_bonus = self._calculate_environmental_bonus(context)
        tactical_bonus = self._calculate_tactical_bonus(context)

        # Apply total enhancement to the roll
        total_enhancement = creativity_bonus + environmental_bonus + tactical_bonus
        enhanced_roll = base_roll + int(total_enhancement)

        # Determine success/failure with enhanced mechanics
        success = enhanced_roll >= success_threshold
        opportunities_gained = 0
        fabula_gained = 1 if success else 0
        fumble = base_roll <= 2
        critical_success = enhanced_roll >= success_threshold + 10
        mechanical_advantage = False

        # Generate detailed description
        detailed_description = self._generate_check_description(
            success, fumble, critical_success, base_roll, enhanced_roll,
            creativity_description, context, creativity_bonus
        )

        # Create opportunities from successful creative actions
        if success and creativity_description and creativity_bonus > 1.0:
            opportunities_gained = self._generate_opportunities(context, creativity_bonus)

        # Contextual impact tracking
        context_impact = self._calculate_context_impact(success, creativity_bonus, context)

        # Update system statistics
        if critical_success:
            self.system_status["critical_successes"] += 1
        if fumble:
            self.system_status["fumbles_occurred"] += 1
        if opportunities_gained > 0:
            self.system_status["opportunities_generated"] += opportunities_gained

        return CheckResult(
            success=success,
            result="SUCCESS" if success else "FAILURE",
            opportunities_gained=opportunities_gained,
            fabula_gained=fabula_gained,
            fumble=fumble,
            critical_success=critical_success,
            mechanical_advantage=mechanical_advantage,
            detailed_description=detailed_description,
            context_impact=context_impact
        )

    def create_clock(self, clock_id: str, name: str, segments: int = 6,
                    description: str = "", category: str = "progress") -> Dict:
        """Create a new progress clock with enhanced tracking"""
        clock_data = {
            "id": clock_id,
            "name": name,
            "segments": segments,
            "filled_segments": 0,
            "description": description,
            "category": category,
            "created_timestamp": datetime.now(),
            "opportunities_generated": [],
            "critical_events": [],
            "completion_bonuses": {
                "opportunities": segments // 2,
                "fabula": segments,
                "narrative_weight": segments * 0.2
            }
        }

        self.active_clocks[clock_id] = clock_data
        self.system_status["total_clocks_created"] += 1

        return clock_data

    def fill_clock_segment(self, clock_id: str, segments_filled: int = 1,
                          reason: str = "", context: EnhancementContext = None) -> ClockFillResult:
        """Fill one or more segments of a progress clock"""
        if clock_id not in self.active_clocks:
            return ClockFillResult.PARTIAL_FILL

        clock = self.active_clocks[clock_id]
        old_filled = clock["filled_segments"]
        new_filled = min(clock["segments"], old_filled + segments_filled)

        clock["filled_segments"] = new_filled

        # Log the fill event with reason
        fill_event = {
            "segments_filled": segments_filled,
            "reason": reason,
            "timestamp": datetime.now(),
            "context": context.__dict__ if context else {}
        }

        # Generate opportunities on significant fills
        if segments_filled > 1 or new_filled - old_filled >= 2:
            opportunities = self._generate_opportunities(context or EnhancementContext([], [], 1.0, "general", 0.5, 0.5), segments_filled)
            clock["opportunities_generated"].extend([f"opportunity_{i}" for i in range(opportunities)])

        # Determine fill result
        if new_filled == clock["segments"]:
            self._complete_clock(clock_id)
            return ClockFillResult.COMPLETE_FILL
        elif new_filled > old_filled:
            return ClockFillResult.PARTIAL_FILL
        else:
            return ClockFillResult.OVERFILL

    def _complete_clock(self, clock_id: str):
        """Handle clock completion with bonuses and effects"""
        clock = self.active_clocks[clock_id]

        # Generate completion bonuses
        bonuses = clock["completion_bonuses"]

        # Create opportunities
        for i in range(bonuses["opportunities"]):
            self._create_global_opportunity(clock["category"], f"From completing: {clock['name']}")

        # Move to completed
        self.completed_clocks[clock_id] = clock
        del self.active_clocks[clock_id]

        self.system_status["total_clocks_completed"] += 1

    def _create_global_opportunity(self, opportunity_type: str, description: str):
        """Create a global opportunity available to all players"""
        opportunity = {
            "type": opportunity_type,
            "description": description,
            "created_timestamp": datetime.now(),
            "claimed": False,
            "mechanical_benefit": self._calculate_opportunity_benefit(opportunity_type)
        }

        self.global_opportunities.append(opportunity)

    def _calculate_opportunity_benefit(self, opportunity_type: str) -> Dict:
        """Calculate mechanical benefits for different opportunity types"""
        benefits = {
            "information_gain": {"bonus_to_next_check": 2},
            "positional_advantage": {"advantage_on_next_roll": True},
            "resource_creation": {"temporary_resource": 1},
            "relationship_development": {"social_bonus": 3},
            "timing_advantage": {"reroll_next_check": True},
            "revelation": {"story_bonus": 2}
        }

        return benefits.get(opportunity_type, {"generic_bonus": 1})

    def _calculate_creativity_bonus(self, creativity_description: str, context: EnhancementContext) -> float:
        """Calculate bonus multiplier from creative descriptions"""
        if not creativity_description:
            return 0.0

        # Analyze creativity description length and keyword richness
        description_length = len(creativity_description)
        keyword_count = len([word for word in ["environment", "tactical", "clever", "innovative"] if word in creativity_description.lower()])

        # Base bonus from description complexity
        base_bonus = min(5.0, description_length / 50)  # Cap at +5

        # Keyword bonus
        keyword_bonus = keyword_count * 0.5

        # Context bonus
        context_bonus = len(context.environmental_elements) * 0.3 + len(context.tactical_factors) * 0.2

        return base_bonus + keyword_bonus + context_bonus

    def _calculate_environmental_bonus(self, context: EnhancementContext) -> float:
        """Calculate bonus from environmental utilization"""
        return len(context.environmental_elements) * 0.5

    def _calculate_tactical_bonus(self, context: EnhancementContext) -> float:
        """Calculate bonus from tactical considerations"""
        return len(context.tactical_factors) * 0.3

    def _generate_check_description(self, success: bool, fumble: bool, critical: bool,
                                  base_roll: int, enhanced_roll: int, creativity_description: str,
                                  context: EnhancementContext, creativity_bonus: float) -> str:
        """Generate detailed narrative description of the check result"""

        if critical:
            outcome = random.choice(self.critical_outcomes.get(context.scene_type, ["Stunning success!"]))
            return f"CRITICAL SUCCESS: {outcome} [Base: {base_roll} + Enhanced: {creativity_bonus:.1f} = {enhanced_roll}]"
        elif fumble:
            outcome = random.choice(self.fumble_outcomes.get(context.scene_type, ["Terrible failure!"]))
            return f"FUMBLE: {outcome} [Base: {base_roll}]"
        elif success:
            if creativity_description and creativity_bonus > 1.0:
                return f"SUCCESS through creativity: {creativity_description} [Enhanced: {enhanced_roll}]"
            else:
                return f"SUCCESS: Solid execution [Roll: {enhanced_roll}]"
        else:
            if creativity_description:
                return f"FAILED despite creativity: {creativity_description} [Enhanced: {enhanced_roll}]"
            else:
                return f"FAILED: Not enough skill or luck [Roll: {enhanced_roll}]"

    def _generate_opportunities(self, context: EnhancementContext, magnitude: int) -> int:
        """Generate opportunities from successful creative actions"""
        base_opportunities = magnitude // 2
        narrative_bonus = int(context.narrative_weight)
        return base_opportunities + narrative_bonus

    def _calculate_context_impact(self, success: bool, creativity_bonus: float, context: EnhancementContext) -> Dict[str, Any]:
        """Calculate how this action impacts the broader context"""
        return {
            "narrative_momentum": 1 if success else -1,
            "creativity_multiplier": creativity_bonus,
            "time_consequences": context.time_pressure,
            "risk_outcome": context.risk_level if success else context.risk_level * 2
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status for reporting"""
        return {
            "enhanced_clock_system": True,
            "active_clocks": len(self.active_clocks),
            "completed_clocks": len(self.completed_clocks),
            "global_opportunities": len(self.global_opportunities),
            "critical_successes_total": self.system_status["critical_successes"],
            "fumbles_total": self.system_status["fumbles_occurred"],
            "opportunities_generated_total": self.system_status["opportunities_generated"],
            "clocks_created_total": self.system_status["total_clocks_created"],
            "clocks_completed_total": self.system_status["total_clocks_completed"]
        }