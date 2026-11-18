import random

def play_game():
    print("Welcome to the Number Guessing Game!")
    print("I have chosen a number between 1 and 50.")
    print("Try to guess it!")

    number = random.randint(1, 50)
    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess (1, 50): "))
            attempts += 1

            if guess < number:
                print("Too Low! Try again.")

            elif guess > number:
                print("Too High! Try again.")

            else:
                print(f"\nCongratulations! You guessed the number {number}!")
                print(f"You got it in {attempts} attempts.")
                break

        except ValueError:
            print("Please enter a valid number.")

    else:
        print(f"\nGame Over! The number was {number}.")


play_game()