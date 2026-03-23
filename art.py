from colorama import Fore, Style

def show_victory_screen(hero_name, hp):
        print(Fore.YELLOW + "="*45)
        print(f"         🏆 MISSION ACCOMPLISHED 🏆          ")
        print("="*45)
        print(Fore.WHITE + r"""
             ___________
            '._==_==_=_.'
            .-\:      /-.
           | (|:.     |) |
            '-|:.     |-'
              \::.    /
               '::. .'
                 ) (
               _.' '._
              `-------`
    """)
        print(Fore.YELLOW + "="*45)
        print(f"  Congratulations, {hero_name}!")
        print(f"  Final Health: {hp}")
        print("  The town celebrates your name tonight!")
        print("="*45 + Style.RESET_ALL)
        input("\n[ Press Enter to Exit Game ]")

def show_game_over():
    print(Fore.RED + "\n" + "!" * 45)
    print("             YOU HAVE FALLEN                 ")
    print("!" * 45)
    print(Fore.WHITE + r"""
               __________
              /          \
             /    REST    \
            /      IN      \
           /     PEACE      \
          /                  \

          |   MORKS QUEST    |
          |                  |
          |   1337 - 2024    |
         \|__________________|/
    """)
    print(Fore.RED + "!" * 45)
    print("  Your journey ends here in the dark...")
    print("!" * 45 + Style.RESET_ALL)
    input("\n[ Press Enter to exit the game ]")