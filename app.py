import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import math
import re


def show_dashboard():
    # 1. Player Header
    user = st.session_state.user
    
    st.title(f"👋 Welcome Back, {user['username']}!")
    
    # Level & XP Progress Bar
    next_level_xp = user["level"] * 100
    xp_progress = min(1.0, user["xp"] / next_level_xp)
    
    col_level, col_bar = st.columns([1, 4])
    with col_level:
        st.subheader(f"⭐ Level {user['level']}")
    with col_bar:
        st.caption(f"XP: {user['xp']} / {next_level_xp}")
        st.progress(xp_progress)

    st.divider()

    # 2. Economy & Stats Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🪙 Coins Balance", user["coins"])
    m2.metric("🔑 Mystery Keys", user["inventory"].count("Key"))
    m3.metric("🎒 Items Owned", len(user["inventory"]))
    m4.metric("🏆 Global Rank", "#42")

    st.divider()

    # 3. Daily Login Reward Claim System
    st.subheader("🎁 Daily Rewards")
    if not user.get("daily_claimed", False):
        if st.button("✨ Claim Daily Bonus (+100 Coins)", type="primary"):
            user["coins"] += 100
            user["daily_claimed"] = True
            st.toast("🎉 Claimed 100 Daily Coins!", icon="🪙")
            st.rerun()
    else:
        st.success("✅ Today's daily reward already claimed! Come back tomorrow.")

    st.divider()

    # 4. Quick Game Launcher & Daily Missions
    c_left, c_right = st.columns([2, 1])

    with c_left:
        st.subheader("🎮 Featured Games")
        
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            with st.container(border=True):
                st.markdown("### 🚪 Mystery Door")
                st.caption("Pick the right door, avoid traps, win loot!")
                if st.button("Play Now", key="btn_door"):
                    st.session_state.current_page = "Mystery Door"
                    st.rerun()

            with st.container(border=True):
                st.markdown("### 🕵️ Find Imposter")
                st.caption("Locate the imposter in minimum clicks.")
                if st.button("Play Now", key="btn_imposter"):
                    st.session_state.current_page = "Find Imposter"
                    st.rerun()

        with g_col2:
            with st.container(border=True):
                st.markdown("### ⌨️ Typing Race")
                st.caption("Test your speed against time.")
                if st.button("Play Now", key="btn_typing"):
                    st.session_state.current_page = "Typing Race"
                    st.rerun()

            with st.container(border=True):
                st.markdown("### 🧩 Memory Match")
                st.caption("Flip cards & find matching pairs.")
                if st.button("Play Now", key="btn_memory"):
                    st.session_state.current_page = "Memory Match"
                    st.rerun()

    with c_right:
        st.subheader("📜 Daily Quests")
        with st.container(border=True):
            st.markdown("✔️ **First Win of the Day**")
            st.caption("Reward: +50 Coins | +20 XP")
            
            st.markdown("⏳ **Play 3 Mini-Games** (1/3)")
            st.caption("Reward: +100 Coins")
            
            st.markdown("⏳ **Crack 1 Code Breaker** (0/1)")
            st.caption("Reward: +1 Mystery Key")
# ==============================================================================
# 🧠 LESSON REQUIREMENT 1: OOP CLASSES
# ==============================================================================

class Dragon:
    """OOP Class representing a Dragon object."""
    def __init__(self, name, element, hp, attack):
        self.name = name
        self.element = element
        self.hp = hp
        self.attack = attack

class Player:
    """OOP Class representing Global Player State."""
    def __init__(self):
        self.gold = 100
        self.dragons = [Dragon("Flame Hatchling", "🔥 Fire", 80, 15)]
        self.scores_history = [10, 20, 30]

    def add_gold(self, amount):
        self.gold += amount
        self.scores_history.append(amount)

# Initialize OOP State
if "player" not in st.session_state:
    st.session_state.player = Player()

player = st.session_state.player

# ==============================================================================
# 📊 LESSON REQUIREMENTS: STREAMLIT, PANDAS, NUMPY & REGEX
# ==============================================================================

