import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Roblox-Style Web Arcade", layout="wide")

st.title("🎮 Web Arcade Hub")
st.write("Real-time browser game with smooth keyboard movement & audio!")

# HTML5/JavaScript Real-Time Game Canvas
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background-color: #0f172a; font-family: Arial, sans-serif; text-align: center; color: white; }
        canvas { background: #1e293b; border: 3px solid #3b82f6; border-radius: 8px; display: block; margin: 20px auto; }
        .instructions { font-size: 16px; color: #94a3b8; }
    </style>
</head>
<body>

    <p class="instructions">🕹️ Use <b>Arrow Keys</b> to Move | Collect 🪙 Coins | Dodge 💥 Red Blocks</p>
    <canvas id="gameCanvas" width="800" height="500"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Web Audio API (Plays real sound without external files!)
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playSound(freq, duration) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.frequency.value = freq;
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            gain.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + duration);
            osc.stop(audioCtx.currentTime + duration);
        }

        // Game State
        let player = { x: 100, y: 250, radius: 18, speed: 5 };
        let coins = [{ x: 400, y: 200 }, { x: 600, y: 300 }, { x: 500, y: 100 }];
        let obstacles = [
            { x: 800, y: 100, speed: 4 },
            { x: 950, y: 250, speed: 6 },
            { x: 1100, y: 400, speed: 5 }
        ];
        let score = 0;
        let keys = {};

        // Keyboard Controls
        window.addEventListener("keydown", e => keys[e.key] = true);
        window.addEventListener("keyup", e => keys[e.key] = false);

        function update() {
            // Player Movement
            if (keys["ArrowLeft"] && player.x > 20) player.x -= player.speed;
            if (keys["ArrowRight"] && player.x < canvas.width - 20) player.x += player.speed;
            if (keys["ArrowUp"] && player.y > 20) player.y -= player.speed;
            if (keys["ArrowDown"] && player.y < canvas.height - 20) player.y += player.speed;

            // Coins Collision
            coins.forEach(c => {
                let dist = Math.hypot(player.x - c.x, player.y - c.y);
                if (dist < player.radius + 12) {
                    score += 10;
                    playSound(880, 0.15); // High beep
                    c.x = Math.random() * 400 + 400;
                    c.y = Math.random() * 400 + 50;
                }
            });

            // Obstacles
            obstacles.forEach(o => {
                o.x -= o.speed;
                if (o.x < -30) {
                    o.x = canvas.width + Math.random() * 200;
                    o.y = Math.random() * 400 + 50;
                }

                // Hit Detection
                if (Math.abs(player.x - (o.x + 15)) < 25 && Math.abs(player.y - (o.y + 15)) < 25) {
                    playSound(150, 0.3); // Low crash sound
                    o.x = canvas.width + 200;
                    score = Math.max(0, score - 5);
                }
            });
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw Player
            ctx.fillStyle = "#3b82f6";
            ctx.beginPath();
            ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
            ctx.fill();

            // Draw Coins
            ctx.fillStyle = "#eab308";
            coins.forEach(c => {
                ctx.beginPath();
                ctx.arc(c.x, c.y, 12, 0, Math.PI * 2);
                ctx.fill();
            });

            // Draw Obstacles
            ctx.fillStyle = "#ef4444";
            obstacles.forEach(o => {
                ctx.fillRect(o.x, o.y, 30, 30);
            });

            // HUD
            ctx.fillStyle = "#ffffff";
            ctx.font = "bold 20px Arial";
            ctx.fillText("🪙 Score: " + score, 20, 35);
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

# Render inside Streamlit
components.html(game_html, height=600)