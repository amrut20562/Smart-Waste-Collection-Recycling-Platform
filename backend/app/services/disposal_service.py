from typing import Dict, Any, Optional

DISPOSAL_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "plastic": {
        "display_name": "Plastic",
        "waste_stream": "Dry Recyclable",
        "instructions": [
            "Rinse out any food or liquid residue thoroughly.",
            "Crush plastic bottles or containers to save bin space.",
            "Place caps back on bottles or discard separately if non-recyclable.",
            "Keep dry and place in the Blue/Dry Recyclable bin."
        ],
        "special_handling": False,
        "pickup_supported": True,
        "warning": None
    },
    "cardboard": {
        "display_name": "Cardboard",
        "waste_stream": "Dry Recyclable / Paper Stream",
        "instructions": [
            "Flatten all cardboard boxes to conserve collection volume.",
            "Remove excessive plastic tape, foam packaging, or bubble wrap.",
            "Keep completely dry; contaminated or greasy cardboard belongs in general trash.",
            "Bundle neatly for scheduled curbside pickup."
        ],
        "special_handling": False,
        "pickup_supported": True,
        "warning": "Greasy or food-soiled cardboard cannot be recycled."
    },
    "paper": {
        "display_name": "Paper",
        "waste_stream": "Dry Recyclable",
        "instructions": [
            "Ensure paper is clean and dry.",
            "Remove plastic sleeves, bindings, or large metal clips.",
            "Do not shred unless containing sensitive personal information.",
            "Place in dry recycling container."
        ],
        "special_handling": False,
        "pickup_supported": True,
        "warning": None
    },
    "metal": {
        "display_name": "Metal & Cans",
        "waste_stream": "Dry Recyclable / Scrap Metal",
        "instructions": [
            "Rinse clean aluminum cans, tin cans, or metal lids.",
            "Do not crush aerosol cans; ensure they are completely empty before disposal.",
            "Separate sharp metal edges safely.",
            "Place in dry recyclable metal collection stream."
        ],
        "special_handling": False,
        "pickup_supported": True,
        "warning": "Ensure pressurized aerosol cans are fully depressurized and empty."
    },
    "glass": {
        "display_name": "Glass",
        "waste_stream": "Glass Recyclable",
        "instructions": [
            "Rinse glass bottles and jars clean of all food/liquid contents.",
            "Remove metal or plastic lids and sort them into their respective streams.",
            "Handle with care to prevent breakage and injury.",
            "Do not mix with ceramics, Pyrex, window panes, or light bulbs."
        ],
        "special_handling": True,
        "pickup_supported": True,
        "warning": "Fragile: broken glass must be wrapped securely in newspaper before handling."
    },
    "compost": {
        "display_name": "Compost & Organic Waste",
        "waste_stream": "Wet / Organic Waste",
        "instructions": [
            "Separate food scraps, fruit peels, vegetable waste, and coffee grounds.",
            "Do not mix with plastic wrappers, stickers, or metal foil.",
            "Use a compostable liner or place directly into the Green/Organic bin.",
            "Schedule frequent pickup to prevent odor and pest buildup."
        ],
        "special_handling": False,
        "pickup_supported": True,
        "warning": "High urgency: organic waste degrades quickly and attracts pests."
    },
    "e_waste": {
        "display_name": "Electronic Waste (E-Waste)",
        "waste_stream": "Hazardous / Specialized E-Waste",
        "instructions": [
            "Remove rechargeable batteries if detachable and recycle at dedicated battery drop-offs.",
            "Wipe all personal data from devices prior to handover.",
            "Keep cables, adapters, and peripherals together.",
            "Schedule specialized municipal e-waste collection."
        ],
        "special_handling": True,
        "pickup_supported": True,
        "warning": "Contains heavy metals and lithium batteries. Never dispose of in regular trash."
    },
    "trash": {
        "display_name": "General Trash (Non-Recyclable)",
        "waste_stream": "General Solid Waste (Landfill)",
        "instructions": [
            "Bag securely to prevent littering and contamination.",
            "Ensure no hazardous liquids or glowing embers are inside.",
            "Place in the Black/Grey General Trash bin."
        ],
        "special_handling": False,
        "pickup_supported": True,
        "warning": None
    }
}

class DisposalService:
    @staticmethod
    def get_guidance(category: str) -> Dict[str, Any]:
        normalized = category.lower().strip()
        if normalized in DISPOSAL_KNOWLEDGE_BASE:
            return DISPOSAL_KNOWLEDGE_BASE[normalized]
        # Fallback for unexpected categories
        return {
            "display_name": category.replace("_", " ").title(),
            "waste_stream": "General Trash",
            "instructions": ["Place in general waste bin safely."],
            "special_handling": False,
            "pickup_supported": True,
            "warning": None
        }