st.set_page_config(page_title="multi-game", page_icon="🎮", layout="wide")

st.title("🎮 multi-game -f")

# Sidebar Data Analytics
st.sidebar.header("📊 Player Stats Lab")
st.sidebar.metric("🪙 Arcade Gold", f"{player.gold}")

# Pandas DataFrame
st.sidebar.subheader("🐉 Dragon Squad (Pandas)")
dragon_df = pd.DataFrame([{"Name": d.name, "Element": d.element, "HP": d.hp, "ATK": d.attack} for d in player.dragons])
st.sidebar.dataframe(dragon_df)

# NumPy Analytics
st.sidebar.subheader("🧮 Score Analytics (NumPy)")
scores_arr = np.array(player.scores_history)
st.sidebar.write(f"- **Mean Score:** `{np.mean(scores_arr):.1f}`")
st.sidebar.write(f"- **Max Score:** `{np.max(scores_arr)}`")

# Regex Input Validation
st.sidebar.subheader("🕵️ Crewmate Verification (Regex)")
username = st.sidebar.text_input("Enter Player Tag:")
if username:
    if re.match(r"^[A-Z][a-z]+$", username):
        st.sidebar.success("Valid Tag!")
    else:
        st.sidebar.warning("Tag must start with a Capital letter!")

# ==============================================================================
# 🎮 FULL WORKING 8-IN-1 GAME ENGINE (WITH AUDIO UNLOCK & FOCUS)
# ==============================================================================

