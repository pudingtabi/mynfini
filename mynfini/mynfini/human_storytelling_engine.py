"""
HUMAN STORYTELLING ENGINE FOR MYNFINI
Transform AI narration into addictive human-quality storytelling
Based on: Game of Thrones subversion, Japanese literature, bestselling book techniques
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class NarrativePriority(Enum):
    """Priority levels for narrative elements"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CLIMAX = 4


class EmotionalTone(Enum):
    """Available emotional tones for storytelling"""
    CONTEMPLATIVE = "contemplative"
    TENSE = "tense"
    HOPEFUL = "hopeful"
    DESPERATE = "desperate"
    MYSTERIOUS = "mysterious"
    TRIUMPHANT = "triumphant"
    TRAGIC = "tragic"
    HUMOROUS = "humorous"
    SUSPENSEFUL = "suspenseful"


@dataclass
class CuriosityGap:
    """Represents a seeded mystery for later revelation"""
    question: str
    seed_text: str
    importance_level: int  # 1-10
    revealed: bool = False
    revelation_pending: bool = False
    foreshadowing_count: int = 0


@dataclass
class EmotionalRollerCoaster:
    """Tracks emotional rhythm for engagement"""
    tension_level: float  # 0.0 - 10.0
    relief_level: float  # 0.0 - 10.0
    cliffhanger_potential: float  # 0.0 - 10.0
    last_emotional_peak: Optional[float] = None
    scene_count: int = 0


@dataclass
class HumanNarrative:
    """Enhanced narrative with human storytelling elements"""
    base_text: str
    enhanced_text: str
    curiosity_gaps: List[CuriosityGap]
    subverted_tropes: List[str]
    cliffhanger_ending: Optional[str] = None
    emotional_tone: Optional[EmotionalTone] = None
    stakes_escalation: float = 0.0
    reader_addiction_score: float = 0.0


