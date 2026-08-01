import streamlit as st
import pandas as pd
import numpy as np
import json
import re
import os
import random

# --- Page Config & Custom Atmospheric Styling ---
st.set_page_config(page_title="Realm of Mystery Doors", page_icon="🗝️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #d1d5db;
    }
    .stButton>button {
        border-radius: 8px !important;
        font-weight: bold !important;
        width: 100%;
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
        return name if re.match(pattern, name) else "Hero1"


# --- 2. JSON Data Persistence (Lesson Requirement) ---
JSON_FILE = "save_data.json"

def load_game_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    return []

def save_game_data(username, outcome, score, achievements):
    history = load_game_data()
    history.append({
        "Username": username,
        "Outcome": outcome,
        "Treasure Score": score,
        "Badges Earned": ", ".join(achievements) if achievements else "None"
    })
    with open(JSON_FILE, "w") as f:
        json.dump(history, f, indent=4)


# --- 3. Audio & Media Helper ---
def play_sound(sound_type):
    sounds = {
        "fanfare": "https://cdn.freesound.org/previews/274/274178_5123851-lq.mp3",
        "trap": "https://cdn.freesound.org/previews/145/145303_2615119-lq.mp3",
        "dice": "https://cdn.freesound.org/previews/320/320655_5260872-lq.mp3"
    }
    if sound_type in sounds:
        st.markdown(f'<audio autoplay hidden><source src="{sounds[sound_type]}" type="audio/mp3"></audio>', unsafe_allow_html=True)


# --- Initialize Session State ---
if 'hp' not in st.session_state:
    st.session_state.hp = 100
if 'points' not in st.session_state:
    st.session_state.points = 150
if 'keys' not in st.session_state:
    st.session_state.keys = 1
if 'potions' not in st.session_state:
    st.session_state.potions = 1
if 'active_riddle' not in st.session_state:
    st.session_state.active_riddle = None
if 'active_mimic' not in st.session_state:
    st.session_state.active_mimic = False
if 'achievements' not in st.session_state:
    st.session_state.achievements = set()


# --- Game Header & Top HUD (Fixed Metric Error!) ---
st.title("🗝️ REALM OF MYSTERY DOORS")

# 🔝 Top Status Bar (Score & Stats formatted as Strings)
hud_col1, hud_col2, hud_col3, hud_col4 = st.columns(4)
hud_col1.metric("💰 Treasure Points", f"{st.session_state.points} Gold")
hud_col2.metric("❤️ Player HP", f"{st.session_state.hp} / 100")
hud_col3.metric("🗝️ Keys", str(st.session_state.keys))
hud_col4.metric("🧪 Health Potions", str(st.session_state.potions))

st.markdown("---")


# --- Sidebar: Profile, Shop, & Mode ---
st.sidebar.header("👤 Adventurer Profile")
raw_name = st.sidebar.text_input("Hero Username (3-12 chars):", "Hero1")
player = Player(raw_name)
st.sidebar.write(f"Playing as: **{player.username}**")

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Game Mode")
mode = st.sidebar.radio("Select Mode:", ["Standard Adventure", "💀 Permadeath Rogue-lite"])

st.sidebar.markdown("---")
st.sidebar.header("🛒 Adventurer Shop")
if st.sidebar.button("🗝️ Buy Key (50 Gold)"):
    if st.session_state.points >= 50:
        st.session_state.points -= 50
        st.session_state.keys += 1
        st.sidebar.success("Key purchased!")
        st.rerun()
    else:
        st.sidebar.error("Not enough Gold!")

if st.sidebar.button("🧪 Buy Potion (40 Gold)"):
    if st.session_state.points >= 40:
        st.session_state.points -= 40
        st.session_state.potions += 1
        st.sidebar.success("Potion purchased!")
        st.rerun()
    else:
        st.sidebar.error("Not enough Gold!")

if st.sidebar.button("❤️ Use Health Potion (+30 HP)"):
    if st.session_state.potions > 0 and st.session_state.hp < 100:
        st.session_state.potions -= 1
        st.session_state.hp = min(100, st.session_state.hp + 30)
        st.sidebar.success("Restored +30 HP!")
        st.rerun()
    else:
        st.sidebar.warning("No potions left or HP is full!")


# --- Check Permadeath / Game Over ---
if st.session_state.hp <= 0:
    play_sound("trap")
    st.error("☠️ **YOU DIED!** You lost all your health on this dungeon run.")
    st.image("https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=500&q=80", width=400)
    
    save_game_data(player.username, "DIED", st.session_state.points, list(st.session_state.achievements))
    
    if st.button("🔄 Restart Dungeon Run"):
        st.session_state.hp = 100
        st.session_state.points = 100
        st.session_state.keys = 1
        st.session_state.potions = 1
        st.session_state.achievements = set()
        st.rerun()
    st.stop()


# --- NPC Cryptic Hints ---
npc_hints = [
    "🧙‍♂️ Gargoyle: 'Door 1 feels surprisingly warm...'",
    "🧙‍♂️ Gargoyle: 'I hear a mimic growling behind Cursed Door...'",
    "🧙‍♂️ Gargoyle: 'Ancient treasures await in the Enchanted Forest!'"
]
st.info(random.choice(npc_hints))


# --- Puzzles & Mini-Games Section ---

# 1. Active Riddle
if st.session_state.active_riddle:
    r = st.session_state.active_riddle
    st.warning(f"📜 **THE DOOR DEMANDS AN ANSWER:** {r['riddle']}")
    ans = st.text_input("Type your answer:").strip().lower()
    
    if st.button("Submit Answer"):
        if ans == r['answer']:
            play_sound("fanfare")
            st.session_state.points += 150
            st.success("✨ Correct! The magical door unlocks and awards +150 Gold!")
            st.session_state.achievements.add("Riddle Master")
        else:
            play_sound("trap")
            st.session_state.hp -= 20
            st.error(f"❌ INCORRECT! A trap triggers! (-20 HP). The answer was: {r['answer']}")
        
        st.session_state.active_riddle = None
        st.rerun()

# 2. Mimic Combat Dice Roll
if st.session_state.active_mimic:
    st.error("👺 **A MIMIC ATTACKS YOU! Roll a D20 to fight!**")
    st.image("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=500&q=80", width=400)
    
    if st.button("🎲 Roll D20 Skill Check"):
        play_sound("dice")
        roll = int(np.random.randint(1, 21))
        
        if roll >= 10:
            play_sound("fanfare")
            st.session_state.points += 200
            st.success(f"⚔️ **CRITICAL HIT! (Rolled {roll})** You defeated the Mimic and collected +200 Gold!")
            st.session_state.achievements.add("Mimic Slayer")
        else:
            play_sound("trap")
            damage = int(np.random.randint(25, 45))
            st.session_state.hp -= damage
            st.error(f"💥 **FAIL! (Rolled {roll})** The Mimic bites you for -{damage} HP!")
        
        st.session_state.active_mimic = False
        st.rerun()


# --- 🚪 Themed Doors World (Working Images) ---
st.markdown("### Choose a World Door to Explore:")

door_col1, door_col2, door_col3 = st.columns(3)

# Door 1: Ancient Temple
with door_col1:
    st.markdown("#### 🏛️ Ancient Temple")
    st.image("https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=500&q=80", use_container_width=True)
    if st.button("Open Temple Door"):
        event = np.random.choice(["gold", "trap", "key"], p=[0.5, 0.3, 0.2])
        if event == "gold":
            play_sound("fanfare")
            st.session_state.points += 100
            st.success("🏛️ You opened an ancient golden chest! (+100 Gold)")
        elif event == "trap":
            play_sound("trap")
            st.session_state.hp -= 15
            st.error("🐍 Poison dart trap! (-15 HP)")
        else:
            st.session_state.keys += 1
            st.info("🗝️ You found an Old Brass Key!")
        st.rerun()

# Door 2: Cursed Mimic Vault (Requires Key)
with door_col2:
    st.markdown("#### 💀 Cursed Vault")
    st.image("https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=500&q=80", use_container_width=True)
    if st.button("Unlock Vault (Uses 1 Key)"):
        if st.session_state.keys > 0:
            st.session_state.keys -= 1
            st.session_state.active_mimic = True
            st.rerun()
        else:
            st.warning("🔒 Door is locked! Buy a Key in the Adventurer Shop.")

# Door 3: Enchanted Forest
with door_col3:
    st.markdown("#### 🌲 Enchanted Forest")
    st.image("https://images.unsplash.com/photo-1511497584788-876761c11969?auto=format&fit=crop&w=500&q=80", use_container_width=True)
    if st.button("Enter Forest Door"):
        event = np.random.choice(["riddle", "potion", "ghost"], p=[0.4, 0.3, 0.3])
        if event == "riddle":
            riddles_list = [
                {"riddle": "What gets wetter the more it dries?", "answer": "towel"},
                {"riddle": "What has hands but cannot clap?", "answer": "clock"},
                {"riddle": "What has to be broken before you can use it?", "answer": "egg"}
            ]
            st.session_state.active_riddle = random.choice(riddles_list)
            st.rerun()
        elif event == "potion":
            st.session_state.potions += 1
            st.success("🧪 A forest spirit gifted you a Health Potion!")
            st.rerun()
        else:
            play_sound("trap")
            st.session_state.hp -= 20
            st.error("👻 A dark forest ghost drains your energy! (-20 HP)")
            st.rerun()


# --- Achievements Badges ---
st.markdown("---")
st.subheader("🏆 Unlocked Achievement Badges")
if st.session_state.achievements:
    badge_cols = st.columns(len(st.session_state.achievements))
    for idx, badge in enumerate(st.session_state.achievements):
        badge_cols[idx].info(f"🏅 {badge}")
else:
    st.caption("No badges earned yet. Solve riddles and fight mimics to unlock badges!")


# --- Hall of Fame & Global Ledger (Pandas) ---
st.markdown("---")
st.subheader("📜 Dungeon Hall of Fame & Adventure Ledger (Pandas)")
history_data = load_game_data()

if history_data:
    df = pd.DataFrame(history_data)
    st.dataframe(df.tail(8), use_container_width=True)
else:
    st.info("No recorded adventures yet.")