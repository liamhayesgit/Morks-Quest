from entities import Enemy
from items import Item


World_map = {
    "Start": {
        "description": "You stand at the forest's edge where sunlight fades into a wall of ancient oaks. Your quest is clear: retrieve the Gemstone from the caves ahead and return back. The path UP leads into the shadows of the treeline.",
        "exits": {"up": "Forest path"}
    },
    "Forest path": {
        "description": "The trail is narrow here, hemmed in by gnarled roots and the watchful eyes of hidden crows. UP the path, the trees grow massive. A silver glint catches your eye near a pile of stones.", 
        "exits": {"up": "Ancient Tree", "down": "Start"},
        "Trigger": "Goblin_Ambush",
        "Item": Item("Shadow Dagger", "A black blade that feels light as a feather.", "increase_agl", 5)
    },
    "Ancient Tree": {
        "description": "A massive, silver-barked oak dominates this clearing, its branches clawing at the sky. A mysterious, dark hollow in the trunk seems just large enough for a treasure to hide within. The forest continues UP into the gloom.", 
        "exits": {"up": "Deep Forest", "down": "Forest path"},
        "Item": Item("Magic Potion", "A glowing red vial that pulses like a heartbeat.", "heal", 50)
    },
    "Deep Forest": {
        "description": "The canopy above is so thick that midday feels like twilight. The forest has grown silent; even the wind fears to whistle through these thorns. UP ahead, the trees give way to a stony cliffside.", 
        "exits": {"up": "Cave", "down": "Ancient Tree"},
        "Item": Item("Iron key", "A heavy, rusted key that looks like it belongs to a sturdy chest.", "Unlocks", 0)
    },
    "Cave": {
        "description": "The mouth of the cave gapes open like a stone maw, breathing out a draft of cold, damp air. UP into the darkness, you hear the steady, rhythmic 'drip-drop' of water echoing off the limestone walls.", 
        "exits": {"up": "Deep Cave", "down": "Deep Forest"},
        "Item": Item("Mana Potion", "A swirling blue liquid that hums with arcane energy.", "mana", 50)
    },
    "Deep Cave": {
        "description": "The cave walls are slick with bioluminescent moss, casting a sickly green glow over the jagged rocks. To your LEFT, a heavy wooden door is embedded in the rock wall, standing completely silent.", 
        "exits": {"down": "Cave", "left": "Treasure Room"},
        "Trigger": "Orc_guard",
        "Item": Item("Sword +1", "A masterfully forged blade that feels perfectly balanced.", "increase_attack", 5)
    },
    "Treasure Room": {
        "description": "Torches flicker in wall-sconces, reflecting off piles of gold and jewels. In the centre of the room sits a massive iron-bound chest, looking both ancient and dangerously well-protected. The only exit is back DOWN the path.", 
        "exits": {"down": "Deep Cave"},
        "is_locked": True,
        "Item": Item("Gemstone", "The legendary Ruby—it pulses with a fierce, internal fire.", "Victory", 0)
    }
}

