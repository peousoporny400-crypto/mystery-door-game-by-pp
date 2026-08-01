import json
import os
import random
import re
import numpy as np
import pandas as pd
import streamlit as st

# --- Page Setup & CSS Styling ---
st.set_page_config(
    page_title="Cyber Multi-Game Hub", page_icon="🕹️", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f111a;
        color: #00ffcc;
    }
    .score-banner {
        background-color: #1a1c29;
        border: 2px solid #00ffcc;
        border-radius: 10px;
        padding: 10px 20px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #00ffcc;
        margin-bottom: 20px;
    }
    .suspect-box {
        background-color: #1a1c29;
        border: 1px solid #00ffcc;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        min-height: 120px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- 1. OOP & RegEx ---
class Player:

  def __init__(self, username):
    self.username = self.validate_username(username)

  @staticmethod
  def validate_username(name):
    pattern = r"^[a-zA-Z0-9_]{3,12}$"
    if re.match(pattern, name):
      return name
    return "Player1"


# --- 2. JSON Storage ---
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
      "Score": score,
  })
  with open(JSON_FILE, "w") as f:
    json.dump(history, f, indent=4)


# --- 3. Audio Player Helper ---
def play_sound(sound_type):
  sounds = {
      "win": "https://cdn.freesound.org/previews/274/274178_5123851-lq.mp3",
      "lose": "https://cdn.freesound.org/previews/331/331912_3248244-lq.mp3",
      "puzzle": (
          "https://cdn.freesound.org/previews/320/320655_5260872-lq.mp3"
      ),
  }
  if sound_type in sounds:
    st.markdown(
        f'<audio autoplay hidden><source src="{sounds[sound_type]}"'
        ' type="audio/mp3"></audio>',
        unsafe_allow_html=True,
    )


# --- Session State Initialization ---
if "points" not in st.session_state:
  st.session_state.points = 100
if "has_shield" not in st.session_state:
  st.session_state.has_shield = False

# Door State
if "active_puzzle" not in st.session_state:
  st.session_state.active_puzzle = None
if "revealed_empty" not in st.session_state:
  st.session_state.revealed_empty = None

# XO State
if "xo_board" not in st.session_state:
  st.session_state.xo_board = [" "] * 9

# Imposter State
if "imposter_data" not in st.session_state:
  st.session_state.imposter_data = None


# --- Header & Top Score Display ---
st.title("🕹️ CYBER MULTI-GAME HUB 🎮")

st.markdown(
    f'<div class="score-banner">💰 CURRENT SCORE: {st.session_state.points} PTS'
    f' {" | 🛡️ Shield Active" if st.session_state.has_shield else ""}</div>',
    unsafe_allow_html=True,
)


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
    st.sidebar.success("Shield Purchased! Protects against 1 loss.")
    st.rerun()
  else:
    st.sidebar.error("Not enough points!")

if st.sidebar.button("🔮 Buy Oracle Glass (75 pts)"):
  if st.session_state.points >= 75:
    st.session_state.points -= 75
    st.session_state.revealed_empty = random.randint(1, 3)
    st.sidebar.success("Oracle Glass Activated! One trap door revealed in Easy.")
    st.rerun()
  else:
    st.sidebar.error("Not enough points!")

if st.session_state.has_shield:
  st.sidebar.info("🛡️ Ghost Shield Active")


# --- Game Selection (With Easy / Medium / Hard Tags) ---
selected_mode = st.radio(
    "Choose Game Mode:",
    [
        "🟢 Easy Mode (Mystery Doors)",
        "🟡 Medium Mode (Tic-Tac-Toe XO)",
        "🔴 Hard Mode (Guess Imposter)",
    ],
    horizontal=True,
)


