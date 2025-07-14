import terminal_game, random
import streamlit as st
from reverse_logic import run_game


st.title("🔀 Reverse Hangman Game")

# Initialize session state if not already done
if "game_mode" not in st.session_state:
    st.session_state.game_mode = None

col1, col2 = st.columns([1, 1])
start_game = col1.button("Start Game")
show_instructions = col2.button("Instructions")

# Handle "Start Game" button
if start_game:
    st.session_state.game_mode = "select_mode"


# Handle "Instructions" button
if show_instructions:
    st.session_state.game_mode = "instructions"


# Handle mode selection
if st.session_state.game_mode == "select_mode":
    st.write("Select how you want to play the game:")
    opt1, opt2 = st.columns([1, 1])

    if opt1.button("Random word from .txt file"):
        st.session_state.game_mode = "file_mode"

    if opt2.button("Think of a word yourself"):
        st.session_state.game_mode = "manual_mode"


# File input mode
if st.session_state.game_mode == "file_mode":
    uploaded_file = st.file_uploader("Choose a .txt file", type="txt")

    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        words = content.splitlines()

        # ✅ Store random word only once
        if "selected_word" not in st.session_state:
            st.session_state.selected_word = random.choice(words)

        st.subheader("File Content:")
        st.text(words)
        st.markdown("</br>", unsafe_allow_html=True)
        st.write(f"Randomly selected word is: **{st.session_state.selected_word}**")

        # ✅ Use the stored word
        run_game(st.session_state.selected_word)

# Manual word guess mode 
if st.session_state.game_mode == "manual_mode":
    st.info("Enter a word and its length. The input is hidden so others can't see it.")
    user_word = st.text_input("Enter your secret word:", type="password")
    if user_word:
        st.session_state.user_word = user_word
        run_game(user_word)

        # You can now pass this to your game logic
        # Example: terminal_game.play_with_manual_word(user_word)

    else:
        st.warning("Please enter a word to continue.")


# Instructions mode
if st.session_state.game_mode == "instructions":
    st.markdown("""
    ### Instructions:
    - Choose a game mode: upload a `.txt` file with words or think of a word yourself.
    - The computer will try to guess your word.
    - For file input, ensure one word per line.
    """)

