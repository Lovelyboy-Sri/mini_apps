import streamlit as st

# Initialize session state
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.word = ""
    st.session_state.word_length = 0
    st.session_state.guessed_word = []
    st.session_state.incorrect_guesses = 0
    st.session_state.used_letters = set()
    st.session_state.letter_index = 0
    st.session_state.letter_frequency = list("etaoinshrdlcumwfgypbvkjxqz")
    st.session_state.log = []

def get_figure_parts():
    return [
        "   ---|---   ",   # 1. Hanger
        "     O      ",    # 2. Head
        "    /|\\     ",   # 3. Arms and torso
        "   `| <== Gun ( Loaded )     ",   # 4. Gun/lever
        "    / \\     ",   # 5. Legs
        "  --------- "    # 6. Feet
    ]

def draw_figure(incorrect):
    parts = get_figure_parts()[:incorrect]
    return "\n".join(parts) + "\n" + "-" * 15

# UI Title
st.title("🔁 Reverse Hangman (Streamlit Edition)")

# Game Setup
if not st.session_state.game_started:
    st.info("Think of a word and enter it below. The app will try to guess it!")
    word_input = st.text_input("Enter your secret word (won't be shown):", type="password")
    if st.button("Start Game") and word_input:
        st.session_state.word = word_input.lower()
        st.session_state.word_length = len(word_input)
        st.session_state.guessed_word = ["_"] * st.session_state.word_length
        st.session_state.max_incorrect_guesses = min(len(word_input) + 2, len(get_figure_parts()))
        st.session_state.game_started = True
        st.rerun()

# Game In Progress
elif st.session_state.game_started and "_" in st.session_state.guessed_word and st.session_state.incorrect_guesses < st.session_state.max_incorrect_guesses:
    # Get next unused guess
    while (st.session_state.letter_index < len(st.session_state.letter_frequency) and
           st.session_state.letter_frequency[st.session_state.letter_index] in st.session_state.used_letters):
        st.session_state.letter_index += 1

    if st.session_state.letter_index >= len(st.session_state.letter_frequency):
        st.warning("I've run out of letters to guess!")
        st.session_state.game_started = False
    else:
        guess = st.session_state.letter_frequency[st.session_state.letter_index]
        st.session_state.used_letters.add(guess)
        st.session_state.letter_index += 1

        indices = [i for i, c in enumerate(st.session_state.word) if c == guess]

        st.write(draw_figure(st.session_state.incorrect_guesses))
        st.write(f"🔠 My guess: **{guess}**")
        st.write("Current guessed word: " + " ".join(st.session_state.guessed_word))

        if indices:
            for pos in indices:
                st.session_state.guessed_word[pos] = guess
            st.success(f"✅ '{guess}' is in the word at positions: {indices}")
            st.session_state.log.append(f"Guess: {guess} → Correct at {indices}")
        else:
            st.session_state.incorrect_guesses += 1
            st.error(f"❌ '{guess}' is not in the word.")
            st.session_state.log.append(f"Guess: {guess} → Incorrect")

        st.button("Next Guess", on_click=st.rerun)

# Game Over
elif st.session_state.game_started:
    st.write(draw_figure(st.session_state.incorrect_guesses))
    st.write("Final Word: " + " ".join(st.session_state.guessed_word))

    if "_" not in st.session_state.guessed_word:
        st.success("🎉 I guessed your word!")
    else:
        st.error("😈 You outsmarted me!")

    st.download_button("📥 Download Log", data="\n".join(st.session_state.log), file_name="reverse_hangman_log.txt")
    
    if st.button("Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