# ==========================================
# 🟢 EASY MODE: MYSTERY DOORS
# ==========================================
if "Easy" in selected_mode:
  st.subheader("🟢 Easy Mode: Mystery Doors 🚪")
  num_doors = 5

  if (
      "winning_door" not in st.session_state
      or st.session_state.get("last_mode") != "Easy"
  ):
    st.session_state.winning_door = int(np.random.randint(1, num_doors + 1))
    st.session_state.puzzle_door = int(np.random.randint(1, num_doors + 1))
    while st.session_state.puzzle_door == st.session_state.winning_door:
      st.session_state.puzzle_door = int(np.random.randint(1, num_doors + 1))
    st.session_state.last_mode = "Easy"

  if st.session_state.active_puzzle:
    st.warning("🧠 **BRAIN PUZZLE DOOR OPENED!** Solve this to win points!")
    p_data = st.session_state.active_puzzle
    user_ans = st.number_input(
        f"What is {p_data['num1']} + {p_data['num2']} x {p_data['num3']}?",
        value=0,
    )

    if st.button("Submit Answer"):
      correct_ans = p_data["num1"] + (p_data["num2"] * p_data["num3"])
      if user_ans == correct_ans:
        st.session_state.points += 150
        play_sound("puzzle")
        st.success("🎉 Correct Answer! You earned +150 Points!")
        save_game_data(
            player.username, "PUZZLE_WIN", "Easy", st.session_state.points
        )
      else:
        play_sound("lose")
        st.error(f"❌ Wrong! The answer was {correct_ans}.")

      st.session_state.active_puzzle = None
      st.session_state.winning_door = int(np.random.randint(1, num_doors + 1))
      st.rerun()

  cols = st.columns(num_doors)
  for i in range(num_doors):
    door_num = i + 1
    label = f"🚪 Door {door_num}"
    if (
        st.session_state.revealed_empty == door_num
        and door_num != st.session_state.winning_door
    ):
      label = f"💀 TRAP Door {door_num}"

    if cols[i].button(label, key=f"door_{door_num}"):
      if door_num == st.session_state.winning_door:
        play_sound("win")
        st.balloons()
        st.session_state.points += 100
        st.success(
            f"🎉 **YOU FOUND THE TREASURE behind Door {door_num}!** (+100 Points)"
        )
        save_game_data(
            player.username, "WIN", "Easy", st.session_state.points
        )
        st.session_state.winning_door = int(
            np.random.randint(1, num_doors + 1)
        )
      elif door_num == st.session_state.puzzle_door:
        st.session_state.active_puzzle = {
            "num1": int(np.random.randint(5, 20)),
            "num2": int(np.random.randint(2, 10)),
            "num3": int(np.random.randint(2, 5)),
        }
        st.rerun()
      else:
        if st.session_state.has_shield:
          st.session_state.has_shield = False
          st.info(
              "🛡️ A Ghost jumped out, but your Shield protected your points!"
          )
        else:
          play_sound("lose")
          st.session_state.points = max(0, st.session_state.points - 30)
          st.error(f"👻 **GHOST!** Door {door_num} was a trap! (-30 Points)")
          save_game_data(
              player.username, "LOSS", "Easy", st.session_state.points
          )
        st.session_state.winning_door = int(
            np.random.randint(1, num_doors + 1)
        )


