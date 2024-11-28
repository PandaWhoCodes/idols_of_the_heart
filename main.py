import streamlit as st
from anthropic import Anthropic

# Initialize Anthropic client
anthropic = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# List of questions and their helper text
questions = [
    {
        "question": "What one thing do you most hope is in your future?",
        "helper": "Career success? A certain salary? Owning your own home? Owning a second one at the beach? Getting married? Seeing your kids grow up to be successful? Having the respect of your teammates? Going pro? Being loved and respected by your colleagues? What is it that, without it, life would hardly seem worth living?"
    },
    {
        "question": "What is the one thing you most worry about losing?",
        "helper": "What one thing could you just absolutely not get along without? Your family? Your job? The love of your spouse? The respect of your kids?"
    },
    # {
    #     "question": "If you could change one thing about yourself right now, what would it be?",
    #     "helper": "Would you lose thirty pounds? Would you change your looks? Your marital status? Your job? Your zip code? Would you have your kids come home? There is certainly nothing wrong with desiring to change our lives. But when we could't imagine being happy unless something changes, we have an idol."
    # },
    # {
    #     "question": "What thing have you sacrificed the most for?",
    #     "helper": "Sacrifice and worship almost always go hand in hand. What have you worked the hardest for? To get the scholarship? To obtain the perfect body? To land the job? To be the best in your field? To get to a certain income level? What you prize most is shown by what you pursue the hardest."
    # },
    # {
    #     "question": "Who is there in your life that you feel like you can't forgive, and why?",
    #     "helper": "An ex-husband ruined your reputation and stole the best years of your life? Your wife who cheated on you and publicly humiliated you? An irresponsible or unethical partner who ruined your business? A close friend who stole your boyfriend? A drunk driver who killed your child? When you cannot forgive someone, it is usually because they took something from you that you depended on for life, happiness, and security."
    # },
    # {
    #     "question": "When do you feel the most significant?",
    #     "helper": "When do you hold your head up the highest? What is there that you hope people find out about you? Do you constantly mention your job, or the job you think you're going to have when you graduate, or where you got your degree from? Are you always looking for ways to show off your house or car? Your identity is whatever makes you feel the mist significant. What makes you feel the most significant is what you put the most weight upon."
    # },
    # {
    #     "question": "What triggers depression in you?",
    #     "helper": "That your kids never call? The fact that your marriage doesn't look like it's ever going to get better? Is it that you have reached a certain age and still aren't married?  Is it when you don't get the recognition you know you deserve? Is it how little you've accomplished? Depression is triggered when something we deemed essential for life and happiness is denied to us."
    # },
    # {
    #     "question": "Where do you turn for comfort when things are not going well?",
    #     "helper": "Maybe you bury yourself in your work to numb the fact that your wife ignores you and your kids are drifting away from you. Or perhaps you find escape in the arms of a lover. Some sensual pleasure, like pornography or comfort food? Perhaps alcohol or drugs?"
    # }
]

def init_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False

def get_idol_analysis(answers):
    prompt = f"""Based on these responses to questions about life priorities and values, identify potential idols (things that might be taking the place of God) in this person's heart. Be gentle but direct in your analysis.

Responses:
{answers}

Please provide a thoughtful analysis of potential idols, explaining why they might be idols and offering gentle, Biblical guidance for addressing them."""

    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=5000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content

def main():
    st.title("Heart Idol Analysis")
    st.write("Answer these questions honestly to help identify potential idols in your heart.")
    
    init_session_state()
    
    if st.session_state.current_question < len(questions):
        current_q = questions[st.session_state.current_question]
        
        st.subheader(current_q["question"])
        st.write(current_q["helper"])
        
        answer = st.text_area("Your answer:", key=f"q_{st.session_state.current_question}")
        
        if st.button("Next"):
            if answer:
                st.session_state.answers[current_q["question"]] = answer
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.warning("Please provide an answer before continuing.")
                
    elif not st.session_state.analysis_complete:
        formatted_answers = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.answers.items()])
        analysis = get_idol_analysis(formatted_answers)
        st.session_state.analysis = analysis
        st.session_state.analysis_complete = True
        st.rerun()
        
    else:
        st.subheader("Analysis of Potential Heart Idols")
        st.write(st.session_state.analysis)
        
        if st.button("Start Over"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()