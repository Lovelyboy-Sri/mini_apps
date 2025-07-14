import streamlit as st

# ---------- Game Setup ----------
def get_figure_parts():
    return [
        "   ---|---   ",
        "     O      ",
        "    /|\\     ",
        "     | <== Gun ( Loaded )     ",
        "    / \\     ",
        "  --------- "
    ]

def draw_figure(incorrect):
    parts = get_figure_parts()[:incorrect]
    return "\n".join(parts) + "\n" + "-" * 15

# ---------- Initialize session state ----------
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

# ---------- UI Title ----------
st.title("🤖 Reverse Hangman (Auto Mode)")

# ---------- Get Word from User ----------
if not st.session_state.game_started:
    st.info("Think of a word and enter it below. The app will try to guess it automatically!")
    word_input = st.text_input("Enter your secret word (won't be shown):", type="password")
    if st.button("Start Game") and word_input:
        word = word_input.strip().lower()
        st.session_state.word = word
        st.session_state.word_length = len(word)
        st.session_state.guessed_word = ["_"] * st.session_state.word_length
        st.session_state.max_incorrect_guesses = min(len(word) + 2, len(get_figure_parts()))
        st.session_state.game_started = True
        st.rerun()

# ---------- Game Logic (Auto Run) ----------
elif st.session_state.game_started:
    word = st.session_state.word
    guessed_word = st.session_state.guessed_word
    max_incorrect = st.session_state.max_incorrect_guesses
    log = st.session_state.log

    # Loop automatically until game ends
    while "_" in guessed_word and st.session_state.incorrect_guesses < max_incorrect:
        # Get next unused letter
        while (st.session_state.letter_index < len(st.session_state.letter_frequency) and
               st.session_state.letter_frequency[st.session_state.letter_index] in st.session_state.used_letters):
            st.session_state.letter_index += 1

        if st.session_state.letter_index >= len(st.session_state.letter_frequency):
            log.append("Ran out of letters to guess.")
            break

        guess = st.session_state.letter_frequency[st.session_state.letter_index]
        st.session_state.used_letters.add(guess)
        st.session_state.letter_index += 1

        indices = [i for i, c in enumerate(word) if c == guess]

        if indices:
            for pos in indices:
                guessed_word[pos] = guess
            log.append(f"✅ Guess '{guess}' → Correct at positions {indices}")
        else:
            st.session_state.incorrect_guesses += 1
            log.append(f"❌ Guess '{guess}' → Incorrect")

    # ---------- Final Results ----------
    st.code(draw_figure(st.session_state.incorrect_guesses), language="text")
    st.write("📌 Final Word: `" + "".join(guessed_word) + "`")
    st.write("🔡 Word State: " + " ".join(guessed_word))
    st.write(f"❗ Incorrect Guesses: {st.session_state.incorrect_guesses} / {max_incorrect}")

    if "_" not in guessed_word:
        st.success("🎉 I guessed your word!")
    else:
        st.error("😈 You outsmarted me!")

    lg_btn, play_btn = st.columns([1,1])
    lg_btn.download_button("📥 Download Log", data="\n".join(log), file_name="reverse_hangman_log.txt")

    if play_btn.button("🔁 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
