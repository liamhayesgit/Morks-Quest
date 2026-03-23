class Item:

    def __init__(self, name, desc, effect_type, amount):
        self.name = name
        self.desc = desc
        self.effect_type = effect_type#'heal, mana, buff
        self.amount = int(amount)
    
    def activate(self, user):
        # Use .lower() here just to be safe!
        effect = self.effect_type.lower().strip()

        if effect == "heal" or effect == "restore_health":
            user.health = min(user.health + self.amount, user.max_health)
            print(f"❤️ {self.name} used! HP is now {user.health}/{user.max_health}")

        elif effect == "mana" or effect == "restore_mana":
            user.mana = min(user.mana + self.amount, user.max_mana)
            print(f"🔮 {self.name} used! MP is now {user.mana}/{user.max_mana}")






magic_potion = Item("magic Potion", "heals you.", "heal", 50),
mana_potion = Item("mana potion", "restores mana", "mana", 75)
sword_plus_one = Item("sword +1", "A sword that increases attack power.", "increase_attack", 5)
shadow_dagger = Item("Shadow Dagger", "A black blade that feels light as a feather.", "increase_agl", 5)
Gemstone = Item("Gemstone", "A bright red Ruby!", "Victory", 0)
Iron_key = Item("Iron key", "for opening a chest", "Unlock", 0)