class HumanStorytellingEngine:
    """Transforms AI outputs into addictive human-quality narratives"""

    def __init__(self):
        self.curiosity_archive: List[CuriosityGap] = []
        self.emotional_coaster = EmotionalRollerCoaster(0.0, 0.0, 0.0)
        self.subversion_library = self._build_subversion_library()
        # Removed undefined method reference

    def enhance_narrative(self, base_narrative: str, context: Dict[str, Any]) -> HumanNarrative:
        """Main method to transform AI narrative into human-quality story"""

        # 1. Seed curiosity gaps
        curiosity_gaps = self._seed_curiosity_gaps(base_narrative, context)

        # 2. Apply narrative subversion
        subverted_text, subverted_tropes = self._apply_narrative_subversion(base_narrative, context)

        # 3. Build emotional arc
        emotionally_enhanced = self._build_emotional_arc(subverted_text, context)

        # 4. Manage cliffhanger ending
        enhanced_text = self._manage_cliffhanger_ending(emotionally_enhanced, context)

        # 5. Escalate stakes strategically
        enhanced_text, stakes_level = self._escalate_stakes(enhanced_text, context)

        # 6. Calculate addiction score
        addiction_score = self._calculate_addiction_score(
            len(curiosity_gaps),
            len(subverted_tropes),
            stakes_level,
            enhanced_text
        )

        return HumanNarrative(
            base_text=base_narrative,
            enhanced_text=enhanced_text,
            curiosity_gaps=curiosity_gaps,
            subverted_tropes=subverted_tropes,
            emotional_tone=self._determine_emotional_tone(enhanced_text, context),
            stakes_escalation=stakes_level,
            reader_addiction_score=addiction_score
        )

    def _seed_curiosity_gaps(self, text: str, context: Dict[str, Any]) -> List[CuriosityGap]:
        """Seed mysteries that create curiosity gaps ("I need to know what this means!")"""
        curiosity_gaps = []

        # Strategic questions to seed
        mystery_templates = [
            {
                "question": "What is truly hidden there?",
                "importance": random.randint(4, 8),
                "trigger_phrases": ["strange marking", "unusual symbol", "cryptic note", "mysterious object"]
            },
            {
                "question": "What does this behavior really mean?",
                "importance": random.randint(5, 9),
                "trigger_phrases": ["unusual behavior", "unexpected reaction", "suspicious glance", "hesitant response"]
            },
            {
                "question": "What consequence will this have?",
                "importance": random.randint(3, 7),
                "trigger_phrases": ["seems insignificant", "appears harmless", "might matter later", "could change everything"]
            }
        ]

        # Scan for trigger phrases to seed mysteries
        trigger_found = False
        for mystery in mystery_templates:
            for trigger in mystery["trigger_phrases"]:
                if trigger in text.lower() and random.random() < 0.7:
                    # Add subversion to the seed text
                    seed_text = self._create_mystery_seed(trigger, mystery["question"])
                    curiosity_gaps.append(CuriosityGap(
                        question=mystery["question"],
                        seed_text=seed_text,
                        importance_level=mystery["importance"]
                    ))
                    trigger_found = True
                    break

        # If no triggers found, create general curiosity gaps based on context
        if not trigger_found or len(curiosity_gaps) == 0:
            general_curiosities = self._create_general_curiosity_gaps(context)
            curiosity_gaps.extend(general_curiosities)

        # Add archived mysteries that weren't revealed
        unresolved_mysteries = [gap for gap in self.curiosity_archive if not gap.revealed]
        if unresolved_mysteries and random.random() < 0.3:
            # Foreshadow existing mysteries
            selected_mystery = random.choice(unresolved_mysteries)
            selected_mystery.foreshadowing_count += 1
            context_mystery = CuriosityGap(
                question=selected_mystery.question,
                seed_text=self._create_forshadowing_seed(selected_mystery),
                importance_level=selected_mystery.importance_level,
                revelation_pending=True
            )
            curiosity_gaps.append(context_mystery)

        return curiosity_gaps

    def _create_mystery_seed(self, base_text: str, question: str) -> str:
        """Create compelling mystery seed text"""
        mystery_constructions = [
            f"{base_text}, though something about it seems... off.",
            f"{base_text}, but you can't shake the feeling it means something more.",
            f"{base_text}. A shiver runs down your spine as you realize this might matter more than expected.",
            f"{base_text}, though why would such a thing be here of all places?"
        ]
        return random.choice(mystery_constructions)

    def _create_forshadowing_seed(self, existing_mystery: CuriosityGap) -> str:
        """Create foreshadowing for existing mysteries"""
        foreshadow_templates = [
            f"The air feels heavy with unspoken meaning, as if echoing {existing_mystery.seed_text.lower()}",
            f"A memory of {existing_mystery.seed_text.lower()} flutters at the edge of your mind.",
            f"Everything seems connected to that moment when {existing_mystery.seed_text.lower()}",
        ]
        return random.choice(foreshadow_templates)

    def _create_general_curiosity_gaps(self, context: Dict[str, Any]) -> List[CuriosityGap]:
        """Create general curiosity gaps when no specific triggers are found"""
        curiosity_gaps = []

        # General curiosity templates based on context
        general_templates = [
            {
                "question": "What is the true nature of this place?",
                "seed_template": "There's something about this location that feels deeper than it appears.",
                "importance": random.randint(4, 7)
            },
            {
                "question": "What are the real motivations of those involved?",
                "seed_template": "You sense there's more to this situation than anyone is letting on.",
                "importance": random.randint(5, 8)
            },
            {
                "question": "What consequences might emerge from recent events?",
                "seed_template": "Actions have a way of rippling outward in unexpected ways.",
                "importance": random.randint(3, 6)
            },
            {
                "question": "What hidden connections bind these events together?",
                "seed_template": "Pieces of a larger puzzle seem to be emerging.",
                "importance": random.randint(6, 9)
            },
            {
                "question": "What will you discover about yourself through this journey?",
                "seed_template": "Every challenge reveals something new about who you are.",
                "importance": random.randint(4, 7)
            }
        ]

        # Create 1-2 general curiosity gaps
        num_gaps = random.randint(1, 2)
        selected_templates = random.sample(general_templates, min(num_gaps, len(general_templates)))

        for template in selected_templates:
            curiosity_gaps.append(CuriosityGap(
                question=template["question"],
                seed_text=template["seed_template"],
                importance_level=template["importance"]
            ))

        return curiosity_gaps

    def _apply_narrative_subversion(self, text: str, context: Dict[str, Any]) -> Tuple[str, List[str]]:
        """Apply Game of Thrones-style subversion to subvert expectations"""

        # Common fantasy tropes to subvert
        tropes_to_subvert = {
            "perfect heroes": {
                "triggers": ["perfect", "flawless", "infallible", "always knows"],
                "subversion": "though perhaps too perfect",
                "technique": "reveal hidden flaw"
            },
            "obvious villains": {
                "triggers": ["clearly evil", "obvious villain", "just a monster"],
                "subversion": "but there's more to their story",
                "technique": "show motivation"
            },
            "heroic victories": {
                "triggers": ["glorious victory", "triumphant heroes", "happy ending"],
                "subversion": "but victory comes at a cost",
                "technique": "add sacrifice/consequence"
            },
            "simple solutions": {
                "triggers": ["simple fix", "easy way", "clear solution"],
                "subversion": "if only it were that straightforward",
                "technique": "add complexity"
            }
        }

        subverted_text = text
        subverted_tropes = []

        for trope_name, trope_data in tropes_to_subvert.items():
            # Check if trope appears with 30% chance to trigger subversion
            if any(trigger in text.lower() for trigger in trope_data["triggers"]) and random.random() < 0.3:
                # Apply subversion
                subverted_text = self._insert_subversion(text, trope_data["subversion"])
                subverted_tropes.append(trope_name)
                break  # Don't over-subvert

        return subverted_text, subverted_tropes

    def _insert_subversion(self, text: str, subversion: str) -> str:
        """Insert subversion into appropriate text location"""
        # Find a period or comma to insert after
        sentences = text.split('. ')
        if len(sentences) > 1:
            # Insert after second sentence
            sentences[1] = f"{sentences[1]} {subversion}"
            return '. '.join(sentences)
        else:
            # Add to end if no good insertion point
            return f"{text} {subversion}"

    def _build_emotional_arc(self, text: str, context: Dict[str, Any]) -> str:
        """Build emotional rhythm that escalates engagement"""

        # Track current emotional state
        current_emotion = self.emotional_coaster.tension_level

        # Determine appropriate emotional enhancement
        if current_emotion < 4.0:
            # Build tension from contemplative
            enhancement = self._build_tensile_emotion(text)
        elif current_emotion < 7.0:
            # Escalate existing tension
            enhancement = self._escalate_emotion(text)
        else:
            # Provide emotional resolution/recovery
            enhancement = self._provide_emotion_resolution(text)

        # Update emotional roller coaster state
        self.emotional_coaster.scene_count += 1
        self.emotional_coaster.last_emotional_peak = current_emotion

        return enhancement

    def _build_tensile_emotion(self, text: str) -> str:
        """Build emotional tension from calm state"""
        tension_phrases = [
            "Though something feels... off.",
            "A tension you can't quite name fills the air.",
            "Everything seems normal, but your instincts scream danger.",
            "The silence feels too deep, too deliberate."
        ]

        self.emotional_coaster.tension_level += random.uniform(1.5, 3.0)
        return f"{text} {random.choice(tension_phrases)}"

    def _escalate_emotion(self, text: str) -> str:
        """Escalate existing emotional tension"""
        escalation_phrases = [
            "Your heart pounds faster as reality sets in.",
            "A cold certainty grips you—this is going exactly where you feared.",
            "Time seems to slow as you realize how badly this could go.",
            "Every cell in your body screams that something terrible is about to happen."
        ]

        self.emotional_coaster.tension_level += random.uniform(0.5, 1.5)
        return f"{text} {random.choice(escalation_phrases)}"

    def _provide_emotion_resolution(self, text: str) -> str:
        """Provide emotional resolution while setting up next tension"""
        resolution_phrases = [
            "You breathe for the first time in minutes—until you remember what comes next.",
            "The immediate danger passes, but the weight of what you've learned settles like stone.",
            "Relief floods through you, brief and beautiful, before cold reality returns.",
            "For one heartbeat, everything is okay—then memory of what's coming shatters the moment."
        ]

        self.emotional_coaster.tension_level = random.uniform(2.0, 4.0)
        return f"{text} {random.choice(resolution_phrases)}"

    def _manage_cliffhanger_ending(self, text: str, context: Dict[str, Any]) -> str:
        """Manage cliffhanger endings that demand continuation"""

        # Check if we should add cliffhanger (30% chance)
        if random.random() < 0.3:
            cliffhanger_templates = [
                "And then you see it—something that changes absolutely everything.",
                "The last thing you notice before everything goes dark is the truth.",
                "In the silence that follows, you finally understand what you've done.",
                "But nothing prepares you for what you discover next.",
                "As you turn to leave, the realization hits you like a physical blow."
            ]

            cliffhanger = random.choice(cliffhanger_templates)
            enhanced_text = f"{text}\n\n{cliffhanger}"
            self.emotional_coaster.cliffhanger_potential += random.uniform(6.0, 9.0)
            return enhanced_text

        return text

    def _escalate_stakes(self, text: str, context: Dict[str, Any]) -> Tuple[str, float]:
        """Strategically escalate stakes to maintain engagement"""
        # Get current stakes from context
        current_stakes = context.get("current_stakes", 3.0)

        # Escalate based on scene importance
        escalation_rate = random.uniform(0.3, 1.2)  # Moderate escalation
        new_stakes = min(current_stakes + escalation_rate, 10.0)  # Cap at max

        # Add stakes-aware language if significant escalation
        if new_stakes - current_stakes > 0.7:
            stakes_phrases = [
                "What's at stake is no longer just your life—it might be everything you've ever cared about.",
                "The consequences spread like ripples in water, touching more than you realized was possible.",
                "You understand, suddenly and completely, that this choice changes more than this moment.",
                "In the widening circle of consequence, you see how much this single action might cost."
            ]

            stakes_text = random.choice(stakes_phrases)
            enhanced_text = f"{text}\n\n{stakes_text}"
        else:
            enhanced_text = text

        return enhanced_text, new_stakes

    def _calculate_addiction_score(self, curiosity_count: int, subversion_count: int,
                                 stakes_level: float, text: str) -> float:
        """Calculate reader addiction likelihood (0.0 - 10.0)"""
        base_score = 3.0  # Base engagement

        # Curiosity gaps add significantly
        curiosity_bonus = curiosity_count * 1.5

        # Subversion adds engagement
        subversion_bonus = subversion_count * 2.0

        # Stakes matter
        stakes_bonus = stakes_level * 0.5

        # Emotional impact from roller coaster
        emotion_bonus = min(self.emotional_coaster.tension_level, 10.0) * 0.3

        # Cliffhanger impact
        cliffhanger_bonus = min(self.emotional_coaster.cliffhanger_potential, 10.0) * 0.4

        total_score = base_score + curiosity_bonus + subversion_bonus + stakes_bonus + emotion_bonus + cliffhanger_bonus
        return min(total_score, 10.0)  # Cap at maximum

    def _build_subversion_library(self) -> Dict[str, Dict[str, str]]:
        """Build library of trope subversions"""
        return {
            "heroic_savior": {
                "subversion": "but their salvation comes with a price they're not sure they can pay",
                "setup": "heroic intentions",
                "payoff": "moral complexity"
            },
            "evil_monster": {
                "subversion": "though understanding what created this horror humanizes the inhuman",
                "setup": "pure evil",
                "payoff": "empathy through understanding"
            },
            "perfect_plan": {
                "subversion": "if only complex situations had simple solutions",
                "setup": "clear solution presented",
                "payoff": "reality is messy"
            }
        }

    def _determine_emotional_tone(self, text: str, context: Dict[str, Any]) -> Optional[EmotionalTone]:
        """Determine emotional tone from content analysis"""
        if self.emotional_coaster.tension_level > 8.0:
            return EmotionalTone.DESPERATE
        elif self.emotional_coaster.tension_level > 6.0:
            return EmotionalTone.SUSPENSEFUL
        elif len([gap for gap in self.curiosity_archive if not gap.revealed]) > 3:
            return EmotionalTone.MYSTERIOUS
        elif "loss" in text.lower() or "failed" in text.lower():
            return EmotionalTone.TRAGIC
        elif "victory" in text.lower() or "succeeded" in text.lower():
            return EmotionalTone.TRIUMPHANT
        else:
            return EmotionalTone.CONTEMPLATIVE


class ProgressiveWorldRevelation:
    """Manages gradual world complexity unveiling like Japanese literature"""

    def __init__(self):
        self.world_layers = {
            "surface": 1.0,     # Basic geography and culture
            "deeper": 2.5,      # Hidden structures and meanings
            "hidden": 4.0,      # Supernatural elements
            "ultimate": 6.0     # Cosmic truths
        }
        self.current_layer = 1.0
        self.reveal_queue = []

    def get_appropriate_complexity(self, player_experience: float) -> float:
        """Determine how much world complexity to reveal based on player experience"""
        # Gradually increase complexity as players engage longer
        if player_experience < 3.0:  # New players
            return min(self.current_layer, self.world_layers["surface"])
        elif player_experience < 6.0:  # Growing players
            return min(self.current_layer, self.world_layers["deeper"])
        elif player_experience < 10.0:  # Experienced players
            return min(self.current_layer, self.world_layers["hidden"])
        else:
            return min(self.current_layer, self.world_layers["ultimate"])