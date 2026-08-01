import streamlit as st
import pandas as pd
import numpy as np
import json
import re
import os
import random

# --- Page Setup & Cool CSS Styling ---
st.set_page_config(page_title="Cyber Mystery Doors", page_icon="🚪", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0f111a;
        color: #00ffcc;
    }
    .door-btn {
        font-size: 20px !important;
        font-weight: bold;
    }
    .shop-card {
        background: #1a1c29;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00ffcc;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# --- 1. OOP & RegEx (Lesson Requirement) ---
class Player:
    def __init__(self, username):
        self.username = self.validate_username(username)

    @staticmethod
    def validate_username(name):
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


# --- 3. Audio Player Helper ---
def play_sound(sound_type):
    # Public domain retro game sounds
    sounds = {
        "win": "https://cdn.freesound.org/previews/274/274178_5123851-lq.mp3",
        "lose": "https://cdn.freesound.org/previews/331/331912_3248244-lq.mp3",
        "puzzle": "https://cdn.freesound.org/previews/320/320655_5260872-lq.mp3"
    }
    if sound_type in sounds:
        st.markdown(f'<audio autoplay hidden><source src="{sounds[sound_type]}" type="audio/mp3"></audio>', unsafe_allow_html=True)


# --- Session State Initialization ---
if 'points' not in st.session_state:
    st.session_state.points = 100
if 'has_shield' not in st.session_state:
    st.session_state.has_shield = False
if 'active_puzzle' not in st.session_state:
    st.session_state.active_puzzle = None
if 'revealed_empty' not in st.session_state:
    st.session_state.revealed_empty = None


# --- Game Header ---
st.title("🚪 CYBER MYSTERY DOORS 🎮")
st.caption("A Python game featuring OOP, RegEx, Pandas, NumPy, JSON, & Sound Effects!")

# --- Sidebar: Profile & Item Shop ---
st.sidebar.header("👤 Player Profile")
raw_name = st.sidebar.text_input("Username (3-12 alphanumeric):", "Player1")
player = Player(raw_name)
st.sidebar.write(f"Playing as: **{player.username}**")

st.sidebar.markdown("---")
st.sidebar.header("🛒 Power-Up Shop")
st.sidebar.write(f"💰 **Points Available:** `{st.session_state.points}`")

if st.sidebar.button("🛡️ Buy Ghost Shield (50 pts)"):
    if st.session_state.points >= 50:
        st.session_state.points -= 50
        st.session_state.has_shield = True
        st.sidebar.success("Shield Purchased! You are safe from the next ghost.")
    else:
        st.sidebar.error("Not enough points!")

if st.sidebar.button("🔮 Buy Oracle Glass (75 pts)"):
    if st.session_state.points >= 75:
        st.session_state.points -= 75
        st.session_state.revealed_empty = random.randint(1, 3)
        st.sidebar.success("Oracle Glass Activated! One trap door will be revealed.")
    else:
        st.sidebar.error("Not enough points!")

if st.session_state.has_shield:
    st.sidebar.info("🛡️ Ghost Shield Active")

# --- Game Setup ---
difficulty = st.radio("Choose Difficulty:", ["Easy (3 Doors)", "Medium (5 Doors)", "Hard (10 Doors)"], horizontal=True)
num_doors = 3 if "3" in difficulty else (5 if "5" in difficulty else 10)

if 'winning_door' not in st.session_state or st.session_state.get('last_num_doors') != num_doors:
    st.session_state.winning_door = int(np.random.randint(1, num_doors + 1))
    st.session_state.puzzle_door = int(np.random.randint(1, num_doors + 1))
    while st.session_state.puzzle_door == st.session_state.winning_door:
        st.session_state.puzzle_door = int(np.random.randint(1, num_doors + 1))
    st.session_state.last_num_doors = num_doors


# --- Render Active Brain Puzzle ---
if st.session_state.active_puzzle:
    st.warning("🧠 **BRAIN PUZZLE DOOR OPENED!** Solve this to win points!")
    p_data = st.session_state.active_puzzle
    user_ans = st.number_input(f"What is {p_data['num1']} + {p_data['num2']} x {p_data['num3']}?", value=0)
    
    if st.button("Submit Answer"):
        correct_ans = p_data['num1'] + (p_data['num2'] * p_data['num3'])
        if user_ans == correct_ans:
            st.session_state.points += 150
            play_sound("puzzle")
            st.success("🎉 Correct Answer! You earned +150 Points!")
            save_game_data(player.username, "PUZZLE_WIN", difficulty, st.session_state.points)
        else:
            play_sound("lose")
            st.error(f"❌ Wrong! The answer was {correct_ans}.")
        
        st.session_state.active_puzzle = None
        st.session_state.winning_door = int(np.random.randint(1, num_doors + 1))
        st.rerun()

# --- Render Doors ---
st.markdown("### Select a Door:")
cols = st.columns(min(num_doors, 5))

for i in range(num_doors):
    door_num = i + 1
    col_idx = i % 5
    
    label = f"🚪 Door {door_num}"
    if st.session_state.revealed_empty == door_num and door_num != st.session_state.winning_door:
        label = f"💀 TRAP Door {door_num}"

    if cols[col_idx].button(label, key=f"door_{door_num}"):
        if door_num == st.session_state.winning_door:
            # Treasure Door
            play_sound("win")
            st.balloons()
            st.session_state.points += 100
            st.success(f"🎉 **YOU FOUND THE TREASURE behind Door {door_num}!** (+100 Points)")
            save_game_data(player.username, "WIN", difficulty, st.session_state.points)
            st.session_state.winning_door = int(np.random.randint(1, num_doors + 1))
        
        elif door_num == st.session_state.puzzle_door:
            # Brain Puzzle Door
            st.session_state.active_puzzle = {
                "num1": int(np.random.randint(5, 20)),
                "num2": int(np.random.randint(2, 10)),
                "num3": int(np.random.randint(2, 5))
            }
            st.rerun()
            
        else:
            # Ghost Door
            if st.session_state.has_shield:
                st.session_state.has_shield = False
                st.info("🛡️ A Ghost jumped out, but your Shield protected your points!")
            else:
                play_sound("lose")
                st.session_state.points = max(0, st.session_state.points - 30)
                st.error(f"👻 **GHOST!** Door {door_num} was a trap! (-30 Points)")
                save_game_data(player.username, "LOSS", difficulty, st.session_state.points)
            
            st.session_state.winning_door = int(np.random.randint(1, num_doors + 1))


# --- 4. Pandas Analytics Table ---
st.markdown("---")
st.subheader("📊 Game History & Leaderboard (Pandas)")
history_data = load_game_data()

if history_data:
    df = pd.DataFrame(history_data)
    st.dataframe(df.tail(8), use_container_width=True)
else:
    st.info("No game history recorded yet. Open a door!")