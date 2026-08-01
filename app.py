import streamlit as st
import random
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Farm & Doors Adventure", page_icon="🌾", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .stButton>button {
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- SAFE SESSION STATE INITIALIZATION ---
def init_game():
    st.session_state.gold = 100
    st.session_state.health = 100
    st.session_state.max_health = 100
    st.session_state.keys = 1  # Integer to prevent type errors!
    st.session_state.potions = 2
    
    # Farming State (Hay Day System)
    st.session_state.farm_plots = [
        {"crop": None, "planted_at": None, "grow_time": 0} for _ in range(4)
    ]
    st.session_state.inventory = {"Wheat": 0, "Magic Beans": 0, "Golden Berries": 0}
    st.session_state.active_puzzle = None
    st.session_state.audio = None


if 'keys' not in st.session_state or type(st.session_state.keys) != int:
    init_game()

# --- HEADER / METRICS ---
st.title("🌾 Mystery Farm & Brain Doors 🚪")

m1, m2, m3, m4 = st.columns(4)
m1.metric("🪙 Gold Points", f"{st.session_state.gold}")
m2.metric("❤️ Health", f"{st.session_state.health}/{st.session_state.max_health}")
m3.metric("🔑 Dungeon Keys", f"{st.session_state.keys}")
m4.metric("🧪 Health Potions", f"{st.session_state.potions}")

st.divider()

# --- AUDIO PLAYBACK ---
if st.session_state.get("audio"):
    st.audio(st.session_state.audio, autoplay=True)
    st.session_state.audio = None

# --- SIDEBAR: SHOP & RECOVER ---
with st.sidebar:
    st.header("🛒 Market & Supplies")
    
    if st.button("🔑 Buy Dungeon Key (40 Gold)"):
        if st.session_state.gold >= 40:
            st.session_state.gold -= 40
            st.session_state.keys += 1
            st.success("Bought 1 Key!")
            st.rerun()
        else:
            st.error("Not enough Gold!")
            
    if st.button("🧪 Buy Potion (30 Gold)"):
        if st.session_state.gold >= 30:
            st.session_state.gold -= 30
            st.session_state.potions += 1
            st.success("Bought 1 Potion!")
            st.rerun()
        else:
            st.error("Not enough Gold!")

    if st.button("❤️ Drink Potion (+30 HP)"):
        if st.session_state.potions > 0 and st.session_state.health < st.session_state.max_health:
            st.session_state.potions -= 1
            st.session_state.health = min(st.session_state.max_health, st.session_state.health + 30)
            st.success("Healed 30 HP!")
            st.rerun()

    st.divider()
    if st.button("🔄 Reset Game"):
        init_game()
        st.rerun()

# --- GAME OVER CHECK ---
if st.session_state.health <= 0:
    st.error("☠️ **GAME OVER! You ran out of health.**")
    if st.button("🔄 Restart Game"):
        init_game()
        st.rerun()
    st.stop()

# --- MAIN TABS ---
tab_farm, tab_doors = st.tabs(["🌾 Hay Day Farm", "🚪 Mystery Doors & Puzzles"])

# ==================== TAB 1: HAY DAY FARMING ====================
with tab_farm:
    st.subheader("👨‍🌾 Your Crops & Harvesting")
    st.caption("Plant crops, harvest them, and sell them for gold or key trades!")

    col_inv, col_plots = st.columns([1, 2])

    with col_inv:
        st.write("### 🧺 Silo Inventory")
        for crop, count in st.session_state.inventory.items():
            st.write(f"- **{crop}**: {count}")
        
        st.write("---")
        st.write("### 💰 Sell Produce")
        if st.button("Sell 1x Wheat (+15 Gold)"):
            if st.session_state.inventory["Wheat"] > 0:
                st.session_state.inventory["Wheat"] -= 1
                st.session_state.gold += 15
                st.rerun()
            else:
                st.error("No Wheat in inventory!")

        if st.button("Sell 1x Magic Beans (+40 Gold)"):
            if st.session_state.inventory["Magic Beans"] > 0:
                st.session_state.inventory["Magic Beans"] -= 1
                st.session_state.gold += 40
                st.rerun()
            else:
                st.error("No Magic Beans in inventory!")

        if st.button("Trade 3x Golden Berries ➡️ 1 Key 🔑"):
            if st.session_state.inventory["Golden Berries"] >= 3:
                st.session_state.inventory["Golden Berries"] -= 3
                st.session_state.keys += 1
                st.success("Traded for 1 Key!")
                st.rerun()
            else:
                st.error("Need 3 Golden Berries!")

    with col_plots:
        st.write("### 🌱 Farm Plots")
        grid = st.columns(2)
        
        seeds = {
            "Wheat": {"cost": 5, "time": 5},
            "Magic Beans": {"cost": 15, "time": 10},
            "Golden Berries": {"cost": 30, "time": 15}
        }

        for idx, plot in enumerate(st.session_state.farm_plots):
            with grid[idx % 2]:
                st.markdown(f"**Plot #{idx + 1}**")
                
                if plot["crop"] is None:
                    selected_seed = st.selectbox(f"Select Seed", list(seeds.keys()), key=f"seed_{idx}")
                    if st.button(f"Plant {selected_seed}", key=f"plant_{idx}"):
                        cost = seeds[selected_seed]["cost"]
                        if st.session_state.gold >= cost:
                            st.session_state.gold -= cost
                            plot["crop"] = selected_seed
                            plot["planted_at"] = time.time()
                            plot["grow_time"] = seeds[selected_seed]["time"]
                            st.rerun()
                        else:
                            st.error("Need more gold!")
                else:
                    elapsed = time.time() - plot["planted_at"]
                    remaining = max(0, int(plot["grow_time"] - elapsed))
                    
                    if remaining > 0:
                        st.info(f"🌾 {plot['crop']} growing... ({remaining}s remaining)")
                        if st.button("🔄 Refresh Status", key=f"ref_{idx}"):
                            st.rerun()
                    else:
                        st.success(f"✨ {plot['crop']} Ready!")
                        if st.button(f"Harvest {plot['crop']}", key=f"harv_{idx}"):
                            st.session_state.inventory[plot["crop"]] += 1
                            plot["crop"] = None
                            plot["planted_at"] = None
                            st.rerun()

