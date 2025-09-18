"""
EXPANDED WORLD SYSTEM FOR MYNFINI
AI-driven world generation that expands as players explore
Implements Session Zero protocol with structured rules
Creates towns, biomes, architecture, items, culture dynamically
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum


class BiomeType(Enum):
    FOREST = "forest"
    DESERT = "desert"
    MOUNTAIN = "mountain"
    FLOODED = "flooded"
    METROPOLIS = "metropolis"
    FRONTIER = "frontier"
    MAGICAL = "magical"


class WorldConsistency(Enum):
    NATURAL = "natural"
    SUPERNATURAL = "supernatural"
    INFLUENCE = "influence"


@dataclass
class SessionZeroProfile:
    """Captures the world vision established in Session Zero"""
    tone: str
    consistency_level: WorldConsistency
    mystery_preference: int  # 1-10
    social_complexity: int  # 1-10
    cultural_uniqueness: int  # 1-10
    magical_rarity: int  # 1-10
    historical_depth: int  # 1-10
    player_archetypes: List[str]
    established_themes: List[str]

    def asdict(self):
        """Convert to dictionary representation"""
        consistency_value = self.consistency_level.value if hasattr(self.consistency_level, 'value') else self.consistency_level
        return {
            "tone": self.tone,
            "consistency_level": consistency_value,
            "mystery_preference": self.mystery_preference,
            "social_complexity": self.social_complexity,
            "cultural_uniqueness": self.cultural_uniqueness,
            "magical_rarity": self.magical_rarity,
            "historical_depth": self.historical_depth,
            "player_archetypes": self.player_archetypes,
            "established_themes": self.established_themes
        }


@dataclass
class GeneratedTown:
    name: str
    region: str
    biome_type: BiomeType
    population: Optional[int]
    primary_industry: str
    power_structure: Dict[str, Any]
    cultural_quirks: List[str]
    notable_sites: List[str]
    hidden_truths: List[str]  # Curiosity gaps
    npcs: List[Dict[str, Any]]
    architecture_style: str
    established_date: str


@dataclass
class GeneratedBiome:
    region_name: str
    biome_type: BiomeType
    environmental_features: List[str]
    inhabitants: List[str]
    resources: List[Dict[str, Any]]
    unique_properties: List[str]
    hidden_locations: List[Dict[str, Any]]  # Progressive discovery
    climate: Dict[str, str]
    seasonal_variations: List[str]


@dataclass
class CulturalElement:
    aspect: str  # "greeting", "custom", "belief", "taboo"
    practice: str
    hidden_meaning: Optional[str] = None
    player_discovered: bool = False


class ExpandedWorldSystem:
    """AI-driven world that expands consistently as players explore"""

    def __init__(self, session_zero_data: Optional[SessionZeroProfile] = None):
        self.session_zero = session_zero_data
        self.explored_regions: Dict[str, Any] = {}
        self.towns: Dict[str, GeneratedTown] = {}
        self.biomes: Dict[str, GeneratedBiome] = {}

        # Tracks player discoveries for consistency
        self.player_knowledge: Dict[str, Dict[str, Any]] = {
            "locations": {},
            "npcs": {},
            "secrets": {},
            "relationships": {},
            "discoveries": []
        }

        self.world_log = []  # Accumulative world changes
        self.next_entity_id = 0

    def apply_session_zero_establishment(self, establishment_data: Dict[str, Any]) -> bool:
        """Apply the exact Session Zero protocol to establish world foundation"""
        try:
            # Parse the 5-step Session Zero establishment

            # Step 1: Tone & Atmosphere Selection
            tone = establishment_data.get("tone", "neutral and imaginative")
            consistency_level = WorldConsistency(establishment_data.get("consistency", "natural"))

            # Step 2: Player Archetype & Theme Recognition
            player_archetypes = establishment_data.get("player_archetypes", ["explorer", "puzzle-solver"])
            established_themes = establishment_data.get("themes", ["discovery through creativity"])

            # Step 3: Complexity Preferences
            mystery_preference = establishment_data.get("mystery_level", 6)
            social_complexity = establishment_data.get("social_depth", 5)
            cultural_uniqueness = establishment_data.get("cultural_originality", 7)

            # Step 4: Magical & Historical Foundation
            magical_rarity = establishment_data.get("magic_rarity", 4)
            historical_depth = establishment_data.get("historical_complexity", 6)

            self.session_zero = SessionZeroProfile(
                tone=tone,
                consistency_level=consistency_level,
                mystery_preference=mystery_preference,
                social_complexity=social_complexity,
                cultural_uniqueness=cultural_uniqueness,
                magical_rarity=magical_rarity,
                historical_depth=historical_depth,
                player_archetypes=player_archetypes,
                established_themes=established_themes
            )

            # Step 5: World Unification Protocol
            self._implement_world_unification_protocol()

            self._log_world_event("Session Zero world establishment completed", type="establishment")
            return True

        except Exception as e:
            self._log_world_event(f"Session Zero establishment failed: {e}", type="error")
            return False

    def generate_town_for_region(self, region_coords: str, player_description: str) -> GeneratedTown:
        """Generate a town when player explores, based on Session Zero rules"""

        # Check what player knows vs needs discovering
        if region_coords in self.explored_regions:
            return self._enhance_previously_generated_town(region_coords, player_description)

        # Generate new town following Session Zero rules
        town = self._create_town_from_session_zero(region_coords, player_description)

        # Ensure consistency with established world
        self._ensure_world_consistency(town, region_coords)

        self.towns[region_coords] = town
        self.explored_regions[region_coords] = {
            "type": "town",
            "generated_at": datetime.now().isoformat(),
            "player_knowledge_level": 0.1  # 0=unknown, 1=fully understood
        }

        self._log_world_event(f"Generated town '{town.name}' in region {region_coords}", type="generation")

        return town

    def generate_biome_for_region(self, region_coords: str, player_description: str) -> GeneratedBiome:
        """Generate a biome when player explores, with progressive revelation"""

        if region_coords in self.biomes:
            return self._reveal_biome_progressively(region_coords)

        # Create biome based on Session Zero establishment
        biome = self._create_biome_from_session_zero(region_coords, player_description)

        # Add hidden locations for progressive discovery (like Japanese literature)
        biome = self._add_progressive_discovery_locations(biome)

        self.biomes[region_coords] = biome

        # Use progressive revelation - don't reveal everything at once
        revealed_biome = self._create_progressive_biome_reveal(biome)

        self._log_world_event(f"Generated biome '{region_coords}' with {len(biome.hidden_locations)} hidden locations", type="generation")

        return revealed_biome

    def create_cultural_element(self, context: Dict[str, Any]) -> CulturalElement:
        """Generate cultural elements that fit Session Zero world"""

        # Determine aspect based on context
        aspect = random.choice(["greeting", "custom", "belief", "taboo", "tradition"])

        # Generate practice that matches world tone and consistency
        if aspect == "greeting":
            practice = self._generate_cultural_greeting()
        elif aspect == "custom":
            practice = self._generate_cultural_custom()
        elif aspect == "belief":
            practice = self._generate_cultural_belief()
        elif aspect == "taboo":
            practice = self._generate_cultural_taboo()
        else:  # tradition
            practice = self._generate_cultural_tradition()

        # Add hidden meaning for progression
        hidden_meaning = self._generate_hidden_meaning(aspect, practice)

        return CulturalElement(
            aspect=aspect,
            practice=practice,
            hidden_meaning=hidden_meaning,
            player_discovered=False
        )

    def update_player_knowledge(self, player_id: str, discovery_type: str, discovery_data: Dict[str, Any]) -> None:
        """Track what each player knows to maintain personalized stories"""

        if player_id not in self.player_knowledge:
            self.player_knowledge[player_id] = {
                "locations": {},
                "npcs": {},
                "secrets": {},
                "relationships": {},
                "discoveries": []
            }

        # Record discovery for consistency and progression
        discovery_entry = {
            "type": discovery_type,
            "data": discovery_data,
            "timestamp": datetime.now().isoformat(),
            "level": self._calculate_discovery_level(discovery_data)
        }

        self.player_knowledge[player_id]["discoveries"].append(discovery_entry)

        # Update specific knowledge areas
        if discovery_type == "location":
            location_key = discovery_data["coords"]
            self.player_knowledge[player_id]["locations"][location_key] = discovery_data

            # Update location knowledge level in world
            if location_key in self.explored_regions:
                self.explored_regions[location_key]["player_knowledge_level"] = min(
                    1.0, self.explored_regions[location_key]["player_knowledge_level"] + 0.15
                )

        elif discovery_type == "secret":
            secret_key = discovery_data["key"]
            self.player_knowledge[player_id]["secrets"][secret_key] = discovery_data

        self._log_world_event(f"Player {player_id} discovered: {discovery_type}", type="discovery")

    def get_player_specific_world(self, player_id: str) -> Dict[str, Any]:
        """Return world tailored to what this player knows and should discover next"""

        if player_id not in self.player_knowledge:
            return self._get_new_player_world()

        player_data = self.player_knowledge[player_id]

        # Determine next mysteries to present based on progression
        pending_mysteries = self._identify_pending_mysteries(player_id)

        # Find locations to introduce next based on archetype and themes
        next_locations = self._calculate_next_discovery_areas(player_id)

        return {
            "known_world": player_data,
            "pending_mysteries": pending_mysteries,
            "suggested_discoveries": next_locations,
            "consistency_rules": self._get_player_consistency_rules(player_id)
        }

    # Private implementation methods

    def _create_town_from_session_zero(self, region_coords: str, player_description: str) -> GeneratedTown:
        """Generate town based on Session Zero establishment"""

        # Generate name based on biome type from player description
        biome_type = self._infer_biome_from_description(player_description)

        name = self._generate_town_name(biome_type, region_coords)

        # Generate power structure based on social complexity preference
        power_structure = self._generate_power_structure(self.session_zero.social_complexity)

        # Create quirks based on cultural uniqueness
        cultural_quirks = self._generate_cultural_quirks(self.session_zero.cultural_uniqueness)

        # Add hidden truths based on mystery preference
        hidden_truths = self._generate_hidden_truths(self.session_zero.mystery_preference)

        # Generate NPCs based on player archetypes
        npcs = self._generate_appropriate_npcs(player_description)

        population = self._calculate_town_population(biome_type)

        return GeneratedTown(
            name=name,
            region=region_coords,
            biome_type=biome_type,
            population=population,
            primary_industry=self._determine_primary_industry(biome_type),
            power_structure=power_structure,
            cultural_quirks=cultural_quirks,
            notable_sites=self._generate_notable_sites(biome_type),
            hidden_truths=hidden_truths,
            npcs=npcs,
            architecture_style=self._generate_architecture_style(biome_type, self.session_zero),
            established_date=self._generate_town_established_date(region_coords)
        )

    def _create_biome_from_session_zero(self, region_coords: str, player_description: str) -> GeneratedBiome:
        """Generate biome based on Session Zero world vision"""

        # Inferred from player description
        biome_type = self._infer_biome_from_description(player_description)

        # Generate consistent with world tone
        environmental_features = self._generate_environmental_features(biome_type, self.session_zero)

        # Inhabitants match established themes
        inhabitants = self._generate_inhabitants(biome_type, self.session_zero)

        # Resources based on historical depth preference
        resources = self._generate_resources(biome_type, self.session_zero.historical_depth)

        # Magical properties based on magical rarity
        unique_properties = self._generate_unique_properties(biome_type, self.session_zero.magical_rarity)

        return GeneratedBiome(
            region_name=region_coords,
            biome_type=biome_type,
            environmental_features=environmental_features,
            inhabitants=inhabitants,
            resources=resources,
            unique_properties=unique_properties,
            hidden_locations=self._generate_hidden_locations(),
            climate=self._generate_climate(biome_type),
            seasonal_variations=self._generate_seasonal_variations(biome_type)
        )

    def _add_progressive_discovery_locations(self, biome: GeneratedBiome) -> GeneratedBiome:
        """Add locations that reveal progressively (Japanese literature style)"""

        hidden_locations = []
        num_hidden = random.randint(3, 8)  # Multiple layers of discovery

        for i in range(num_hidden):
            location = {
                "name": self._generate_mysterious_location_name(biome, i),
                "description_seeds": self._create_location_discovery_seeds(i),
                "reveal_condition": self._determine_reveal_condition(i),
                "complexity_level": i + 1,  # Escalating complexity
                "discovery_state": "hidden"
            }
            hidden_locations.append(location)

        biome.hidden_locations = hidden_locations
        return biome

    def _create_location_discovery_seeds(self, level: int) -> List[str]:
        """Create discovery clues that escalate over time"""
        seed_templates = [
            ["slight irregularity", "unusual detail", "curious presence"],
            ["partial pattern", "inconsistent behavior", "suspicious evidence"],
            ["growing strangeness", "accumulating clues", "pressing questions"],
            ["undeniable truth", "inescapable reality", "transformative revelation"]
        ]

        if level < len(seed_templates):
            return seed_templates[level]
        else:
            return seed_templates[-1]  # Maximum complexity

    def _ensure_world_consistency(self, newly_generated: Any, region: str) -> None:
        """Ensure new generation is consistent with established world laws"""

        # Check against session zero rules
        if isinstance(newly_generated, GeneratedTown):
            # Ensure town politics match complexity preferences
            # Get complexity from type or default to simple
            power_type = newly_generated.power_structure.get("type", "simple")
            type_complexity = {"simple": 1, "moderate": 2, "complex": 3}.get(power_type, 1)

            if type_complexity > self.session_zero.social_complexity // 3 + 1:
                newly_generated.power_structure = self._simplify_power_structure(newly_generated.power_structure)

            # Ensure mysteries match preference
            if len(newly_generated.hidden_truths) > self.session_zero.mystery_preference + 1:
                newly_generated.hidden_truths = newly_generated.hidden_truths[:self.session_zero.mystery_preference]

    def _log_world_event(self, event: str, category: str = "general", type: str = "info") -> None:
        """Log world changes for consistency checks"""
        self.world_log.append({
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "category": category,
            "type": type
        })

    # Helper methods would continue with all the specific generation logic...
    def _generate_mysterious_location_name(self, biome: GeneratedBiome, level: int) -> str:
        return f"Hidden Depth {level}"  # Simplified

    def _determine_reveal_condition(self, complexity_level: int) -> str:
        conditions = ["casual_observation", "skillful_investigation", "profound_revelation", "character_transformation"]
        return conditions[min(complexity_level - 1, len(conditions) - 1)]

    def _simplify_power_structure(self, power_structure: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation would simplify complex politics
        return power_structure

    def _infer_biome_from_description(self, player_description: str) -> BiomeType:
        # Parse player description for biome indicators
        description_lower = player_description.lower()

        if any(word in description_lower for word in ["forest", "woods", "trees"]):
            return BiomeType.FOREST
        elif any(word in description_lower for word in ["desert", "sand", "dune"]):
            return BiomeType.DESERT
        elif any(word in description_lower for word in ["mountain", "peak", "high"]):
            return BiomeType.MOUNTAIN
        elif any(word in description_lower for word in ["flooded", "underwater", "wet"]):
            return BiomeType.FLOODED
        elif any(word in description_lower for word in ["city", "metropolis", "urban"]):
            return BiomeType.METROPOLIS
        else:
            return BiomeType.FRONTIER

    def _generate_town_name(self, biome_type: BiomeType, region_coords: str) -> str:
        """Generate a town name based on biome type and region"""
        biome_prefixes = {
            BiomeType.FOREST: ["Green", "Oak", "Timber", "Leaf", "Wood"],
            BiomeType.DESERT: ["Sand", "Dust", "Oasis", "Sun", "Dune"],
            BiomeType.MOUNTAIN: ["High", "Stone", "Peak", "Cliff", "Summit"],
            BiomeType.FLOODED: ["Water", "Tide", "Flood", "Bay", "Marsh"],
            BiomeType.METROPOLIS: ["Great", "Grand", "Capital", "Imperial", "Royal"],
            BiomeType.FRONTIER: ["New", "Edge", "Border", "Front", "Wild"]
        }

        prefixes = biome_prefixes.get(biome_type, ["New"])
        suffixes = ["ville", "town", "borough", "haven", "crossing", "falls", "ridge", "valley"]

        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)

        return f"{prefix}{suffix}"

    def _generate_power_structure(self, social_complexity: int) -> Dict[str, Any]:
        """Generate a power structure based on social complexity"""
        structures = [
            {"type": "simple", "description": "Single leader or small council"},
            {"type": "moderate", "description": "Multiple competing factions"},
            {"type": "complex", "description": "Intricate web of political alliances"}
        ]

        index = min(2, max(0, social_complexity // 4))
        return structures[index]

    def _generate_cultural_quirks(self, cultural_uniqueness: int) -> List[str]:
        """Generate cultural quirks based on uniqueness preference"""
        all_quirks = [
            "unusual greeting customs",
            "specific dining etiquette",
            "unique local festivals",
            "strange superstitions",
            "distinctive fashion",
            "peculiar architecture",
            "special local cuisine",
            "uncommon religious practices"
        ]

        num_quirks = max(1, min(5, cultural_uniqueness // 2))
        return random.sample(all_quirks, num_quirks)

    def _generate_hidden_truths(self, mystery_preference: int) -> List[str]:
        """Generate hidden truths based on mystery preference"""
        truths = [
            "a secret organization operates in the shadows",
            "the town's founding story hides a dark truth",
            "certain locations hold more significance than they appear",
            "some residents are not who they claim to be",
            "ancient artifacts are hidden throughout the area"
        ]

        num_truths = max(1, min(4, mystery_preference // 3))
        return random.sample(truths, num_truths)

    def _generate_appropriate_npcs(self, player_description: str) -> List[Dict[str, Any]]:
        """Generate NPCs appropriate to the player description"""
        return [
            {
                "name": "Local Guide",
                "role": "information source",
                "personality": "helpful but cautious"
            },
            {
                "name": "Town Elder",
                "role": "authority figure",
                "personality": "wise but secretive"
            }
        ]

    def _calculate_town_population(self, biome_type: BiomeType) -> int:
        """Calculate town population based on biome type"""
        population_map = {
            BiomeType.FOREST: 800,
            BiomeType.DESERT: 400,
            BiomeType.MOUNTAIN: 600,
            BiomeType.FLOODED: 1200,
            BiomeType.METROPOLIS: 5000,
            BiomeType.FRONTIER: 300
        }

        return population_map.get(biome_type, 500)

    def _determine_primary_industry(self, biome_type: BiomeType) -> str:
        """Determine primary industry based on biome type"""
        industry_map = {
            BiomeType.FOREST: "logging and herbalism",
            BiomeType.DESERT: "mining and trade",
            BiomeType.MOUNTAIN: "mining and stonework",
            BiomeType.FLOODED: "fishing and trade",
            BiomeType.METROPOLIS: "commerce and crafts",
            BiomeType.FRONTIER: "hunting and farming"
        }

        return industry_map.get(biome_type, "mixed economy")

    def _generate_notable_sites(self, biome_type: BiomeType) -> List[str]:
        """Generate notable sites based on biome type"""
        sites_map = {
            BiomeType.FOREST: ["ancient grove", "hermit's cave", "hidden waterfall"],
            BiomeType.DESERT: ["oasis temple", "buried ruins", "trading post"],
            BiomeType.MOUNTAIN: ["cliffside monastery", "mining camp", "watchtower"],
            BiomeType.FLOODED: ["lighthouse", "floating market", "sunken ruins"],
            BiomeType.METROPOLIS: ["grand palace", "market district", "university"],
            BiomeType.FRONTIER: ["fort outpost", "pioneer settlement", "landmark rock"]
        }

        return sites_map.get(biome_type, ["local landmark", "meeting place", "historical site"])

    def _generate_architecture_style(self, biome_type: BiomeType, session_zero: SessionZeroProfile) -> str:
        """Generate architecture style based on biome and session zero"""
        styles = {
            BiomeType.FOREST: "wooden and natural materials",
            BiomeType.DESERT: "adobe and stone construction",
            BiomeType.MOUNTAIN: "stone and timber buildings",
            BiomeType.FLOODED: "elevated structures and bridges",
            BiomeType.METROPOLIS: "diverse and elaborate designs",
            BiomeType.FRONTIER: "simple and functional construction"
        }

        return styles.get(biome_type, "practical local style")

    def _generate_town_established_date(self, region_coords: str) -> str:
        """Generate a plausible establishment date"""
        years_ago = random.randint(50, 500)
        return f"{1000 - years_ago} years ago"

    def _generate_environmental_features(self, biome_type: BiomeType, session_zero: SessionZeroProfile) -> List[str]:
        """Generate environmental features based on biome type and session zero"""
        features_map = {
            BiomeType.FOREST: ["dense canopy", "winding streams", "ancient trees", "hidden clearings"],
            BiomeType.DESERT: ["shifting sands", "rocky outcrops", "oasis springs", "ancient ruins"],
            BiomeType.MOUNTAIN: ["steep cliffs", "narrow passes", "high peaks", "hidden valleys"],
            BiomeType.FLOODED: ["shallow waters", "marshy lands", "river channels", "flood plains"],
            BiomeType.METROPOLIS: ["wide boulevards", "tall buildings", "market squares", "public parks"],
            BiomeType.FRONTIER: ["open plains", "scattered settlements", "wild territories", "resource sites"]
        }

        base_features = features_map.get(biome_type, ["natural terrain", "local wildlife", "weather patterns"])

        # Add more features based on cultural uniqueness
        if session_zero.cultural_uniqueness > 7:
            base_features.append("unique cultural landmarks")
        if session_zero.magical_rarity > 5:
            base_features.append("magical phenomena")

        return base_features

    def _generate_inhabitants(self, biome_type: BiomeType, session_zero: SessionZeroProfile) -> List[str]:
        """Generate inhabitants based on biome type and session zero"""
        inhabitants_map = {
            BiomeType.FOREST: ["woodcutters", "herbalists", "hunters", "druids"],
            BiomeType.DESERT: ["nomads", "traders", "miners", "scholars"],
            BiomeType.MOUNTAIN: ["miners", "hermits", "guides", "warriors"],
            BiomeType.FLOODED: ["fishers", "sailors", "merchants", "artisans"],
            BiomeType.METROPOLIS: ["merchants", "nobles", "craftsmen", "entertainers"],
            BiomeType.FRONTIER: ["pioneers", "settlers", "scouts", "rangers"]
        }

        return inhabitants_map.get(biome_type, ["locals", "travelers", "merchants"])

    def _generate_resources(self, biome_type: BiomeType, historical_depth: int) -> List[Dict[str, Any]]:
        """Generate resources based on biome type and historical depth"""
        resources_map = {
            BiomeType.FOREST: [
                {"type": "timber", "rarity": "common"},
                {"type": "herbs", "rarity": "uncommon"},
                {"type": "game", "rarity": "common"}
            ],
            BiomeType.DESERT: [
                {"type": "minerals", "rarity": "rare"},
                {"type": "water", "rarity": "scarce"},
                {"type": "gems", "rarity": "very rare"}
            ],
            BiomeType.MOUNTAIN: [
                {"type": "stone", "rarity": "common"},
                {"type": "metals", "rarity": "uncommon"},
                {"type": "precious stones", "rarity": "rare"}
            ],
            BiomeType.FLOODED: [
                {"type": "fish", "rarity": "common"},
                {"type": "water plants", "rarity": "uncommon"},
                {"type": "shellfish", "rarity": "common"}
            ],
            BiomeType.METROPOLIS: [
                {"type": "luxury goods", "rarity": "varied"},
                {"type": "crafted items", "rarity": "common"},
                {"type": "imported goods", "rarity": "rare"}
            ],
            BiomeType.FRONTIER: [
                {"type": "raw materials", "rarity": "common"},
                {"type": "land", "rarity": "abundant"},
                {"type": "wildlife", "rarity": "common"}
            ]
        }

        base_resources = resources_map.get(biome_type, [{"type": "basic supplies", "rarity": "common"}])

        # Add historical resources for deeper history
        if historical_depth > 7:
            base_resources.append({"type": "ancient artifacts", "rarity": "very rare"})

        return base_resources

    def _generate_unique_properties(self, biome_type: BiomeType, magical_rarity: int) -> List[str]:
        """Generate unique properties based on biome type and magical rarity"""
        properties_map = {
            BiomeType.FOREST: ["natural healing", "enhanced senses", "plant communication"],
            BiomeType.DESERT: ["heat resistance", "water conservation", "night vision"],
            BiomeType.MOUNTAIN: ["heightened reflexes", "thin air adaptation", "stone sense"],
            BiomeType.FLOODED: ["water breathing", "buoyancy control", "current reading"],
            BiomeType.METROPOLIS: ["social networking", "information gathering", "cultural awareness"],
            BiomeType.FRONTIER: ["self-reliance", "danger sensing", "resourcefulness"]
        }

        base_properties = properties_map.get(biome_type, ["local adaptation", "environmental familiarity"])

        # Add magical properties for higher magical rarity
        if magical_rarity > 6:
            base_properties.append("magical energy sensitivity")
        if magical_rarity > 8:
            base_properties.append("supernatural phenomenon occurrence")

        return base_properties

    def _generate_hidden_locations(self) -> List[Dict[str, Any]]:
        """Generate hidden locations for discovery"""
        return [
            {
                "name": "Forgotten Cave",
                "type": "exploration",
                "difficulty": "moderate",
                "potential": "ancient secrets"
            },
            {
                "name": "Abandoned Ruins",
                "type": "investigation",
                "difficulty": "high",
                "potential": "powerful artifacts"
            }
        ]

    def _generate_climate(self, biome_type: BiomeType) -> Dict[str, str]:
        """Generate climate information for biome"""
        climate_map = {
            BiomeType.FOREST: {"temperature": "moderate", "precipitation": "high", "seasons": "distinct"},
            BiomeType.DESERT: {"temperature": "hot", "precipitation": "very low", "seasons": "minimal"},
            BiomeType.MOUNTAIN: {"temperature": "cool to cold", "precipitation": "moderate", "seasons": "distinct"},
            BiomeType.FLOODED: {"temperature": "moderate", "precipitation": "high", "seasons": "wet and dry"},
            BiomeType.METROPOLIS: {"temperature": "varied", "precipitation": "moderate", "seasons": "distinct"},
            BiomeType.FRONTIER: {"temperature": "varied", "precipitation": "moderate", "seasons": "distinct"}
        }

        return climate_map.get(biome_type, {"temperature": "moderate", "precipitation": "moderate", "seasons": "distinct"})

    def _generate_seasonal_variations(self, biome_type: BiomeType) -> List[str]:
        """Generate seasonal variations for biome"""
        variations_map = {
            BiomeType.FOREST: ["spring blooms", "summer growth", "autumn colors", "winter dormancy"],
            BiomeType.DESERT: ["day heat", "night cold", "sandstorm season", "rare rainfall"],
            BiomeType.MOUNTAIN: ["snow cover", "avalanche risk", "clear views", "rockfall danger"],
            BiomeType.FLOODED: ["flood season", "dry season", "storm season", "calm waters"],
            BiomeType.METROPOLIS: ["festival seasons", "market days", "political events", "social gatherings"],
            BiomeType.FRONTIER: ["settlement expansion", "resource gathering", "weather challenges", "growth periods"]
        }

        return variations_map.get(biome_type, ["standard seasonal changes"])

    def _reveal_biome_progressively(self, region_coords: str) -> GeneratedBiome:
        """Reveal biome information progressively"""
        # For now, just return the existing biome
        return self.biomes[region_coords]

    def _create_progressive_biome_reveal(self, biome: GeneratedBiome) -> GeneratedBiome:
        """Create a progressive reveal of biome information"""
        # For now, just return the biome as is
        return biome

    def _implement_world_unification_protocol(self) -> None:
        """Ensure all future expansions maintain unity with Session Zero foundation"""
        # This would ensure consistency rules are applied to all future generations
        pass