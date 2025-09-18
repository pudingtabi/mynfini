"""
SESSION ZERO ENHANCED PROTOCOL FOR MYNFINI
Implements the complete 5-step Session Zero protocol with structured rules
Creates world foundation based on universal storytelling principles
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from expanded_world_system import ExpandedWorldSystem, SessionZeroProfile, BiomeType, WorldConsistency


class SessionZeroProtocol:
    """Implements the complete 5-step Session Zero world establishment protocol"""

    def __init__(self, world_system: ExpandedWorldSystem):
        self.world_system = world_system
        self.session_progress = 0
        self.establishment_data = {}
        self.discoveries = []

    def initiate_session_zero(self) -> Dict[str, Any]:
        """Execute the complete 5-step Session Zero establishment protocol"""

        print("=== SESSION ZERO: World Foundation Establishment ===")
        print("Building a world that lives, breathes, and evolves with your creativity...")
        print()

        # Step 1: Tone & Atmosphere Foundation
        step1_result = self._execute_step1_tone_atmosphere()
        if not step1_result["success"]:
            return step1_result
        self.establishment_data.update(step1_result)

        # Step 2: Player Archetype & Theme Recognition
        step2_result = self._execute_step2_archetype_themed()
        if not step2_result["success"]:
            return step2_result
        self.establishment_data.update(step2_result)

        # Step 3: Complexity & Depth Calibration
        step3_result = self._execute_step3_complexity_depth()
        if not step3_result["success"]:
            return step3_result
        self.establishment_data.update(step3_result)

        # Step 4: Magical & Historical Foundation
        step4_result = self._execute_step4_magical_historical()
        if not step4_result["success"]:
            return step4_result
        self.establishment_data.update(step4_result)

        # Step 5: World Unification Protocol
        step5_result = self._execute_step5_world_unification()
        if not step5_result["success"]:
            return step5_result
        self.establishment_data.update(step5_result)

        # Create comprehensive establishment record
        establishment_record = self._create_establishment_record([
            step1_result, step2_result, step3_result, step4_result, step5_result
        ])

        return {
            "success": True,
            "establishment_record": establishment_record,
            "discoveries": self.discoveries,
            "session_zero_profile": self._build_session_zero_profile(establishment_record),
            "world_greeting": self._generate_world_greeting(establishment_record)
        }

    def _execute_step1_tone_atmosphere(self) -> Dict[str, Any]:
        """Step 1: Establish the emotional and atmospheric foundation of the world"""
        print("STEP 1: World Tone & Atmosphere Selection")
        print("=" * 50)

        # Present tone options based on bestselling narrative theory
        tone_options = self._get_tone_options()

        print("Available World Tones:")
        for i, tone in enumerate(tone_options, 1):
            print(f"{i}. {tone['name']}: {tone['description']}")
            print(f"   Narrative Engine: {tone['narrative_engine']}")
            print()

        # For automation/demo, select randomly but can be replaced with player choice
        selected_tone = random.choice(tone_options)
        print(f"Selected World Tone: {selected_tone['name']}")

        # Determine consistency level based on tone
        consistency_level = random.choice(["natural", "influence", "supernatural"])
        print(f"World Consistency Level: {consistency_level}")

        # Log this discovery for future use
        self.discoveries.append({
            "type": "foundational",
            "step": 1,
            "tone": selected_tone['name'],
            "narrative_engine": selected_tone['narrative_engine'],
            "consistency": consistency_level
        })

        return {
            "success": True,
            "tone": selected_tone['name'],
            "narrative_engine": selected_tone['narrative_engine'],
            "consistency_level": consistency_level,
            "guiding_principle": selected_tone['guiding_principle']
        }

    def _execute_step2_archetype_themed(self) -> Dict[str, Any]:
        """Step 2: Recognize player archetypes and establish world themes based on them"""
        print("\nSTEP 2: Player Archetype & Theme Recognition")
        print("=" * 50)

        # Analyze player approach patterns from previous interactions
        archetype_scores = self._analyze_player_archetype_patterns()

        # Present archetype findings
        print("Identified Player Archetypes (based on previous creativity):")
        for archetype, score in archetype_scores.items():
            print(f"• {archetype.title()}: {score:.1f}/10 ({self._get_archetype_description(archetype)})")

        # Establish themes based on primary archetypes
        primary_archetypes = [a for a, s in archetype_scores.items() if s >= 7.0]
        if len(primary_archetypes) < 2:
            primary_archetypes = list(archetype_scores.keys())[:3]  # Top 3 if few high scores

        established_themes = self._establish_themes_from_archetypes(primary_archetypes)

        print(f"\nWorld Themes Established:")
        for theme in established_themes:
            print(f"• {theme}")

        # Suggest archetype-specific progression paths
        progression_paths = self._suggest_progression_paths(primary_archetypes)

        established_themes = self._establish_themes_from_archetypes(primary_archetypes)
        progression_paths = self._suggest_progression_paths(primary_archetypes)

        return {
            "success": True,
            "player_archetypes": archetype_scores,
            "primary_archetypes": primary_archetypes,
            "established_themes": established_themes,
            "progression_paths": progression_paths
        }

    def _execute_step3_complexity_depth(self) -> Dict[str, Any]:
        """Step 3: Calibrate world complexity based on player preferences"""
        print("\nSTEP 3: Complexity & Depth Calibration")
        print("=" * 50)

        # Complexity sliders based on narrative psychology
        complexity_preferences = self._present_complexity_sliders()

        # For demo, randomly calibrate (in real implementation, these would have defaults)
        calibrated_complexities = {
            "mystery_preference": random.randint(4, 8),
            "social_complexity": random.randint(3, 9),
            "cultural_uniqueness": random.randint(5, 10),
            "magical_rarity": random.randint(2, 7),
            "historical_depth": random.randint(4, 9),
            "revelation_timing": random.choice(["immediate", "gradual", "delayed", "episodic"])
        }

        print("Complexity Calibration Complete:")
        print(f"• Mystery Preference: {calibrated_complexities['mystery_preference']}/10")
        print(f"• Social Complexity: {calibrated_complexities['social_complexity']}/10")
        print(f"• Cultural Uniqueness: {calibrated_complexities['cultural_uniqueness']}/10")
        print(f"• Magical Rarity: {calibrated_complexities['magical_rarity']}/10")
        print(f"• Historical Depth: {calibrated_complexities['historical_depth']}/10")

        return {
            "success": True,
            "calibrated_complexities": calibrated_complexities
        }

    def _execute_step4_magical_historical(self) -> Dict[str, Any]:
        """Step 4: Establish magical systems and historical foundation based on complexity preferences"""
        print("\nSTEP 4: Magical & Historical Foundation")
        print("=" * 50)

        # Generate foundational world elements
        calibrated_complexities = self.establishment_data.get("calibrated_complexities", {})
        magical_rarity = calibrated_complexities.get("magical_rarity", 4)
        historical_depth = calibrated_complexities.get("historical_depth", 6)

        # Establish world constants
        world_constants = self._establish_world_constants(magical_rarity, historical_depth)

        # Create historical timeline
        historical_timeline = self._generate_historical_timeline(historical_depth)

        # Define cultural archetypes
        cultural_archetypes = self._define_cultural_archetypes()

        print("World Foundation Established:")
        print("• Magic System: Defined")
        print("• Historical Timeline: Created")
        print("• Cultural Archetypes: Identified")
        print("• World Constants: Locked")

        return {
            "success": True,
            "world_constants": world_constants,
            "historical_timeline": historical_timeline,
            "cultural_archetypes": cultural_archetypes
        }

    def _execute_step5_world_unification(self) -> Dict[str, Any]:
        """Step 5: Unify all elements into coherent world and generate first story"""
        print("\nSTEP 5: World Unification Protocol")
        print("=" * 50)

        # Combine all previous steps into unified world profile
        session_profile = SessionZeroProfile(
            tone=self.establishment_data["tone"],
            consistency_level=WorldConsistency(self.establishment_data["consistency_level"]),
            mystery_preference=self.establishment_data["calibrated_complexities"]["mystery_preference"],
            social_complexity=self.establishment_data["calibrated_complexities"]["social_complexity"],
            cultural_uniqueness=self.establishment_data["calibrated_complexities"]["cultural_uniqueness"],
            magical_rarity=self.establishment_data["calibrated_complexities"]["magical_rarity"],
            historical_depth=self.establishment_data["calibrated_complexities"]["historical_depth"],
            player_archetypes=list(self.establishment_data["player_archetypes"].keys()),
            established_themes=self.establishment_data["established_themes"]
        )

        # Apply to world system
        success = self.world_system.apply_session_zero_establishment(session_profile.asdict())

        if success:
            # Generate first mystery/challenge based on established parameters
            first_mystery = self._generate_first_discovery(session_profile)
            self.discoveries.append(first_mystery)

            # Create world greeting that introduces the player to their world
            world_greeting = self._generate_world_greeting()

            print("World Unification Complete!")
            print("Your world now lives and will evolve based on your creativity.")

            return {
                "success": True,
                "session_zero_profile": session_profile,
                "first_mystery": first_mystery,
                "world_greeting": world_greeting
            }
        else:
            return {
                "success": False,
                "error": "Failed to unify world establishment"
            }

    # Helper methods would continue here...

    def _get_tone_options(self) -> List[Dict[str, str]]:
        """Get narrative tone options based on bestselling book research"""
        return [
            {
                "name": "Tragic Optimism",
                "description": "Hope exists alongside inevitable darkness",
                "narrative_engine": "Epic scale with intimate character moments",
                "guiding_principle": "Even in despair, light finds a way"
            },
            {
                "name": "Noble Tragedy",
                "description": "Heroism emerges through sacrifice and loss",
                "narrative_engine": "Character deaths that mean something",
                "guiding_principle": "The noble path is never easy"
            },
            {
                "name": "Mysterious Wonder",
                "description": "World reveals itself gradually through discovery",
                "narrative_engine": "Progressive revelation with cultural depth",
                "guiding_principle": "Every mystery solved reveals another"
            },
            {
                "name": "Moral Complexity",
                "description": "No good or evil - only choices and consequences",
                "narrative_engine": "Gray morality with real stakes",
                "guiding_principle": "Everyone has reasons for what they do"
            }
        ]

    def _analyze_player_archetype_patterns(self) -> Dict[str, float]:
        """Analyze how players approach situations to determine their archetype"""
        # In real implementation, this would analyze historical player behavior
        # For demo, return random patterns
        return {
            "explorer": random.uniform(5.0, 10.0),
            "problem_solver": random.uniform(4.0, 9.0),
            "leader": random.uniform(3.0, 8.0),
            "protector": random.uniform(2.0, 9.0),
            "innovator": random.uniform(4.0, 10.0)
        }

    def _get_archetype_description(self, archetype: str) -> str:
        descriptions = {
            "explorer": "Driven by curiosity and discovery",
            "problem_solver": "Enjoys puzzles and logical challenges",
            "leader": "Naturally takes charge in social situations",
            "protector": "Concerned for others' wellbeing",
            "innovator": "Creates unique solutions through creativity"
        }
        return descriptions.get(archetype, "Unknown archetype")

    def _establish_themes_from_archetypes(self, archetypes: List[str]) -> List[str]:
        """Establish world themes based on player archetypes using bestselling narrative theory"""
        theme_mapping = {
            "explorer": [
                "discovery through creativity",
                "hidden knowledge waiting to be found",
                "mysteries that reveal deeper truths"
            ],
            "problem_solver": [
                "logic puzzles with emotional stakes",
                "riddles that unlock world secrets",
                "challenges that test both mind and heart"
            ],
            "leader": [
                "group dynamics and social influence",
                "moral choices that affect communities",
                "power struggles with personal costs"
            ],
            "protector": [
                "sacrifice for the greater good",
                "defending the innocent from hidden threats",
                "personal loss for collective gain"
            ],
            "innovator": [
                "creative solutions to impossible problems",
                "reimagining the world through fresh eyes",
                "breaking traditions to forge new paths"
            ]
        }

        themes = []
        for archetype in archetypes:
            if archetype in theme_mapping:
                themes.extend(theme_mapping[archetype])

        # Remove duplicates while preserving order
        unique_themes = []
        for theme in themes:
            if theme not in unique_themes:
                unique_themes.append(theme)

        # Return top 5 themes to avoid overwhelming complexity
        return unique_themes[:5]

    def _suggest_progression_paths(self, archetypes: List[str]) -> List[str]:
        """Suggest character progression paths based on player archetypes"""
        progression_mapping = {
            "explorer": [
                "Cartographer - mapping unknown territories reveals world secrets",
                "Lore Seeker - collecting fragments unlocks ancient mysteries",
                "Boundary Walker - crossing thresholds grants new perspectives"
            ],
            "problem_solver": [
                "Logic Master - solving puzzles enhances mental capabilities",
                "Pattern Reader - recognizing connections reveals hidden truths",
                "Riddle Keeper - understanding metaphors unlocks deeper meaning"
            ],
            "leader": [
                "Influence Weaver - building relationships creates political power",
                "Community Builder - nurturing others strengthens collective bonds",
                "Moral Compass - making hard choices earns respect and followers"
            ],
            "protector": [
                "Shield Bearer - defending others builds resilience and strength",
                "Guardian Path - protecting what matters reveals true character",
                "Sacrificial Hero - giving up personal goals for others' wellbeing"
            ],
            "innovator": [
                "Creative Genius - breaking rules leads to revolutionary solutions",
                "Visionary Path - seeing possibilities others miss",
                "Paradigm Shifter - challenging norms transforms the world"
            ]
        }

        paths = []
        for archetype in archetypes:
            if archetype in progression_mapping:
                paths.extend(progression_mapping[archetype])

        # Remove duplicates while preserving order
        unique_paths = []
        for path in paths:
            if path not in unique_paths:
                unique_paths.append(path)

        # Return top 5 progression paths
        return unique_paths[:5]

    def _present_complexity_sliders(self) -> List[Dict[str, Any]]:
        return [
            {"name": "Mystery Preference", "description": "How deep should the mysteries go?", "range": [1, 10]},
            {"name": "Social Complexity", "description": "How intricate are social structures and politics?", "range": [1, 10]},
            {"name": "Cultural Uniqueness", "description": "How original and unusual are cultural elements?", "range": [1, 10]},
            {"name": "Magical Rarity", "description": "How common is magic in this world?", "range": [1, 10]},
            {"name": "Historical Depth", "description": "How deep does history go?", "range": [1, 10]},
            {"name": "Revelation Timing", "description": "How quickly should mysteries be revealed?", "choices": ["immediate", "gradual", "delayed", "episodic"]}
        ]

    def _create_establishment_record(self, step_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a comprehensive establishment record from all step results"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "steps": {}
        }

        for i, result in enumerate(step_results, 1):
            record["steps"][f"step_{i}"] = result

        return record

    def _establish_world_constants(self, magical_rarity: int, historical_depth: int) -> Dict[str, Any]:
        """Establish fundamental world constants based on complexity preferences"""
        return {
            "magic_observable": magical_rarity > 5,  # Magic is obvious if rarity is high
            "history_layered": historical_depth > 6,  # Deep history has layers
            "cultural_stability": max(1, 10 - magical_rarity),  # More magic = less stability
            "mystery_density": min(10, historical_depth + magical_rarity),  # More complexity = more mysteries
            "revelation_speed": "gradual" if historical_depth > 7 else "moderate"
        }

    def _generate_historical_timeline(self, historical_depth: int) -> List[Dict[str, Any]]:
        """Generate a historical timeline based on depth preference"""
        timeline = []
        base_years = [-1000, -500, -200, -50, 0, 50, 200, 500, 1000]  # Relative years

        for i, year in enumerate(base_years[:historical_depth]):
            timeline.append({
                "year": year,
                "event": f"Significant Event {i+1}",
                "impact": f"Shaped the world in important ways",
                "mystery": f"Hidden truth about this event waits to be discovered"
            })

        return timeline

    def _define_cultural_archetypes(self) -> List[Dict[str, Any]]:
        """Define cultural archetypes for the world"""
        return [
            {
                "name": "Traditionalist",
                "values": ["preservation", "ancestry", "ritual"],
                "conflicts": ["change", "foreign influence"],
                "mysteries": ["ancient secrets", "forbidden knowledge"]
            },
            {
                "name": "Innovator",
                "values": ["progress", "creativity", "adaptation"],
                "conflicts": ["tradition", "stability"],
                "mysteries": ["experimental discoveries", "new possibilities"]
            },
            {
                "name": "Guardian",
                "values": ["protection", "community", "sacrifice"],
                "conflicts": ["self-interest", "external threats"],
                "mysteries": ["hidden dangers", "secret guardians"]
            }
        ]

    def _generate_first_discovery(self, session_profile: SessionZeroProfile) -> Dict[str, Any]:
        """Generate the first mystery/challenge based on established parameters"""
        return {
            "type": "initial_mystery",
            "description": "A subtle anomaly in the world catches your attention",
            "clues": [
                "Something feels slightly off about this place",
                "There's an unusual pattern in the environment",
                "A local mentions something they've noticed"
            ],
            "revelation_path": "gradual",
            "stakes": session_profile.mystery_preference / 2.0
        }

    def _generate_world_greeting(self, establishment_record: Optional[Dict[str, Any]] = None) -> str:
        """Generate a world greeting that introduces the player to their world"""
        if establishment_record:
            # Use the establishment record to create a personalized greeting
            tone = establishment_record.get("steps", {}).get("step_1", {}).get("tone", "mysterious")
            return f"Welcome to a world of {tone.lower()} where your creativity shapes reality itself."
        else:
            # Default greeting
            return "Welcome to your world, where every choice you make matters and stories unfold uniquely for you."

    def _extract_emotional_indicators(self, discovery_text: str) -> Dict[str, Any]:
        """Extract emotional tone indicators from player description"""
        text_lower = discovery_text.lower()

        indicators = {
            "dark": text_lower.count("dark") + text_lower.count("gloom") + text_lower.count("shadow"),
            "bright": text_lower.count("bright") + text_lower.count("light") + text_lower.count("hope"),
            "mysterious": text_lower.count("mystery") + text_lower.count("unknown") + text_lower.count("secret"),
            "adventurous": text_lower.count("adventure") + text_lower.count("explore") + text_lower.count("journey")
        }

        # Determine primary tone
        primary_tone = max(indicators, key=indicators.get) if any(indicators.values()) else "neutral"

        return {
            "indicators": indicators,
            "primary_tone": primary_tone,
            "intensity": sum(indicators.values())
        }

    def _identify_cultural_elements(self, discovery_text: str) -> List[str]:
        """Identify cultural elements mentioned in player description"""
        text_lower = discovery_text.lower()
        cultural_elements = []

        if any(word in text_lower for word in ["tradition", "custom", "ritual"]):
            cultural_elements.append("traditional")
        if any(word in text_lower for word in ["innovation", "new", "modern"]):
            cultural_elements.append("innovative")
        if any(word in text_lower for word in ["community", "people", "group"]):
            cultural_elements.append("communal")
        if any(word in text_lower for word in ["magic", "spell", "enchant"]):
            cultural_elements.append("magical")
        if any(word in text_lower for word in ["history", "ancient", "old"]):
            cultural_elements.append("historical")

        return cultural_elements if cultural_elements else ["diverse"]

    def _detect_magical_references(self, discovery_text: str) -> List[str]:
        """Detect magical/supernatural references in player description"""
        text_lower = discovery_text.lower()
        magical_refs = []

        if "magic" in text_lower:
            magical_refs.append("magic")
        if any(word in text_lower for word in ["spell", "wizard", "sorcerer"]):
            magical_refs.append("spellcasting")
        if any(word in text_lower for word in ["enchant", "charm", "bless"]):
            magical_refs.append("enchantment")
        if any(word in text_lower for word in ["dragon", "beast", "monster"]):
            magical_refs.append("magical_creatures")
        if any(word in text_lower for word in ["artifact", "relic", "ancient"]):
            magical_refs.append("magical_artifacts")

        return magical_refs

    def _analyze_social_complexity_preferences(self, discovery_text: str) -> Dict[str, Any]:
        """Analyze social complexity preferences from player description"""
        text_lower = discovery_text.lower()

        return {
            "political_intrigue": text_lower.count("politics") + text_lower.count("power") + text_lower.count("rule"),
            "social_dynamics": text_lower.count("social") + text_lower.count("relationship") + text_lower.count("interact"),
            "group_conflict": text_lower.count("conflict") + text_lower.count("war") + text_lower.count("battle"),
            "cultural_diversity": text_lower.count("culture") + text_lower.count("tradition") + text_lower.count("custom")
        }

    def _determine_consistency_from_references(self, magical_references: List[str]) -> str:
        """Determine world consistency level from magical references"""
        if len(magical_references) > 3:
            return "supernatural"
        elif len(magical_references) > 0:
            return "influence"
        else:
            return "natural"

    def _assess_historical_interest(self, discovery_text: str) -> int:
        """Assess player's interest in historical depth"""
        text_lower = discovery_text.lower()
        historical_words = ["history", "ancient", "old", "past", "ancestral", "traditional", "legacy"]

        count = sum(text_lower.count(word) for word in historical_words)
        # Scale to 1-10 range
        return min(10, max(1, count * 2))

    def _build_session_zero_profile(self, establishment_record: List[Dict[str, Any]]) -> SessionZeroProfile:
        """Combine all establishment data into comprehensive world profile"""
        return SessionZeroProfile(
            tone=self.establishment_data["tone"],
            consistency_level=WorldConsistency(self.establishment_data["consistency_level"]),
            mystery_preference=self.establishment_data["calibrated_complexities"]["mystery_preference"],
            social_complexity=self.establishment_data["calibrated_complexities"]["social_complexity"],
            cultural_uniqueness=self.establishment_data["calibrated_complexities"]["cultural_uniqueness"],
            magical_rarity=self.establishment_data["calibrated_complexities"]["magical_rarity"],
            historical_depth=self.establishment_data["calibrated_complexities"]["historical_depth"],
            player_archetypes=list(self.establishment_data["player_archetypes"].keys()),
            established_themes=self.establishment_data["established_themes"]
        )


