import pygame
import random
import sys
import math

# --- 1. INITIALIZE ---
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 Python Roblox-Style Arcade Hub")
clock = pygame.time.Clock()

# Colors
DARK_BG = (15, 23, 42)
CARD_BG = (30, 41, 59)
TEXT_WHITE = (241, 245, 249)
GOLD = (234, 179, 8)
RED = (239, 68, 68)
BLUE = (59, 130, 246)
GREEN = (34, 197, 94)
PURPLE = (168, 85, 247)

# Fonts
title_font = pygame.font.SysFont("Arial", 40, bold=True)
hud_font = pygame.font.SysFont("Arial", 24, bold=True)

# Sound Generator
def create_sound(freq, duration):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        val = int(127 + 127 * math.sin(2 * math.pi * freq * t))
        buf.append(max(0, min(255, val)))
    return pygame.mixer.Sound(buffer=bytes(buf))

coin_sound = create_sound(880, 0.12)
hit_sound = create_sound(160, 0.25)
click_sound = create_sound(440, 0.08)

# Game Manager State
current_scene = "MENU"  # "MENU", "RACER", "OX", "TILES"
total_gold = 0

# ==============================================================================
# 🎮 GAME 1: RACER STATE
# ==============================================================================
racer_x, racer_y = 100, 300
racer_coins = []
racer_obs = []

def reset_racer():
    global racer_x, racer_y, racer_coins, racer_obs
    racer_x, racer_y = 100, 300
    racer_coins = [{"x": random.randint(400, 750), "y": random.randint(50, 550)} for _ in range(4)]
    racer_obs = [{"x": random.randint(800, 1100), "y": random.randint(50, 550), "speed": random.randint(5, 8)} for _ in range(4)]

# ==============================================================================
# ❌⭕ GAME 2: OX TIC-TAC-TOE STATE
# ==============================================================================
ox_board = [""] * 9
ox_winner = None

def reset_ox():
    global ox_board, ox_winner
    ox_board = [""] * 9
    ox_winner = None

def check_ox_winner(b):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for x, y, z in wins:
        if b[x] == b[y] == b[z] and b[x] != "":
            return b[x]
    return "Tie" if "" not in b else None

# ==============================================================================
# 🎵 GAME 3: TILES HOP RHYTHM STATE
# ==============================================================================
falling_tiles = []
tile_score = 0

def reset_tiles():
    global falling_tiles, tile_score
    falling_tiles = []
    tile_score = 0

# ==============================================================================
# MAIN ENGINE LOOP (60 FPS)
# ==============================================================================
reset_racer()
reset_ox()
reset_tiles()