arcade_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; padding: 0; background-color: #0f172a; font-family: 'Segoe UI', sans-serif; color: white; text-align: center; user-select: none; }
        .grid-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 15px; }
        .game-card { background: #1e293b; border: 2px solid #3b82f6; border-radius: 10px; padding: 15px; cursor: pointer; transition: 0.2s; }
        .game-card:hover { transform: scale(1.05); background: #2563eb; }
        canvas { background: #020617; border: 3px solid #3b82f6; border-radius: 10px; display: block; margin: 10px auto; outline: none; }
        .btn { background: #eab308; color: #000; font-weight: bold; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; margin-bottom: 10px; }
        .btn:hover { background: #fde047; }
    </style>
</head>
<body>

    <div id="menu-grid" class="grid-container">
        <div class="game-card" onclick="startGame('racer')">🏎️<br><b>Hill Climb Racer</b><br><small>Drive & Collect</small></div>
        <div class="game-card" onclick="startGame('tiles')">🎵<br><b>Tiles Hop</b><br><small>Press 1, 2, 3</small></div>
        <div class="game-card" onclick="startGame('ox')">❌⭕<br><b>OX Tic-Tac-Toe</b><br><small>Play vs AI</small></div>
        <div class="game-card" onclick="startGame('candy')">🍬<br><b>Candy Match</b><br><small>Tap Matching Pair</small></div>
        <div class="game-card" onclick="startGame('imposter')">🕵️<br><b>Guess Imposter</b><br><small>Find Suspicious</small></div>
        <div class="game-card" onclick="startGame('dragon')">🐉<br><b>Dragon Arena</b><br><small>Boss Battle</small></div>
        <div class="game-card" onclick="startGame('chess')">♟️<br><b>Chess Tactics</b><br><small>Pick Move</small></div>
        <div class="game-card" onclick="startGame('puzzle')">🧩<br><b>Math Puzzle</b><br><small>Logic Solver</small></div>
    </div>

    <div id="game-view" style="display: none;">
        <button class="btn" onclick="showMenu()">⬅️ Back to Arcade Menu</button>
        <canvas id="gameCanvas" width="750" height="400" tabindex="1"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        let currentGame = "";
        let keys = {};
        let audioUnlocked = false;

        // Key listeners attached to window & canvas for instant response
        window.addEventListener("keydown", e => { keys[e.key] = true; });
        window.addEventListener("keyup", e => { keys[e.key] = false; });

        // Web Audio Context setup
        let audioCtx = null;

        function initAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            audioUnlocked = true;
        }

        function playSound(freq, duration) {
            if (!audioCtx || audioCtx.state !== 'running') return;
            try {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.value = freq;
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
                osc.stop(audioCtx.currentTime + duration);
            } catch(e) {}
        }

        // Canvas Click Listener & Audio Unlocker
        canvas.addEventListener("click", function(e) {
            initAudio();
            canvas.focus();
            const rect = canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;
            handleCanvasClick(mx, my);
        });

        // Game States
        let racer = { x: 100, y: 200, score: 0, coins: [{x: 400, y: 150}, {x: 600, y: 250}], obs: [{x: 750, y: 200, spd: 4}] };
        let tiles = { falling: [], score: 0 };
        let oxBoard = ["", "", "", "", "", "", "", "", ""];
        let imposterPos = Math.floor(Math.random() * 4);
        let dragonHp = 100;

        // Candy Match Logic
        let candyItems = ["🍬", "🍭", "🍬", "🍫"];
        let candySelected = -1;
        let candyScore = 0;

        function shuffleCandies() {
            candyItems = ["🍬", "🍭", "🍬", "🍫"].sort(() => Math.random() - 0.5);
            candySelected = -1;
        }

        function startGame(name) {
            currentGame = name;
            document.getElementById("menu-grid").style.display = "none";
            document.getElementById("game-view").style.display = "block";
            
            // Auto focus canvas so key controls work right away
            setTimeout(() => canvas.focus(), 100);

            if (name === 'ox') oxBoard = ["", "", "", "", "", "", "", "", ""];
            if (name === 'dragon') dragonHp = 100;
            if (name === 'candy') shuffleCandies();
            if (name === 'racer') racer = { x: 100, y: 200, score: 0, coins: [{x: 400, y: 150}, {x: 600, y: 250}], obs: [{x: 750, y: 200, spd: 4}] };
            if (name === 'tiles') tiles = { falling: [], score: 0 };

            requestAnimationFrame(runLoop);
        }

        function showMenu() {
            currentGame = "";
            document.getElementById("menu-grid").style.display = "grid";
            document.getElementById("game-view").style.display = "none";
        }

        function handleCanvasClick(mx, my) {
            // 🍬 CANDY MATCH
            if (currentGame === 'candy') {
                for (let i = 0; i < candyItems.length; i++) {
                    let rx = 100 + i * 140;
                    if (mx > rx && mx < rx + 100 && my > 130 && my < 230) {
                        playSound(500, 0.1);
                        if (candySelected === -1) {
                            candySelected = i;
                        } else {
                            if (candySelected !== i && candyItems[candySelected] === candyItems[i]) {
                                playSound(880, 0.25);
                                candyScore += 10;
                                alert("🎉 Match Found! +10 Score!");
                                shuffleCandies();
                            } else {
                                playSound(150, 0.2);
                                candySelected = -1;
                            }
                        }
                    }
                }
            } 
            // ❌⭕ TIC TAC TOE
            else if (currentGame === 'ox') {
                for (let i = 0; i < 9; i++) {
                    let rx = 250 + (i % 3) * 85;
                    let ry = 90 + Math.floor(i / 3) * 85;
                    if (mx > rx && mx < rx + 75 && my > ry && my < ry + 75 && oxBoard[i] === "") {
                        oxBoard[i] = "❌";
                        playSound(600, 0.1);
                        let empty = oxBoard.map((v, idx) => v === "" ? idx : null).filter(v => v !== null);
                        if (empty.length > 0) oxBoard[empty[Math.floor(Math.random() * empty.length)]] = "⭕";
                        break;
                    }
                }
            } 
            // 🕵️ IMPOSTER
            else if (currentGame === 'imposter') {
                for (let i = 0; i < 4; i++) {
                    let rx = 90 + i * 150;
                    if (mx > rx && mx < rx + 110 && my > 140 && my < 250) {
                        if (i === imposterPos) {
                            playSound(880, 0.2);
                            alert("🎉 Correct! You found the Imposter!");
                            imposterPos = Math.floor(Math.random() * 4);
                        } else {
                            playSound(150, 0.2);
                            alert("❌ Innocent Crewmate!");
                        }
                    }
                }
            } 
            // 🐉 DRAGON ARENA
            else if (currentGame === 'dragon') {
                if (mx > 275 && mx < 475 && my > 280 && my < 340) {
                    dragonHp -= 20;
                    playSound(400, 0.1);
                    if (dragonHp <= 0) {
                        playSound(880, 0.3);
                        alert("🐉 Dragon Defeated!");
                        dragonHp = 100;
                    }
                }
            } 
            // ♟️ CHESS TACTICS
            else if (currentGame === 'chess') {
                if (mx > 250 && mx < 500 && my > 280 && my < 340) {
                    playSound(880, 0.2);
                    alert("♟️ Checkmate Delivered!");
                }
            } 
            // 🧩 MATH PUZZLE
            else if (currentGame === 'puzzle') {
                if (mx > 250 && mx < 500 && my > 250 && my < 310) {
                    playSound(880, 0.2);
                    alert("🧩 Math Solved!");
                }
            }
        }

        function runLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Audio Helper Banner
            if (!audioUnlocked) {
                ctx.fillStyle = "#eab308"; ctx.font = "14px Arial";
                ctx.fillText("🔊 Click canvas once to enable sound effects!", 250, 20);
            }

            // 🏎️ 1. RACER
            if (currentGame === 'racer') {
                if ((keys["ArrowUp"] || keys["w"]) && racer.y > 20) racer.y -= 5;
                if ((keys["ArrowDown"] || keys["s"]) && racer.y < 380) racer.y += 5;
                if ((keys["ArrowLeft"] || keys["a"]) && racer.x > 20) racer.x -= 5;
                if ((keys["ArrowRight"] || keys["d"]) && racer.x < 730) racer.x += 5;

                ctx.fillStyle = "#3b82f6"; ctx.beginPath(); ctx.arc(racer.x, racer.y, 16, 0, Math.PI*2); ctx.fill();

                ctx.fillStyle = "#eab308";
                racer.coins.forEach(c => {
                    ctx.beginPath(); ctx.arc(c.x, c.y, 10, 0, Math.PI*2); ctx.fill();
                    if (Math.hypot(racer.x - c.x, racer.y - c.y) < 26) {
                        playSound(880, 0.1);
                        racer.score += 5;
                        c.x = 400 + Math.random()*300;
                        c.y = 50 + Math.random()*300;
                    }
                });

                ctx.fillStyle = "#ef4444";
                racer.obs.forEach(o => {
                    o.x -= o.spd;
                    if (o.x < -20) { o.x = 750; o.y = 50 + Math.random()*300; }
                    ctx.fillRect(o.x, o.y, 25, 25);
                    if (Math.abs(racer.x - o.x) < 22 && Math.abs(racer.y - o.y) < 22) {
                        playSound(150, 0.2);
                        o.x = 750;
                    }
                });
                ctx.fillStyle = "#ffffff"; ctx.font = "16px Arial";
                ctx.fillText("🕹️ Arrow/WASD Keys to move! Score: " + racer.score, 20, 40);
            }

            // 🎵 2. TILES HOP
            else if (currentGame === 'tiles') {
                if (Math.random() < 0.03) tiles.falling.push({ col: Math.floor(Math.random() * 3), y: 0 });
                ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 3;
                ctx.beginPath(); ctx.moveTo(150, 320); ctx.lineTo(600, 320); ctx.stroke();

                tiles.falling.forEach((t, idx) => {
                    t.y += 3;
                    ctx.fillStyle = "#a855f7";
                    ctx.fillRect(200 + t.col * 130, t.y, 90, 35);

                    if (t.y > 290 && t.y < 340) {
                        if ((t.col === 0 && keys["1"]) || (t.col === 1 && keys["2"]) || (t.col === 2 && keys["3"])) {
                            playSound(700, 0.1);
                            tiles.score += 10;
                            tiles.falling.splice(idx, 1);
                        }
                    }
                });
                ctx.fillStyle = "#ffffff"; ctx.font = "16px Arial";
                ctx.fillText("🎵 Press 1, 2, or 3 when tile hits green line! Score: " + tiles.score, 20, 40);
            }

            // ❌⭕ 3. TIC-TAC-TOE
            else if (currentGame === 'ox') {
                ctx.fillStyle = "#ffffff"; ctx.font = "20px Arial";
                ctx.fillText("❌⭕ Tap a square to play vs AI", 250, 50);
                for (let i = 0; i < 9; i++) {
                    let rx = 250 + (i % 3) * 85;
                    let ry = 90 + Math.floor(i / 3) * 85;
                    ctx.fillStyle = "#1e293b"; ctx.fillRect(rx, ry, 75, 75);
                    ctx.fillStyle = oxBoard[i] === "❌" ? "#eab308" : "#ef4444";
                    ctx.font = "bold 32px Arial"; ctx.fillText(oxBoard[i], rx + 22, ry + 50);
                }
            }

            // 🍬 4. CANDY MATCH PAIR
            else if (currentGame === 'candy') {
                ctx.fillStyle = "#ffffff"; ctx.font = "22px Arial";
                ctx.fillText("🍬 Tap matching candies! Score: " + candyScore, 200, 50);

                candyItems.forEach((c, idx) => {
                    let rx = 100 + idx * 140;
                    ctx.fillStyle = (candySelected === idx) ? "#2563eb" : "#1e293b";
                    ctx.strokeStyle = "#3b82f6";
                    ctx.lineWidth = 2;
                    ctx.fillRect(rx, 130, 100, 100);
                    ctx.strokeRect(rx, 130, 100, 100);

                    ctx.font = "50px Arial";
                    ctx.fillText(c, rx + 22, 198);
                });
            }

            // 🐉 5. DRAGON ARENA
            else if (currentGame === 'dragon') {
                ctx.fillStyle = "#ffffff"; ctx.font = "22px Arial";
                ctx.fillText("🐉 Dragon Boss Battle", 270, 50);
                ctx.fillStyle = "#ef4444"; ctx.fillRect(220, 80, 300, 20);
                ctx.fillStyle = "#22c55e"; ctx.fillRect(220, 80, (dragonHp / 100) * 300, 20);

                ctx.fillStyle = "#2563eb"; ctx.fillRect(275, 280, 200, 60);
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 20px Arial";
                ctx.fillText("⚔️ ATTACK!", 320, 318);
            }

            // 🕵️ 6. GUESS IMPOSTER
            else if (currentGame === 'imposter') {
                ctx.fillStyle = "#ffffff"; ctx.font = "20px Arial";
                ctx.fillText("🕵️ Tap the suspicious crewmate!", 230, 50);
                let colors = ["#ef4444", "#3b82f6", "#22c55e", "#eab308"];
                for (let i = 0; i < 4; i++) {
                    ctx.fillStyle = colors[i];
                    ctx.fillRect(90 + i * 150, 140, 110, 110);
                }
            }

            // ♟️ 7. CHESS TACTICS
            else if (currentGame === 'chess') {
                ctx.fillStyle = "#ffffff"; ctx.font = "22px Arial";
                ctx.fillText("♟️ Chess Tactics: Find Checkmate", 210, 50);
                ctx.font = "60px Arial"; ctx.fillText("♚ ♛ ♞", 300, 180);

                ctx.fillStyle = "#22c55e"; ctx.fillRect(250, 280, 250, 60);
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 20px Arial";
                ctx.fillText("Execute Move ♟️", 295, 318);
            }

            // 🧩 8. MATH PUZZLE
            else if (currentGame === 'puzzle') {
                ctx.fillStyle = "#ffffff"; ctx.font = "22px Arial";
                ctx.fillText("🧩 Solve: 7 + 5 = ?", 280, 80);

                ctx.fillStyle = "#a855f7"; ctx.fillRect(250, 250, 250, 60);
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 20px Arial";
                ctx.fillText("Select 12", 330, 288);
            }

            if (currentGame !== "") requestAnimationFrame(runLoop);
        }
    </script>
</body>
</html>
"""

components.html(arcade_html, height=520)