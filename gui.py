import re
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Arcade Game Hub", page_icon="🕹️", layout="wide")

# ---------------------------------------------------------------------------
# Global Streamlit theme (dark neon-arcade shell around the component)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    :root{
        --hub-bg:#0A0C16;
        --hub-panel:#12162A;
        --hub-card:#181D35;
        --hub-border:#2A3158;
        --hub-cyan:#2DE2E6;
        --hub-magenta:#FF3E9A;
        --hub-gold:#FFC145;
        --hub-text:#EDEFF7;
        --hub-muted:#8891B5;
    }

    .stApp{
        background:
            radial-gradient(circle at 15% 0%, rgba(45,226,230,0.06), transparent 40%),
            radial-gradient(circle at 85% 10%, rgba(255,62,154,0.06), transparent 40%),
            var(--hub-bg);
    }
    section[data-testid="stSidebar"]{
        background:linear-gradient(180deg, #0D1022, #0A0C16 70%);
        border-right:1px solid var(--hub-border);
    }
    section[data-testid="stSidebar"] *{
        font-family:'Space Grotesk', sans-serif;
        color:var(--hub-text);
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3{
        font-family:'Press Start 2P', monospace;
        font-size:13px !important;
        letter-spacing:0.5px;
        color:var(--hub-cyan);
        text-shadow:0 0 10px rgba(45,226,230,0.35);
    }
    section[data-testid="stSidebar"] [data-testid="stMetricValue"]{
        font-family:'JetBrains Mono', monospace;
        color:var(--hub-gold);
    }
    section[data-testid="stSidebar"] [data-testid="stMetricLabel"]{
        color:var(--hub-muted);
    }
    section[data-testid="stSidebar"] input{
        background:var(--hub-card) !important;
        color:var(--hub-text) !important;
        border:1px solid var(--hub-border) !important;
        border-radius:8px !important;
    }
    .stApp h1{
        font-family:'Press Start 2P', monospace;
        font-size:22px;
        color:var(--hub-text);
        text-shadow:0 0 18px rgba(45,226,230,0.25);
        letter-spacing:1px;
    }
    div[data-testid="stProgress"] > div > div{
        background-image:linear-gradient(90deg, var(--hub-cyan), var(--hub-magenta)) !important;
    }
    div[data-testid="stProgress"]{
        background:var(--hub-panel);
        border-radius:999px;
        border:1px solid var(--hub-border);
        padding:2px;
    }
    hr{ border-color:var(--hub-border) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = {"username": "Captain", "level": 1, "xp": 40}

user = st.session_state.user

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("🕹️ CONTROL PANEL")
st.sidebar.subheader("🕵️ CREWMATE VERIFICATION")
username_input = st.sidebar.text_input("Enter Player Tag:")
if username_input:
    if re.match(r"^[A-Z][a-z]+$", username_input):
        st.sidebar.success(f"Welcome, {username_input}!")
        st.session_state.user["username"] = username_input
    else:
        st.sidebar.warning("Tag must start with a capital letter, followed by lowercase letters.")

st.sidebar.divider()
st.sidebar.header("🏆 PLAYER STATS")
st.sidebar.metric("Level", user["level"])
st.sidebar.metric("XP", user["xp"])
st.sidebar.divider()
st.sidebar.caption("🔊 Mute, high scores and profile data are all managed inside the arcade panel below.")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title(f"👋 WELCOME BACK, {user['username'].upper()}")
next_level_xp = user["level"] * 100
xp_progress = min(1.0, user["xp"] / next_level_xp)
st.progress(xp_progress, text=f"Level {user['level']} Progress ({user['xp']}/{next_level_xp} XP)")
st.divider()

# ---------------------------------------------------------------------------
# Arcade component (HTML/CSS/JS) — 8 playable mini-games
# ---------------------------------------------------------------------------
ARCADE_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0A0C16;
    --panel: #12162A;
    --card: #181D35;
    --card-border: #2A3158;
    --cyan: #2DE2E6;
    --magenta: #FF3E9A;
    --gold: #FFC145;
    --good: #4ADE80;
    --bad: #FF5C7A;
    --text: #EDEFF7;
    --muted: #8891B5;
    --font-display: 'Press Start 2P', monospace;
    --font-body: 'Space Grotesk', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
  }
  * { box-sizing: border-box; }
  html, body { height: 100%; }
  body {
    margin: 0; padding: 0;
    background:
      radial-gradient(circle at 20% -10%, rgba(45,226,230,0.10), transparent 45%),
      radial-gradient(circle at 90% 0%, rgba(255,62,154,0.10), transparent 40%),
      var(--bg);
    font-family: var(--font-body);
    color: var(--text);
    user-select: none;
    position: relative;
    min-height: 100vh;
  }

  /* CRT scanline overlay — the signature texture that ties every screen together */
  body::before {
    content: "";
    position: fixed; inset: 0;
    background: repeating-linear-gradient(
      to bottom,
      rgba(255,255,255,0.028) 0px,
      rgba(255,255,255,0.028) 1px,
      transparent 1px,
      transparent 3px
    );
    pointer-events: none;
    z-index: 500;
    mix-blend-mode: overlay;
  }

  /* ===================== Marquee header ===================== */
  .app-header {
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 12px; padding: 18px 26px;
    background: linear-gradient(180deg, #10142A 0%, #0C0F1E 100%);
    border-bottom: 1px solid var(--card-border);
    box-shadow: 0 6px 24px rgba(0,0,0,0.45);
    position: relative;
  }
  .app-header::after{
    content:"";
    position:absolute; left:0; right:0; bottom:-1px; height:2px;
    background: linear-gradient(90deg, transparent, var(--cyan), var(--magenta), transparent);
    opacity:0.7;
  }
  .brand { display: flex; align-items: center; gap: 12px; }
  .brand .logo {
    font-size: 26px;
    filter: drop-shadow(0 0 8px rgba(45,226,230,0.6));
  }
  .brand h1 {
    font-family: var(--font-display);
    font-size: 15px; margin: 0; letter-spacing: 2px;
    color: var(--cyan);
    text-shadow: 0 0 6px rgba(45,226,230,0.55), 0 0 18px rgba(45,226,230,0.25);
    animation: flicker 6s infinite;
  }
  @keyframes flicker {
    0%, 92%, 100% { opacity: 1; }
    93% { opacity: 0.65; }
    94% { opacity: 1; }
    95% { opacity: 0.8; }
    96% { opacity: 1; }
  }
  .header-right { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
  .profile-badge {
    display: flex; align-items: center; gap: 10px;
    background: var(--panel); padding: 8px 16px 8px 8px; border-radius: 999px;
    border: 1px solid var(--card-border);
    box-shadow: inset 0 0 0 1px rgba(45,226,230,0.06);
  }
  .avatar {
    width: 32px; height: 32px; border-radius: 50%;
    background: conic-gradient(from 180deg, var(--cyan), var(--magenta), var(--cyan));
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-family: var(--font-display); font-size: 12px;
    color: #0A0C16;
    box-shadow: 0 0 10px rgba(45,226,230,0.4);
  }
  .profile-meta { font-size: 12px; line-height: 1.35; font-family: var(--font-mono); }
  .profile-meta .name { font-weight: 700; font-family: var(--font-body); color: var(--text); font-size: 13px; }
  .profile-meta .sub { color: var(--muted); }
  .toggle-btn {
    background: var(--card); border: 1px solid var(--card-border); color: var(--text);
    padding: 9px 16px; border-radius: 999px; cursor: pointer; font-size: 12.5px;
    font-family: var(--font-body); font-weight: 600; transition: all .2s;
    letter-spacing: 0.3px;
  }
  .toggle-btn.on { background: rgba(74,222,128,0.12); color: var(--good); border-color: rgba(74,222,128,0.4); box-shadow: 0 0 12px rgba(74,222,128,0.15); }
  .toggle-btn.off { background: #23283F; color: var(--muted); border-color: var(--card-border); }
  .toggle-btn:hover { transform: translateY(-1px); }

  /* ===================== Game grid ===================== */
  .grid-container {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px; padding: 28px;
  }
  .game-card {
    position: relative; background: linear-gradient(180deg, var(--card), #141834);
    border: 1px solid var(--card-border); border-radius: 14px; padding: 22px 16px 18px;
    text-align: center; cursor: pointer; overflow: hidden;
    box-shadow: 0 10px 24px rgba(0,0,0,0.35);
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
  }
  .game-card::before{
    content:"";
    position:absolute; top:0; left:0; right:0; height:3px;
    background: linear-gradient(90deg, var(--cyan), var(--magenta));
    opacity:0; transition: opacity .18s ease;
  }
  .game-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 36px rgba(0,0,0,.5), 0 0 0 1px rgba(45,226,230,0.25), 0 0 24px rgba(45,226,230,0.12);
    border-color: var(--cyan);
  }
  .game-card:hover::before{ opacity:1; }
  .game-card .icon {
    font-size: 38px; display: block; margin-bottom: 10px;
    filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));
  }
  .game-card b {
    display: block; font-size: 12.5px; font-family: var(--font-display);
    margin-bottom: 8px; letter-spacing: 0.5px; line-height: 1.5; color: var(--text);
  }
  .game-card small { color: var(--muted); font-size: 11.5px; display: block; font-family: var(--font-body); }
  .game-card .best {
    margin-top: 12px; font-size: 10.5px; color: var(--gold);
    background: rgba(255,193,69,0.08); border: 1px solid rgba(255,193,69,0.25);
    border-radius: 999px; padding: 4px 10px; display: inline-block;
    font-family: var(--font-mono); letter-spacing: 0.3px;
  }

  /* ===================== Game view ===================== */
  #game-view { padding: 20px 26px 34px 26px; }
  .game-toolbar {
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 10px; margin-bottom: 14px;
  }
  .btn {
    background: linear-gradient(180deg, var(--cyan), #1FB9BD); color: #06161A; font-weight: 700; padding: 10px 20px;
    border: none; border-radius: 10px; cursor: pointer; font-size: 13px;
    font-family: var(--font-body); letter-spacing: 0.3px;
    transition: filter .15s, transform .1s;
    box-shadow: 0 6px 16px rgba(45,226,230,0.25);
  }
  .btn:hover { filter: brightness(1.08); }
  .btn:active { transform: scale(0.96); }
  .btn.secondary {
    background: var(--card); color: var(--text); border: 1px solid var(--card-border);
    box-shadow: none;
  }
  .btn.secondary:hover { background: #1F2542; border-color: var(--cyan); }

  .farm-toolbar { display: flex; justify-content: center; gap: 10px; margin-bottom: 14px; flex-wrap: wrap; }
  .farm-btn {
    background: var(--card); color: var(--text); font-weight: 600; padding: 9px 15px;
    border: 1px solid var(--card-border); border-radius: 10px; cursor: pointer; font-size: 12.5px;
    font-family: var(--font-body);
    transition: background .2s, border-color .2s, color .2s;
  }
  .farm-btn:hover { background: #1F2542; border-color: var(--cyan); }
  .farm-btn.active { background: rgba(255,193,69,0.14); color: var(--gold); border-color: var(--gold); }

  canvas {
    background: #0D0F1E;
    border: 2px solid var(--card-border); border-radius: 16px;
    display: block; margin: 0 auto; outline: none; max-width: 100%;
    box-shadow: 0 14px 40px rgba(0,0,0,.5), inset 0 0 60px rgba(45,226,230,0.04);
    touch-action: none;
  }

  .toast {
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
    background: var(--card); border: 1px solid var(--cyan); padding: 11px 22px;
    border-radius: 12px; font-size: 13px; font-family: var(--font-body); font-weight: 600;
    opacity: 0; pointer-events: none;
    box-shadow: 0 10px 30px rgba(0,0,0,0.45);
    transition: opacity .3s, transform .3s; z-index: 999; max-width: 90%; text-align: center;
  }
  .toast.show { opacity: 1; transform: translateX(-50%) translateY(-6px); }
  .toast.good { border-color: var(--good); box-shadow: 0 10px 30px rgba(74,222,128,0.15); }
  .toast.bad { border-color: var(--bad); box-shadow: 0 10px 30px rgba(255,92,122,0.15); }

  footer.credit {
    text-align: center; color: var(--muted); font-size: 11px; padding: 18px;
    font-family: var(--font-mono); letter-spacing: 0.3px;
  }
  #errorBanner {
    display: none; background: #2A1420; color: #FFB4C6; border: 1px solid var(--bad);
    padding: 12px 18px; margin: 14px 26px; border-radius: 10px; font-size: 12.5px;
    font-family: var(--font-mono); white-space: pre-wrap;
  }
</style>
</head>
<body>
  <div id="errorBanner"></div>

  <div class="app-header">
    <div class="brand"><span class="logo">🕹️</span><h1>ARCADE GAME HUB</h1></div>
    <div class="header-right">
      <button class="toggle-btn" id="soundToggle">🔊 ON</button>
      <div class="profile-badge">
        <div class="avatar" id="avatarInitial">?</div>
        <div class="profile-meta">
          <div class="name" id="profileName">__USERNAME__</div>
          <div class="sub">LV __LEVEL__ · __XP__/__NEXT_XP__ XP</div>
        </div>
      </div>
    </div>
  </div>

  <!-- MENU -->
  <div id="menu-grid" class="grid-container">
    <div class="game-card" data-game="racer">
      <span class="icon">🏎️</span><b>HILL CLIMB<br/>RACER</b><small>Drive &amp; Collect Coins</small>
      <div class="best" data-best="racer">Best: 0</div>
    </div>
    <div class="game-card" data-game="tiles">
      <span class="icon">🎵</span><b>TILES HOP</b><small>Press 1 · 2 · 3</small>
      <div class="best" data-best="tiles">Best: 0</div>
    </div>
    <div class="game-card" data-game="ox">
      <span class="icon">❌⭕</span><b>TIC-TAC-TOE</b><small>Play vs AI</small>
      <div class="best" data-best="ox">W-L-D: 0-0-0</div>
    </div>
    <div class="game-card" data-game="candy">
      <span class="icon">🍬</span><b>CANDY MATCH</b><small>Tap Matching Pairs</small>
      <div class="best" data-best="candy">Best: 0</div>
    </div>
    <div class="game-card" data-game="imposter">
      <span class="icon">🕵️</span><b>GUESS<br/>IMPOSTER</b><small>Find the Suspicious One</small>
      <div class="best" data-best="imposter">Found: 0</div>
    </div>
    <div class="game-card" data-game="hayday">
      <span class="icon">🌾</span><b>MINI FARM</b><small>Farming Simulator</small>
      <div class="best" data-best="hayday">Best coins: 30</div>
    </div>
    <div class="game-card" data-game="fish">
      <span class="icon">🎣</span><b>FISH CATCHER</b><small>Deep Sea Fishing (60s)</small>
      <div class="best" data-best="fish">Best: 0</div>
    </div>
    <div class="game-card" data-game="puzzle">
      <span class="icon">🧩</span><b>MATH PUZZLE</b><small>Logic Solver</small>
      <div class="best" data-best="puzzle">Solved: 0</div>
    </div>
  </div>

  <!-- GAME VIEW  Define Width and Height -->
  <div id="game-view" style="display:none;">
    <div class="game-toolbar">
      <button class="btn secondary" id="backBtn">⬅️ Back to Arcade Menu</button>
      <div id="hudExtra" style="font-size:12px;color:var(--muted);font-family:var(--font-mono);"></div>
    </div>
    <div id="hayday-toolbar" class="farm-toolbar" style="display:none;">
      <button id="fbtn-wheat" class="farm-btn active" data-tool="wheat">🌾 Wheat (Free)</button>
      <button id="fbtn-corn" class="farm-btn" data-tool="corn">🌽 Corn (5 Coins)</button>
      <button id="fbtn-carrot" class="farm-btn" data-tool="carrot">🥕 Carrot (12 Coins)</button>
      <button id="fbtn-harvest" class="farm-btn" data-tool="harvest">🚜 Harvest</button>
      <button class="farm-btn" id="expandBtn">🪵 Expand Plot (50 Coins)</button>
      <button class="farm-btn" id="sellBtn">💰 Sell Silo</button>
    </div>
    <canvas id="gameCanvas" width="750" height="420" tabindex="1"></canvas>
  </div>

  <footer class="credit">ARCADE GAME HUB · profile-based local high scores · click/tap the canvas to enable sound</footer>
  <div class="toast" id="toast"></div>

<script>
  window.addEventListener("error", function (e) {
    const banner = document.getElementById("errorBanner");
    if (banner) {
      banner.style.display = "block";
      banner.textContent = "⚠️ A script error occurred, so the game may not respond:\n" +
        e.message + " (line " + e.lineno + ")\n" +
        "Please screenshot this and share it so the bug can be fixed.";
    }
  });
</script>
<script>
(function () {
  "use strict";

  // =====================================================================
  // Profile, settings, persistence
  // =====================================================================
  const PROFILE = "__USERNAME__" || "Player";
  document.getElementById("profileName").textContent = PROFILE;
  document.getElementById("avatarInitial").textContent = PROFILE.charAt(0).toUpperCase();

  function statsKey() { return "arcade_hub_stats_" + PROFILE; }
  function defaultStats() {
    return { racer: 0, tiles: 0, candy: 0, fish: 0, hayday: 30,
             ox: { w: 0, l: 0, d: 0 }, imposter: 0, puzzle: 0 };
  }
  function getStats() {
    try {
      const raw = localStorage.getItem(statsKey());
      return raw ? Object.assign(defaultStats(), JSON.parse(raw)) : defaultStats();
    } catch (e) { return defaultStats(); }
  }
  function saveStats(s) { try { localStorage.setItem(statsKey(), JSON.stringify(s)); } catch (e) {} }
  function bumpBest(game, value) {
    const s = getStats();
    if (value > (s[game] || 0)) { s[game] = value; saveStats(s); }
    return getStats()[game];
  }
  function refreshMenuBadges() {
    const s = getStats();
    document.querySelector('[data-best="racer"]').textContent = "Best: " + s.racer;
    document.querySelector('[data-best="tiles"]').textContent = "Best: " + s.tiles;
    document.querySelector('[data-best="candy"]').textContent = "Best: " + s.candy;
    document.querySelector('[data-best="fish"]').textContent = "Best: " + s.fish;
    document.querySelector('[data-best="hayday"]').textContent = "Best coins: " + s.hayday;
    document.querySelector('[data-best="imposter"]').textContent = "Found: " + s.imposter;
    document.querySelector('[data-best="puzzle"]').textContent = "Solved: " + s.puzzle;
    document.querySelector('[data-best="ox"]').textContent = "W-L-D: " + s.ox.w + "-" + s.ox.l + "-" + s.ox.d;
  }
  refreshMenuBadges();

  let soundOn = true;
  try { soundOn = localStorage.getItem("arcade_hub_sound") !== "off"; } catch (e) {}
  const soundToggle = document.getElementById("soundToggle");
  function refreshSoundUI() {
    soundToggle.textContent = soundOn ? "🔊 ON" : "🔇 OFF";
    soundToggle.className = "toggle-btn " + (soundOn ? "on" : "off");
  }
  refreshSoundUI();
  soundToggle.addEventListener("click", function () {
    soundOn = !soundOn;
    refreshSoundUI();
    try { localStorage.setItem("arcade_hub_sound", soundOn ? "on" : "off"); } catch (e) {}
  });

  // =====================================================================
  // Toast (replaces blocking alert() calls)
  // =====================================================================
  let toastTimer;
  function showToast(msg, kind) {
    const toast = document.getElementById("toast");
    toast.textContent = msg;
    toast.className = "toast show" + (kind ? " " + kind : "");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove("show"); }, 1900);
  }

  // =====================================================================
  // Canvas / input
  // =====================================================================
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");
  let currentGame = "";
  let keys = {};
  let audioUnlocked = false;

  window.addEventListener("keydown", function (e) {
    keys[e.key] = true;
    if (e.key === " " || e.code === "Space") {
      e.preventDefault();
      if (currentGame === "fish") triggerHook();
    }
  });
  window.addEventListener("keyup", function (e) { keys[e.key] = false; });

  // Audio synth
  let audioCtx = null;
  function initAudio() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === "suspended") audioCtx.resume();
    audioUnlocked = true;
  }
  function playSound(freq, duration) {
    if (!soundOn || !audioCtx || audioCtx.state !== "running") return;
    try {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "sine";
      osc.frequency.value = freq;
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start();
      gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
      osc.stop(audioCtx.currentTime + duration);
    } catch (e) {}
  }

  function canvasPointFromEvent(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return { x: (clientX - rect.left) * scaleX, y: (clientY - rect.top) * scaleY };
  }
  function onCanvasActivate(e) {
    initAudio();
    canvas.focus();
    const p = canvasPointFromEvent(e);
    handleCanvasClick(p.x, p.y);
  }
  canvas.addEventListener("click", onCanvasActivate);
  canvas.addEventListener("touchstart", function (e) { e.preventDefault(); onCanvasActivate(e); }, { passive: false });

  // =====================================================================
  // Minigame state
  // =====================================================================
  // Racer
  let racer = {};
  function resetRacer() {
    racer = {
      x: 100, y: 200, lives: 3, score: 0, speed: 4, gameOver: false, invuln: 0,
      coins: [ { x: 400, y: 150 }, { x: 600, y: 250 } ],
      obs: [ { x: 750, y: 120 + Math.random() * 260 } ]
    };
  }

  // Tiles Hop
  let tiles = {};
  function resetTiles() {
    tiles = { falling: [], score: 0, lives: 3, gameOver: false, speed: 3, spawnRate: 0.025, combo: 0 };
  }

  // Tic-Tac-Toe
  let oxBoard = ["", "", "", "", "", "", "", "", ""];
  let oxGameOver = false;

  // Guess the Impostor
  let imposter = {};
  function nextImposterRound() {
    imposter.baseHue = Math.floor(Math.random() * 360);
    imposter.oddIndex = Math.floor(Math.random() * 4);
    imposter.shift = Math.max(6, 22 - imposter.streak * 2); // gets subtler as the streak grows
  }
  function resetImposter() {
    imposter = { lives: 3, streak: 0, gameOver: false };
    nextImposterRound();
  }

  // Candy Match (memory-pair game)
  let candy = {};
  const CANDY_EMOJI = ["🍬", "🍭", "🍫", "🍩", "🍪", "🧁"];
  function resetCandy(pairCount) {
    pairCount = pairCount || 4;
    const emojis = CANDY_EMOJI.slice(0, pairCount);
    let deck = emojis.concat(emojis);
    for (let i = deck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const tmp = deck[i]; deck[i] = deck[j]; deck[j] = tmp;
    }
    candy = {
      cards: deck.map(function (e) { return { emoji: e, matched: false }; }),
      flippedIdx: [], moves: 0, matches: 0, locked: false, gameOver: false, cols: 4
    };
  }

  // Math Puzzle
  let puzzle = {};
  function makePuzzle() {
    const streak = puzzle.streak || 0;
    const opPool = streak >= 4 ? ["+", "-", "×"] : (streak >= 2 ? ["+", "-"] : ["+"]);
    const op = opPool[Math.floor(Math.random() * opPool.length)];
    let a, b, answer;
    if (op === "+") {
      a = 1 + Math.floor(Math.random() * (20 + streak * 2));
      b = 1 + Math.floor(Math.random() * (20 + streak * 2));
      answer = a + b;
    } else if (op === "-") {
      a = 5 + Math.floor(Math.random() * (25 + streak * 2));
      b = 1 + Math.floor(Math.random() * a);
      answer = a - b;
    } else {
      a = 2 + Math.floor(Math.random() * (6 + Math.min(streak, 6)));
      b = 2 + Math.floor(Math.random() * (6 + Math.min(streak, 6)));
      answer = a * b;
    }
    const choices = new Set([answer]);
    let guard = 0;
    while (choices.size < 4 && guard < 40) {
      guard++;
      const delta = Math.floor(Math.random() * 9) - 4;
      const wrong = answer + (delta === 0 ? 5 : delta);
      if (wrong >= 0) choices.add(wrong);
    }
    puzzle.a = a; puzzle.b = b; puzzle.op = op; puzzle.answer = answer;
    puzzle.choices = Array.from(choices).sort(function () { return Math.random() - 0.5; });
  }
  function resetPuzzle() {
    puzzle = { streak: 0, best: getStats().puzzle || 0, feedback: "", feedbackTimer: 0 };
    makePuzzle();
  }

  // Farm
  let farmCoins = 30;
  let selectedFarmTool = "wheat";
  let silo = { wheat: 0, corn: 0, carrot: 0 };
  let landPlots = [];

  function initHayDay() {
    farmCoins = Math.max(farmCoins, 30);
    landPlots = [];
    const cols = 3, rows = 2, tileW = 90, tileH = 60, originX = 180, originY = 120;
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        landPlots.push({ x: originX + c*(tileW+15), y: originY + r*(tileH+15), w: tileW, h: tileH,
                          state: "empty", crop: null, growthProgress: 0 });
      }
    }
  }

  document.querySelectorAll(".farm-btn[data-tool]").forEach(function (b) {
    b.addEventListener("click", function () {
      selectedFarmTool = b.dataset.tool;
      document.querySelectorAll(".farm-btn").forEach(function (x) { x.classList.remove("active"); });
      b.classList.add("active");
    });
  });
  document.getElementById("expandBtn").addEventListener("click", expandFarm);
  document.getElementById("sellBtn").addEventListener("click", sellCrops);

  function expandFarm() {
    if (farmCoins >= 50) {
      farmCoins -= 50;
      playSound(700, 0.2);
      const tileW = 90, tileH = 60;
      const last = landPlots[landPlots.length - 1];
      let nextX = last.x + tileW + 15, nextY = last.y;
      if (nextX > canvas.width - tileW - 40) { nextX = 180; nextY = last.y + tileH + 15; }
      landPlots.push({ x: nextX, y: nextY, w: tileW, h: tileH, state: "empty", crop: null, growthProgress: 0 });
      showToast("🎉 New land plot unlocked!", "good");
    } else {
      showToast("❌ Need 50 coins to expand.", "bad");
    }
  }
  function sellCrops() {
    const earnings = (silo.wheat*4) + (silo.corn*15) + (silo.carrot*35);
    if (earnings > 0) {
      farmCoins += earnings;
      playSound(880, 0.25);
      showToast("💰 Sold all crops for " + earnings + " coins!", "good");
      silo.wheat = 0; silo.corn = 0; silo.carrot = 0;
      bumpBest("hayday", farmCoins);
    } else {
      showToast("🌾 Silo is empty — harvest crops first.", "bad");
    }
  }

  // Fish
  let fishScore = 0, fishTimeLeft = 60, fishGameOver = false, fishTimerInterval = null;
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
      fishes.push(Object.assign({ x: dir === 1 ? -30 : canvas.width + 30,
                                   y: 110 + Math.random()*260, dir: dir }, type));
    }
  }
  function triggerHook() {
    if (fishGameOver) return;
    if (hook.state === "idle") hook.state = "dropping";
    else if (hook.state === "dropping") hook.state = "reeling";
  }
  function resetFish() {
    fishScore = 0; fishTimeLeft = 60; fishGameOver = false;
    fishes = []; hook.state = "idle"; hook.y = hook.startY; hook.caughtFish = null; boat.x = 340;
    if (fishTimerInterval) clearInterval(fishTimerInterval);
    fishTimerInterval = setInterval(function () {
      if (currentGame === "fish" && !fishGameOver && fishTimeLeft > 0) {
        fishTimeLeft--;
        if (fishTimeLeft === 0) {
          fishGameOver = true;
          bumpBest("fish", fishScore);
          refreshMenuBadges();
        }
      }
    }, 1000);
  }

  // =====================================================================
  // Tic-Tac-Toe AI (minimax, with a small chance of an imperfect move so
  // it stays beatable instead of forcing a draw every single game)
  // =====================================================================
  function oxEmptyIndices(b) {
    const r = [];
    for (let i = 0; i < 9; i++) if (b[i] === "") r.push(i);
    return r;
  }
  function oxCheckWinner(b) {
    const lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    for (const line of lines) {
      const a = line[0], c = line[1], d = line[2];
      if (b[a] && b[a] === b[c] && b[a] === b[d]) return b[a];
    }
    if (oxEmptyIndices(b).length === 0) return "draw";
    return null;
  }
  function oxMinimax(b, isMaximizing) {
    const winner = oxCheckWinner(b);
    if (winner === "⭕") return { score: 10 };
    if (winner === "❌") return { score: -10 };
    if (winner === "draw") return { score: 0 };

    const moves = [];
    oxEmptyIndices(b).forEach(function (idx) {
      const newBoard = b.slice();
      newBoard[idx] = isMaximizing ? "⭕" : "❌";
      const result = oxMinimax(newBoard, !isMaximizing);
      moves.push({ idx: idx, score: result.score });
    });

    let best = moves[0];
    moves.forEach(function (m) {
      if (isMaximizing ? m.score > best.score : m.score < best.score) best = m;
    });
    return best;
  }
  function oxAIMove(b) {
    const empties = oxEmptyIndices(b);
    if (empties.length === 9) return 4; // opening: take the center
    if (Math.random() < 0.15) return empties[Math.floor(Math.random() * empties.length)];
    return oxMinimax(b, true).idx;
  }

  function shuffleCandies() { /* kept for backwards compatibility, unused */ }

  // =====================================================================
  // Navigation
  // =====================================================================
  document.querySelectorAll(".game-card").forEach(function (card) {
    card.addEventListener("click", function () { startGame(card.dataset.game); });
  });
  document.getElementById("backBtn").addEventListener("click", showMenu);

  function startGame(name) {
    currentGame = name;
    document.getElementById("menu-grid").style.display = "none";
    document.getElementById("game-view").style.display = "block";
    document.getElementById("hayday-toolbar").style.display = (name === "hayday") ? "flex" : "none";
    setTimeout(function () { canvas.focus(); }, 100);

    if (name === "ox") { oxBoard = ["", "", "", "", "", "", "", "", ""]; oxGameOver = false; }
    if (name === "candy") resetCandy(4);
    if (name === "racer") resetRacer();
    if (name === "tiles") resetTiles();
    if (name === "hayday") initHayDay();
    if (name === "imposter") resetImposter();
    if (name === "puzzle") resetPuzzle();
    if (name === "fish") resetFish();

    requestAnimationFrame(runLoop);
  }

  function showMenu() {
    currentGame = "";
    document.getElementById("hayday-toolbar").style.display = "none";
    if (fishTimerInterval) clearInterval(fishTimerInterval);
    if (farmCoins) bumpBest("hayday", farmCoins);
    refreshMenuBadges();
    document.getElementById("menu-grid").style.display = "grid";
    document.getElementById("game-view").style.display = "none";
  }

  // =====================================================================
  // Click handling per game
  // =====================================================================
  function handleCanvasClick(mx, my) {
    if (currentGame === "racer") {
      if (racer.gameOver) resetRacer();

    } else if (currentGame === "tiles") {
      if (tiles.gameOver) resetTiles();

    } else if (currentGame === "candy") {
      if (candy.gameOver) { resetCandy(4); return; }
      if (candy.locked) return;
      const cols = candy.cols, cardW = 140, cardH = 140, gapX = 20, gapY = 20;
      const totalW = cols * cardW + (cols - 1) * gapX;
      const startX = (canvas.width - totalW) / 2;
      const startY = 90;
      for (let i = 0; i < candy.cards.length; i++) {
        const col = i % cols, row = Math.floor(i / cols);
        const rx = startX + col * (cardW + gapX), ry = startY + row * (cardH + gapY);
        if (mx > rx && mx < rx + cardW && my > ry && my < ry + cardH) {
          const card = candy.cards[i];
          if (card.matched || candy.flippedIdx.indexOf(i) !== -1) break;
          playSound(500, 0.08);
          candy.flippedIdx.push(i);
          if (candy.flippedIdx.length === 2) {
            candy.moves++;
            const i1 = candy.flippedIdx[0], i2 = candy.flippedIdx[1];
            if (candy.cards[i1].emoji === candy.cards[i2].emoji) {
              candy.cards[i1].matched = true; candy.cards[i2].matched = true;
              candy.matches++;
              playSound(880, 0.25);
              showToast("🎉 Match found!", "good");
              candy.flippedIdx = [];
              if (candy.matches === candy.cards.length / 2) {
                candy.gameOver = true;
                const scoreValue = Math.max(10, 100 - (candy.moves - candy.cards.length / 2) * 5);
                bumpBest("candy", scoreValue);
                refreshMenuBadges();
                showToast("🏆 Board cleared in " + candy.moves + " moves!", "good");
              }
            } else {
              candy.locked = true;
              playSound(150, 0.2);
              setTimeout(function () { candy.flippedIdx = []; candy.locked = false; }, 700);
            }
          }
          break;
        }
      }

    } else if (currentGame === "ox") {
      if (oxGameOver) { oxBoard = ["", "", "", "", "", "", "", "", ""]; oxGameOver = false; return; }
      for (let i = 0; i < 9; i++) {
        const rx = 250 + (i % 3) * 85, ry = 90 + Math.floor(i / 3) * 85;
        if (mx > rx && mx < rx + 75 && my > ry && my < ry + 75 && oxBoard[i] === "") {
          oxBoard[i] = "❌";
          playSound(600, 0.1);
          const winner = oxCheckWinner(oxBoard);
          if (winner) { endOx(winner); return; }
          const aiIdx = oxAIMove(oxBoard);
          if (aiIdx !== undefined && aiIdx !== null) oxBoard[aiIdx] = "⭕";
          const winner2 = oxCheckWinner(oxBoard);
          if (winner2) { endOx(winner2); return; }
          break;
        }
      }

    } else if (currentGame === "imposter") {
      if (imposter.gameOver) { resetImposter(); return; }
      for (let i = 0; i < 4; i++) {
        const rx = 90 + i * 150;
        if (mx > rx && mx < rx + 110 && my > 140 && my < 250) {
          if (i === imposter.oddIndex) {
            playSound(880, 0.2);
            imposter.streak++;
            showToast("🎉 Found it! Streak: " + imposter.streak, "good");
            bumpBest("imposter", imposter.streak);
            refreshMenuBadges();
            nextImposterRound();
          } else {
            playSound(150, 0.2);
            imposter.lives--;
            if (imposter.lives <= 0) {
              imposter.gameOver = true;
              showToast("💀 Out of lives — tap to try again", "bad");
            } else {
              showToast("❌ That one's innocent! Lives left: " + imposter.lives, "bad");
            }
          }
          break;
        }
      }

    } else if (currentGame === "hayday") {
      landPlots.forEach(function (plot) {
        if (mx > plot.x && mx < plot.x + plot.w && my > plot.y && my < plot.y + plot.h) {
          if (plot.state === "empty") {
            if (selectedFarmTool === "wheat") {
              plot.state = "growing"; plot.crop = "wheat"; plot.growthProgress = 0; playSound(400, 0.1);
            } else if (selectedFarmTool === "corn") {
              if (farmCoins >= 5) { farmCoins -= 5; plot.state = "growing"; plot.crop = "corn"; plot.growthProgress = 0; playSound(450, 0.1); }
              else showToast("Not enough coins for corn!", "bad");
            } else if (selectedFarmTool === "carrot") {
              if (farmCoins >= 12) { farmCoins -= 12; plot.state = "growing"; plot.crop = "carrot"; plot.growthProgress = 0; playSound(520, 0.1); }
              else showToast("Not enough coins for carrot!", "bad");
            }
          } else if (selectedFarmTool === "harvest" && plot.state === "ready") {
            silo[plot.crop]++; plot.state = "empty"; plot.crop = null; plot.growthProgress = 0; playSound(650, 0.12);
          }
        }
      });

    } else if (currentGame === "fish") {
      if (fishGameOver) resetFish();
      else triggerHook();

    } else if (currentGame === "puzzle") {
      const choiceW = 150, choiceH = 70, gapX = 30, gapY = 25, cols = 2;
      const totalW = cols * choiceW + (cols - 1) * gapX;
      const startX = (canvas.width - totalW) / 2;
      const startY = 160;
      puzzle.choices.forEach(function (val, i) {
        const col = i % cols, row = Math.floor(i / cols);
        const rx = startX + col * (choiceW + gapX), ry = startY + row * (choiceH + gapY);
        if (mx > rx && mx < rx + choiceW && my > ry && my < ry + choiceH) {
          if (val === puzzle.answer) {
            playSound(880, 0.2);
            puzzle.streak++;
            if (puzzle.streak > puzzle.best) puzzle.best = puzzle.streak;
            puzzle.feedback = "✅ Correct! Streak " + puzzle.streak;
            puzzle.feedbackTimer = 900;
            bumpBest("puzzle", puzzle.best);
            refreshMenuBadges();
          } else {
            playSound(150, 0.2);
            puzzle.feedback = "❌ Not quite — the answer was " + puzzle.answer;
            puzzle.feedbackTimer = 1200;
            puzzle.streak = 0;
          }
          makePuzzle();
        }
      });
    }
  }

  function endOx(result) {
    oxGameOver = true;
    const s = getStats();
    if (result === "❌") { s.ox.w += 1; showToast("🎉 You win!", "good"); playSound(880, 0.25); }
    else if (result === "⭕") { s.ox.l += 1; showToast("😢 AI wins!", "bad"); playSound(150, 0.25); }
    else { s.ox.d += 1; showToast("🤝 Draw!"); }
    saveStats(s);
    refreshMenuBadges();
  }

  // =====================================================================
  // Main render loop
  // =====================================================================
  function runLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!audioUnlocked) {
      ctx.fillStyle = "#eab308"; ctx.font = "14px Arial";
      ctx.fillText("🔊 Click/tap the canvas once to enable sound effects!", 200, 20);
    }

    if (currentGame === "racer") {
      if (!racer.gameOver) {
        if ((keys["ArrowUp"] || keys["w"]) && racer.y > 20) racer.y -= 5;
        if ((keys["ArrowDown"] || keys["s"]) && racer.y < 380) racer.y += 5;
        if ((keys["ArrowLeft"] || keys["a"]) && racer.x > 20) racer.x -= 5;
        if ((keys["ArrowRight"] || keys["d"]) && racer.x < 730) racer.x += 5;
        if (racer.invuln > 0) racer.invuln -= 16;
        racer.speed = 4 + Math.floor(racer.score / 50) * 0.6;
        if (racer.obs.length < 1 + Math.floor(racer.score / 100)) {
          racer.obs.push({ x: 750 + Math.random() * 200, y: 50 + Math.random() * 300 });
        }
      }

      ctx.fillStyle = (racer.invuln > 0 && Math.floor(racer.invuln / 100) % 2 === 0) ? "rgba(59,130,246,0.4)" : "#3b82f6";
      ctx.beginPath(); ctx.arc(racer.x, racer.y, 16, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = "#eab308";
      racer.coins.forEach(function (c) {
        ctx.beginPath(); ctx.arc(c.x, c.y, 10, 0, Math.PI*2); ctx.fill();
        if (!racer.gameOver && Math.hypot(racer.x - c.x, racer.y - c.y) < 26) {
          playSound(880, 0.1); racer.score += 5;
          bumpBest("racer", racer.score); refreshMenuBadges();
          c.x = 400 + Math.random()*300; c.y = 50 + Math.random()*300;
        }
      });
      ctx.fillStyle = "#ef4444";
      racer.obs.forEach(function (o) {
        if (!racer.gameOver) o.x -= racer.speed;
        if (o.x < -20) { o.x = 750 + Math.random()*100; o.y = 50 + Math.random()*300; }
        ctx.fillRect(o.x, o.y, 25, 25);
        if (!racer.gameOver && racer.invuln <= 0 && Math.abs(racer.x - o.x) < 22 && Math.abs(racer.y - o.y) < 22) {
          playSound(150, 0.2);
          racer.lives--;
          racer.invuln = 1200;
          o.x = 750 + Math.random()*100; o.y = 50 + Math.random()*300;
          if (racer.lives <= 0) {
            racer.gameOver = true;
            bumpBest("racer", racer.score); refreshMenuBadges();
          } else {
            showToast("💥 Crash! Lives left: " + racer.lives, "bad");
          }
        }
      });
      ctx.fillStyle = "#ffffff"; ctx.font = "16px Arial";
      ctx.fillText("🕹 Arrow/WASD to move — Score: " + racer.score + "   Lives: " + "❤️".repeat(Math.max(0, racer.lives)), 20, 40);
      if (racer.gameOver) {
        ctx.fillStyle = "rgba(15,23,42,0.85)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#f59e0b"; ctx.font = "bold 32px Segoe UI"; ctx.fillText("CRASHED OUT", 260, 190);
        ctx.fillStyle = "#ffffff"; ctx.font = "18px Segoe UI"; ctx.fillText("Score: " + racer.score + " — tap the track to restart", 190, 230);
      }

    } else if (currentGame === "tiles") {
      if (!tiles.gameOver) {
        tiles.speed = 3 + Math.floor(tiles.score / 50) * 0.5;
        tiles.spawnRate = Math.min(0.05, 0.022 + tiles.score / 4000);
        if (Math.random() < tiles.spawnRate) tiles.falling.push({ col: Math.floor(Math.random()*3), y: 0, hit: false });
      }
      ctx.strokeStyle = "#22c55e"; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(150, 320); ctx.lineTo(600, 320); ctx.stroke();

      tiles.falling.forEach(function (t, idx) {
        if (!tiles.gameOver) t.y += tiles.speed;
        ctx.fillStyle = "#a855f7";
        ctx.fillRect(200 + t.col*130, t.y, 90, 35);
        if (tiles.gameOver) return;
        if (t.y > 290 && t.y < 340 && !t.hit) {
          if ((t.col === 0 && keys["1"]) || (t.col === 1 && keys["2"]) || (t.col === 2 && keys["3"])) {
            playSound(700, 0.1); tiles.score += 10; tiles.combo++;
            t.hit = true;
            tiles.falling.splice(idx, 1);
            bumpBest("tiles", tiles.score); refreshMenuBadges();
          }
        } else if (t.y > 340) {
          tiles.falling.splice(idx, 1);
          if (!t.hit) {
            tiles.combo = 0;
            tiles.lives--;
            playSound(150, 0.2);
            if (tiles.lives <= 0) {
              tiles.gameOver = true;
              bumpBest("tiles", tiles.score); refreshMenuBadges();
            } else {
              showToast("Missed! Lives left: " + tiles.lives, "bad");
            }
          }
        }
      });
      ctx.fillStyle = "#ffffff"; ctx.font = "16px Arial";
      ctx.fillText("🎵 Press 1·2·3 — Score: " + tiles.score + "  Combo: " + tiles.combo + "  Lives: " + "❤️".repeat(Math.max(0, tiles.lives)), 20, 40);
      if (tiles.gameOver) {
        ctx.fillStyle = "rgba(15,23,42,0.85)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#f59e0b"; ctx.font = "bold 32px Segoe UI"; ctx.fillText("OUT OF LIVES", 250, 190);
        ctx.fillStyle = "#ffffff"; ctx.font = "18px Segoe UI"; ctx.fillText("Score: " + tiles.score + " — tap to restart", 260, 230);
      }

    } else if (currentGame === "ox") {
      ctx.fillStyle = "#ffffff"; ctx.font = "20px Arial";
      ctx.fillText(oxGameOver ? "Game over — tap the board to play again" : "❌⭕ Tap a square to play vs AI", 210, 50);
      for (let i = 0; i < 9; i++) {
        const rx = 250 + (i % 3) * 85, ry = 90 + Math.floor(i / 3) * 85;
        ctx.fillStyle = "#1e293b"; ctx.fillRect(rx, ry, 75, 75);
        ctx.fillStyle = oxBoard[i] === "❌" ? "#eab308" : "#ef4444";
        ctx.font = "bold 32px Arial"; ctx.fillText(oxBoard[i], rx + 22, ry + 50);
      }

    } else if (currentGame === "candy") {
      ctx.fillStyle = "#ffffff"; ctx.font = "18px Arial";
      ctx.fillText("🍬 Memory Match — Moves: " + candy.moves + "   Matches: " + candy.matches + "/" + (candy.cards.length / 2), 150, 50);
      const cols = candy.cols, cardW = 140, cardH = 140, gapX = 20, gapY = 20;
      const totalW = cols * cardW + (cols - 1) * gapX;
      const startX = (canvas.width - totalW) / 2;
      const startY = 90;
      candy.cards.forEach(function (card, i) {
        const col = i % cols, row = Math.floor(i / cols);
        const rx = startX + col * (cardW + gapX), ry = startY + row * (cardH + gapY);
        const flipped = card.matched || candy.flippedIdx.indexOf(i) !== -1;
        ctx.fillStyle = card.matched ? "#14532d" : (flipped ? "#2563eb" : "#1e293b");
        ctx.strokeStyle = card.matched ? "#22c55e" : "#3b82f6"; ctx.lineWidth = 2;
        ctx.fillRect(rx, ry, cardW, cardH); ctx.strokeRect(rx, ry, cardW, cardH);
        if (flipped) {
          ctx.font = "54px Arial"; ctx.fillText(card.emoji, rx + cardW/2 - 27, ry + cardH/2 + 18);
        } else {
          ctx.fillStyle = "#64748b"; ctx.font = "bold 30px Arial"; ctx.fillText("?", rx + cardW/2 - 9, ry + cardH/2 + 10);
        }
      });
      if (candy.gameOver) {
        ctx.fillStyle = "rgba(15,23,42,0.85)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#f59e0b"; ctx.font = "bold 30px Segoe UI"; ctx.fillText("BOARD CLEARED!", 230, 190);
        ctx.fillStyle = "#ffffff"; ctx.font = "18px Segoe UI"; ctx.fillText("Solved in " + candy.moves + " moves — tap to play again", 170, 230);
      }

    } else if (currentGame === "imposter") {
      ctx.fillStyle = "#ffffff"; ctx.font = "18px Arial";
      ctx.fillText("🕵️ Spot the impostor — Streak: " + imposter.streak + "   Lives: " + "❤️".repeat(Math.max(0, imposter.lives)), 130, 50);
      for (let i = 0; i < 4; i++) {
        const rx = 90 + i * 150;
        const lightness = 50 + (i === imposter.oddIndex ? imposter.shift : 0);
        ctx.fillStyle = "hsl(" + imposter.baseHue + ", 65%, " + lightness + "%)";
        ctx.fillRect(rx, 140, 110, 110);
      }
      if (imposter.gameOver) {
        ctx.fillStyle = "rgba(15,23,42,0.85)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#f59e0b"; ctx.font = "bold 30px Segoe UI"; ctx.fillText("OUT OF LIVES", 250, 190);
        ctx.fillStyle = "#ffffff"; ctx.font = "18px Segoe UI"; ctx.fillText("Best streak: " + getStats().imposter + " — tap to retry", 200, 230);
      }

    } else if (currentGame === "hayday") {
      ctx.fillStyle = "#15803d"; ctx.fillRect(0, 0, canvas.width, canvas.height);
      landPlots.forEach(function (plot) {
        if (plot.state === "growing") {
          const speed = plot.crop === "wheat" ? 1.8 : (plot.crop === "corn" ? 1.0 : 0.6);
          plot.growthProgress += speed;
          if (plot.growthProgress >= 100) { plot.growthProgress = 100; plot.state = "ready"; }
        }
      });
      landPlots.forEach(function (plot) {
        ctx.fillStyle = "#78350f"; ctx.fillRect(plot.x, plot.y, plot.w, plot.h);
        ctx.strokeStyle = "#451a03"; ctx.lineWidth = 3; ctx.strokeRect(plot.x, plot.y, plot.w, plot.h);
        if (plot.state === "growing") {
          ctx.fillStyle = "#22c55e";
          const progressSize = (plot.growthProgress / 100) * (plot.w - 30);
          ctx.fillRect(plot.x + 15, plot.y + plot.h/2 - 5, progressSize, 10);
        } else if (plot.state === "ready") {
          ctx.font = "30px Segoe UI";
          const icon = plot.crop === "wheat" ? "🌾" : (plot.crop === "corn" ? "🌽" : "🥕");
          ctx.fillText(icon, plot.x + plot.w/2 - 15, plot.y + plot.h/2 + 10);
        }
      });
      ctx.fillStyle = "rgba(15,23,42,0.75)"; ctx.fillRect(0, 0, canvas.width, 40);
      ctx.fillStyle = "#fef08a"; ctx.font = "bold 15px Segoe UI";
      ctx.fillText("🪙 Coins: " + farmCoins, 30, 26);
      ctx.fillText("🌾 Wheat: " + silo.wheat, 200, 26);
      ctx.fillText("🌽 Corn: " + silo.corn, 380, 26);
      ctx.fillText("🥕 Carrot: " + silo.carrot, 560, 26);

    } else if (currentGame === "fish") {
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
            if (hook.caughtFish) {
              playSound(880, 0.2); fishScore += hook.caughtFish.points; hook.caughtFish = null;
              bumpBest("fish", fishScore); refreshMenuBadges();
            }
          }
        }
        fishes.forEach(function (f, idx) {
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
      ctx.fillStyle = "#38bdf8"; ctx.fillRect(0, 0, canvas.width, 50);
      ctx.fillStyle = "#0284c7"; ctx.fillRect(0, 50, canvas.width, 4);
      ctx.fillStyle = "#78350f"; ctx.beginPath();
      ctx.moveTo(boat.x, boat.y); ctx.lineTo(boat.x + boat.width, boat.y);
      ctx.lineTo(boat.x + boat.width - 12, boat.y + boat.height); ctx.lineTo(boat.x + 12, boat.y + boat.height);
      ctx.closePath(); ctx.fill();
      ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(hook.x, hook.startY); ctx.lineTo(hook.x, hook.y); ctx.stroke();
      ctx.strokeStyle = "#cbd5e1"; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.arc(hook.x - 4, hook.y, 4, 0, Math.PI); ctx.stroke();
      fishes.forEach(function (f) {
        ctx.fillStyle = f.color; ctx.beginPath();
        ctx.ellipse(f.x, f.y, f.size, f.size/1.6, 0, 0, Math.PI*2); ctx.fill();
        ctx.beginPath(); const tailX = f.x - (f.size * f.dir);
        ctx.moveTo(tailX, f.y); ctx.lineTo(tailX - (8*f.dir), f.y - 6); ctx.lineTo(tailX - (8*f.dir), f.y + 6);
        ctx.closePath(); ctx.fill();
        ctx.fillStyle = "#000"; ctx.beginPath();
        ctx.arc(f.x + (f.size/2*f.dir), f.y - 2, 2, 0, Math.PI*2); ctx.fill();
      });
      ctx.fillStyle = "#ffffff"; ctx.font = "bold 18px Segoe UI";
      ctx.fillText("🪙 Score: " + fishScore, 20, 30);
      ctx.fillText("⏳ Time: " + fishTimeLeft + "s", canvas.width - 130, 30);
      if (fishGameOver) {
        ctx.fillStyle = "rgba(15,23,42,0.85)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#f59e0b"; ctx.font = "bold 36px Segoe UI"; ctx.fillText("TIME'S UP!", 280, 190);
        ctx.fillStyle = "#ffffff"; ctx.font = "22px Segoe UI"; ctx.fillText("Final score: " + fishScore + " — tap to fish again", 210, 230);
      }

    } else if (currentGame === "puzzle") {
      ctx.fillStyle = "#ffffff"; ctx.font = "26px Arial";
      ctx.fillText("🧩 " + puzzle.a + " " + puzzle.op + " " + puzzle.b + " = ?", 270, 90);
      ctx.font = "14px Arial"; ctx.fillStyle = "#94a3b8";
      ctx.fillText("Streak: " + puzzle.streak + "   Best: " + puzzle.best, 300, 118);

      const choiceW = 150, choiceH = 70, gapX = 30, gapY = 25, cols = 2;
      const totalW = cols * choiceW + (cols - 1) * gapX;
      const startX = (canvas.width - totalW) / 2;
      const startY = 150;
      puzzle.choices.forEach(function (val, i) {
        const col = i % cols, row = Math.floor(i / cols);
        const rx = startX + col * (choiceW + gapX), ry = startY + row * (choiceH + gapY);
        ctx.fillStyle = "#a855f7"; ctx.fillRect(rx, ry, choiceW, choiceH);
        ctx.strokeStyle = "#7c3aed"; ctx.lineWidth = 2; ctx.strokeRect(rx, ry, choiceW, choiceH);
        ctx.fillStyle = "#ffffff"; ctx.font = "bold 22px Arial";
        ctx.fillText(String(val), rx + choiceW/2 - 12, ry + choiceH/2 + 8);
      });

      if (puzzle.feedbackTimer > 0) {
        puzzle.feedbackTimer -= 16;
        ctx.fillStyle = puzzle.feedback.indexOf("✅") === 0 ? "#4ade80" : "#f87171";
        ctx.font = "bold 16px Arial";
        ctx.fillText(puzzle.feedback, 230, 345);
      }
    }

    if (currentGame !== "") requestAnimationFrame(runLoop);
  }
})();
</script>
</body>
</html>
"""

html = (
    ARCADE_TEMPLATE
    .replace("__USERNAME__", str(user["username"]))
    .replace("__LEVEL__", str(user["level"]))
    .replace("__XP__", str(user["xp"]))
    .replace("__NEXT_XP__", str(next_level_xp))
)

components.html(html, height=920, scrolling=True)