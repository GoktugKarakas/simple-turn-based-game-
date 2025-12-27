from decorator import *
import random
import time

class Ability:
    def __init__(self, name, damage, cooldown):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.turns_left = 0 

class Character:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.abilities = [Ability('Basic Attack', 10, cooldown=0)]

    def add_ability(self, ability):
        self.abilities.append(ability)

    def reduce_cooldowns(self):
        for ability in self.abilities:
            if ability.turns_left > 0:

                ability.turns_left -= 1

    def heal(self):
        lucky_turn = random.randint(1, 100) <= 40
        
        if lucky_turn:
            print(f"{styles.GREEN}{styles.BOLD}{styles.UNDERLINE}DOUBLE HEALING{styles.RESET}")
            heal_amount = 50

        else:
            heal_amount = 25

        self.hp += heal_amount

        if self.hp > self.max_hp: 
            self.hp = self.max_hp

        print(f"{styles.CYAN}{self.name} {styles.GREEN}healed for {heal_amount} HP! {styles.RESET}{styles.BOLD}(HP: {self.hp}/{self.max_hp}){styles.RESET}")

    def attack(self, target, chosen_ability_index):
        move = self.abilities[chosen_ability_index]
        
        if move.turns_left > 0:
            print(f"{styles.UNDERLINE}{move.name} is on cooldown! Turn wasted.{styles.RESET}")
            return False 

        final_damage = move.damage
        is_crit = random.randint(1, 100) <= 20
        
        if is_crit:
            final_damage = final_damage * 2
            print(f"{styles.BOLD}{styles.UNDERLINE}{styles.RED}CRITICAL HIT!!!!!!! Damage doubled!{styles.RESET}")

        print(f'{styles.CYAN}{self.name}{styles.RESET} hits {styles.RED}{target.name}{styles.RESET} with {move.name} for {styles.UNDERLINE}{final_damage} dmg!s{styles.RESET}')
        target.take_damage(final_damage)
        
        move.turns_left = move.cooldown
        return True 

    def take_damage(self, amount):
        self.hp -= amount
        display_hp = max(0, self.hp)
        print(f'{styles.CYAN}{self.name}{styles.RESET} took {styles.UNDERLINE}{amount} damage{styles.RESET}{styles.BOLD}| HP: {display_hp}/{self.max_hp}{styles.RESET} ')

        if self.hp <= 0:
            self.die()

    def die(self):
        print(f'{styles.CYAN}{self.name}{styles.RESET}{styles.RED} has been defeated{styles.RESET}')

class Assasin(Character):
    def __init__(self, name):
        super().__init__(name, hp=100) 
        self.add_ability(Ability('Backstab', 40, cooldown=3))
        self.add_ability(Ability('Arrow', 30, cooldown=2))
        self.add_ability(Ability('Smoke Screen', 15, cooldown=1))

class Brute(Character):
    def __init__(self, name):
        super().__init__(name, hp=150)
        self.add_ability(Ability('Slam', 30, cooldown=2))
        self.add_ability(Ability('Smash', 70, cooldown=5))
        self.add_ability(Ability('Kick', 40, cooldown=3))

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, hp=75)
        self.add_ability(Ability('Curse', 60, cooldown=4))
        self.add_ability(Ability('Fireball', 30, cooldown=2))
        self.add_ability(Ability('Lightning Bolt', 50, cooldown=3))
       
class Game():
    def __init__(self):
        self.player = None
        self.enemy = None 

    def character_selection(self):
        print(f"{styles.BLUE}{styles.BOLD}--- NEW GAME ---{styles.RESET}")
        valid_inputs = ["Brute", "Mage", "Assasin"]
        
        while True:
            selection = input('Choose Character (Brute, Mage, Assasin): ').title()

            if selection in valid_inputs: 
                break
            print('Invalid selection.')

        if selection == 'Assasin': 
            self.player = Assasin('Player')
            
        elif selection == 'Mage': 
            self.player = Mage('Player')

        elif selection == 'Brute':
            self.player = Brute('Player') 

        enemy_types = [
            {"name": "Goblin", "hp": 180, "move": "Throwing dagger", "dmg": 25 , "cooldown": 1},
            {"name": "Ebony Knight", "hp": 240, "move": "Berserker", "dmg": 45, "cooldown": 3},
            {"name": "Bandit", "hp": 200, "move": "Club", "dmg": 35, "cooldown": 2},
            {"name": "Dragon", "hp": 350, "move": "Fire Breath", "dmg": 60 , "cooldown": 4}
        ]
    
        enemy_data = random.choice(enemy_types)
        
        self.enemy = Character(enemy_data["name"], enemy_data["hp"])
        self.enemy.add_ability(Ability(enemy_data["move"], enemy_data["dmg"], enemy_data["cooldown"]))
        
        print(f"\nYou made your choice {styles.CYAN}{self.player.name}.{styles.RESET}{styles.RED} A wild {self.enemy.name} appears!{styles.RESET}\n")
   
    def turn_system(self):
        while self.player.hp > 0 and self.enemy.hp > 0:
            
            print(f"\n{styles.UNDERLINE}--- YOUR TURN ---{styles.RESET}")
            self.player.reduce_cooldowns() 
            
            action = input("Type (A) to Attack or (H) to Heal: ").upper()
            
            if action == 'H':
                self.player.heal()
            else:
                print("Select an attack:")
                for index, ability in enumerate(self.player.abilities):
                    status = "READY"
                    if ability.turns_left > 0:
                        status = f"WAIT {ability.turns_left} TURNS"
                    print(f"{styles.BOLD}[{index}] {ability.name} (Dmg: {ability.damage}) - [{status}]{styles.RESET}")
            
                try:
                    choice = int(input("Enter number: "))
                    if choice < 0 or choice >= len(self.player.abilities):
                        print("Invalid choice!")
                        continue
                    
                    if self.player.abilities[choice].turns_left > 0:
                        print("That move is not ready yet!")
                        continue

                    success = self.player.attack(self.enemy, choice)
                    if not success: continue 
                    
                except ValueError:
                    print("Invalid input.")
                    continue

            if self.enemy.hp <= 0:
                print(f"\n{styles.GREEN} VICTORY!{styles.RESET}")
                print(f"{styles.BOLD}..............Returning to main Menu{styles.RESET}")
                break
            
            time.sleep(2)

            print(f"\n{self.enemy.name}'s TURN")
            self.enemy.reduce_cooldowns()
            
            strong_move = self.enemy.abilities[-1]
            if strong_move.turns_left == 0:
                self.enemy.attack(self.player, -1)
            else:
                print(f"({styles.PURPLE}Enemy {strong_move.name} is charging...){styles.RESET}")
                self.enemy.attack(self.player, 0)

            if self.player.hp <= 0:
                print(f"\n{styles.RED} GAME OVER{styles.RESET}")
                print(f"{styles.BOLD}..............Returning to main Menu{styles.RESET}")
                break