# ==========================================
# 🟡 MEDIUM MODE: HARDER TIC-TAC-TOE (XO)
# ==========================================
elif "Medium" in selected_mode:
  st.subheader("🟡 Medium Mode: Smart AI Tic-Tac-Toe (XO) ❌⭕")
  st.caption(
      "Play as **X**. The AI (**O**) will block your moves and try to win!"
  )

  WIN_LINES = [
      (0, 1, 2),
      (3, 4, 5),
      (6, 7, 8),  # rows
      (0, 3, 6),
      (1, 4, 7),
      (2, 5, 8),  # cols
      (0, 4, 8),
      (2, 4, 6),  # diagonals
  ]

  def check_winner(b):
    for x, y, z in WIN_LINES:
      if b[x] == b[y] == b[z] and b[x] != " ":
        return b[x]
    if " " not in b:
      return "Draw"
    return None

  def smart_ai_move(b):
    empty = [i for i, v in enumerate(b) if v == " "]
    if not empty:
      return None

    # 1. Check if AI can WIN this turn
    for i in empty:
      temp = b.copy()
      temp[i] = "O"
      if check_winner(temp) == "O":
        return i

    # 2. BLOCK Player 'X' from winning next turn
    for i in empty:
      temp = b.copy()
      temp[i] = "X"
      if check_winner(temp) == "X":
        return i

    # 3. Take Center if available
    if 4 in empty:
      return 4

    # 4. Take Corners
    corners = [i for i in [0, 2, 6, 8] if i in empty]
    if corners:
      return random.choice(corners)

    # 5. Fallback random
    return random.choice(empty)

  def reset_xo():
    st.session_state.xo_board = [" "] * 9

  board = st.session_state.xo_board
  grid_cols = st.columns(3)

  for idx in range(9):
    col = grid_cols[idx % 3]
    btn_label = board[idx] if board[idx] != " " else " "
    if col.button(
        btn_label if btn_label != " " else f"- ({idx+1}) -", key=f"xo_{idx}"
    ):
      if board[idx] == " ":
        # Player move
        board[idx] = "X"
        winner = check_winner(board)

        # Smart AI move
        if not winner:
          ai_idx = smart_ai_move(board)
          if ai_idx is not None:
            board[ai_idx] = "O"
            winner = check_winner(board)

        if winner == "X":
          play_sound("win")
          st.balloons()
          st.session_state.points += 100
          st.success("🎉 You beat the Smart AI! (+100 Points)")
          save_game_data(
              player.username, "WIN", "Medium XO", st.session_state.points
          )
          reset_xo()
        elif winner == "O":
          if st.session_state.has_shield:
            st.session_state.has_shield = False
            st.info("🛡️ You lost, but your Shield protected your points!")
          else:
            play_sound("lose")
            st.session_state.points = max(0, st.session_state.points - 30)
            st.error("❌ Smart AI Won! (-30 Points)")
            save_game_data(
                player.username, "LOSS", "Medium XO", st.session_state.points
            )
          reset_xo()
        elif winner == "Draw":
          st.session_state.points += 20
          st.info("🤝 Draw against Smart AI! (+20 Points)")
          save_game_data(
              player.username, "DRAW", "Medium XO", st.session_state.points
          )
          reset_xo()
        st.rerun()

  if st.button("Reset Board"):
    reset_xo()
    st.rerun()


