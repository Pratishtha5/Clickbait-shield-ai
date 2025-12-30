import pygame
from game import Game

pygame.init()

try:
    game = Game()
    game.run()
except Exception as e:
    print("CRITICAL ERROR:", e)
finally:
    pygame.quit()
