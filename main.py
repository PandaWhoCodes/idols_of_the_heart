import streamlit as st
from anthropic import Anthropic

# Initialize Anthropic client
anthropic = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTitle {
        color: #2c3e50;
        font-family: 'Crimson Text', serif;
        text-align: center;
        font-size: 3em !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 2em;
    }
    .stSubheader {
        color: #34495e;
        font-family: 'Crimson Text', serif;
        font-size: 1.8em !important;
    }
    .helper-text {
        font-style: italic;
        color: #666;
        font-size: 0.9em;
        background-color: #f9f9f9;
        padding: 1em;
        border-left: 3px solid #7f8c8d;
        margin: 1em 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# List of questions and their helper text
questions = [
    {
        "question": "What one thing do you most hope is in your future?",
        "helper": "Examples to consider (these are just prompts, please share your own honest answer):\n\n"
        "• Career success\n• A certain salary\n• Owning your own home\n"
        "• Getting married\n• Seeing your children succeed\n"
        "• Having respect from peers\n• Professional achievement\n\n"
        "What is it that, without it, life would hardly seem worth living?",
    },
    {
        "question": "What is the one thing you most worry about losing?",
        "helper": "What one thing could you just absolutely not get along without? Your family? Your job? The love of your spouse? The respect of your kids?",
    },
    {
        "question": "If you could change one thing about yourself right now, what would it be?",
        "helper": "Would you lose thirty pounds? Would you change your looks? Your marital status? Your job? Your zip code? Would you have your kids come home?",
    },
    {
        "question": "What thing have you sacrificed the most for?",
        "helper": "What have you worked the hardest for? To get the scholarship? To obtain the perfect body? To land the job? To be the best in your field? To get to a certain income level? What you prize most is shown by what you pursue the hardest.",
    },
    {
        "question": "Who is there in your life that you feel like you can't forgive, and why?",
        "helper": "An ex-husband ruined your reputation and stole the best years of your life? An irresponsible or unethical partner who ruined your business? A close friend who stole your boyfriend?",
    },
    {
        "question": "When do you feel the most significant?",
        "helper": "When do you hold your head up the highest? What is there that you hope people find out about you? Do you constantly mention your job, or the job you think you're going to have when you graduate, or where you got your degree from? Your identity is whatever makes you feel the most significant. What makes you feel the most significant is what you put the most weight upon.",
    },
    {
        "question": "What triggers depression in you?",
        "helper": "Depression is triggered when something we deemed essential for life and happiness is denied to us.",
    },
    {
        "question": "Where do you turn for comfort when things are not going well?",
        "helper": "Maybe you bury yourself in your work to numb the fact that your wife ignores you and your kids are drifting away from you. Or perhaps you find escape in the arms of a lover. Some sensual pleasure, like pornography or comfort food? Perhaps alcohol or drugs?",
    },
]


def init_session_state(restart=False):
    if "current_question" not in st.session_state or not restart:
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.analysis_complete = False
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False


def get_idol_analysis(answers):
    prompt = f"""Based on these responses to questions about life priorities and values, identify potential idols (things that might be taking the place of God) in this person's heart. Be gentle but direct in your analysis.

Responses:
{answers}

Please provide a thoughtful analysis of potential idols, explaining why they might be idols and offering gentle, Biblical guidance for addressing them."""

    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=5000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content


def main():
    st.title("✨ Idols of the heart 💖")
    st.markdown(
        """
        <div style='text-align: center; font-style: italic; margin-bottom: 2em;'>
        "Search me, O God, and know my heart; test me and know my anxious thoughts." - Psalm 139:23
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize session state only if not already initialized
    if "current_question" not in st.session_state:
        init_session_state()

    if st.session_state.current_question < len(questions):
        current_q = questions[st.session_state.current_question]

        st.subheader(
            f"Question {st.session_state.current_question + 1} of {len(questions)}"
        )
        st.markdown(f"### {current_q['question']}")

        # Display helper text in a distinct format
        st.markdown(
            f"""
            <div class='helper-text'>
            {current_q['helper']}
            </div>
        """,
            unsafe_allow_html=True,
        )

        answer = st.text_area(
            "Your reflection:", key=f"answer_{st.session_state.current_question}"
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "Continue →",
                key=f"button_{st.session_state.current_question}",
            ):
                if answer:
                    st.session_state.answers[current_q["question"]] = answer
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.warning("Please share your reflection before continuing.")

    elif not st.session_state.analysis_complete:
        with st.spinner("Preparing spiritual insights..."):
            formatted_answers = "\n\n".join(
                [f"Q: {q}\nA: {a}" for q, a in st.session_state.answers.items()]
            )
            analysis = get_idol_analysis(formatted_answers)
            st.session_state.analysis = analysis
            st.session_state.analysis_complete = True
            st.rerun()

    else:
        st.markdown("### 🕊️ Your idols of the heart are 🕊️")

        analysis_text = str(st.session_state.analysis)
        analysis_text = analysis_text.replace("TextBlock(text='", "")
        analysis_text = analysis_text.replace("', type='text')", "")
        analysis_text = analysis_text.replace("\\n", "\n")
        analysis_text = analysis_text.replace("\\'", "'")
        paragraphs = [p.strip() for p in analysis_text.split("\n\n") if p.strip()]
        for i, paragraph in enumerate(paragraphs):
            st.write(paragraph)
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start again", key="start_over"):
                st.session_state.clear()
                st.rerun()


if __name__ == "__main__":
    main()
