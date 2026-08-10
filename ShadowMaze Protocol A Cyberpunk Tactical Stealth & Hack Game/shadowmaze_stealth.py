import math
import random
import sys
import pygame

# --- INITIALIZATION & SETTINGS ---
pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("ShadowMaze Protocol: Tactical Stealth Engine")
clock = pygame.time.Clock()

# Theme Colors
COLOR_BG = (10, 14, 23)
COLOR_WALL = (30, 41, 59)
COLOR_PLAYER = (56, 189, 248)
COLOR_GUARD = (239, 68, 68)
COLOR_LIGHT = (253, 224, 71, 90)  # Semi-transparent light cone
COLOR_NODE = (245, 158, 11)
COLOR_EXIT = (16, 185, 129)
COLOR_TEXT = (241, 245, 249)
COLOR_HUD_BG = (15, 23, 42, 210)


# --- GAME CLASSES ---
class Player:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.radius = 14
    self.speed = 4.5

  def move(self, dx, dy, walls):
    # Separate axis movement for smooth sliding against wall collision
    new_x = self.x + dx * self.speed
    if not any(w.collidepoint(new_x, self.y) for w in walls):
      self.x = new_x

    new_y = self.y + dy * self.speed
    if not any(w.collidepoint(self.x, new_y) for w in walls):
      self.y = new_y

  def draw(self, surface):
    pygame.draw.circle(
        surface, COLOR_PLAYER, (int(self.x), int(self.y)), self.radius
    )
    pygame.draw.circle(
        surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius - 5
    )


class Guard:

  def __init__(self, x, y, waypoints, speed=2.5):
    self.x = x
    self.y = y
    self.waypoints = waypoints
    self.target_idx = 0
    self.speed = speed
    self.angle = 0
    self.fov = math.pi / 3  # 60 Degree vision cone angle
    self.view_dist = 220

  def update(self):
    target = self.waypoints[self.target_idx]
    dx = target[0] - self.x
    dy = target[1] - self.y
    dist = math.hypot(dx, dy)

    if dist < 5:
      self.target_idx = (self.target_idx + 1) % len(self.waypoints)
    else:
      self.angle = math.atan2(dy, dx)
      self.x += (dx / dist) * self.speed
      self.y += (dy / dist) * self.speed

  def sees_player(self, player_x, player_y):
    dx = player_x - self.x
    dy = player_y - self.y
    dist = math.hypot(dx, dy)

    if dist < self.view_dist:
      angle_to_p = math.atan2(dy, dx)
      diff = (angle_to_p - self.angle + math.pi) % (2 * math.pi) - math.pi
      if abs(diff) < self.fov / 2:
        return True
    return False

  def draw(self, surface):
    # Vision Light Cone
    cone_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    p1 = (self.x, self.y)
    p2 = (
        self.x + math.cos(self.angle - self.fov / 2) * self.view_dist,
        self.y + math.sin(self.angle - self.fov / 2) * self.view_dist,
    )
    p3 = (
        self.x + math.cos(self.angle + self.fov / 2) * self.view_dist,
        self.y + math.sin(self.angle + self.fov / 2) * self.view_dist,
    )
    pygame.draw.polygon(cone_surf, COLOR_LIGHT, [p1, p2, p3])
    surface.blit(cone_surf, (0, 0))

    # Guard Body
    pygame.draw.circle(surface, COLOR_GUARD, (int(self.x), int(self.y)), 16)


class HackNode:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.hacked = False

  def draw(self, surface):
    color = COLOR_EXIT if self.hacked else COLOR_NODE
    pygame.draw.rect(surface, color, (self.x - 12, self.y - 12, 24, 24))


# --- LEVEL BUILDER ---
def build_level(level_num):
  walls = [
      pygame.Rect(100, 100, WIDTH - 200, 20),
      pygame.Rect(100, HEIGHT - 100, WIDTH - 200, 20),
      pygame.Rect(100, 100, 20, HEIGHT - 200),
      pygame.Rect(WIDTH - 120, 100, 20, HEIGHT - 200),
      # Interior Corridors
      pygame.Rect(300, 250, 20, 300),
      pygame.Rect(600, 100, 20, 350),
      pygame.Rect(900, 300, 20, 300),
  ]

  player = Player(180, 180)

  nodes = [
      HackNode(200, HEIGHT - 180),
      HackNode(750, 180),
      HackNode(WIDTH - 220, HEIGHT - 180),
  ]

  guards = [
      Guard(
          350,
          200,
          [(350, 200), (550, 200), (550, 500), (350, 500)],
          speed=2.5 + (level_num * 0.3),
      ),
      Guard(
          650,
          550,
          [(650, 550), (850, 550), (850, 200), (650, 200)],
          speed=2.8 + (level_num * 0.3),
      ),
  ]

  return player, walls, nodes, guards


