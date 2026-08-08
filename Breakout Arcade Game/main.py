import sys
import random
import pygame

# Initialize Pygame
pygame.init()

# --- DEFAULT CONFIGURATION ---
DEFAULT_WIDTH = 900
DEFAULT_HEIGHT = 650
FPS = 60

# Palette
COLOR_BG = (15, 23, 42)          # Slate Dark
COLOR_PADDLE = (56, 189, 248)     # Cyan Neon
COLOR_BALL = (248, 250, 252)       # White
COLOR_TEXT = (226, 232, 240)       # Light Slate

# Brick Color Tier Configuration
BRICK_PALETTE = [
    (239, 68, 68),   # Red
    (249, 115, 22),  # Orange
    (234, 179, 8),   # Yellow
    (34, 197, 94),   # Green
    (168, 85, 247),  # Purple
    (236, 72, 153),  # Pink
]


class Particle:
    """Particle effect when a brick breaks."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.lifetime = 20
        self.radius = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


class Paddle:
    def __init__(self, screen_w, screen_h):
        self.width_ratio = 0.14  # 14% of screen width
        self.height = 14
        self.speed = 10
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.resize(screen_w, screen_h)

    def resize(self, screen_w, screen_h):
        old_center_x = self.rect.centerx if self.rect.width > 0 else screen_w // 2
        width = max(80, int(screen_w * self.width_ratio))
        self.rect = pygame.Rect(0, screen_h - 45, width, self.height)
        self.rect.centerx = old_center_x

    def move(self, direction, screen_w):
        if direction == "left" and self.rect.left > 10:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < screen_w - 10:
            self.rect.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_PADDLE, self.rect, border_radius=7)


class Ball:
    def __init__(self, screen_w, screen_h):
        self.radius = 8
        self.base_speed = 5.0
        self.speed_multiplier = 1.0
        self.x = screen_w // 2
        self.y = screen_h - 70
        self.dx = 4.0
        self.dy = -4.0
        self.active = False

    def reset(self, screen_w, screen_h, level):
        self.x = screen_w // 2
        self.y = screen_h - 70
        # Increase ball speed proportionally with each level (+15% speed per level)
        self.speed_multiplier = 1.0 + (level - 1) * 0.15
        speed = self.base_speed * self.speed_multiplier
        self.dx = random.choice([-speed, speed])
        self.dy = -speed
        self.active = False

    def move(self):
        if self.active:
            self.x += self.dx
            self.y += self.dy

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self, surface):
        pygame.draw.circle(surface, COLOR_BALL, (int(self.x), int(self.y)), self.radius)


class Brick:
    def __init__(self, x, y, width, height, color, points):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.points = points

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255, 45), self.rect, width=1, border_radius=4)


class BreakoutGame:
    def __init__(self):
        # Enable RESIZABLE window flag
        self.screen_w = DEFAULT_WIDTH
        self.screen_h = DEFAULT_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.RESIZABLE)
        pygame.display.set_caption("Breakout Studio Pro - Multi-Level")
        self.clock = pygame.time.Clock()
        self.is_fullscreen = False

        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_state = "MENU"  # MENU, PLAYING, LEVEL_CLEAR, GAMEOVER, WIN

        self.paddle = Paddle(self.screen_w, self.screen_h)
        self.ball = Ball(self.screen_w, self.screen_h)
        self.bricks = []
        self.particles = []

        self._update_fonts()
        self._build_bricks()

    def _update_fonts(self):
        """Scales fonts relative to current window dimensions."""
        base_size = min(self.screen_w, self.screen_h)
        self.font_score = pygame.font.SysFont("Plus Jakarta Sans", max(16, int(base_size * 0.035)), bold=True)
        self.font_title = pygame.font.SysFont("Plus Jakarta Sans", max(28, int(base_size * 0.07)), bold=True)
        self.font_sub = pygame.font.SysFont("Plus Jakarta Sans", max(14, int(base_size * 0.03)))

    def _build_bricks(self):
        """Generates brick layout scaled to window size and current level."""
        self.bricks.clear()
        cols = min(12, 6 + self.level)  # More columns in higher levels
        rows = min(6, 3 + (self.level // 2))  # More rows as levels progress

        padding = 6
        offset_y = max(60, int(self.screen_h * 0.12))
        total_padding_x = (cols + 1) * padding
        brick_w = (self.screen_w - total_padding_x) // cols
        brick_h = max(18, int(self.screen_h * 0.035))

        offset_x = (self.screen_w - (cols * (brick_w + padding) - padding)) // 2

        for r in range(rows):
            color = BRICK_PALETTE[r % len(BRICK_PALETTE)]
            points = (rows - r) * 10 * self.level
            for c in range(cols):
                bx = offset_x + c * (brick_w + padding)
                by = offset_y + r * (brick_h + padding)
                self.bricks.append(Brick(bx, by, brick_w, brick_h, color, points))

    def handle_resize(self, width, height):
        """Adapts game dimensions seamlessly on window resize."""
        self.screen_w = max(500, width)
        self.screen_h = max(400, height)
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.RESIZABLE)
        
        self._update_fonts()
        self.paddle.resize(self.screen_w, self.screen_h)
        if not self.ball.active:
            self.ball.reset(self.screen_w, self.screen_h, self.level)
        self._build_bricks()

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            info = pygame.display.Info()
            self.handle_resize(info.current_w, info.current_h)
        else:
            self.handle_resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    def next_level(self):
        self.level += 1
        self.ball.reset(self.screen_w, self.screen_h, self.level)
        self._build_bricks()
        self.game_state = "PLAYING"

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.particles.clear()
        self.paddle = Paddle(self.screen_w, self.screen_h)
        self.ball.reset(self.screen_w, self.screen_h, self.level)
        self._build_bricks()
        self.game_state = "PLAYING"

    def handle_collisions(self):
        # Screen wall collisions
        if self.ball.x - self.ball.radius <= 0 or self.ball.x + self.ball.radius >= self.screen_w:
            self.ball.dx *= -1
        if self.ball.y - self.ball.radius <= 0:
            self.ball.dy *= -1

        # Bottom floor loss
        if self.ball.y + self.ball.radius >= self.screen_h:
            self.lives -= 1
            if self.lives <= 0:
                self.game_state = "GAMEOVER"
            else:
                self.ball.reset(self.screen_w, self.screen_h, self.level)

        # Paddle collision with dynamic angle bounce
        if self.ball.rect.colliderect(self.paddle.rect) and self.ball.dy > 0:
            offset = (self.ball.x - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            max_speed = self.ball.base_speed * self.ball.speed_multiplier
            self.ball.dx = offset * (max_speed * 1.2)
            self.ball.dy = -abs(self.ball.dy)

        # Brick collisions
        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                self.ball.dy *= -1
                self.score += brick.points
                self.bricks.remove(brick)

                # Particles
                for _ in range(8):
                    self.particles.append(Particle(brick.rect.centerx, brick.rect.centery, brick.color))
                break

        # Level clear condition
        if not self.bricks:
            self.game_state = "LEVEL_CLEAR"

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.screen.fill(COLOR_BG)

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle Window Resizing
                elif event.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:
                        self.handle_resize(event.w, event.h)

                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_f, pygame.K_F11]:
                        self.toggle_fullscreen()

                    if event.key == pygame.K_SPACE:
                        if self.game_state in ["MENU", "GAMEOVER", "WIN"]:
                            self.reset_game()
                        elif self.game_state == "LEVEL_CLEAR":
                            self.next_level()
                        elif self.game_state == "PLAYING" and not self.ball.active:
                            self.ball.active = True

            # Controls
            keys = pygame.key.get_pressed()
            if self.game_state == "PLAYING":
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.paddle.move("left", self.screen_w)
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.paddle.move("right", self.screen_w)

                self.ball.move()
                self.handle_collisions()

            # Particles
            for particle in self.particles[:]:
                particle.update()
                if particle.lifetime <= 0:
                    self.particles.remove(particle)

            # Render World
            for brick in self.bricks:
                brick.draw(self.screen)

            for particle in self.particles:
                particle.draw(self.screen)

            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)

            # Render HUD
            score_txt = self.font_score.render(f"SCORE: {self.score}", True, COLOR_TEXT)
            level_txt = self.font_score.render(f"LEVEL: {self.level}", True, COLOR_PADDLE)
            lives_txt = self.font_score.render(f"LIVES: {'❤️ ' * self.lives}", True, COLOR_TEXT)

            self.screen.blit(score_txt, (20, 15))
            self.screen.blit(level_txt, (self.screen_w // 2 - level_txt.get_width() // 2, 15))
            self.screen.blit(lives_txt, (self.screen_w - lives_txt.get_width() - 20, 15))

            # Overlay Screens
            if self.game_state != "PLAYING":
                overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
                overlay.fill((15, 23, 42, 225))
                self.screen.blit(overlay, (0, 0))

                if self.game_state == "MENU":
                    title = self.font_title.render("BREAKOUT STUDIO PRO", True, COLOR_PADDLE)
                    sub = self.font_sub.render("Press SPACE to Launch Ball | F11 for Fullscreen", True, COLOR_TEXT)
                elif self.game_state == "LEVEL_CLEAR":
                    title = self.font_title.render(f"LEVEL {self.level} CLEARED! 🎉", True, (34, 197, 94))
                    sub = self.font_sub.render(f"Ball Speed Increased! Press SPACE for Level {self.level + 1}", True, COLOR_TEXT)
                elif self.game_state == "GAMEOVER":
                    title = self.font_title.render("GAME OVER", True, (239, 68, 68))
                    sub = self.font_sub.render(f"Reached Level {self.level} | Score: {self.score} | Press SPACE to Restart", True, COLOR_TEXT)

                self.screen.blit(title, title.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 25)))
                self.screen.blit(sub, sub.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 25)))

            pygame.display.flip()


if __name__ == "__main__":
    game = BreakoutGame()
    game.run()