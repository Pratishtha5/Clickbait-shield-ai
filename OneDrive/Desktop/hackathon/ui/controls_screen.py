import pygame
from settings import WIDTH, HEIGHT

class ControlsScreen:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 30)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "BACK"
        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))
        lines = [
            "CONTROLS",
            "",
            "A / D  - Move",
            "SPACE  - Jump",
            "ESC    - Pause / Back",
            "",
            "Decisions are made by actions, not menus."
        ]

        y = 100
        for line in lines:
            txt = self.font.render(line, True, (200, 200, 200))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, y))
            y += 40
