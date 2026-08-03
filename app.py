import math
import re
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# ------------------------------------------------------------------------------
# 1. PAGE SETUP & DASHBOARD HEADER
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Arcade Dashboard", page_icon="🎮", layout="wide")


def show_dashboard():
    if "user" not in st.session_state:
        st.session_state.user = {"username": "Captain", "level": 1, "xp": 40}

    user = st.session_state.user
    st.title(f"👋 Welcome Back, {user['username']}!")

    # Progress Bar
    next_level_xp = user["level"] * 100
    xp_progress = min(1.0, user["xp"] / next_level_xp)
    st.progress(
        xp_progress,
        text=f"Level {user['level']} Progress ({user['xp']}/{next_level_xp} XP)",
    )
    st.divider()


show_dashboard()

# Sidebar Setup
st.sidebar.subheader("🕵️ Crewmate Verification (Regex)")
username_input = st.sidebar.text_input("Enter Player Tag:")
if username_input:
    if re.match(r"^[A-Z][a-z]+$", username_input):
        st.sidebar.success("Valid Tag!")
        st.session_state.user["username"] = username_input
    else:
        st.sidebar.warning("Tag must start with a Capital letter!")

st.sidebar.header("🏆 Player Dashboard")
st.sidebar.metric("Target Score", "100 pts")

# ------------------------------------------------------------------------------
# 2. MASTER HTML & JAVASCRIPT GAME ENGINE (8-IN-1 ARCADE)
# ------------------------------------------------------------------------------
arcade_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { 
            margin: 0; 
            padding: 0; 
            background-color: #0f172a; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            color: white; 
            text-align: center; 
            user-select: none; 
        }
        .grid-container { 
            display: grid; 
            grid-template-columns: repeat(4, 1fr); 
            gap: 12px; 
            padding: 15px; 
        }
        .game-card { 
            background: #1e293b; 
            border: 2px solid #3b82f6; 
            border-radius: 10px; 
            padding: 15px; 
            cursor: pointer; 
            transition: transform 0.2s, background-color 0.2s; 
        }
        .game-card:hover { 
            transform: scale(1.04); 
            background: #2563eb; 
        }
        canvas { 
            background: #020617; 
            border: 3px solid #3b82f6; 
            border-radius: 10px; 
            display: block; 
            margin: 10px auto; 
            outline: none; 
        }
        .btn { 
            background: #eab308; 
            color: #000; 
            font-weight: bold; 
            padding: 8px 16px; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer; 
            margin-bottom: 10px; 
        }
        .btn:hover { 
            background: #fde047; 
        }
    </style>
