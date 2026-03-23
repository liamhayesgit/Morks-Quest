import random
from symtable import Class
from colorama import init, Fore, Style
init(autoreset=True)


class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role.capitalize()
        self.role = role
        self.inventory = []

        if role == "Warrior":
            self.health = 150
            self.max_health = 150
            self.max_mana = 0
            self.mana = 0
            self.rage = 0
            self.max_rage = 100
            self.strength = 15
            self.magic = 5
            self.agl = 10
            self.ac = 14
            self.strmodifier = 2
            self.magicmodifier = 0
            self.aglmodifier = 1
            self.spells = []
            self.mana = 0
        elif role == "Mage":
            self.health = 75
            self.max_health = 75
            self.max_mana = 100
            self.mana = 100
            self.rage = 0
            self.max_rage = 0
            self.strength = 5
            self.magic = 15
            self.agl = 5
            self.ac = 10
            self.strmodifier = 0
            self.magicmodifier = 2
            self.aglmodifier = 0
            self.spells = ["Fireball", "Heal"]
        elif role == "Rogue":
            self.health = 100
            self.max_health = 100
            self.max_mana = 0
            self.mana = 0
            self.rage = 0
            self.max_rage = 0
            self.strength = 10
            self.magic = 10
            self.agl = 15
            self.ac = 12
            self.strmodifier = 1
            self.magicmodifier = 1
            self.aglmodifier = 2
            self.spells = []
            self.mana = 0
   #Normal attack 
    def attack(self, enemy):
        if self.role == "Warrior":
            modifier = self.strmodifier
        elif self.role == "Rogue":
            modifier = self.aglmodifier
        else:
            modifier = 0
        raw_roll = self.roll_dice(20)
        modifier = self.strmodifier if self.role == "Warrior" else self.aglmodifier
        total_roll = raw_roll + modifier

        print(f" {self.name} rolled a {raw_roll}!")

        if raw_roll == 20:
         damage =  (self.roll_dice(6) + modifier) * 2
         enemy.health -= damage
         print(f"Nat 20! Crit Hit!")
         print(f"You dealt {damage} massive damage to {enemy.name}!")

        elif total_roll >= enemy.ac:
            damage = self.roll_dice(6) + modifier
            enemy.health -= damage
            print(f"Hit! {self.name} deals {damage} damage to {enemy.name}.")
            
            if self.role == "Warrior":
             gain = random.randint(10, 15)
             self.rage = min(self.max_rage, self.rage + gain)
             print(f"{self.name} gains {gain} rage!")
        if total_roll < (enemy.ac):
            print(f"{self.name}'s attack is blocked")            
            if enemy.health <= 0:
               enemy.health = 0
            else:
                    print(f"{enemy.name} has {enemy.health} health remaining!")                 
#mighty blow
    def mighty_blow(self, enemy):
        '''Performs a powerful attack that consumes rage'''
        if self.role != "Warrior":
            print("Only Warriors can perform Mighty Blow!")
            return False
        
        if self.rage >= 50:
            print(f"{self.name} unleashes a Mighty Blow!")
            damage = (self.roll_dice(6) * 3 + self.strmodifier) * 2
            enemy.health -= damage
            self.rage -= 50
            print(f"Mighty Blow hits for {damage} damage! Current rage: {self.rage}/{self.max_rage} RP")
            return True
        else:
            print("Not enough rage to perform Mighty Blow!")
            return False
