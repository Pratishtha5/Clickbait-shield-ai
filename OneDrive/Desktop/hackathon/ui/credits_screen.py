import pygame
from settings import WIDTH, HEIGHT

class CreditsScreen:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 28)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "BACK"
        return None

    def draw(self, screen):
        screen.fill((5, 5, 5))
        lines = [
            "PROTOCOL",
            "",
            "Game Design & Programming",
            "",
            "",
            "Built with Pygame",
            "AI observes. Humanity decides.",
            "",
            "ESC to return"
        ]

        y = 120
        for line in lines:
            txt = self.font.render(line, True, (180, 180, 180))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, y))
            y += 35