# ==========================================
# 🔴 HARD MODE: HARDER GUESS THE IMPOSTER
# ==========================================
elif "Hard" in selected_mode:
  st.subheader("🔴 Hard Mode: Tricky Imposter Deduction 🕵️")
  st.caption(
      "Read closely! The lies are subtler and test math, logic, & trivia. Win:"
      " +200 Pts | Loss: -50 Pts"
  )

  if (
      not st.session_state.imposter_data
      or st.session_state.get("last_mode") != "Hard"
  ):
    scenarios = [
        {
            "topic": "Prime Numbers",
            "statements": {
                "Alpha": "2 is the only even prime number.",
                "Beta": (
                    "1 is the smallest prime number."
                ),  # LIE (1 is not prime)
                "Gamma": "13 is a prime number.",
            },
            "imposter": "Beta",
            "hint": "1 is NOT a prime number! 2 is the smallest prime number.",
        },
        {
            "topic": "Solar System Science",
            "statements": {
                "Vortex": "Venus is the hottest planet in our solar system.",
                "Nova": "Jupiter has the shortest day of all planets.",
                "Pulse": (
                    "Mars has 4 moons named Phobos, Deimos, Titan, and Io."
                ),  # LIE
            },
            "imposter": "Pulse",
            "hint": (
                "Mars only has 2 moons (Phobos & Deimos). Titan is Saturn's"
                " moon!"
            ),
        },
        {
            "topic": "Computing & Bytes",
            "statements": {
                "Byte": "There are 8 bits in 1 byte.",
                "RAM": "1 Kilobyte is equal to 1,024 Bytes.",
                "Core": "1 Megabyte is equal to 500 Kilobytes exactly.",  # LIE
            },
            "imposter": "Core",
            "hint": "1 Megabyte is 1,024 Kilobytes, not 500!",
        },
        {
            "topic": "Geometry Facts",
            "statements": {
                "Vector": "All internal angles of a triangle sum to 180°.",
                "Matrix": "A hexagon has 6 straight sides.",
                "Axiom": (
                    "A square has internal angles summing to 540°."
                ),  # LIE
            },
            "imposter": "Axiom",
            "hint": "A square's internal angles sum to 360° (4 x 90°)!",
        },
        {
            "topic": "Logic Clues",
            "statements": {
                "Agent X": "If it rains, the grass gets wet.",
                "Agent Y": "An electric train moving North has smoke blowing South.",  # LIE
                "Agent Z": "Ice floats because it is less dense than water.",
            },
            "imposter": "Agent Y",
            "hint": "Electric trains don't produce smoke!",
        },
    ]
    st.session_state.imposter_data = random.choice(scenarios)
    st.session_state.last_mode = "Hard"

  data = st.session_state.imposter_data
  st.markdown(f"**Topic:** `{data['topic']}`")

  cols = st.columns(3)
  suspects = list(data["statements"].keys())

  for idx, name in enumerate(suspects):
    with cols[idx]:
      st.markdown(
          f"<div class='suspect-box'><h3>👤 {name}</h3><p><i>\"{data['statements'][name]}\"</i></p></div>",
          unsafe_allow_html=True,
      )
      if st.button(f"Accuse {name}", key=f"accuse_{name}"):
        if name == data["imposter"]:
          play_sound("win")
          st.balloons()
          st.session_state.points += 200
          st.success(
              f"🎉 **CORRECT! {name} WAS THE IMPOSTER!** (+200 Points)\n\n*Reason:* "
              f" {data['hint']}"
          )
          save_game_data(
              player.username, "WIN", "Hard Imposter", st.session_state.points
          )
        else:
          if st.session_state.has_shield:
            st.session_state.has_shield = False
            st.info(
                f"🛡️ Wrong guess! {name} was innocent, but your Ghost Shield"
                " saved your points!"
            )
          else:
            play_sound("lose")
            st.session_state.points = max(0, st.session_state.points - 50)
            st.error(
                f"❌ WRONG! {name} was telling the truth! The imposter was"
                f" {data['imposter']}. (-50 Points)"
            )
            save_game_data(
                player.username,
                "LOSS",
                "Hard Imposter",
                st.session_state.points,
            )

        st.session_state.imposter_data = None  # Reset scenario
        st.rerun()


# ==========================================
# 📊 ANALYTICS & HISTORY SECTION
# ==========================================
st.markdown("---")
left_col, right_col = st.columns([2, 1])

with left_col:
  st.subheader("📜 Game History (Pandas)")
  history_data = load_game_data()

  if history_data:
    df = pd.DataFrame(history_data)
    st.dataframe(df.tail(8), use_container_width=True)
  else:
    st.info("No game history recorded yet. Play a round!")

with right_col:
  st.subheader("📈 Quick Stats")
  if history_data:
    df = pd.DataFrame(history_data)
    total_games = len(df)
    total_wins = len(df[df["Result"].str.contains("WIN")])
    win_rate = round((total_wins / total_games) * 100, 1)

    st.metric(label="Total Rounds Played", value=total_games)
    st.metric(label="Win Rate", value=f"{win_rate}%")
  else:
    st.write("Play rounds to see your statistics!")