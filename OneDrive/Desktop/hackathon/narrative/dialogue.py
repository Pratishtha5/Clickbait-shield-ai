import pygame

class DialogueBox:
    def __init__(self):
        self.active = False
        self.text = ""
        self.timer = 0

    def show(self, text):
        self.text = text
        self.active = True
        self.timer = 0

    def update(self):
        if not self.active:
            return False
        self.timer += 1
        if self.timer > 120:
            self.active = False
            return True
        return False

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (0, 0, 0), (50, 450, 700, 100))
            font = pygame.font.SysFont(None, 24)
            txt = font.render(self.text, True, (0, 255, 0))
            screen.blit(txt, (70, 480))
