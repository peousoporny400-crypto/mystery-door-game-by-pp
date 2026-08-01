import streamlit as st
import pandas as pd
import numpy as np
import json
import re
import os
import random

# --- Page Setup ---
st.set_page_config(page_title="Mystery Doors RPG", page_icon="🚪", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #00ffcc;
    }
    .stButton>button {
        border-radius: 10px !important;
        font-weight: bold !important;
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
        return name if re.match(pattern, name) else "Adventurer1"


# --- 2. JSON File Storage (Lesson Requirement) ---
JSON_FILE = "save_data.json"

def load_game_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_game_data(username, result, gold):
    history = load_game_data()
    history.append({
        "Username": username,
        "Result": result,
        "Gold Score": int(gold)
    })
    with open(JSON_FILE, "w") as f:
        json.dump(history, f, indent=4)


# --- Initialize Session States (Strict Integer Types) ---
if 'gold' not in st.session_state:
    st.session_state.gold = 100
if 'hp' not in st.session_state:
    st.session_state.hp = 100
if 'keys' not in st.session_state:
    st.session_state.keys = 1
if 'potions' not in st.session_state:
    st.session_state.potions = 1
if 'audio_to_play' not in st.session_state:
    st.session_state.audio_to_play = None


# --- Game Header & Top HUD ---
st.title("🚪 MYSTERY DOORS: DUNGEON QUEST ⚔️")

# Top HUD Bar
hud1, hud2, hud3, hud4 = st.columns(4)
hud1.metric("💰 Gold Points", f"{st.session_state.gold}")
hud2.metric("❤️ Player Health", f"{st.session_state.hp} / 100")
hud3.metric("🗝️ Dungeon Keys", f"{st.session_state.keys}")
hud4.metric("🧪 Health Potions", f"{st.session_state.potions}")

st.markdown("---")


# --- Audio Player Trigger ---
if st.session_state.audio_to_play:
    st.audio(st.session_state.audio_to_play, autoplay=True)
    st.session_state.audio_to_play = None


# --- Sidebar: Profile & Shop ---
st.sidebar.header("👤 Player Profile")
raw_name = st.sidebar.text_input("Username (3-12 alphanumeric):", "Adventurer1")
player = Player(raw_name)
st.sidebar.write(f"Hero: **{player.username}**")

st.sidebar.markdown("---")
st.sidebar.header("🛒 Item Shop")

if st.sidebar.button("🗝️ Buy Key (40 Gold)"):
    if st.session_state.gold >= 40:
        st.session_state.gold -= 40
        st.session_state.keys += 1
        st.sidebar.success("Bought 1 Key!")
        st.rerun()
    else:
        st.sidebar.error("Not enough Gold!")

if st.sidebar.button("🧪 Buy Potion (30 Gold)"):
    if st.session_state.gold >= 30:
        st.session_state.gold -= 30
        st.session_state.potions += 1
        st.sidebar.success("Bought 1 Health Potion!")
        st.rerun()
    else:
        st.sidebar.error("Not enough Gold!")

if st.sidebar.button("❤️ Drink Health Potion (+30 HP)"):
    if st.session_state.potions > 0 and st.session_state.hp < 100:
        st.session_state.potions -= 1
        st.session_state.hp = min(100, st.session_state.hp + 30)
        st.sidebar.success("Healed +30 HP!")
        st.rerun()
    else:
        st.sidebar.warning("No potions or health already full!")


# --- Game Over Check ---
if st.session_state.hp <= 0:
    st.error("☠️ **GAME OVER! You ran out of health in the dungeon.**")
    save_game_data(player.username, "DIED", st.session_state.gold)
    
    if st.button("🔄 Restart Game"):
        st.session_state.hp = 100
        st.session_state.gold = 100
        st.session_state.keys = 1
        st.session_state.potions = 1
        st.rerun()
    st.stop()


# --- Main Game: 3 Mystery Doors ---
st.subheader("🚪 Pick a Door to Explore:")

col1, col2, col3 = st.columns(3)

# DOOR 1: Treasure Room
with col1:
    st.markdown("### 🏛️ Door 1: Gold Vault")
    st.caption("Safe door, chance for big gold points.")
    if st.button("Open Door 1"):
        reward = int(np.random.choice([50, 100, 150]))
        st.session_state.gold += reward
        st.session_state.audio_to_play = "https://cdn.freesound.org/previews/274/274178_5123851-lq.mp3"
        st.success(f"🎉 You found a Golden Chest! (+{reward} Gold)")
        save_game_data(player.username, "TREASURE", st.session_state.gold)
        st.rerun()

# DOOR 2: Ghost Trap Door
with col2:
    st.markdown("### 👻 Door 2: Haunted Room")
    st.caption("Risky! Might lose HP or find a potion.")
    if st.button("Open Door 2"):
        event = np.random.choice(["ghost", "potion"], p=[0.7, 0.3])
        if event == "ghost":
            st.session_state.hp -= 25
            st.session_state.audio_to_play = "https://cdn.freesound.org/previews/145/145303_2615119-lq.mp3"
            st.error("👻 A GHOST ATTACKS YOU! (-25 HP)")
            save_game_data(player.username, "GHOST_TRAP", st.session_state.gold)
        else:
            st.session_state.potions += 1
            st.info("🧪 You scared the ghost away and found a Health Potion!")
        st.rerun()

# DOOR 3: Locked Boss Vault (Requires Key)
with col3:
    st.markdown("### 🔒 Door 3: Locked Vault")
    st.caption("Requires 1 Key! High Risk, High Reward.")
    if st.button("Unlock Door 3 (1 Key)"):
        if st.session_state.keys > 0:
            st.session_state.keys -= 1
            jackpot = int(np.random.choice([200, 300, 500]))
            st.session_state.gold += jackpot
            st.session_state.audio_to_play = "https://cdn.freesound.org/previews/274/274178_5123851-lq.mp3"
            st.balloons()
            st.success(f"💎 **JACKPOT!** You unlocked the master vault! (+{jackpot} Gold)")
            save_game_data(player.username, "JACKPOT", st.session_state.gold)
            st.rerun()
        else:
            st.warning("🔒 Door is locked! Buy a Key in the Shop sidebar.")


# --- 4. Pandas Leaderboard Table ---
st.markdown("---")
st.subheader("📜 Dungeon History & Scores (Pandas)")
history_data = load_game_data()

if history_data:
    df = pd.DataFrame(history_data)
    st.dataframe(df.tail(8), use_container_width=True)
else:
    st.info("No games played yet. Click a door to start!")