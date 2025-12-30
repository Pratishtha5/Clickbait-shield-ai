import pygame
from settings import *

class Player:
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 30, 40)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False

    def update(self, dt, tiles):
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        if keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = JUMP_FORCE

        self.vel.y += GRAVITY

        self.rect.x += self.vel.x * dt
        self._collide(tiles, "x")

        self.rect.y += self.vel.y
        self.on_ground = False
        self._collide(tiles, "y")

    def _collide(self, tiles, dir):
        for tile in tiles:
            if self.rect.colliderect(tile):
                if dir == "y":
                    if self.vel.y > 0:
                        self.rect.bottom = tile.top
                        self.vel.y = 0
                        self.on_ground = True
                    elif self.vel.y < 0:
                        self.rect.top = tile.bottom
                        self.vel.y = 0
                if dir == "x":
                    if self.vel.x > 0:
                        self.rect.right = tile.left
                    elif self.vel.x < 0:
                        self.rect.left = tile.right

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 200, 255), self.rect)
