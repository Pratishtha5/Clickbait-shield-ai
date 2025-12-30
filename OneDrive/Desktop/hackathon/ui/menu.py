import pygame
from settings import WIDTH, HEIGHT

class MainMenu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 44)
        self.small = pygame.font.SysFont(None, 28)

        self.options = [
            "START GAME",
            "AI ANALYSIS",
            "CONTROLS",
            "CREDITS",
            "QUIT"
        ]
        self.selected = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            if event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None

    def draw(self, screen):
        screen.fill((15, 15, 15))
        title = self.font.render("PROTOCOL", True, (0, 200, 200))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        for i, option in enumerate(self.options):
            color = (0, 255, 255) if i == self.selected else (200, 200, 200)
            text = self.small.render(option, True, color)
            screen.blit(text, (WIDTH//2 - 80, 200 + i * 40))
