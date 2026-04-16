import pygame

class Ball:


    RADIUS     = 25          # Ball radius in pixels (diameter = 50)
    STEP       = 20          # Pixels moved per key press
    COLOR      = (220, 40, 40)    # Red fill
    OUTLINE    = (160, 10, 10)    # Darker red outline

    def __init__(self, screen_width, screen_height):
        self.screen_width  = screen_width
        self.screen_height = screen_height

        # Start in the center of the screen
        self.x = screen_width  // 2
        self.y = screen_height // 2

    # ── Movement ──────────────────────────────────────────────────────────────

    def move(self, direction):
        
        new_x, new_y = self.x, self.y

        if direction == "up":
            new_y -= self.STEP
        elif direction == "down":
            new_y += self.STEP
        elif direction == "left":
            new_x -= self.STEP
        elif direction == "right":
            new_x += self.STEP

        # Boundary check — only apply if the new position keeps ball on screen
        if self._in_bounds(new_x, new_y):
            self.x, self.y = new_x, new_y
        # else: silently ignore 

    def _in_bounds(self, x, y):
        r = self.RADIUS
        return (r <= x <= self.screen_width  - r and
                r <= y <= self.screen_height - r)

    # ── Drawing ───────────────────────────────────────────────────────────────

    def draw(self, screen):
        # Shadow / outline circle
        pygame.draw.circle(screen, self.OUTLINE, (self.x, self.y), self.RADIUS)
        # Main fill circle (slightly smaller)
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.RADIUS - 2)
        # Highlight (small white spot for 3-D look)
        highlight_pos = (self.x - self.RADIUS // 3, self.y - self.RADIUS // 3)
        pygame.draw.circle(screen, (255, 160, 160), highlight_pos, self.RADIUS // 5)

    # ── Info ──────────────────────────────────────────────────────────────────

    def get_position(self):
        return (self.x, self.y)