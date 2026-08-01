import streamlit as st
import pandas as pd
import numpy as np
import json
import re
import os

# --- 1. OOP & RegEx (Lesson Requirements) ---
class Player:
    """OOP Player Class with RegEx username validation."""
    def __init__(self, username):
        self.username = self.validate_username(username)

    @staticmethod
    def validate_username(name):
        # RegEx Metacharacters: ^ (start), [a-zA-Z0-9_] (alphanumeric/underscore), {3,12} (length), $ (end)
        pattern = r"^[a-zA-Z0-9_]{3,12}$"
        if re.match(pattern, name):
            return name
        return "Player1"


# --- 2. JSON Storage (Lesson Requirement) ---
JSON_FILE = "save_data.json"

def load_game_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    return []

def save_game_data(username, result, difficulty, score):
    history = load_game_data()
    history.append({
        "Username": username,
        "Result": result,
        "Difficulty": difficulty,
        "Score": score
    })
    with open(JSON_FILE, "w") as f:
        json.dump(history, f, indent=4)


# --- 3. Streamlit Web UI ---
st.set_page_config(page_title="Mystery Door Game", page_icon="🚪")

st.title("🚪 Mystery Door Game")
st.caption("Powered by Python, OOP, Pandas, NumPy, JSON, & RegEx!")

# Sidebar for User Settings & RegEx validation
st.sidebar.header("👤 Player Profile")
raw_name = st.sidebar.text_input("Username (3-12 characters):", "Player1")
player = Player(raw_name)

if player.username == "Player1" and raw_name != "Player1":
    st.sidebar.warning("⚠️ Invalid username format! Defaulting to 'Player1'. Use 3-12 letters/numbers.")
else:
    st.sidebar.success(f"Playing as: **{player.username}**")

# Difficulty selector
difficulty = st.sidebar.selectbox("Choose Difficulty:", ["Easy (3 Doors)", "Medium (5 Doors)", "Hard (10 Doors)"])
num_doors = 3 if "3" in difficulty else (5 if "5" in difficulty else 10)

# Initialize Session State
if 'winning_door' not in st.session_state or st.session_state.get('last_num_doors') != num_doors:
    st.session_state.winning_door = int(np.random.randint(1, num_doors + 1)) # NumPy
    st.session_state.last_num_doors = num_doors
    st.session_state.score = 0

st.write(f"### Pick a door to find the 🏆 treasure! (1 in {num_doors} chance)")

# --- Render Door Buttons ---
cols = st.columns(min(num_doors, 5)) # Dynamic columns layout

for i in range(num_doors):
    door_num = i + 1
    col_idx = i % 5
    
    if cols[col_idx].button(f"🚪 Door {door_num}", key=f"door_{door_num}"):
        if door_num == st.session_state.winning_door:
            # NumPy generated multiplier prize
            multiplier = int(np.random.choice([1, 2, 5], p=[0.6, 0.3, 0.1])) 
            points = 100 * multiplier
            st.session_state.score += points
            
            st.balloons()
            st.success(f"🎉 **YOU WIN!** Found the treasure behind Door {door_num}! (+{points} pts, Multiplier x{multiplier})")
            save_game_data(player.username, "WIN", difficulty, st.session_state.score)
        else:
            st.error(f"👻 **GHOST!** Door {door_num} was empty. The treasure was behind Door {st.session_state.winning_door}.")
            save_game_data(player.username, "LOSS", difficulty, st.session_state.score)
        
        # Reset winning door for next round
        st.session_state.winning_door = int(np.random.randint(1, num_doors + 1))

st.metric(label="Current Score", value=st.session_state.score)

# --- 4. Pandas Game Analytics (Lesson Requirement) ---
st.markdown("---")
st.subheader("📊 Class Analytics & History (Pandas)")

history_data = load_game_data()
if history_data:
    df = pd.DataFrame(history_data) # Pandas DataFrame
    st.dataframe(df.tail(10), use_container_width=True) # Display interactive table
    
    # Quick statistics summary using Pandas
    col1, col2 = st.columns(2)
    col1.metric("Total Games Played", len(df))
    wins_count = len(df[df['Result'] == 'WIN'])
    col2.metric("Total Wins", wins_count)
else:
    st.info("No game history recorded yet. Open a door to play!")
    