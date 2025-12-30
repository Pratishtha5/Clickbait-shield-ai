import pygame
from settings import WIDTH, HEIGHT

class StatsScreen:
    def __init__(self, game_data):
        self.data = game_data
        self.font = pygame.font.SysFont(None, 32)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "BACK"
        return None

    def draw(self, screen):
        screen.fill((10, 10, 10))
        title = self.font.render("AI ANALYSIS", True, (0, 200, 200))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        y = 150
        for k, v in self.data.stats.items():
            txt = self.font.render(f"{k.upper()} : {v}", True, (200, 200, 200))
            screen.blit(txt, (WIDTH//2 - 120, y))
            y += 40

        hint = self.font.render("ESC to return", True, (120, 120, 120))
        screen.blit(hint, (WIDTH//2 - 80, 520))