</head>
<body>

    <!-- MAIN MENU GRID -->
    <div id="menu-grid" class="grid-container">
        <div class="game-card" onclick="startGame('racer')">🏎️<br><b>Hill Climb Racer</b><br><small>Drive & Collect</small></div>
        <div class="game-card" onclick="startGame('tiles')">🎵<br><b>Tiles Hop</b><br><small>Press 1, 2, 3</small></div>
        <div class="game-card" onclick="startGame('ox')">❌⭕<br><b>OX Tic-Tac-Toe</b><br><small>Play vs AI</small></div>
        <div class="game-card" onclick="startGame('candy')">🍬<br><b>Candy Match</b><br><small>Tap Matching Pair</small></div>
        <div class="game-card" onclick="startGame('imposter')">🕵️<br><b>Guess Imposter</b><br><small>Find Suspicious</small></div>
        <div class="game-card" onclick="startGame('dragon')">🐉<br><b>Dragon Arena</b><br><small>Boss Battle</small></div>
        <div class="game-card" onclick="startGame('Fish')">🎣<br><b>Fish Catcher</b><br><small>Deep Sea Fishing</small></div>
        <div class="game-card" onclick="startGame('puzzle')">🧩<br><b>Math Puzzle</b><br><small>Logic Solver</small></div>
    </div>

    <!-- CANVAS GAME VIEW -->
    <div id="game-view" style="display: none;">
        <button class="btn" onclick="showMenu()">⬅️ Back to Arcade Menu</button>
        <canvas id="gameCanvas" width="750" height="420" tabindex="1"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        let currentGame = "";
        let keys = {};
        let audioUnlocked = false;

        // Key Listeners
        window.addEventListener("keydown", e => { 
            keys[e.key] = true; 
            if (e.key === " " || e.code === "Space") {
                if (currentGame === 'Fish') triggerHook();
            }
        });
        window.addEventListener("keyup", e => { keys[e.key] = false; });

        // Audio Synth Setup
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

        canvas.addEventListener("click", function(e) {
            initAudio();
            canvas.focus();
            const rect = canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;
            handleCanvasClick(mx, my);
        });

        // Minigame States
        let racer = { x: 100, y: 200, score: 0, coins: [{x: 400, y: 150}, {x: 600, y: 250}], obs: [{x: 750, y: 200, spd: 4}] };
        let tiles = { falling: [], score: 0 };
        let oxBoard = ["", "", "", "", "", "", "", "", ""];
        let imposterPos = Math.floor(Math.random() * 4);
        let dragonHp = 100;
        let candyItems = ["🍬", "🍭", "🍬", "🍫"];
        let candySelected = -1;
        let candyScore = 0;

        // Deep Fishing Game State
        let fishScore = 0;
        let fishTimeLeft = 60;
        let fishGameOver = false;
        let fishTimerInterval = null;
        const boat = { x: 340, y: 40, width: 70, height: 20, speed: 5 };
        const hook = { x: 375, y: 60, startY: 60, maxDepth: 380, speed: 6, state: "idle", caughtFish: null };
        const fishTypes = [
            { name: "Small Fry", color: "#facc15", size: 14, speed: 2.5, points: 10 },
            { name: "Bass", color: "#f97316", size: 20, speed: 1.8, points: 20 },
            { name: "Rare Blue", color: "#a855f7", size: 26, speed: 3.0, points: 50 },
            { name: "Golden Fish", color: "#ef4444", size: 18, speed: 3.5, points: 100 }
        ];
        let fishes = [];

        function spawnFish() {
            if (fishes.length < 8) {
                const type = fishTypes[Math.floor(Math.random() * fishTypes.length)];
                const dir = Math.random() < 0.5 ? 1 : -1;
                fishes.push({
                    x: dir === 1 ? -30 : canvas.width + 30,
                    y: 110 + Math.random() * 260,
                    dir: dir,
                    ...type
                });
            }
        }

        function triggerHook() {
            if (fishGameOver) return;
            if (hook.state === "idle") hook.state = "dropping";
            else if (hook.state === "dropping") hook.state = "reeling";
        }

        function shuffleCandies() {
            candyItems = ["🍬", "🍭", "🍬", "🍫"].sort(() => Math.random() - 0.5);
            candySelected = -1;
        }

        function startGame(name) {
            currentGame = name;
            document.getElementById("menu-grid").style.display = "none";
            document.getElementById("game-view").style.display = "block";
            setTimeout(() => canvas.focus(), 100);

            if (name === 'ox') oxBoard = ["", "", "", "", "", "", "", "", ""];
            if (name === 'dragon') dragonHp = 100;
            if (name === 'candy') shuffleCandies();
            if (name === 'racer') racer = { x: 100, y: 200, score: 0, coins: [{x: 400, y: 150}, {x: 600, y: 250}], obs: [{x: 750, y: 200, spd: 4}] };
            if (name === 'tiles') tiles = { falling: [], score: 0 };
            
            if (name === 'Fish') {
                fishScore = 0; fishTimeLeft = 60; fishGameOver = false;
                fishes = []; hook.state = "idle"; hook.y = hook.startY; hook.caughtFish = null; boat.x = 340;
                if(fishTimerInterval) clearInterval(fishTimerInterval);
                fishTimerInterval = setInterval(() => {
                    if (currentGame === 'Fish' && !fishGameOver && fishTimeLeft > 0) {
                        fishTimeLeft--;
                        if (fishTimeLeft === 0) fishGameOver = true;
                    }
                }, 1000);
            }

            requestAnimationFrame(runLoop);
        }

        function showMenu() {
            currentGame = "";
            if(fishTimerInterval) clearInterval(fishTimerInterval);
            document.getElementById("menu-grid").style.display = "grid";
            document.getElementById("game-view").style.display = "none";
        }

        function handleCanvasClick(mx, my) {
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
            } else if (currentGame === 'ox') {
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
            } else if (currentGame === 'imposter') {
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
            } else if (currentGame === 'dragon') {
                if (mx > 275 && mx < 475 && my > 280 && my < 340) {
                    dragonHp -= 20;
                    playSound(400, 0.1);
                    if (dragonHp <= 0) {
                        playSound(880, 0.3);
                        alert("🐉 Dragon Defeated!");
                        dragonHp = 100;
                    }
                }
            } else if (currentGame === 'Fish') {
                triggerHook();
            } else if (currentGame === 'puzzle') {
                if (mx > 250 && mx < 500 && my > 250 && my < 310) {
                    playSound(880, 0.2);
                    alert("🧩 Math Solved!");
                }
            }
        }

        function runLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (!audioUnlocked) {
                ctx.fillStyle = "#eab308"; ctx.font = "14px Arial";
                ctx.fillText("🔊 Click canvas once to enable sound effects!", 250, 20);
            }

            // 1. RACER GAME
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
                        playSound(880, 0.1); racer.score += 5;
                        c.x = 400 + Math.random()*300; c.y = 50 + Math.random()*300;
                    }
                });

                ctx.fillStyle = "#ef4444";
                racer.obs.forEach(o => {
                    o.x -= o.spd;
                    if (o.x < -20) { o.x = 750; o.y = 50 + Math.random()*300; }
                    ctx.fillRect(o.x, o.y, 25, 25);
                    if (Math.abs(racer.x - o.x) < 22 && Math.abs(racer.y - o.y) < 22) { playSound(150, 0.2); o.x = 750; }
                });
                ctx.fillStyle = "#ffffff"; ctx.font = "16px Arial";
                ctx.fillText("🕹️ Arrow/WASD Keys to move! Score: " + racer.score, 20, 40);

            // 2. TILES HOP
            } else if (currentGame === 'tiles') {
                if (Math.random() < 0.03) tiles.falling.push({ col: Math.floor(Math.random() * 3), y: 0 });
                ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 3;
                ctx.beginPath(); ctx.moveTo(150, 320); ctx.lineTo(600, 320); ctx.stroke();

                tiles.falling.forEach((t, idx) => {
                    t.y += 3; ctx.fillStyle = "#a855f7";
                    ctx.fillRect(200 + t.col * 130, t.y, 90, 35);
                    if (t.y > 290 && t.y < 340) {
                        if ((t.col === 0 && keys["1"]) || (t.col === 1 && keys["2"]) || (t.col === 2 && keys["3"])) {
                            playSound(700, 0.1); tiles.score += 10; tiles.falling.splice(idx, 1);
                        }
                    }
                });
                ctx.fillStyle = "#ffffff"; ctx.font = "16px Arial";
                ctx.fillText("🎵 Press 1, 2, or 3 when tile hits green line! Score: " + tiles.score, 20, 40);

            // 3. OX TIC-TAC-TOE
            } else if (currentGame === 'ox') {
                ctx.fillStyle = "#ffffff"; ctx.font = "20px Arial";
                ctx.fillText("❌⭕ Tap a square to play vs AI", 250, 50);
                for (let i = 0; i < 9; i++) {
                    let rx = 250 + (i % 3) * 85;
                    let ry = 90 + Math.floor(i / 3) * 85;
                    ctx.fillStyle = "#1e293b"; ctx.fillRect(rx, ry, 75, 75);
                    ctx.fillStyle = oxBoard[i] === "❌" ? "#eab308" : "#ef4444";
                    ctx.font = "bold 32px Arial"; ctx.fillText(oxBoard[i], rx + 22, ry + 50);
                }

            // 4. CANDY MATCH
            } else if (currentGame === 'candy') {
                ctx.fillStyle = "#ffffff"; ctx.font = "22px Arial";
                ctx.fillText("🍬 Tap matching candies! Score: " + candyScore, 200, 50);
                candyItems.forEach((c, idx) => {
                    let rx = 100 + idx * 140;
                    ctx.fillStyle = (candySelected === idx) ? "#2563eb" : "#1e293b";
                    ctx.strokeStyle = "#3b82f6"; ctx.lineWidth = 2;
                    ctx.fillRect(rx, 130, 100, 100); ctx.strokeRect(rx, 130, 100, 100);
                    ctx.font = "50px Arial"; ctx.fillText(c, rx + 22, 198);
                });

            // 5. GUESS IMPOSTER
            } else if (currentGame === 'imposter') {
                ctx.fillStyle = "#ffffff"; ctx.font = "20px Arial";
                ctx.fillText("🕵️ Tap the suspicious crewmate!", 230, 50);
                let colors = ["#ef4444", "#3b82f6", "#22c55e", "#eab308"];
                for (let i = 0; i < 4; i++) {
                    ctx.fillStyle = colors[i];
                    ctx.fillRect(90 + i * 150, 140, 110, 110);
                }

            // 6. DRAGON ARENA
            } else if (currentGame === 'dragon') {
                ctx.fillStyle = "#ffffff"; ctx.font = "22px Arial";
                ctx.fillText("🐉 Dragon Boss HP: " + dragonHp, 280, 50);
                ctx.fillStyle = "#ef4444"; ctx.fillRect(200, 80, dragonHp * 3.5, 25);
                ctx.fillStyle = "#22c55e"; ctx.fillRect(275, 280, 200, 60);
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 20px Arial"; ctx.fillText("ATTACK!", 330, 318);

            // 7. FISH CATCHER (DEEP SEA ENGINE)
            } else if (currentGame === 'Fish') {
                if (!fishGameOver) {
                    if (hook.state === "idle") {
                        if ((keys["ArrowLeft"] || keys["a"] || keys["A"]) && boat.x > 10) boat.x -= boat.speed;
                        if ((keys["ArrowRight"] || keys["d"] || keys["D"]) && boat.x < canvas.width - boat.width - 10) boat.x += boat.speed;
                        hook.x = boat.x + boat.width / 2;
                    }
                    if (hook.state === "dropping") {
                        hook.y += hook.speed;
                        if (hook.y >= hook.maxDepth) hook.state = "reeling";
                    } else if (hook.state === "reeling") {
                        hook.y -= hook.speed;
                        if (hook.caughtFish) { hook.caughtFish.x = hook.x; hook.caughtFish.y = hook.y + 10; }
                        if (hook.y <= hook.startY) {
                            hook.state = "idle"; hook.y = hook.startY;
                            if (hook.caughtFish) { playSound(880, 0.2); fishScore += hook.caughtFish.points; hook.caughtFish = null; }
                        }
                    }

                    fishes.forEach((f, idx) => {
                        if (f !== hook.caughtFish) f.x += f.speed * f.dir;
                        if (hook.state === "dropping" && !hook.caughtFish) {
                            if (Math.hypot(hook.x - f.x, hook.y - f.y) < f.size + 8) {
                                hook.caughtFish = f; hook.state = "reeling"; playSound(500, 0.15);
                            }
                        }
                        if ((f.dir === 1 && f.x > canvas.width + 50) || (f.dir === -1 && f.x < -50)) {
                            if (f !== hook.caughtFish) fishes.splice(idx, 1);
                        }
                    });
                    spawnFish();
                }

                // Water Background
                ctx.fillStyle = "#38bdf8"; ctx.fillRect(0, 0, canvas.width, 50);
                ctx.fillStyle = "#0284c7"; ctx.fillRect(0, 50, canvas.width, 4);

                // Boat & Hook
                ctx.fillStyle = "#78350f"; ctx.beginPath();
                ctx.moveTo(boat.x, boat.y); ctx.lineTo(boat.x + boat.width, boat.y);
                ctx.lineTo(boat.x + boat.width - 12, boat.y + boat.height); ctx.lineTo(boat.x + 12, boat.y + boat.height);
                ctx.closePath(); ctx.fill();

                ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 1.5;
                ctx.beginPath(); ctx.moveTo(hook.x, hook.startY); ctx.lineTo(hook.x, hook.y); ctx.stroke();
                ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 2.5;
                ctx.beginPath(); ctx.arc(hook.x - 4, hook.y, 4, 0, Math.PI); ctx.stroke();

                // Render Swimming Fishes
                fishes.forEach(f => {
                    ctx.fillStyle = f.color; ctx.beginPath();
                    ctx.ellipse(f.x, f.y, f.size, f.size / 1.6, 0, 0, Math.PI * 2); ctx.fill();
                    ctx.beginPath(); let tailX = f.x - (f.size * f.dir);
                    ctx.moveTo(tailX, f.y); ctx.lineTo(tailX - (8 * f.dir), f.y - 6); ctx.lineTo(tailX - (8 * f.dir), f.y + 6);
                    ctx.closePath(); ctx.fill();
                    ctx.fillStyle = "#000"; ctx.beginPath();
                    ctx.arc(f.x + (f.size / 2 * f.dir), f.y - 2, 2, 0, Math.PI * 2); ctx.fill();
                });

                // Fishing UI Overlay
                ctx.fillStyle = "#ffffff"; ctx.font = "bold 18px Segoe UI";
                ctx.fillText("🪙 Score: " + fishScore, 20, 30);
                ctx.fillText("⏳ Time: " + fishTimeLeft + "s", canvas.width - 130, 30);

                if (fishGameOver) {
                    ctx.fillStyle = "rgba(15, 23, 42, 0.85)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = "#f59e0b"; ctx.font = "bold 36px Segoe UI"; ctx.fillText("TIME'S UP!", 280, 190);
                    ctx.fillStyle = "#ffffff"; ctx.font = "22px Segoe UI"; ctx.fillText("Final Score: " + fishScore + " points", 265, 240);
                }

            // 8. MATH PUZZLE
            } else if (currentGame === 'puzzle') {
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

# ------------------------------------------------------------------------------
# 3. RENDER APPLICATION
# ------------------------------------------------------------------------------
components.html(arcade_html, height=520)