def create_session_zero_from_discovery(player_discovery: str, world_system: ExpandedWorldSystem) -> Dict[str, Any]:
    """Create Session Zero establishment when player first describes their world vision"""

    extractor = PlayerVisionExtractor()
    vision_data = extractor.extract_world_vision_from_discovery(player_discovery)

    protocol = SessionZeroProtocol(world_system)
    return protocol.initiate_session_zero()


class PlayerVisionExtractor:
    """Extracts world vision parameters from player's initial descriptions"""

    def extract_world_vision_from_discovery(self, discovery_text: str) -> Dict[str, Any]:
        """Analyze player description to determine Session Zero parameters"""

        # Parse emotional tone indicators
        emotion_indicators = self._extract_emotional_indicators(discovery_text)

        # Identify cultural elements mentioned
        cultural_elements = self._identify_cultural_elements(discovery_text)

        # Detect magical/supernatural references
        magical_references = self._detect_magical_references(discovery_text)

        # Determine social complexity preferred
        social_indicators = self._analyze_social_complexity_preferences(discovery_text)

        return {
            "tone_preference": emotion_indicators["primary_tone"],
            "consistency_level": self._determine_consistency_from_references(magical_references),
            "mystery_indicators": len(discovery_text.split("?")) + discovery_text.lower().count("what"),
            "cultural_elements": cultural_elements,
            "historical_depth": self._assess_historical_interest(discovery_text),
            "social_preferences": social_indicators
        }