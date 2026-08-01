import streamlit as st
import pandas as pd
import numpy as np
import json
import re
import os
import random

# --- Page Setup & Cyber Arcade Styling ---
st.set_page_config(page_title="Cyber Mystery Doors", page_icon="🚪", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #00ffcc;
    }
    
    /* Ghost Animation */
    .ghost-overlay {
        position: fixed;
        top: 30%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 140px;
        z-index: 9999;
        animation: ghostJump 1.5s ease-in-out forwards;
        text-shadow: 0 0 30px #ff0055, 0 0 60px #ff0055;
        pointer-events: none;
    }

    @keyframes ghostJump {
        0% { transform: translate(-50%, -50%) scale(0.1); opacity: 0; }
        50% { transform: translate(-50%, -50%) scale(1.3); opacity: 1; }
        100% { transform: translate(-50%, -70%) scale(0.3); opacity: 0; }
    }
    
    /* Neon Door Buttons */
    .stButton>button {
        border-radius: 12px !important;
        font-weight: bold !important;
        border: 2px solid #00ffcc !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #00ffcc !important;
        transform: scale(1.03);
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


# --- 3. Audio & Animations ---
def play_sound(sound_url):
    st.components.v1.html(
        f'<audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>',
        height=0
    )

def trigger_ghost():
    play_sound("https://assets.mixkit.co/active_storage/sfx/2658/2658-preview.mp3")
    st.markdown('<div class="ghost-overlay">👻</div>', unsafe_allow_html=True)


# --- Session State ---
if 'points' not in st.session_state:
    st.session_state.points = 100
if 'has_shield' not in st.session_state:
    st.session_state.has_shield = False
if 'active_puzzle' not in st.session_state:
    st.session_state.active_puzzle = None


# --- Game Header ---
st.title("🚪 CYBER MYSTERY DOORS 🎮")
st.caption("Featuring Python OOP, RegEx, Pandas, NumPy, JSON, & Mini-Games!")

# --- Sidebar: Profile & Item Shop ---
st.sidebar.header("👤 Player Profile")
raw_name = st.sidebar.text_input("Username (3-12 chars):", "Player1")
player = Player(raw_name)
st.sidebar.write(f"Playing as: **{player.username}**")

st.sidebar.markdown("---")
st.sidebar.header("🛒 Cyber Shop")
st.sidebar.write(f"💰 **Points Available:** `{st.session_state.points}`")

if st.sidebar.button("🛡️ Ghost Shield (50 pts)"):
    if st.session_state.points >= 50:
        st.session_state.points -= 50
        st.session_state.has_shield = True
        st.sidebar.success("Shield Active! Blocks 1 ghost trap.")
    else:
        st.sidebar.error("Not enough points!")

if st.session_state.has_shield:
    st.sidebar.info("🛡️ Shield Enabled")

# --- Game Modes ---
st.markdown("---")
game_mode = st.selectbox(
    "🎮 Select Arena Mode:",
    ["🎁 Chaos Roulette (Surprise per Door)", "💣 Bomb Defusal Mode", "🎰 Casino Jackpot Mode"]
)

num_doors = 6

if 'winning_door' not in st.session_state or st.session_state.get('last_mode') != game_mode:
    st.session_state.winning_door = int(np.random.randint(1, num_doors + 1))
    st.session_state.last_mode = game_mode


# --- Interactive Puzzles / Mini-Games ---
if st.session_state.active_puzzle:
    pz = st.session_state.active_puzzle
    
    # Puzzle 1: Bomb Defusal
    if pz == "defuse":
        st.error("💣 **BOMB TRAP ACTIVATED! Cut the right wire to defuse!**")
        wire_col1, wire_col2, wire_col3 = st.columns(3)
        
        chosen_wire = None
        if wire_col1.button("🔴 Cut Red Wire"): chosen_wire = "red"
        if wire_col2.button("🔵 Cut Blue Wire"): chosen_wire = "blue"
        if wire_col3.button("🟢 Cut Green Wire"): chosen_wire = "green"
        
        if chosen_wire:
            safe_wire = random.choice(["red", "blue", "green"])
            if chosen_wire == safe_wire:
                st.session_state.points += 200
                play_sound("https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3")
                st.success("💥 BOMB DEFUSED! You earned +200 Points!")
                save_game_data(player.username, "DEFUSE_WIN", game_mode, st.session_state.points)
            else:
                trigger_ghost()
                st.session_state.points = max(0, st.session_state.points - 50)
                st.error(f"💥 BOOM! The safe wire was {safe_wire.upper()}! (-50 pts)")
                save_game_data(player.username, "BOOM_LOSS", game_mode, st.session_state.points)
            
            st.session_state.active_puzzle = None
            st.rerun()

    # Puzzle 2: Secret Code Hacker
    elif pz == "hack":
        st.warning("🔐 **VAULT CODE HACKER! Guess the 1-digit master code (1-5):**")
        secret = random.randint(1, 5)
        user_guess = st.slider("Select Code Digit:", 1, 5)
        
        if st.button("Hack System"):
            if user_guess == secret:
                st.session_state.points += 150
                play_sound("https://assets.mixkit.co/active_storage/sfx/2019/2019-preview.mp3")
                st.success("🔓 ACCESS GRANTED! System hacked for +150 Points!")
                save_game_data(player.username, "HACK_WIN", game_mode, st.session_state.points)
            else:
                trigger_ghost()
                st.error(f"❌ ACCESS DENIED! The code was {secret}.")
            
            st.session_state.active_puzzle = None
            st.rerun()


# --- Render Doors ---
st.write(f"### Select a Cyber Door:")
cols = st.columns(min(num_doors, 6))

for i in range(num_doors):
    door_num = i + 1
    col_idx = i % 6

    if cols[col_idx].button(f"🚪 Door {door_num}", key=f"door_{door_num}"):
        
        # Outcome Probabilities
        event = np.random.choice(["treasure", "ghost", "bomb", "hack"], p=[0.3, 0.3, 0.2, 0.2])
        
        if event == "treasure":
            play_sound("https://assets.mixkit.co/active_storage/sfx/2019/2019-preview.mp3")
            st.balloons()
            st.session_state.points += 100
            st.success(f"🏆 **GOLDEN CHEST behind Door {door_num}!** (+100 pts)")
            save_game_data(player.username, "WIN", game_mode, st.session_state.points)
            
        elif event == "ghost":
            if st.session_state.has_shield:
                st.session_state.has_shield = False
                st.info("🛡️ Shield blocked the ghost jump!")
            else:
                trigger_ghost()
                st.session_state.points = max(0, st.session_state.points - 30)
                st.error(f"👻 **EEK! Ghost Trap behind Door {door_num}!** (-30 pts)")
                save_game_data(player.username, "LOSS", game_mode, st.session_state.points)
                
        elif event == "bomb":
            st.session_state.active_puzzle = "defuse"
            st.rerun()
            
        elif event == "hack":
            st.session_state.active_puzzle = "hack"
            st.rerun()


# --- Pandas Analytics ---
st.markdown("---")
st.subheader("📊 Class Leaderboard & History (Pandas)")
history_data = load_game_data()

if history_data:
    df = pd.DataFrame(history_data)
    st.dataframe(df.tail(8), use_container_width=True)
else:
    st.info("No game history recorded yet.")