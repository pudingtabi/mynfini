"""
COMPLETE Narrative Points System - MYNFINI Revolutionary Implementation
Replaces traditional Fabula Points with narrative-driven economy system
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import json
import uuid
from datetime import datetime
from collections import deque, defaultdict

class NPEarningTrigger(Enum):
    """Triggers for earning narrative points"""
    RISK_TAKING = "risk_taking"
    ROLEPLAYING_DEPTH = "roleplaying_depth"
    EMOTIONAL_INVESTMENT = "emotional_investment"
    STORY_ADVANCEMENT = "story_advancement"
    CHARACTER_GROWTH = "character_growth"
    SACRIFICIAL_CHOICE = "sacrificial_choice"
    CREATIVE_PROBLEM_SOLVING = "creative_problem_solving"
    DRAMATIC_TIMING = "dramatic_timing"
    RELATIONSHIP_DEVELOPMENT = "relationship_development"

class NPActivity(Enum):
    """Activities that can be done with narrative points"""
    RETCON_SCENE = "retcon_scene"
    INTRODUCE_ELEMENT = "introduce_element"
    EMPOWER_CHARACTER = "empower_character"
    NARRATIVE_ESCAPE = "narrative_escape"
    DRAMATIC_REVEAL = "dramatic_reveal"
    CHARACTER_RETCON = "character_retcon"
    ENVIRONMENT_MANIPULATION = "environment_manipulation"
    FORESHADOWING = "foreshadowing"

@dataclass
class NPCAction:
    """Action taken using narrative points"""
    action_type: NPActivity
    description: str
    cost: int
    timestamp: datetime
    character_context: Optional[Dict] = None
    narrative_justification: Optional[str] = None

@dataclass
class NPTransaction:
    """Transaction record for narrative points"""
    id: str
    amount: int
    balance_after: int
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    trigger: Optional[NPEarningTrigger] = None
    activity: Optional[NPActivity] = None
    character_id: Optional[str] = None
    scene_context: Optional[Dict] = None

class NarrativePointsSystem:
    """
    COMPLETE Narrative Points System Implementation
    Manages narrative point economy for dramatic storytelling
    """

    def __init__(self):
        self.player_balances = defaultdict(int)
        self.transaction_history = defaultdict(list)
        self.earnings_this_session = defaultdict(int)
        self.spending_this_session = defaultdict(int)
        self.current_scene_points = 0

        # Configured earnings and costs
        self.earning_rates = {
            NPEarningTrigger.RISK_TAKING: 2,
            NPEarningTrigger.ROLEPLAYING_DEPTH: 3,
            NPEarningTrigger.EMOTIONAL_INVESTMENT: 2,
            NPEarningTrigger.STORY_ADVANCEMENT: 1,
            NPEarningTrigger.CHARACTER_GROWTH: 2,
            NPEarningTrigger.SACRIFICIAL_CHOICE: 4,
            NPEarningTrigger.CREATIVE_PROBLEM_SOLVING: 2,
            NPEarningTrigger.DRAMATIC_TIMING: 1,
            NPEarningTrigger.RELATIONSHIP_DEVELOPMENT: 1
        }

        self.activity_costs = {
            NPActivity.RETCON_SCENE: 5,
            NPActivity.INTRODUCE_ELEMENT: 3,
            NPActivity.EMPOWER_CHARACTER: 4,
            NPActivity.NARRATIVE_ESCAPE: 6,
            NPActivity.DRAMATIC_REVEAL: 2,
            NPActivity.CHARACTER_RETCON: 8,
            NPActivity.ENVIRONMENT_MANIPULATION: 3,
            NPActivity.FORESHADOWING: 2
        }

    def earn_points(self, trigger: NPEarningTrigger, description: str,
                   character_id: Optional[str] = None, scene_context: Optional[Dict] = None) -> int:
        """Earn narrative points for player actions"""
        amount = self.earning_rates.get(trigger, 1)

        if character_id:
            old_balance = self.player_balances[character_id]
            self.player_balances[character_id] += amount

            transaction = NPTransaction(
                id=str(uuid.uuid4()),
                trigger=trigger,
                amount=amount,
                balance_after=self.player_balances[character_id],
                description=description,
                character_id=character_id,
                scene_context=scene_context
            )

            self.transaction_history[character_id].append(transaction)
            self.earnings_this_session[character_id] += amount

        return amount

    def spend_points(self, activity: NPActivity, description: str,
                    character_id: Optional[str] = None,
                    scene_context: Optional[Dict] = None) -> bool:
        """Spend narrative points on activities"""
        if not character_id:
            # Use generic account for session-wide points
            character_id = "session_general"

        cost = self.activity_costs.get(activity, 1)

        if self.player_balances[character_id] >= cost:
            old_balance = self.player_balances[character_id]
            self.player_balances[character_id] -= cost

            transaction = NPTransaction(
                id=str(uuid.uuid4()),
                activity=activity,
                amount=cost,
                balance_after=self.player_balances[character_id],
                description=description,
                character_id=character_id,
                scene_context=scene_context
            )

            self.transaction_history[character_id].append(transaction)
            self.spending_this_session[character_id] += cost

            return True
        else:
            return False

    def get_balance(self, character_id: str = "session_general") -> int:
        """Get current narrative points balance"""
        return self.player_balances.get(character_id, 0)

    def get_session_earnings(self, character_id: str = "session_general") -> int:
        """Get earnings this session"""
        return self.earnings_this_session.get(character_id, 0)

    def get_session_spending(self, character_id: str = "session_general") -> int:
        """Get spending this session"""
        return self.spending_this_session.get(character_id, 0)

    def get_transaction_history(self, character_id: str = "session_general", limit: int = None) -> List[NPTransaction]:
        """Get transaction history"""
        history = self.transaction_history.get(character_id, [])
        if limit:
            return history[-limit:]
        return history

    def get_active_opportunities(self) -> List[Dict]:
        """Get current opportunities for earning narrative points"""
        current_earnings = self.earnings_this_session

        opportunities = []

        # Standard opportunities available any time
        opportunities.append({
            "trigger": NPEarningTrigger.CHARACTER_GROWTH,
            "description": "Show character development or emotional depth",
            "potential_reward": self.earning_rates[NPEarningTrigger.CHARACTER_GROWTH],
            "difficulty": "medium",
            "rarity": "common"
        })

        opportunities.append({
            "trigger": NPEarningTrigger.CREATIVE_PROBLEM_SOLVING,
            "description": "Solve problems creatively using environmental elements",
            "potential_reward": self.earning_rates[NPEarningTrigger.CREATIVE_PROBLEM_SOLVING],
            "difficulty": "medium",
            "rarity": "common"
        })

        # Risk-based opportunities (higher reward)
        opportunities.append({
            "trigger": NPEarningTrigger.RISK_TAKING,
            "description": "Take meaningful risks for story advancement",
            "potential_reward": self.earning_rates[NPEarningTrigger.RISK_TAKING],
            "difficulty": "high",
            "rarity": "uncommon"
        })

        opportunities.append({
            "trigger": NPEarningTrigger.SACRIFICIAL_CHOICE,
            "description": "Make significant personal sacrifice for others or story",
            "potential_reward": self.earning_rates[NPEarningTrigger.SACRIFICIAL_CHOICE],
            "difficulty": "very_high",
            "rarity": "rare"
        })

        return opportunities

    def generate_narrative_suggestions(self, character_id: str = "session_general", context: Optional[Dict] = None) -> List[str]:
        """Generate narrative suggestions for earning points"""
        suggestions = []
        opportunities = self.get_active_opportunities()
        current_balance = self.get_balance(character_id)

        # Base suggestions
        if current_balance < 3:
            suggestions.append("Consider taking a risk or showing emotional investment")
            suggestions.append("Look for ways to advance the story meaningfully")

        suggestions.extend([
            "Develop character relationships or show personal growth",
            "Use creative problem-solving with environmental elements",
            "Time high-drama moments for maximum narrative impact"
        ])

        return suggestions[:5]  # Limit to top 5 suggestions

    def calculate_narrative_pressure(self, character_id: str = "session_general") -> float:
        """Calculate current narrative pressure/urgency"""
        current_balance = self.get_balance(character_id)
        session_earnings = self.get_session_earnings(character_id)

        # Base pressure calculation
        if current_balance < 2:
            return 0.7  # High pressure - encourage earning
        elif current_balance < 5:
            return 0.4  # Medium pressure
        elif current_balance < 10:
            return 0.2  # Low pressure
        else:
            return 0.0  # No pressure - encourage spending

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status for API reporting"""
        total_earned = sum(self.earnings_this_session.values())
        total_spent = sum(self.spending_this_session.values())

        return {
            "narrative_points_system": True,  # This system is active!
            "total_points_held": sum(self.player_balances.values()),
            "earnings_this_session": total_earned,
            "spending_this_session": total_spent,
            "average_earning_per_session": total_earned / max(1, len(self.earnings_this_session)),
            "active_opportunities": len(self.get_active_opportunities()),
            "pressure_level": self.calculate_narrative_pressure()
        }

    def apply_narrative_pressure_bonus(self, trigger: NPEarningTrigger, original_amount: int) -> int:
        """Apply pressure-based bonuses to earnings"""
        pressure = self.calculate_narrative_pressure()

        if pressure > 0.5:
            bonus = max(1, int(original_amount * 0.5))
            return original_amount + bonus
        elif pressure > 0.3:
            bonus = max(1, int(original_amount * 0.3))
            return original_amount + bonus
        else:
            return original_amount

    def reset_session_data(self):
        """Reset session-specific tracking"""
        self.earnings_this_session.clear()
        self.spending_this_session.clear()
        self.current_scene_points = 0