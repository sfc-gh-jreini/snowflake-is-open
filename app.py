import streamlit as st
import random
import time
import snowflake.connector
import os

st.set_page_config(page_title="🧩 Match the Snowflake OSS Tool", layout="centered")

st.title("🔷 Match the Snowflake OSS Tool to What It Does")
st.markdown("Think you know your open source Snowflake stack? Match each project to its purpose!")

# --- Start Screen: Enter Name and Start Quiz ---
if not st.session_state.get("quiz_started", False):
    user_name = st.text_input("Enter your name:")
    if st.button("Start Quiz") and user_name:
        st.session_state['quiz_started'] = True
        st.session_state['user_name'] = user_name
        st.session_state['start_time'] = time.time()
        # Ensure that the score is recorded only once per quiz
        st.session_state.pop("score_submitted", None)
        st.rerun()
    st.stop()

# --- Quiz Code ---
# Add the reset quiz button
if st.button("🔄 Reset Quiz"):
    st.session_state.clear()
    st.rerun()

# Define correct matches
projects = {
    "TruLens": "🔍 Evaluations & tracing for LLM apps",
    "Apache Iceberg": "🧊 Open table format for huge analytics datasets",
    "Apache Polaris": "📚 Open metadata and data catalog system",
    "Arctic Embed": "🧠 Tiny but powerful embedding model",
    "Streamlit": "📱 Build and share beautiful data apps",
    "ArcticTraining": "🏋️ Simplify LLM training experiments"
}

project_names = list(projects.keys())
project_descriptions = list(projects.values())

# Shuffle project descriptions only once per session
if "shuffled_descriptions" not in st.session_state:
    st.session_state.shuffled_descriptions = random.sample(project_descriptions, len(project_descriptions))

# Shuffle project order only once per session
if "shuffled_names" not in st.session_state:
    st.session_state.shuffled_names = random.sample(project_names, len(project_names))

st.markdown("### 🔁 Your Matches")
user_answers = {}

# Use the shuffled order for projects
for name in st.session_state.shuffled_names:
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

    # Record the quiz end time and calculate duration
    end_time = time.time()
    duration = end_time - st.session_state.start_time

    # Establish a connection to Snowflake (update details as needed)
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"), 
        password=os.getenv("SNOWFLAKE_PASSWORD"), 
        account=os.getenv("SNOWFLAKE_ACCOUNT"), 
        warehouse="COMPUTE_WH", 
        database="OPEN_SNOW", 
        schema="PUBLIC"
    )
    cursor = conn.cursor()

    # At the end of the quiz, insert the result into the Snowflake table
    if "score_submitted" not in st.session_state:
        insert_query = """
            INSERT INTO leaderboard_table (user_name, correct, duration) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (st.session_state.user_name, correct, f"{duration:.2f}"))
        st.session_state["score_submitted"] = True

# --- Leaderboard Display in Sidebar ---
with st.sidebar:
    st.markdown("## Leaderboard")
    # Read leaderboard from Snowflake, ordered by score descending, then duration ascending
    select_query = """
        SELECT user_name, correct, duration 
        FROM leaderboard_table 
        ORDER BY correct DESC, duration ASC
    """
    cursor.execute(select_query)
    leaderboard = cursor.fetchall()
    if leaderboard:
        for row in leaderboard:
            st.write(f"Name: **{row[0]}**, Score: **{row[1]}/{len(projects)}**, Time: **{row[2]} seconds**")
    else:
        st.info("No leaderboard data yet.")

st.markdown("---")
st.caption("Made with ❤️ + Streamlit. Powered by Snowflake OSS 🔷")