while True:
    screen.fill(DARK_BG)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --------------------------------------------------------------------------
    # SCENE: ARCADE MENU HUB
    # --------------------------------------------------------------------------
    if current_scene == "MENU":
        title = title_font.render("🎮 ROBLOX PYTHON ARCADE HUB", True, TEXT_WHITE)
        gold_txt = hud_font.render(f"🪙 Total Gold Earned: {total_gold}", True, GOLD)
        screen.blit(title, (120, 50))
        screen.blit(gold_txt, (280, 110))

        # Menu Cards Buttons
        mouse_pos = pygame.mouse.get_pos()
        
        btn_racer = pygame.Rect(100, 180, 600, 100)
        btn_ox = pygame.Rect(100, 310, 600, 100)
        btn_tiles = pygame.Rect(100, 440, 600, 100)

        for btn, text, color in [(btn_racer, "🏎️ PLAY: Hill Climb Racer (Arrow Keys)", BLUE),
                                 (btn_ox, "❌⭕ PLAY: OX Tic-Tac-Toe vs AI (Mouse Click)", GREEN),
                                 (btn_tiles, "🎵 PLAY: Tiles Hop Rhythm (Keys 1, 2, 3)", PURPLE)]:
            bg = color if btn.collidepoint(mouse_pos) else CARD_BG
            pygame.draw.rect(screen, bg, btn, border_radius=12)
            lbl = hud_font.render(text, True, TEXT_WHITE)
            screen.blit(lbl, (btn.x + 40, btn.y + 35))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_racer.collidepoint(event.pos):
                    click_sound.play()
                    reset_racer()
                    current_scene = "RACER"
                elif btn_ox.collidepoint(event.pos):
                    click_sound.play()
                    reset_ox()
                    current_scene = "OX"
                elif btn_tiles.collidepoint(event.pos):
                    click_sound.play()
                    reset_tiles()
                    current_scene = "TILES"

    # --------------------------------------------------------------------------
    # SCENE: 🏎️ HILL CLIMB RACER
    # --------------------------------------------------------------------------
    elif current_scene == "RACER":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and racer_x > 30: racer_x -= 6
        if keys[pygame.K_RIGHT] and racer_x < 770: racer_x += 6
        if keys[pygame.K_UP] and racer_y > 30: racer_y -= 6
        if keys[pygame.K_DOWN] and racer_y < 570: racer_y += 6

        # Draw Coins
        for coin in racer_coins:
            pygame.draw.circle(screen, GOLD, (coin["x"], coin["y"]), 12)
            if math.hypot(racer_x - coin["x"], racer_y - coin["y"]) < 32:
                total_gold += 10
                coin_sound.play()
                coin["x"] = random.randint(800, 1000)
                coin["y"] = random.randint(50, 550)

        # Draw Obstacles
        for obs in racer_obs:
            obs["x"] -= obs["speed"]
            if obs["x"] < -20:
                obs["x"] = random.randint(800, 1100)
                obs["y"] = random.randint(50, 550)
            pygame.draw.rect(screen, RED, (obs["x"], obs["y"], 30, 30))

            if abs(racer_x - (obs["x"]+15)) < 30 and abs(racer_y - (obs["y"]+15)) < 30:
                hit_sound.play()
                obs["x"] = random.randint(800, 1100)

        # Draw Player
        pygame.draw.circle(screen, BLUE, (racer_x, racer_y), 20)

        txt = hud_font.render(f"🪙 Gold: {total_gold} | Press ESC for Menu", True, TEXT_WHITE)
        screen.blit(txt, (20, 20))

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            current_scene = "MENU"

    # --------------------------------------------------------------------------
    # SCENE: ❌⭕ OX (TIC-TAC-TOE)
    # --------------------------------------------------------------------------
    elif current_scene == "OX":
        txt = hud_font.render(f"❌⭕ Tic-Tac-Toe | Press ESC for Menu", True, TEXT_WHITE)
        screen.blit(txt, (20, 20))

        grid_rects = []
        for i in range(9):
            row, col = i // 3, i % 3
            rect = pygame.Rect(250 + col * 105, 150 + row * 105, 100, 100)
            grid_rects.append(rect)
            pygame.draw.rect(screen, CARD_BG, rect, border_radius=8)

            mark = hud_font.render(ox_board[i], True, GOLD if ox_board[i] == "❌" else RED)
            screen.blit(mark, (rect.x + 40, rect.y + 35))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ox_winner is None:
                for idx, rect in enumerate(grid_rects):
                    if rect.collidepoint(event.pos) and ox_board[idx] == "":
                        ox_board[idx] = "❌"
                        click_sound.play()
                        ox_winner = check_ox_winner(ox_board)
                        
                        # AI Move
                        empty = [i for i, v in enumerate(ox_board) if v == ""]
                        if empty and ox_winner is None:
                            ox_board[random.choice(empty)] = "⭕"
                            ox_winner = check_ox_winner(ox_board)
                        
                        if ox_winner == "❌":
                            total_gold += 30
                            coin_sound.play()

        if ox_winner:
            w_txt = hud_font.render(f"Winner: {ox_winner}! Click anywhere on board to reset", True, GREEN)
            screen.blit(w_txt, (220, 490))
            if pygame.mouse.get_pressed()[0]:
                reset_ox()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            current_scene = "MENU"

    # --------------------------------------------------------------------------
    # SCENE: 🎵 TILES HOP RHYTHM
    # --------------------------------------------------------------------------
    elif current_scene == "TILES":
        txt = hud_font.render(f"🎵 Press 1, 2, or 3 when tile hits line! Score: {tile_score} | ESC for Menu", True, TEXT_WHITE)
        screen.blit(txt, (20, 20))

        # Target Line
        pygame.draw.line(screen, GREEN, (200, 500), (600, 500), 4)

        # Spawn Tiles
        if random.random() < 0.04:
            col = random.choice([0, 1, 2])
            falling_tiles.append({"col": col, "y": 50})

        # Render Lanes
        for i in range(3):
            pygame.draw.rect(screen, CARD_BG, (220 + i * 130, 80, 100, 400), 2)
            lbl = hud_font.render(str(i + 1), True, GOLD)
            screen.blit(lbl, (260 + i * 130, 520))

        # Update Tiles
        for t in falling_tiles[:]:
            t["y"] += 6
            pygame.draw.rect(screen, PURPLE, (225 + t["col"] * 130, t["y"], 90, 40), border_radius=6)

            if t["y"] > 550:
                falling_tiles.remove(t)

        for event in events:
            if event.type == pygame.KEYDOWN:
                pressed_col = None
                if event.key == pygame.K_1: pressed_col = 0
                elif event.key == pygame.K_2: pressed_col = 1
                elif event.key == pygame.K_3: pressed_col = 2

                if pressed_col is not None:
                    hit = False
                    for t in falling_tiles[:]:
                        if t["col"] == pressed_col and abs(t["y"] - 480) < 40:
                            tile_score += 10
                            total_gold += 5
                            coin_sound.play()
                            falling_tiles.remove(t)
                            hit = True
                            break
                    if not hit:
                        hit_sound.play()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            current_scene = "MENU"

    # Refresh Window
    pygame.display.flip()
    clock.tick(60)