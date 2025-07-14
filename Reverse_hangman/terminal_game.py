import random

def get_figure_parts():
    return [
        "   ---|---   ",   # 1. Hanger
        "     O      ",    # 2. Head
        "    /|\\     ",   # 3. Arms and torso
        "     | <== Gun ( Loaded )     ",    # 4. Gun/lever
        "    / \\     ",   # 5. Legs
        "  --------- "    # 6. Feet
    ]

def draw_figure(incorrect, max_parts):
    figure_parts = get_figure_parts()
    print("\nCharacter Progress:")
    for i in range(incorrect):
        if i < len(figure_parts):
            print(figure_parts[i])
    print("-" * 15)


def reverse_hangman():
    print("Welcome to Reverse Hangman!")
    print("Think of a word and I'll try to guess it. Don't tell me the word!")

    word_length = int(input("Enter the length of your word: "))
    guessed_word = ['_'] * word_length
    print("Your word looks like this:", ' '.join(guessed_word))

    figure_parts = get_figure_parts()
    max_incorrect_guesses = min(word_length + 2, len(figure_parts))

    # Smarter letter frequency order
    letter_frequency = list("etaoinshrdlcumwfgypbvkjxqz")
    
    used_letters = set()  # Track guessed letters to avoid repeats
    incorrect_guesses = 0
    letter_index = 0

    while incorrect_guesses < max_incorrect_guesses and '_' in guessed_word:
        print(f"\nIncorrect guesses left: {max_incorrect_guesses - incorrect_guesses}")
        draw_figure(incorrect_guesses, max_incorrect_guesses)
        print("Current guessed word:", ' '.join(guessed_word))
        
        # Get the next unused letter
        while letter_index < len(letter_frequency) and letter_frequency[letter_index] in used_letters:
            letter_index += 1

        if letter_index >= len(letter_frequency):
            print("I've run out of letters to guess!")
            break

        guess = letter_frequency[letter_index]
        used_letters.add(guess)

        print(f"My guess is: {guess}")
        response = input(f"Is '{guess}' in your word? (yes/no): ").strip().lower()

        if response == 'yes':
            positions_input = input(f"Enter all positions where '{guess}' appears (e.g., 0 2 4): ").strip()
            
            raw_parts = positions_input.split()
            positions = set() 

            for part in raw_parts:
                if part.isdigit():
                    pos = int(part)
                    if 0 <= pos < word_length:
                        positions.add(pos)
                    else:
                        print(f"⚠️ Position {pos} is out of range (0 to {word_length - 1}). Ignored.")
                else:
                    print(f"⚠️ '{part}' is not a valid number. Ignored.")

            if not positions:
                print("⚠️ No valid positions entered. Try to be accurate next time.")
            else:
                for pos in positions:
                    guessed_word[pos] = guess

        elif response == 'no':
            incorrect_guesses += 1
            print("Wrong guess. Adding to the figure...")

        else:
            print("⚠️ Please answer with 'yes' or 'no'. No changes made.")


    draw_figure(incorrect_guesses, max_incorrect_guesses)
    
    if '_' not in guessed_word:
        print("\n🎉 I guessed your word! It was:", ''.join(guessed_word))
    else:
        print("\n😈 You outsmarted me! I couldn't guess your word.")
        print("What I had:", ''.join(guessed_word))