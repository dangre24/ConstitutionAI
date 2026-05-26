import streamlit as st
from openai import OpenAI
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="ConstitutionAI", page_icon="⚖️", layout="wide")

st.markdown("""
<script>
const streamlitDoc = window.parent.document;

const observer = new MutationObserver(() => {

    const darkModeButton = streamlitDoc.querySelector('[title="Settings"]');

    // Force dark theme background
    streamlitDoc.body.style.backgroundColor = "#0b0b0f";

    // Force app background
    const app = streamlitDoc.querySelector('.stApp');
    if (app) {
        app.style.background = "#0b0b0f";
    }
});

observer.observe(streamlitDoc, {
    childList: true,
    subtree: true
});
</script>
""", unsafe_allow_html=True)

client = OpenAI()

def load_lottie_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

law_animation = load_lottie_file("justice_animation.json")

st.markdown("""
<style>

/* App background */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(120, 72, 32, 0.25), transparent 35%),
        linear-gradient(135deg, #0b0b0f 0%, #111117 45%, #1b1612 100%);
    color: #f5f1ea !important;
}

/* Force Streamlit text to stay visible */
html, body, [class*="css"], label, p, span, div {
    color: #f5f1ea !important;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 68px;
    font-weight: 800;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #d6b36a, #f5deb3, #9f6b32);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.sub-title {
    text-align: center;
    font-size: 24px;
    color: #cfc3ad !important;
    margin-bottom: 35px;
}

/* Warning box */
[data-testid="stAlert"] {
    background-color: rgba(92, 73, 25, 0.85) !important;
    border: 1px solid rgba(214,179,106,0.45) !important;
    border-radius: 16px !important;
}

[data-testid="stAlert"] * {
    color: #fff4cf !important;
    font-size: 20px !important;
}

/* Text area label */
[data-testid="stTextArea"] label,
[data-testid="stTextArea"] label * {
    color: #ffffff !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}

/* Text area box */
[data-testid="stTextArea"] textarea {
    background-color: rgba(20, 20, 28, 0.96) !important;
    color: #ffffff !important;
    border-radius: 18px !important;
    border: 1px solid rgba(214,179,106,0.35) !important;
    font-size: 22px !important;
}

/* Placeholder text */
[data-testid="stTextArea"] textarea::placeholder {
    color: #b8b0a3 !important;
    opacity: 1 !important;
}

/* Analysis box */
.analysis-box {
    background: linear-gradient(145deg, rgba(28,28,36,0.96), rgba(16,16,22,0.96));
    padding: 35px;
    border-radius: 24px;
    border: 1px solid rgba(214,179,106,0.22);
    box-shadow: 0 8px 40px rgba(0,0,0,0.45);
    font-size: 20px;
    line-height: 1.75;
    margin-top: 20px;
    color: #f5f1ea !important;
}

.analysis-box * {
    color: #f5f1ea !important;
}

/* Analysis headings */
.analysis-box h1,
.analysis-box h2,
.analysis-box h3 {
    font-size: 34px;
    color: #e7c98a !important;
    margin-top: 35px;
    margin-bottom: 18px;
    border-left: 4px solid rgba(214,179,106,0.55);
    padding-left: 14px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7a4b20, #b88442) !important;
    color: white !important;
    border-radius: 14px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    padding: 14px 28px !important;
    border: none !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #b88442, #e0b36f) !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚖️ ConstitutionAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Search, Seizure & Civil Rights Simulator</div>', unsafe_allow_html=True)

st.warning("This application is for educational purposes only and is NOT legal advice.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "initial_response" not in st.session_state:
    st.session_state.initial_response = ""

if "followup_response" not in st.session_state:
    st.session_state.followup_response = ""

scenario = st.text_area(
    "Enter a police/legal scenario:",
    placeholder="Example: I was pulled over. The officer searched my backpack without asking.",
    height=220
)

if st.button("Analyze Scenario"):

    if not scenario.strip():
        st.error("Please enter a scenario first.")

    else:
        st.session_state.conversation = [
            {"role": "user", "content": scenario}
        ]

        initial_prompt = f"""
You are an educational constitutional law assistant.

This is NOT legal advice.

Analyze the scenario in a SHORT, clear way.

User scenario:
{scenario}

Use this exact format:

# Sneaky Things To Look Out For
- Give 3-5 subtle legal red flags.

# Rights Potentially Involved
- Briefly mention any amendments that could be of use for the user to have knowledge of.

# Quick Analysis
- Give a concise search/seizure, Miranda, arrest, or due process analysis.

# Summary
- Give a short 2-4 sentence summary.

# Follow-Up Questions
Ask 5 specific questions that best fit this exact situation.
Only ask relevant questions.
"""

        with st.spinner("Analyzing scenario..."):
            bottom_animation = st.empty()

            with bottom_animation.container():
                st_lottie(
                    law_animation,
                    height=180,
                    key="loading_animation_initial"
                )

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=initial_prompt
            )

            bottom_animation.empty()

        st.session_state.initial_response = response.output_text

if st.session_state.initial_response:

    st.subheader("Initial Constitutional Analysis")

    st.markdown(
        f'<div class="analysis-box">{st.session_state.initial_response}</div>',
        unsafe_allow_html=True
    )


# ---------------- SHOW FOLLOW-UP RESPONSE ----------------

if st.session_state.followup_response:

    st.subheader("Continued Constitutional Analysis")

    st.markdown(
        f'<div class="analysis-box">{st.session_state.followup_response}</div>',
        unsafe_allow_html=True
    )

# ---------------- FOLLOW-UP INPUT AT BOTTOM ----------------

if st.session_state.initial_response:

    st.divider()

    followup_input = st.text_area(
        "Answer the follow-up questions or add more details:",
        height=220,
        placeholder="Answer the AI's follow-up questions here..."
    )

    if st.button("Submit Follow Up"):

        if not followup_input.strip():

            st.error("Please enter a response.")

        else:

            st.session_state.conversation.append(
                {"role": "user", "content": followup_input}
            )

            conversation_text = "\n\n".join(
                [
                    f"{m['role'].upper()}: {m['content']}"
                    for m in st.session_state.conversation
                ]
            )

            followup_prompt = f"""
You are continuing an educational constitutional law discussion.

This is NOT legal advice.

Conversation:
{conversation_text}

Keep the response SHORT and clear.

Use this exact format:

# Updated Analysis
- Briefly explain what the new details change.

# Sneaky Things To Look Out For
- Give 3-5 new or updated red flags.

# Strongest Arguments
- Individual:
- Law enforcement:

# Summary
- Give a short 2-4 sentence conclusion.

# Next Follow-Up Questions
Ask 5 relevant follow-up questions based only on what still needs clarification.
"""

            with st.spinner("Generating response..."):

                bottom_animation = st.empty()

                with bottom_animation.container():

                    st_lottie(
                        law_animation,
                        height=180,
                        key="loading_animation_followup"
                    )

                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=followup_prompt
                )

                bottom_animation.empty()

            st.session_state.followup_response = response.output_text

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "ConstitutionAI is an educational legal-tech simulator for constitutional law, police encounters, and civil rights analysis."
)        

# Run with:
# streamlit run app.py