#sneak attack

    def sneak_attack(self, target):
        # 1. Give the Rogue a built-in +5 to HIT from shadows
        hit_roll = self.roll_dice(20) + self.aglmodifier + 5
        print(f"🎯 {self.name} strikes from the darkness! (Roll: {hit_roll} vs AC {target.ac})")

        if hit_roll >= target.ac:
            # 2. Use 3d10 for massive "Assassin" damage
            damage = self.roll_dice(10) + self.roll_dice(10) + self.roll_dice(10) + self.aglmodifier
            print(f"🗡️ SNEAK ATTACK! You dealt {damage} damage!")
            target.take_damage(damage)
        else:
            print(f"💨 {target.name} sensed your presence! The attack missed.")


    def add_item(self, item):
        self.inventory.append(item)

    def get_spell_list(self):
        if self.role == "Mage":
            return ["Fireball", "Heal"]
        else:
            return []
   #spells 
    def get_spell_display(self):
        output = "\nAvailable Spells:\n"
        for spell in self.get_spell_list():
            output += f" - {spell}\n"
        return output

    def cast_spell(self, spell_name, target):
        '''Casts a spell if the player has enough mana'''
        if self.role != "Mage":
            print("Only Mages can cast spells!")
            return
        
        if spell_name == "Fireball":
            if self.mana >= 10:
                self.mana -= 10
                damage = random.randint(25, 40) + self.magicmodifier
                print(f"{self.name} casts Fireball!")
                target.health -= damage
                print(f"Fireball hits for {damage} damage!")
                return "Fireball"
            else:
                print("Not enough mana to cast Fireball!")
                return None
        elif spell_name == "Heal":
            if self.mana >= 15:
                self.mana -= 15
                heal_amount = random.randint(15, 35)
                self.health += heal_amount
                if self.health > self.max_health:
                    self.health = self.max_health
                print(f"{self.name} heals for {heal_amount} health! Current health: {self.health}/{self.max_health} HP")
                return "Heal"
        else:
            print("not enough mana to cast Heal!")
            return None

    
        
    def roll_dice(self, sides):
        return random.randint(1, sides)
    
    def get_mana_bar(self):
        if self.mana <= 0 and self.role != "Mage":
            return ""
        total_bars = 20
        mana_ratio = max(0, min(self.mana / self.max_mana, 1))
        filled_bars = int(mana_ratio * total_bars)
        empty_bars = total_bars - filled_bars
        color = Fore.BLUE if mana_ratio > 0.3 else Fore.CYAN
        return f"{Style.BRIGHT}{color}[{"█" * filled_bars} {"-" * empty_bars}] {self.mana}/{self.max_mana} MP{Style.RESET_ALL}"

    def get_rage_bar(self):
        if self.rage <= 0 and self.role != "Warrior":
            return ""
        total_bars = 20
        rage_ratio = max(0, min(self.rage / self.max_rage, 1))
        filled_bars = int(rage_ratio * total_bars)
        empty_bars = total_bars - filled_bars
        color = Fore.RED if rage_ratio > 0.3 else Fore.YELLOW
        return f"{Style.BRIGHT}{color}[{"█" * filled_bars} {"-" * empty_bars}] {self.rage}/{self.max_rage} RP{Style.RESET_ALL}"
    
    def get_health_bar(self):
        total_bars = 20
        health_ratio = self.health / self.max_health
        filled_bars = max(0, int(health_ratio * total_bars))
        empty_bars = total_bars - filled_bars
        
        if health_ratio <= 0.3:
            color = Fore.RED
        elif health_ratio <= 0.7:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN
        
        return f"{Style.BRIGHT}{color}[{'█' * filled_bars}{'-' * empty_bars}] {self.health}/{self.max_health} HP{Style.RESET_ALL}"
            

    def check_if_hit(self, attack_roll):
        '''Returns True if hit and False if miss'''
        if attack_roll >= self.ac:
            print(f"{self.name} was hit!")
            return True
        else:
            print(f"{self.name} avoided taking damage!")
            return False
                        
    def take_damage(self, amount):
        '''Reduces health by damage taken'''
        self.health -= amount
        if self.health <0: self.health = 0
        print(f"{self.name} takes {amount} damage.")
        if self.health <= 0:
            print(f"{self.name} has been defeated!")



#---Enemy class---#
class Enemy:
    def __init__(self, name, type):
        self.name = name
        self.type = type

        if type == "Goblin":
            self.health = 20
            self.max_health = 20
            self.strength = 10
            self.magic = 5
            self.agl = 5
            self.ac = 10
            self.strmodifier = 0
            self.magicmodifier = 0
            self.aglmodifier = 0
        elif type == "Orc":
            self.health = 85
            self.max_health = 85
            self.strength = 15
            self.magic = 0
            self.agl = 5
            self.ac = 12
            self.strmodifier = 2
            self.magicmodifier = 0
            self.aglmodifier = 0
        elif type == "Troll":
            self.health = 160
            self.max_health = 160
            self.strength = 20
            self.magic = 0
            self.agl = 5
            self.ac = 14
            self.strmodifier = 4
            self.magicmodifier = 0
            self.aglmodifier = 0

        
    def roll_dice(self, sides):
        import random
        return random.randint(1, sides)

    def attack(self, target):
        print(f"\n---{self.name}'s turn---")

        raw_roll = self.roll_dice(20)
        modifier  = 5
        total_roll = raw_roll + modifier

        print(f" 🎲 {self.name} rolled a {raw_roll} + {modifier} = {total_roll} vs your AC {target.ac}")

        if total_roll >= target.ac:
            if self.type == "Troll":
                print(f" {self.name} slams his massive fists into the ground!")
                damage = self.roll_dice(12) + 15
            elif self.type == "Orc":
                print(f"{self.name} swings a rusty cleaver!")
                damage = self.roll_dice(8) + 10
            else:
             print(f"{self.name} lunges with a rusty shank!")
             damage = self.roll_dice(6) + 2
            target.take_damage(damage)
        else:
            print(f"{target.name} avoided the blow")

    def check_if_hit(self, attack_roll):
        '''Returns True if hit and False if miss'''
        if attack_roll >= self.ac:
            print(f"{self.name} was hit!")
            return True
        else:
            print(f"{self.name} avoided taking damage!")
            return False      
        
    def take_damage(self, amount):
        '''Reduces health by damage taken'''
        self.health -= amount
        if self.health < 0: self.health = 0
        print(f'{self.name} shrieks!')
        print(f'{self.name} has {self.health} health remaining.')
        if self.health <= 0:
            print(f"{self.name} has been defeated!")

  
    def get_health_bar(self):
        total_bars = 20
        health_ratio = self.health / self.max_health
        filled_bars = max(0, int(health_ratio * total_bars))
        empty_bars = total_bars - filled_bars
        
        if health_ratio <= 0.3:
            color = Fore.RED
        elif health_ratio <= 0.7:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN
        
        return f"{Style.BRIGHT}{color}[{'█' * filled_bars}{'-' * empty_bars}] {self.health}/{self.max_health} HP{Style.RESET_ALL}"
    


            