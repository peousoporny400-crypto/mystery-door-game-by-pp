import random

def play_game():
    print("========================================")
    print("Welcome to the Mystery Door Game!")
    print("========================================")
    print("In front of you are 3 mystery doors: [1]  [2]  [3]")
    
    # Randomly select which door has the winning prize
    winning_door = random.randint(1, 3)
    
    # Get user input
    try:
        player_choice = int(input("\nWhich door do you choose to open? (1, 2, or 3): "))
    except ValueError:
        print("Invalid input! You must enter a number.")
        return

    # Check winning condition
    if player_choice < 1 or player_choice > 3:
        print("That door doesn't exist!")
    elif player_choice == winning_door:
        print(f"\n🎉 Door {player_choice} opens... YOU FOUND THE TREASURE! You win!")
    else:
        print(f"\n👻 Door {player_choice} opens... A ghost jumps out! Game over.")
        print(f"The treasure was behind Door {winning_door}.")

# Game Loop
if __name__ == "__main__":
    while True:
        play_game()
        replay = input("\nDo you want to play again? (y/n): ").strip().lower()
        if replay != 'y':
            print("Thanks for playing!")
            break