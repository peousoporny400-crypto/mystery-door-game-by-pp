import streamlit as st
import pandas as pd
import numpy as np
import math
import random
import time
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="Ultimate Roblox Arcade Hub", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .stButton>button { border-radius: 8px !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- SOUND EFFECT HELPER ---
SOUNDS = {
    "win": "https://cdn.freesound.org/previews/274/274178_5123851-lq.mp3",
    "fail": "https://cdn.freesound.org/previews/145/145303_2615119-lq.mp3",
    "click": "https://cdn.freesound.org/previews/256/256116_3263906-lq.mp3"
}

def play_sound(sound_key):
    if sound_key in SOUNDS:
        st.audio(SOUNDS[sound_key], autoplay=True)

# ==============================================================================
# 🧠 LESSON 1: OOP CLASSES
# ==============================================================================

class Dragon:
    """OOP Class for Dragon City feature."""
    def __init__(self, name, element, hp, attack):
        self.name = name
        self.element = element
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.level = 1

    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5


class Player:
    """OOP Class for Global Player Stats."""
    def __init__(self):
        self.gold = 150
        self.health = 100
        self.max_health = 100
        self.dragons = [Dragon("Flame Hatchling", "🔥 Fire", 80, 15)]
        self.inventory = {"Wheat": 0, "Dragon Fruit": 0, "Car Fuel": 2}
        self.scores_history = []

    def add_gold(self, amount):
        self.gold += amount
        self.scores_history.append(amount)

    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False


# Init Session State
if "player" not in st.session_state:
    st.session_state.player = Player()

player = st.session_state.player

# ==============================================================================
# 🎮 HERO HEADER & SIDEBAR MENU
# ==============================================================================

st.markdown("""
    <div style="background: linear-gradient(90deg, #1e1b4b, #312e81, #4338ca); padding: 20px; border-radius: 12px; text-align: center; color: white;">
        <h1>🎮 ULTIMATE PYTHON ARCADE PORTAL 🎮</h1>
        <p>Built with OOP, Pandas, NumPy, Math, Regex Metacharacters & Sound Effects!</p>
    </div>
    <br>
""", unsafe_allow_html=True)

st.sidebar.title("🕹️ Arcade Select")
current_game = st.sidebar.radio(
    "Choose Game Module:",
    [
        "🐉 Dragon City Breeder",
        "🍬 Candy Crush Match-3",
        "🏎️ Hill Climb Racing",
        "♟️ Chess Challenge",
        "🎵 Tiles Hop Rhythm",
        "❌⭕ OX (Tic-Tac-Toe)",
        "🕵️ Guess Imposter",
        "🧩 Tile & Math Puzzle",
        "📊 Pandas & NumPy Analytics Lab"
    ]
)

st.sidebar.divider()
st.sidebar.metric("🪙 Arcade Gold", f"{player.gold}")
st.sidebar.metric("🐉 Dragons Owned", f"{len(player.dragons)}")

# ==============================================================================
# 🐉 GAME 1: DRAGON CITY
# ==============================================================================
if current_game == "🐉 Dragon City Breeder":
    st.title("🐉 Dragon City Breeder & Arena")
    
    tab_team, tab_arena = st.tabs(["🐉 Dragon Roster", "⚔️ Battle Arena"])

    with tab_team:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Your Dragon Squad (Pandas Frame)")
            dragon_data = [{"Name": d.name, "Element": d.element, "Level": d.level, "HP": f"{d.hp}/{d.max_hp}", "Attack": d.attack} for d in player.dragons]
            st.dataframe(pd.DataFrame(dragon_data), use_container_width=True)

        with col2:
            st.subheader("🥚 Hatchery")
            if st.button("Hatch Frost Wyrm (60 Gold)"):
                if player.spend_gold(60):
                    player.dragons.append(Dragon("Frost Wyrm", "❄️ Ice", 90, 18))
                    play_sound("win")
                    st.success("Hatched a Frost Wyrm!")
                    st.rerun()
                else:
                    play_sound("fail")
                    st.error("Not enough gold!")

    with tab_arena:
        st.subheader("⚔️ Wild Dragon Battle")
        if "wild_hp" not in st.session_state:
            st.session_state.wild_hp = 100

        active_d = player.dragons[0]
        st.write(f"**Your Active Dragon:** {active_d.name} (Level {active_d.level})")
        st.write(f"**Wild Boss HP:** {st.session_state.wild_hp}/100")

        if st.button("🔥 Attack Wild Boss!"):
            damage = int(active_d.attack + np.random.randint(-3, 6))
            st.session_state.wild_hp -= damage
            play_sound("click")
            st.info(f"Dealt {damage} damage!")

            if st.session_state.wild_hp <= 0:
                reward = int(np.random.randint(40, 80))
                player.add_gold(reward)
                play_sound("win")
                st.balloons()
                st.success(f"🎉 Boss Defeated! Earned {reward} Gold!")
                st.session_state.wild_hp = 100
                active_d.level_up()
                st.rerun()

# ==============================================================================
# 🍬 GAME 2: CANDY CRUSH SAGA
# ==============================================================================
elif current_game == "🍬 Candy Crush Match-3":
    st.title("🍬 Candy Crush Emoji Matcher")
    
    if "candy_grid" not in st.session_state:
        candies = ["🍬", "🍭", "🍩", "🍫"]
        st.session_state.candy_grid = np.random.choice(candies, size=(3, 3))

    st.table(pd.DataFrame(st.session_state.candy_grid, columns=["Col 1", "Col 2", "Col 3"]))

    if st.button("🔀 Swap Candies!"):
        candies = ["🍬", "🍭", "🍩", "🍫"]
        st.session_state.candy_grid = np.random.choice(candies, size=(3, 3))
        
        row_matches = any(len(set(row)) == 1 for row in st.session_state.candy_grid)
        if row_matches:
            player.add_gold(50)
            play_sound("win")
            st.success("🎉 CANDY MATCH! Earned +50 Gold!")
        else:
            play_sound("click")
            st.info("No match this turn!")
        st.rerun()

# ==============================================================================
# 🏎️ GAME 3: HILL CLIMB RACING
# ==============================================================================
elif current_game == "🏎️ Hill Climb Racing":
    st.title("🏎️ Hill Climb Driver")
    
    if "distance" not in st.session_state:
        st.session_state.distance = 0
    if "fuel" not in st.session_state:
        st.session_state.fuel = 100

    col1, col2 = st.columns(2)
    col1.metric("🏁 Distance", f"{st.session_state.distance:.1f} m")
    col2.metric("⛽ Fuel", f"{st.session_state.fuel:.0f}%")

    hill_angle = round(math.degrees(math.sin(st.session_state.distance / 10)), 1)
    st.write(f"📐 Slope Angle: `{hill_angle}°`")

    if st.session_state.fuel > 0:
        if st.button("🏎️ Gas Pedal"):
            st.session_state.distance += 5.5
            fuel_used = 8 + (hill_angle / 10 if hill_angle > 0 else 2)
            st.session_state.fuel = max(0, st.session_state.fuel - fuel_used)
            play_sound("click")
            
            if st.session_state.distance >= 50:
                player.add_gold(60)
                play_sound("win")
                st.success("🏆 Reached Mountain Peak! (+60 Gold)")
                st.session_state.distance = 0
                st.session_state.fuel = 100
            st.rerun()
    else:
        st.error("Out of fuel!")
        if st.button("Refill Fuel (20 Gold)"):
            if player.spend_gold(20):
                st.session_state.fuel = 100
                st.rerun()

# ==============================================================================
# ♟️ GAME 4: CHESS CHALLENGE
# ==============================================================================
elif current_game == "♟️ Chess Challenge":
    st.title("♟️ Chess Tactics")
    
    st.table(pd.DataFrame([["👑", "⬜", "⬜"], ["⬜", "♟️", "⬜"], ["⬜", "⬜", "🐴"]]))
    choice = st.radio("Pick your move:", ["Jump to Top Right", "Jump to Middle", "Jump to Top Left"])

    if st.button("Execute Move"):
        if re.search(r"Top Right", choice):
            player.add_gold(45)
            play_sound("win")
            st.success("🎉 CHECKMATE! (+45 Gold)")
        else:
            play_sound("fail")
            st.error("❌ Blunder! Try again.")

# ==============================================================================
# 🎵 GAME 5: TILES HOP RHYTHM
# ==============================================================================
elif current_game == "🎵 Tiles Hop Rhythm":
    st.title("🎵 Tiles Hop Reaction")
    
    if "tile_target" not in st.session_state:
        st.session_state.tile_target = random.choice(["🎵 Tile A", "🎶 Tile B", "🎼 Tile C"])

    st.subheader(f"Hop Target: **{st.session_state.tile_target}**")
    cols = st.columns(3)
    tiles = ["🎵 Tile A", "🎶 Tile B", "🎼 Tile C"]

    for idx, t in enumerate(tiles):
        with cols[idx]:
            if st.button(f"Hop {t}", key=f"th_{idx}"):
                if t == st.session_state.tile_target:
                    player.add_gold(25)
                    play_sound("win")
                    st.success("✨ Perfect Hop! (+25 Gold)")
                    st.session_state.tile_target = random.choice(tiles)
                    st.rerun()
                else:
                    play_sound("fail")
                    st.error("💥 Missed!")

# ==============================================================================
# ❌⭕ GAME 6: OX (TIC-TAC-TOE)
# ==============================================================================
elif current_game == "❌⭕ OX (Tic-Tac-Toe)":
    st.title("❌⭕ OX Tic-Tac-Toe vs Bot")
    
    if "board" not in st.session_state:
        st.session_state.board = [""] * 9

    def check_winner(b):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for x, y, z in wins:
            if b[x] == b[y] == b[z] and b[x] != "":
                return b[x]
        return "Tie" if "" not in b else None

    grid = st.columns(3)
    for i in range(9):
        with grid[i % 3]:
            lbl = st.session_state.board[i] if st.session_state.board[i] != "" else " "
            if st.button(lbl, key=f"ox_{i}", use_container_width=True):
                if st.session_state.board[i] == "" and check_winner(st.session_state.board) is None:
                    st.session_state.board[i] = "❌"
                    empty = [idx for idx, val in enumerate(st.session_state.board) if val == ""]
                    if empty and check_winner(st.session_state.board) is None:
                        st.session_state.board[random.choice(empty)] = "⭕"
                    play_sound("click")
                    st.rerun()

    w = check_winner(st.session_state.board)
    if w == "❌":
        player.add_gold(30)
        play_sound("win")
        st.success("🎉 You won! (+30 Gold)")
        if st.button("Reset Board"):
            st.session_state.board = [""] * 9
            st.rerun()

# ==============================================================================
# 🕵️ GAME 7: GUESS THE IMPOSTER (REGEX VALIDATION)
# ==============================================================================
elif current_game == "🕵️ Guess Imposter":
    st.title("🕵️ Find the Imposter")
    
    if "imposter_name" not in st.session_state:
        st.session_state.imposter_name = random.choice(["Red", "Blue", "Green", "Yellow"])

    guess = st.text_input("Name suspect (e.g., Red, Blue):")
    if st.button("Eject Suspect"):
        if not re.match(r"^[A-Z][a-z]+$", guess):
            st.warning("⚠️ Formatting Rule: Start with a Capital letter!")
        elif guess == st.session_state.imposter_name:
            player.add_gold(40)
            play_sound("win")
            st.success("🎉 Correct! Found Imposter (+40 Gold)")
            st.session_state.imposter_name = random.choice(["Red", "Blue", "Green", "Yellow"])
        else:
            play_sound("fail")
            st.error("❌ Crewmate was innocent!")

# ==============================================================================
# 🧩 GAME 8: TILE & MATH PUZZLE
# ==============================================================================
elif current_game == "🧩 Tile & Math Puzzle":
    st.title("🧩 Distance Logic Puzzle")
    
    ans = st.number_input("Find hypotenuse $c$ for $a=3, b=4$:", step=1.0)
    if st.button("Check Math Answer"):
        if ans == math.sqrt(3**2 + 4**2):
            player.add_gold(35)
            play_sound("win")
            st.success("🎉 Correct distance ($c = 5.0$)! (+35 Gold)")
        else:
            play_sound("fail")
            st.error("❌ Incorrect math!")

# ==============================================================================
# 📊 GAME 9: DATA SCIENCE LAB
# ==============================================================================
elif current_game == "📊 Pandas & NumPy Analytics Lab":
    st.title("📊 Data Analytics Science Lab")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Summary Table (Pandas)")
        st.dataframe(pd.DataFrame({"Stat": ["Gold", "Health"], "Value": [player.gold, player.health]}), use_container_width=True)

    with col2:
        st.subheader("🧮 Stats (NumPy)")
        if len(player.scores_history) > 0:
            arr = np.array(player.scores_history)
            st.write(f"- **Mean Earnings (np.mean):** `{np.mean(arr):.2f}` Gold")
            st.write(f"- **Max Earned (np.max):** `{np.max(arr)}` Gold")