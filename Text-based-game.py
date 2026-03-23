from entities import Player, Enemy
from items import Item
from world import World_map
import random
import time 
from colorama import Fore, Style
from art import show_victory_screen, show_game_over
auto_reset = True
#Combat system#
def start_combat(hero, target, room_data):  
    while hero.health > 0 and target.health > 0:
        action  = ""
        name_width = max(len(hero.name), len(target.name)) + 2
        print(f"\n{target.name:<{name_width}} HP: {target.get_health_bar()}")
        print('----------------------------------------------------------')
        print(f"{hero.name:<{name_width}} HP: {hero.get_health_bar()}")
        if hero.role == "Mage":
             print(f"{' ' * name_width} MP: {hero.get_mana_bar()}")
        if hero.role == "Warrior":
             print(f"{' ' * name_width} RP: {hero.get_rage_bar()}")
          #player turn#
        # --- STEP 1: CHOOSE THE MENU BASED ON ROLE ---
        if hero.role == "Warrior":
            if hero.rage >= 50:
                print(f"{Fore.RED}Mighty Blow is available!{Style.RESET_ALL}")
            action = input("Do you [attack], [mighty blow], [run], or [use item]? ").lower().strip()
        
        elif hero.role == "Mage":
            action = input("Do you [attack], [cast spell], [run], or [use item]? ").lower().strip()
        
        elif hero.role == "Rogue":
            action = input("Do you [attack], [sneak attack], [run], or [use item]? ").lower().strip()

        # --- STEP 2: PERFORM THE ACTION ---
# Inside start_combat in main.py
        if action == "sneak attack":
             if hero.role == "Rogue":
        # Just call the function from entities.py
                hero.sneak_attack(target)
             else:
                 print("❌ Only Rogues can perform sneak attacks!")


        elif action == "mighty blow":
            if hero.role == "Warrior":
                if hero.rage >= 50:
                    hero.mighty_blow(target)
                else:
                    print("Not enough rage! (50 required)")
                    continue # Restarts the turn


                    

                time.sleep(1)           

        if action == "attack":
            hero.attack(target)
            time.sleep(1)  # Pause for dramatic effect

        elif action == "cast spell":
                if not hero.spells:
                    print("You don't know any spells!")
                    continue
                spell_choice = input("Enter spell name (Fireball or Heal): ").capitalize()

                if spell_choice in hero.spells:
                    hero.cast_spell(spell_choice, target)
                else:
                    print("You don't know that spell!")
                    continue

                time.sleep(1)  # Pause for dramatic effect

        elif action == "use item":
            choice = input("what do you want to use(magic/mana potion): ").lower().strip()

            found = False
            for item in hero.inventory:
                 if item.name.lower() == choice:
                      item.activate(hero)
                      print(hero.get_health_bar())
                      print(hero.get_mana_bar())
                      hero.inventory.remove(item)
                      found = True
                      break
            if not found:
             print("you don't have that item!")

            

        elif action == "run":
            print(f"{hero.name} runs away from the combat!")
            return "run"
        
        time.sleep(1)  # Pause for dramatic effect
        
            #target turn#
        if target.health > 0:
             target.attack(hero)

        time.sleep(1)  # Pause for dramatic effect
                  
        if target.health <= 0:
               print(f"{target.name} has been defeated!")
               return True
        

        if hero.health <= 0:
                show_game_over()
                game_running = False
        
                if target.type == "Orc":
                    print("The Orc drops a sword")
                    room_data["Item"] = ("sword +1", "A sword that increases attack", "increases attack")
                    

                    
               
