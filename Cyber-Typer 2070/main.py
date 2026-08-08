import sys
import random
import time
import math
import array
import pygame

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Fixed Internal Virtual Canvas Dimensions
VIRTUAL_WIDTH = 1000
VIRTUAL_HEIGHT = 700
FPS = 60

# Palette
COLOR_BG = (10, 15, 30)            # Deep Space Slate
COLOR_PANEL = (18, 26, 47)         # Terminal Glass
COLOR_BORDER = (56, 189, 248)       # Neon Cyan
COLOR_TEXT_MAIN = (248, 250, 252)   # Bright White
COLOR_TEXT_MUTED = (100, 116, 139) # Slate Muted
COLOR_ACCENT_GREEN = (34, 197, 94) # Matrix Green
COLOR_ACCENT_RED = (239, 68, 68)   # Alert Red
COLOR_CURSOR = (236, 72, 153)      # Neon Pink
COLOR_ALERT = (245, 158, 11)       # Amber Alert

# Code Prompts
CODE_PROMPTS = [
    "def calculate_metrics(data):",
    "import pandas as pd",
    "git commit -m 'Fix production bug'",
    "npm run build --production",
    "select * from users where active = True;",
    "docker-compose up -d --build",
    "const response = await fetch(url);",
    "for item in array.items():",
    "lambda x: x['score'] * 100",
    "python main.py --env production",
    "return jsonify({'status': 200});",
    "pip install pandas scikit-learn",
    "model.fit(X_train, y_train)",
    "export default function App() {"
]

# Security Breaches Commands
SECURITY_OVERRIDES = [
    "sudo systemctl restart firewall",
    "iptables -A INPUT -p tcp --dport 80 -j DROP",
    "killall -9 malicious_process",
    "chmod 700 /etc/security/keys",
    "openssl req -x509 -newkey rsa:4096"
]


# --- SYNTHESIZED SOUND ENGINE ---
def generate_beep_sound(frequency=440, duration=0.08, volume=0.1):
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = array.array('h', [0] * (n_samples * 2))
    for i in range(n_samples):
        t = float(i) / sample_rate
        val = int(math.sin(2.0 * math.pi * frequency * t) * 32767 * volume)
        buf[i * 2] = val
        buf[i * 2 + 1] = val
    return pygame.mixer.Sound(buffer=buf)


try:
    SND_KEY = generate_beep_sound(600, 0.04, 0.08)
    SND_ERROR = generate_beep_sound(180, 0.12, 0.15)
    SND_ALERT = generate_beep_sound(880, 0.2, 0.2)
    SND_SUCCESS = generate_beep_sound(1200, 0.1, 0.1)
except Exception:
    SND_KEY = SND_ERROR = SND_ALERT = SND_SUCCESS = None