# --- MAIN GAME LOOP ---
def run_game():
  current_level = 1
  player, walls, nodes, guards = build_level(current_level)

  game_over = False
  level_cleared = False
  font = pygame.font.SysFont("Consolas", 20, bold=True)
  font_large = pygame.font.SysFont("Consolas", 46, bold=True)

  while True:
    screen.fill(COLOR_BG)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()

        if not game_over and not level_cleared:
          # Hack Node Interaction (E or SPACE)
          if event.key in [pygame.K_e, pygame.K_SPACE]:
            for node in nodes:
              if (
                  not node.hacked
                  and math.hypot(player.x - node.x, player.y - node.y) < 45
              ):
                node.hacked = True

        if game_over and event.key == pygame.K_r:
          run_game()

    if not game_over and not level_cleared:
      # Movement Handling
      dx, dy = 0, 0
      if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy -= 1
      if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy += 1
      if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx -= 1
      if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx += 1

      if dx != 0 or dy != 0:
        # Normalize diagonal movement speed
        mag = math.hypot(dx, dy)
        player.move(dx / mag, dy / mag, walls)

      # Update Guards & Stealth Detection
      for guard in guards:
        guard.update()
        if guard.sees_player(player.x, player.y):
          game_over = True

      # Level Completion Check
      if all(node.hacked for node in nodes):
        level_cleared = True

    # --- DRAWING OBJECTS ---
    for wall in walls:
      pygame.draw.rect(screen, COLOR_WALL, wall)

    for node in nodes:
      node.draw(screen)

    for guard in guards:
      guard.draw(screen)

    player.draw(screen)

    # --- HUD OVERLAY ---
    hud_surf = pygame.Surface((360, 110), pygame.SRCALPHA)
    hud_surf.fill(COLOR_HUD_BG)
    pygame.draw.rect(hud_surf, (148, 163, 184, 80), (0, 0, 360, 110), 2)

    lvl_surf = font.render(f"SECTOR LEVEL: {current_level}", True, COLOR_TEXT)
    hacked_cnt = sum(1 for n in nodes if n.hacked)
    nodes_surf = font.render(
        f"NODES HACKED: {hacked_cnt}/{len(nodes)}", True, COLOR_NODE
    )
    ctrl_surf = font.render(
        "MOVE: [WASD] | HACK: [E/SPACE]", True, COLOR_PLAYER
    )

    hud_surf.blit(lvl_surf, (20, 15))
    hud_surf.blit(nodes_surf, (20, 45))
    hud_surf.blit(ctrl_surf, (20, 75))
    screen.blit(hud_surf, (20, 20))

    if game_over:
      over_surf = font_large.render(
          "DETECTION ALARM: INFILTRATION FAILED", True, COLOR_GUARD
      )
      restart_surf = font.render(
          "Press 'R' to Restart Mission | 'ESC' to Quit", True, COLOR_TEXT
      )
      screen.blit(
          over_surf, (WIDTH // 2 - over_surf.get_width() // 2, HEIGHT // 2 - 40)
      )
      screen.blit(
          restart_surf,
          (WIDTH // 2 - restart_surf.get_width() // 2, HEIGHT // 2 + 20),
      )

    if level_cleared:
      clear_surf = font_large.render(
          f"SECTOR {current_level} HACKED & CLEARED!", True, COLOR_EXIT
      )
      next_surf = font.render(
          "Advancing to next security protocol...", True, COLOR_TEXT
      )
      screen.blit(
          clear_surf,
          (WIDTH // 2 - clear_surf.get_width() // 2, HEIGHT // 2 - 40),
      )
      screen.blit(
          next_surf, (WIDTH // 2 - next_surf.get_width() // 2, HEIGHT // 2 + 20)
      )
      pygame.display.flip()
      pygame.time.delay(2000)

      # Advance Level
      current_level += 1
      level_cleared = False
      player, walls, nodes, guards = build_level(current_level)

    pygame.display.flip()
    clock.tick(FPS)


if __name__ == "__main__":
  run_game()