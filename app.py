import streamlit as st
import pandas as pd
import numpy as np
import json
import re
import os
import random
import time

# --- Page Setup & Cyber Styling + Animations ---
st.set_page_config(page_title="Cyber Mystery Doors", page_icon="🚪", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #58a6ff;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
    }
    
    /* Ghost Pop-up Animation */
    .ghost-overlay {
        position: fixed;
        top: 30%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 150px;
        z-index: 9999;
        animation: ghostJump 1.8s ease-in-out forwards;
        text-shadow: 0 0 30px #ff0055, 0 0 60px #ff0055;
        pointer-events: none;
    }

    @keyframes ghostJump {
        0% { transform: translate(-50%, -50%) scale(0.2); opacity: 0; }
        40% { transform: translate(-50%, -50%) scale(1.3); opacity: 1; }
        70% { transform: translate(-50%, -60%) scale(1.1); opacity: 0.9; }
        100% { transform: translate(-50%, -70%) scale(0.5); opacity: 0; }
    }
    </style>
""", unsafe_allow_html=True)


# --- 1. OOP & RegEx (Lesson Requirements) ---
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

def save_game_data(username, result, mode, score):
    history = load_game_data()
    history.append({
        "Username": username,
        "Result": result,
        "Mode": mode,
        "Score": score
    })
    with open(JSON_FILE, "w") as f:
        json.dump(history, f, indent=4)


# --- 3. Audio & Ghost Animation Helpers ---
def play_sound(sound_type):
    sounds = {
        "win": "https://cdn.freesound.org/previews/274/274178_5123851-lq.mp3",
        "ghost_scary": "https://cdn.freesound.org/previews/145/145303_2615119-lq.mp3", # Scary ghost laugh sound
        "puzzle": "https://cdn.freesound.org/previews/320/320655_5260872-lq.mp3"
    }
    if sound_type in sounds:
        st.markdown(f'<audio autoplay hidden><source src="{sounds[sound_type]}" type="audio/mp3"></audio>', unsafe_allow_html=True)

def trigger_ghost_jumpscare():
    play_sound("ghost_scary")
    st.markdown('<div class="ghost-overlay">👻</div>', unsafe_allow_html=True)


# --- Session State Initialization ---
if 'points' not in st.session_state:
    st.session_state.points = 100
if 'has_shield' not in st.session_state:
    st.session_state.has_shield = False
if 'active_puzzle' not in st.session_state:
    st.session_state.active_puzzle = None


# --- Game Header ---
st.title("🚪 CYBER MYSTERY DOORS 🎮")
st.caption("Featuring Python OOP, RegEx, Pandas, NumPy, JSON, & Interactive Game Modes!")

# --- Sidebar: Profile & Item Shop ---
st.sidebar.header("👤 Player Profile")
raw_name = st.sidebar.text_input("Username (3-12 chars):", "Player1")
player = Player(raw_name)
st.sidebar.write(f"Playing as: **{player.username}**")

st.sidebar.markdown("---")
st.sidebar.header("🛒 Item Shop")
st.sidebar.write(f"💰 **Points Available:** `{st.session_state.points}`")

if st.sidebar.button("🛡️ Ghost Shield (50 pts)"):
    if st.session_state.points >= 50:
        st.session_state.points -= 50
        st.session_state.has_shield = True
        st.sidebar.success("Shield Active! Ghost loss blocked once.")
    else:
        st.sidebar.error("Not enough points!")

if st.session_state.has_shield:
    st.sidebar.info("🛡️ Shield Enabled")

# --- Game Mode Selector ---
st.markdown("---")
game_mode = st.selectbox(
    "🎮 Select Game Mode:",
    ["Standard Treasure Hunt", "🎁 Mystery Roulette (Surprise per Door)", "🏰 Boss Battle (3 Stages)"]
)

# Set door counts based on mode
if game_mode == "Standard Treasure Hunt":
    num_doors = 5
elif game_mode == "🎁 Mystery Roulette (Surprise per Door)":
    num_doors = 6
else:  # Boss Battle Mode
    num_doors = 8

if 'winning_door' not in st.session_state or st.session_state.get('last_mode') != game_mode:
    st.session_state.winning_door = int(np.random.randint(1, num_doors + 1))
    st.session_state.last_mode = game_mode


# --- Active Brain Puzzle Component ---
if st.session_state.active_puzzle:
    p = st.session_state.active_puzzle
    st.info(f"🧠 **PUZZLE CHALLENGE!** {p['type']}")
    
    if p['type'] == "Math Problem":
        ans = st.number_input(f"Solve: {p['n1']} + ({p['n2']} x {p['n3']})", value=0)
        expected = p['n1'] + (p['n2'] * p['n3'])
    else:  # Word Unscramble
        ans = st.text_input(f"Unscramble this Python word: **{p['scrambled']}**").lower().strip()
        expected = p['solution']

    if st.button("Submit Puzzle Answer"):
        if ans == expected:
            st.session_state.points += 150
            play_sound("puzzle")
            st.success("🎉 Correct! Earned +150 Points!")
            save_game_data(player.username, "PUZZLE_WIN", game_mode, st.session_state.points)
        else:
            trigger_ghost_jumpscare()
            st.error(f"❌ Incorrect! The answer was {expected}.")
        
        st.session_state.active_puzzle = None
        st.rerun()


# --- Render Doors ---
st.write(f"### Pick a Door ({num_doors} doors available):")
cols = st.columns(min(num_doors, 5))

words_list = ["python", "pandas", "numpy", "module", "string"]

for i in range(num_doors):
    door_num = i + 1
    col_idx = i % 5

    if cols[col_idx].button(f"🚪 Door {door_num}", key=f"door_{door_num}"):
        
        # Mode 1: Mystery Roulette
        if game_mode == "🎁 Mystery Roulette (Surprise per Door)":
            outcome = np.random.choice(["treasure", "ghost", "puzzle"], p=[0.3, 0.4, 0.3])
            
            if outcome == "treasure":
                play_sound("win")
                st.balloons()
                st.session_state.points += 100
                st.success(f"🏆 Door {door_num} had GOLD! (+100 pts)")
                save_game_data(player.username, "WIN", game_mode, st.session_state.points)
            elif outcome == "ghost":
                if st.session_state.has_shield:
                    st.session_state.has_shield = False
                    st.info("🛡️ Shield blocked the ghost!")
                else:
                    trigger_ghost_jumpscare()
                    st.session_state.points = max(0, st.session_state.points - 30)
                    st.error(f"👻 **EEK! A Ghost jumps out from Door {door_num}!** (-30 pts)")
                    save_game_data(player.username, "LOSS", game_mode, st.session_state.points)
            else:  # Trigger Puzzle
                word = random.choice(words_list)
                scrambled = "".join(random.sample(word, len(word)))
                st.session_state.active_puzzle = {
                    "type": "Word Unscramble",
                    "scrambled": scrambled,
                    "solution": word
                }
                st.rerun()

        # Mode 2 & 3: Standard & Boss Battle
        else:
            if door_num == st.session_state.winning_door:
                play_sound("win")
                st.balloons()
                mult = int(np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1]))
                pts = 100 * mult
                st.session_state.points += pts
                st.success(f"🎉 TREASURE FOUND behind Door {door_num}! (+{pts} pts)")
                save_game_data(player.username, "WIN", game_mode, st.session_state.points)
            else:
                if st.session_state.has_shield:
                    st.session_state.has_shield = False
                    st.info("🛡️ Shield saved your points!")
                else:
                    trigger_ghost_jumpscare()
                    st.session_state.points = max(0, st.session_state.points - 20)
                    st.error(f"👻 **EEK! A Ghost pops out of Door {door_num}!** Treasure was behind Door {st.session_state.winning_door}.")
                    save_game_data(player.username, "LOSS", game_mode, st.session_state.points)

            st.session_state.winning_door = int(np.random.randint(1, num_doors + 1))


# --- Pandas Game Analytics ---
st.markdown("---")
st.subheader("📊 Class Leaderboard & History (Pandas)")
history_data = load_game_data()

if history_data:
    df = pd.DataFrame(history_data)
    st.dataframe(df.tail(8), use_container_width=True)
else:
    st.info("No game history recorded yet.")