class CyberTyperGame:
    def __init__(self):
        # Set hardware flags for seamless OS scaling without resolution disruption
        flags = pygame.RESIZABLE | pygame.SCALED
        self.screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), flags)
        pygame.display.set_caption("Cyber-Typer 2070: Developer Terminal")
        self.clock = pygame.time.Clock()

        # Canvas surface for drawing internal virtual grid
        self.canvas = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

        # Fixed Crisp Fonts
        self.font_title = pygame.font.SysFont("Consolas", 36, bold=True)
        self.font_code = pygame.font.SysFont("Consolas", 26)
        self.font_hud = pygame.font.SysFont("Consolas", 18, bold=True)

        self.reset_game()

    def reset_game(self):
        self.target_code = random.choice(CODE_PROMPTS)
        self.user_input = ""
        self.score = 0
        self.time_left = 60.0
        self.streak = 0
        self.max_streak = 0
        self.total_chars = 0
        self.correct_chars = 0
        self.game_state = "MENU"  # MENU, PLAYING, GAMEOVER

        # Breach Task Variables
        self.active_breach = False
        self.breach_code = ""
        self.breach_input = ""
        self.breach_timer = 0.0
        self.next_breach_trigger = random.uniform(10.0, 25.0)

    def trigger_breach_alert(self):
        self.active_breach = True
        self.breach_code = random.choice(SECURITY_OVERRIDES)
        self.breach_input = ""
        self.breach_timer = 12.0
        if SND_ALERT:
            SND_ALERT.play()

    def calculate_wpm_and_accuracy(self):
        elapsed_min = (60.0 - self.time_left) / 60.0
        if elapsed_min <= 0:
            return 0, 100.0
        words = self.correct_chars / 5.0
        wpm = int(words / elapsed_min)
        acc = (self.correct_chars / self.total_chars * 100) if self.total_chars > 0 else 100.0
        return max(0, wpm), min(100.0, acc)

    def draw_glass_panel(self, x, y, w, h, border_color=COLOR_BORDER):
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill((18, 26, 47, 230))
        self.canvas.blit(panel, (x, y))
        pygame.draw.rect(self.canvas, border_color, (x, y, w, h), width=2, border_radius=10)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.canvas.fill(COLOR_BG)

            if self.game_state == "PLAYING":
                self.time_left -= dt

                if not self.active_breach and (60.0 - self.time_left) >= self.next_breach_trigger:
                    self.trigger_breach_alert()

                if self.active_breach:
                    self.breach_timer -= dt
                    if self.breach_timer <= 0:
                        self.active_breach = False
                        self.score = max(0, self.score - 300)
                        self.next_breach_trigger = (60.0 - self.time_left) + random.uniform(15.0, 25.0)
                        if SND_ERROR:
                            SND_ERROR.play()

                if self.time_left <= 0:
                    self.time_left = 0
                    self.game_state = "GAMEOVER"

            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if self.game_state in ["MENU", "GAMEOVER"]:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                            self.game_state = "PLAYING"

                    elif self.game_state == "PLAYING":
                        if event.key == pygame.K_BACKSPACE:
                            if self.active_breach:
                                self.breach_input = self.breach_input[:-1]
                            else:
                                self.user_input = self.user_input[:-1]

                        elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                            if self.active_breach:
                                if self.breach_input == self.breach_code:
                                    self.score += 400
                                    self.active_breach = False
                                    self.next_breach_trigger = (60.0 - self.time_left) + random.uniform(15.0, 25.0)
                                    if SND_SUCCESS:
                                        SND_SUCCESS.play()
                            else:
                                if self.user_input == self.target_code:
                                    multiplier = 1 + (self.streak // 5)
                                    self.score += (100 + len(self.target_code) * 2) * multiplier
                                    self.target_code = random.choice(CODE_PROMPTS)
                                    self.user_input = ""
                                    if SND_SUCCESS:
                                        SND_SUCCESS.play()

                        else:
                            char = event.unicode
                            if char and ord(char) >= 32:
                                if self.active_breach:
                                    if len(self.breach_input) < len(self.breach_code):
                                        self.breach_input += char
                                else:
                                    if len(self.user_input) < len(self.target_code):
                                        self.user_input += char
                                        self.total_chars += 1
                                        idx = len(self.user_input) - 1
                                        if self.target_code[idx] == char:
                                            self.correct_chars += 1
                                            self.streak += 1
                                            self.max_streak = max(self.max_streak, self.streak)
                                            if SND_KEY:
                                                SND_KEY.play()
                                        else:
                                            self.streak = 0
                                            if SND_ERROR:
                                                SND_ERROR.play()

            # --- RENDERING (VIRTUAL CANVAS) ---
            self.draw_glass_panel(50, 40, 900, 620)

            title_txt = self.font_title.render("⚡ CYBER-TYPER 2070 ⚡", True, COLOR_BORDER)
            self.canvas.blit(title_txt, (VIRTUAL_WIDTH // 2 - title_txt.get_width() // 2, 55))

            if self.game_state == "PLAYING":
                wpm, accuracy = self.calculate_wpm_and_accuracy()

                # HUD
                t_color = COLOR_ACCENT_RED if self.time_left < 10 else COLOR_TEXT_MAIN
                hud_1 = self.font_hud.render(f"TIME: {self.time_left:.1f}s", True, t_color)
                hud_2 = self.font_hud.render(f"SPEED: {wpm} WPM", True, COLOR_ACCENT_GREEN)
                hud_3 = self.font_hud.render(f"ACC: {accuracy:.1f}%", True, COLOR_BORDER)
                hud_4 = self.font_hud.render(f"STREAK: {self.streak}x", True, COLOR_CURSOR)
                hud_5 = self.font_hud.render(f"SCORE: {self.score}", True, COLOR_TEXT_MAIN)

                self.canvas.blit(hud_1, (80, 115))
                self.canvas.blit(hud_2, (260, 115))
                self.canvas.blit(hud_3, (450, 115))
                self.canvas.blit(hud_4, (640, 115))
                self.canvas.blit(hud_5, (800, 115))

                # Terminal Inner Box
                self.draw_glass_panel(80, 155, 840, 475, border_color=(255, 255, 255, 30))

                if not self.active_breach:
                    prompt_lbl = self.font_hud.render("// TARGET CODE COMMAND:", True, COLOR_TEXT_MUTED)
                    self.canvas.blit(prompt_lbl, (110, 185))

                    start_x = 110
                    start_y = 230
                    for i, char in enumerate(self.target_code):
                        if i < len(self.user_input):
                            c = COLOR_ACCENT_GREEN if self.user_input[i] == char else COLOR_ACCENT_RED
                        else:
                            c = COLOR_TEXT_MUTED
                        cs = self.font_code.render(char, True, c)
                        self.canvas.blit(cs, (start_x, start_y))
                        start_x += cs.get_width()

                    input_lbl = self.font_hud.render("> ENTER COMMAND:", True, COLOR_BORDER)
                    self.canvas.blit(input_lbl, (110, 330))

                    in_surf = self.font_code.render(self.user_input, True, COLOR_TEXT_MAIN)
                    self.canvas.blit(in_surf, (110, 375))

                    if (int(time.time() * 2) % 2) == 0:
                        cx = 110 + in_surf.get_width() + 2
                        pygame.draw.rect(self.canvas, COLOR_CURSOR, (cx, 375, 10, 28))

                else:
                    alert_lbl = self.font_title.render(f"⚠️ SYSTEM BREACH ALERT! ({self.breach_timer:.1f}s)", True, COLOR_ACCENT_RED)
                    self.canvas.blit(alert_lbl, (110, 185))

                    code_lbl = self.font_hud.render("// TYPE OVERRIDE COMMAND IMMEDIATELY:", True, COLOR_ALERT)
                    self.canvas.blit(code_lbl, (110, 250))

                    target_s = self.font_code.render(self.breach_code, True, COLOR_TEXT_MAIN)
                    self.canvas.blit(target_s, (110, 290))

                    in_lbl = self.font_hud.render("> OVERRIDE INPUT:", True, COLOR_ACCENT_RED)
                    self.canvas.blit(in_lbl, (110, 360))

                    b_surf = self.font_code.render(self.breach_input, True, COLOR_ALERT)
                    self.canvas.blit(b_surf, (110, 400))

            elif self.game_state == "MENU":
                s1 = self.font_code.render("Developer Speed & Multi-Tasking Terminal", True, COLOR_TEXT_MAIN)
                s2 = self.font_hud.render("Type code & respond to live security alerts.", True, COLOR_TEXT_MUTED)
                s3 = self.font_title.render("Press SPACE to Start Terminal", True, COLOR_ACCENT_GREEN)

                self.canvas.blit(s1, (VIRTUAL_WIDTH // 2 - s1.get_width() // 2, 220))
                self.canvas.blit(s2, (VIRTUAL_WIDTH // 2 - s2.get_width() // 2, 280))
                self.canvas.blit(s3, (VIRTUAL_WIDTH // 2 - s3.get_width() // 2, 420))

            elif self.game_state == "GAMEOVER":
                wpm, acc = self.calculate_wpm_and_accuracy()
                o_title = self.font_title.render("SESSION COMPLETED", True, COLOR_ACCENT_GREEN)
                f_score = self.font_code.render(f"Final Score: {self.score}", True, COLOR_TEXT_MAIN)
                f_wpm = self.font_code.render(f"Typing Speed: {wpm} WPM", True, COLOR_BORDER)
                f_streak = self.font_code.render(f"Max Combo Streak: {self.max_streak}x", True, COLOR_CURSOR)
                f_acc = self.font_code.render(f"Accuracy Rate: {acc:.1f}%", True, COLOR_ACCENT_GREEN)
                r_prompt = self.font_hud.render("Press SPACE to Restart Game", True, COLOR_TEXT_MUTED)

                self.canvas.blit(o_title, (VIRTUAL_WIDTH // 2 - o_title.get_width() // 2, 120))
                self.canvas.blit(f_score, (VIRTUAL_WIDTH // 2 - f_score.get_width() // 2, 200))
                self.canvas.blit(f_wpm, (VIRTUAL_WIDTH // 2 - f_wpm.get_width() // 2, 260))
                self.canvas.blit(f_streak, (VIRTUAL_WIDTH // 2 - f_streak.get_width() // 2, 320))
                self.canvas.blit(f_acc, (VIRTUAL_WIDTH // 2 - f_acc.get_width() // 2, 380))
                self.canvas.blit(r_prompt, (VIRTUAL_WIDTH // 2 - r_prompt.get_width() // 2, 480))

            # Render Virtual Canvas onto Main Window with automatic scaling
            self.screen.blit(self.canvas, (0, 0))
            pygame.display.flip()


if __name__ == "__main__":
    game = CyberTyperGame()
    game.run()