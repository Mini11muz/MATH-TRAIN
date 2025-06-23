import streamlit as st
import random

# Feedback options
revision_feedback = {
    "correct": [
        "Nice work! Keep it up. 💪",
        "That's spot on! You're getting better.",
        "Correct! Great focus there.",
        "That's the spirit! You're on a roll!",
        "Brilliant! You're mastering this!",
        "You nailed it—math power activated! ✨",
    ],
    "wrong": [
        "That's okay, just keep practicing. 🌱",
        "Oops! Don't worry—mistakes help us learn.",
        "Not quite, but you're on the right track!",
        "No worries—each mistake is a step forward. 🧗",
        "Try again—you’re closer than you think!",
    ]
}

def get_random_feedback(result):
    return random.choice(revision_feedback[result])

def get_nums(diff, operation):
    ranges = {
        "easy": (0, 100), "medium": (100, 1000),
        "hard": (1000, 10000), "challenging": (10000, 100000)
    }
    if operation in ["division", "multiplication"]:
        ranges = {
            "easy": (1, 25), "medium": (25, 100),
            "hard": (100, 250), "challenging": (250, 500)
        }
    return ranges.get(diff, (0, 100))

def ask_question(num1, num2, operation):
    if operation == "addition":
        return num1, num2, num1 + num2, "+"
    elif operation == "subtraction":
        return num1, num2, num1 - num2, "-"
    elif operation == "multiplication":
        return num1, num2, num1 * num2, "×"
    elif operation == "division":
        num2 = max(1, num2)
        num1 = num1 * num2
        return num1, num2, num1 / num2, "÷"
    else:
        return None, None, None, ""

def main():
    st.title("🧠 Math Trainer")
    st.write("Practice your mental math with feedback and scoring!")

    mode = st.selectbox("Choose Game Mode", ["Revision"])
    operation = st.selectbox("Select Operation", ["addition", "subtraction", "multiplication", "division"])
    difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard", "challenging"])

    min_num, max_num = get_nums(difficulty, operation)

    # Session state setup
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "new_question" not in st.session_state:
        st.session_state.new_question = True

    if st.session_state.new_question or "answer" not in st.session_state:
        num1 = random.randint(min_num, max_num)
        num2 = random.randint(min_num, max_num)
        st.session_state.num1, st.session_state.num2, st.session_state.answer, st.session_state.symbol = ask_question(num1, num2, operation)
        st.session_state.new_question = False

    st.markdown(f"### What is {st.session_state.num1} {st.session_state.symbol} {st.session_state.num2}?")
    user_input = st.text_input("Your answer", key="user_input")

    if st.button("Submit"):
        try:
            guess = float(user_input)
            if abs(guess - st.session_state.answer) < 0.001:
                st.success(get_random_feedback("correct"))
                st.session_state.score += 1
            else:
                st.error(f"The answer was {st.session_state.answer}")
                st.info(get_random_feedback("wrong"))

            st.session_state.new_question = True
            st.experimental_rerun()  # Optional: remove this line if automatic rerun from state is working well

        except ValueError:
            st.warning("Please enter a valid number.")

    st.markdown(f"### 🧮 Score: {st.session_state.score}")

if __name__ == "__main__":
    main()
