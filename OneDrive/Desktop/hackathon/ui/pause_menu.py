import pygame
from settings import WIDTH, HEIGHT

class PauseMenu:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 32)
        self.options = ["RESUME", "AI ANALYSIS", "EXIT TO MENU"]
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
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        for i, opt in enumerate(self.options):
            color = (0, 255, 255) if i == self.selected else (200, 200, 200)
            txt = self.font.render(opt, True, color)
            screen.blit(txt, (WIDTH//2 - 80, 250 + i * 40))
