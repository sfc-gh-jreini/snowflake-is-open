import streamlit as st
import random

st.set_page_config(page_title="🧩 Match the Snowflake OSS Tool", layout="centered")

st.title("🔷 Match the Snowflake OSS Tool to What It Does")
st.markdown("Think you know your open source Snowflake stack? Match each project to its purpose!")

# Define correct matches
projects = {
    "TruLens": "🔍 Evaluations & tracing for LLM apps",
    "Apache Iceberg": "🧊 Open table format for huge analytics datasets",
    "Apache Polaris": "📚 Open metadata and data catalog system",
    "Arctic Embed": "🧠 Tiny but powerful embedding model",
    "Streamlit": "📱 Build and share beautiful data apps",
}

project_names = list(projects.keys())
project_descriptions = list(projects.values())

# Shuffle only once per session
if "shuffled_descriptions" not in st.session_state:
    st.session_state.shuffled_descriptions = random.sample(project_descriptions, len(project_descriptions))

st.markdown("### 🔁 Your Matches")
user_answers = {}

for name in project_names:
    user_answers[name] = st.selectbox(
        f"What does **{name}** do?",
        [""] + st.session_state.shuffled_descriptions,
        key=name
    )

if st.button("✅ Check My Matches"):
    correct = 0
    st.markdown("---")
    for name in project_names:
        user_choice = user_answers[name]
        correct_desc = projects[name]
        if user_choice == correct_desc:
            st.success(f"🎯 **{name}**: Correct!")
            correct += 1
        else:
            st.error(f"❌ **{name}**: Not quite! You picked: _{user_choice}_")
            st.info(f"👉 It actually does: **{correct_desc}**")

    st.markdown("---")
    if correct == len(projects):
        st.balloons()
        st.success("🔥 Perfect score! You really know your Snowflake OSS tools.")
    elif correct >= 3:
        st.success(f"👏 Not bad! You got {correct} out of {len(projects)} right.")
    else:
        st.warning(f"😅 Only {correct} correct. Want to try again?")

st.markdown("---")
st.caption("Made with ❤️ + Streamlit. Powered by Snowflake OSS 🔷")
