import pygame
from settings import *

class Level:
    def __init__(self, layout):
        self.tiles = []
        self.terminal = None

        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                if cell == "#":
                    self.tiles.append(
                        pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )
                if cell == "T":
                    self.terminal = pygame.Rect(
                        x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE
                    )

    def check_terminal(self, player_rect):
        return self.terminal and player_rect.colliderect(self.terminal)

    def draw(self, screen):
        for tile in self.tiles:
            pygame.draw.rect(screen, (120, 120, 120), tile)
        if self.terminal:
            pygame.draw.rect(screen, (0, 255, 255), self.terminal)