#Game loop#
def start_game():
    print("============================================")
    print("|        Mork's Quest: The Cursed Cave     |")
    print("============================================")  
    print("  [         Controls are as written      ]") 
    input("  [ Press Enter to start your adventure! ]")
   

    name = input("Enter your character's name: ")
    print("\n Welcome, " + name + "! Choose your class: Warrior: Frontline fighter, Mage: Destructive spellcaster, or Rogue: Stealthy problem solver.")
    role = input("Enter your class: ").capitalize()
    while role not in ["Warrior", "Mage", "Rogue"]:
        print("Invalid class. Please choose Warrior, Mage, or Rogue.")
        role = input("Enter your class: ").capitalize()
    
    hero = Player(name, role)#!!! important for combat system, do not delete or change the name of this variable!!!#
    print(f"\nWelcome, {hero.name} the {hero.role}! Your adventure begins now.")

    current_room = "Start"
    game_running = True
    has_treasure = False
    has_sword = False
  

    while game_running:  # Main game loop
        controls = {
             "1": "up",
             "2": "down",
             "3": "left",
             "4": "right"
        }
        room_data = World_map[current_room]
        print(f"\n---{current_room}---")
        print(room_data["description"])
        #Enemy triggers
        if "Trigger" in room_data and room_data["Trigger"] == "Goblin_Ambush":
            if random.random() < 1:  # 50% chance of goblin ambush
                print("A Goblin ambushes you!")
                Goblin_ambush = Enemy("Sneaky Goblin", "Goblin")
                start_combat(hero, Goblin_ambush, room_data)
            else:
                print("You manage to avoid the goblin ambush!")

            del room_data["Trigger"]  # Remove the trigger after it has been activated

        if current_room == "Deep Cave" and not room_data.get("cleared"):
             print("\nAn Orc guard stands before you blocking your way deeper!")
             mini_boss = Enemy("Mog", "Orc")
             start_combat(hero, mini_boss, room_data)
             room_data["cleared"] = True
             print("You feel stronger after that victory!")
             hero.max_health += 20

        #Item code
        if room_data.get("is_locked"):
            print("The chest is locked and you need a key to open it.")

            # This checks if the item IS the string OR if the item's .name matches
            has_key = any(item.name.lower().strip() == "iron key" for item in hero.inventory)

            if has_key:
                use_key = input("Use your Iron key? (yes/no)?").lower()
                if use_key == 'yes':
                        print("With a grinding protest the lock on the chest opens!")
                        room_data["is_locked"] = False
                    
                    # Optional: Remove the key so it's 'used up'
                        for item in hero.inventory:
                            if item.name.lower().strip() == "iron key":
                                hero.inventory.remove(item)
                                break 

            else:
                print("You don't have the right key. Maybe it's in the forest?")

        # --- UNIVERSAL PICKUP BLOCK ---
        if not room_data.get("is_locked") and "Item" in room_data:
            found_item = room_data.get("Item")

            print(f"\n✨ You found {found_item.name}!")
            take_item = input("Do you want to take it? (yes/no): ").lower().strip()

            if take_item == "yes":
                # 1. Add the object to your inventory (Works for Key, Sword, Potion)
                hero.add_item(found_item)
                print(f"✅ The {found_item.name} has been added to your inventory.")

                # 2. SPECIAL TRIGGER: If it's the Gemstone, spawn the Boss
                if found_item.name.lower() == "gemstone":
                    has_treasure = True
                    print("\n🚨 STEVE THE TROLL APPEARS!")
                    boss = Enemy("Steve", "Troll")
                    start_combat(hero, boss, room_data)
                
                # 3. Remove it from the room so it doesn't stay there
                del room_data["Item"]
                  
                        


        print("Exits: " + ", ".join(room_data["exits"].keys()))
        Move = input("Move (1-UP/2-DOWN/3-LEFT/4-RIGHT): ").lower()
        if Move in controls:
             Move = controls[Move]
        if Move in room_data["exits"]:
            current_room = room_data["exits"][Move]
        else:
            print("Invalid move. Please choose a valid exit.")

        if current_room == "Start" and has_treasure:
                    show_victory_screen(hero.name, hero.health)
                    game_running = False
                    
start_game()