# ==================== TAB 2: BRAIN PUZZLE DOORS ====================
with tab_doors:
    st.subheader("🚪 The Brain Puzzle Dungeon")
    st.caption("Open doors to face logic puzzles, solve riddles, or claim hidden rewards!")

    if st.session_state.active_puzzle is None:
        d1, d2, d3 = st.columns(3)
        
        with d1:
            st.markdown("### 🚪 Door 1: Math Lock")
            if st.button("Enter Door 1"):
                st.session_state.active_puzzle = "math"
                st.rerun()
                
        with d2:
            st.markdown("### 🔑 Door 2: Vault (Needs Key)")
            if st.button("Open Vault"):
                if st.session_state.keys > 0:
                    st.session_state.keys -= 1
                    found = random.randint(50, 100)
                    st.session_state.gold += found
                    st.session_state.audio = "https://cdn.freesound.org/previews/274/274178_5123851-lq.mp3"
                    st.success(f"Vault opened! Found {found} Gold!")
                else:
                    st.error("You need a Dungeon Key!")
                    
        with d3:
            st.markdown("### 🧩 Door 3: Logic Riddle")
            if st.button("Enter Door 3"):
                st.session_state.active_puzzle = "riddle"
                st.rerun()

    # --- ACTIVE PUZZLE DISPLAY ---
    else:
        st.divider()
        if st.session_state.active_puzzle == "math":
            st.write("### 🧠 Brain Challenge: Code Breaker")
            st.write("Solve the equation to disarm the trap and get 40 Gold:")
            st.latex(r"(12 \times 4) - 18 = ?")
            
            ans = st.number_input("Your Answer:", step=1, key="math_ans")
            if st.button("Submit Code"):
                if ans == 30:
                    st.session_state.audio = "https://cdn.freesound.org/previews/274/274178_5123851-lq.mp3"
                    st.success("🎉 Trap Disarmed! You earned 40 Gold!")
                    st.session_state.gold += 40
                else:
                    st.session_state.audio = "https://cdn.freesound.org/previews/145/145303_2615119-lq.mp3"
                    st.error("💥 Wrong code! Trap triggered (-20 HP)")
                    st.session_state.health -= 20
                st.session_state.active_puzzle = None
                st.rerun()

        elif st.session_state.active_puzzle == "riddle":
            st.write("### 🧩 Brain Challenge: Sphinx Riddle")
            st.write("> *'The more of me you take, the more you leave behind. What am I?'*")
            
            r_ans = st.text_input("Your Answer:", key="riddle_ans")
            if st.button("Solve Riddle"):
                if "footstep" in r_ans.lower() or "step" in r_ans.lower():
                    st.session_state.audio = "https://cdn.freesound.org/previews/274/274178_5123851-lq.mp3"
                    st.success("🎉 Correct! You were awarded 1 Key and 30 Gold!")
                    st.session_state.keys += 1
                    st.session_state.gold += 30
                else:
                    st.session_state.audio = "https://cdn.freesound.org/previews/145/145303_2615119-lq.mp3"
                    st.error("❌ Incorrect! Darkness hits you (-15 HP)")
                    st.session_state.health -= 15
                st.session_state.active_puzzle = None
                st.rerun()