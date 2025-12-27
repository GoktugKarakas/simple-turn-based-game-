from code import Game
from decorator import *

def main():
    
    print(f"{styles.BOLD}{styles.PURPLE}===============WELCOME TO GAME===============\n {styles.GREEN})Play \n {styles.RED})Exit{styles.RESET}")

    while True:

        flag = ['Play' , "Exit"]
        try:
            user_choice = input(":::>>>>>> ").title()
        except Exception as e:
            print(e)

        if user_choice not in flag:
            print("Select one of the options")
        
        elif user_choice == 'Play':
            g = Game()
            g.character_selection()
            g.turn_system()
          

        
        else:
            print("Bye")
            break

if __name__ == "__main__":
    main()
