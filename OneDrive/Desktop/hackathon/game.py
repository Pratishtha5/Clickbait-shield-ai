import pygame
from settings import *
from core.player import Player
from core.level import Level
from narrative.dialogue import DialogueBox
from data.levels import LEVELS
from game_state import GameState
from data.game_data import GameData
from ui.menu import MainMenu
from data.endings import get_ending

from ui.stats_screen import StatsScreen
from ui.controls_screen import ControlsScreen
from ui.credits_screen import CreditsScreen
from ui.pause_menu import PauseMenu


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PROTOCOL")
        self.clock = pygame.time.Clock()

        # ---------- STATE & DATA ----------
        self.state = GameState.MENU
        self.data = GameData()

        # ---------- UI ----------
        self.menu = MainMenu()
        self.dialogue = DialogueBox()
        self.stats_screen = StatsScreen(self.data)
        self.controls_screen = ControlsScreen()
        self.credits_screen = CreditsScreen()
        self.pause_menu = PauseMenu()

        # ---------- GAME OBJECTS ----------
        self.player = None
        self.level = None

    # ---------- LOAD LEVEL ----------
    def load_level(self):
        self.level = Level(LEVELS[self.data.current_level])
        self.player = Player((100, 120))

    # ---------- MAIN LOOP ----------
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # ---------- GLOBAL ESC ----------
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state in (
                        GameState.STATS,
                        GameState.CONTROLS,
                        GameState.CREDITS
                    ):
                        self.state = GameState.MENU

                # ---------- MENU INPUT ----------
                if self.state == GameState.MENU:
                    action = self.menu.handle_input(event)

                    if action == "START GAME":
                        self.load_level()
                        self.state = GameState.PLAYING

                    elif action == "AI ANALYSIS":
                        self.state = GameState.STATS

                    elif action == "CONTROLS":
                        self.state = GameState.CONTROLS

                    elif action == "CREDITS":
                        self.state = GameState.CREDITS

                    elif action == "QUIT":
                        running = False

                # ---------- PAUSE MENU ----------
                elif self.state == GameState.PAUSED:
                    action = self.pause_menu.handle_input(event)
                    if action == "RESUME":
                        self.state = GameState.PLAYING
                    elif action == "AI ANALYSIS":
                        self.state = GameState.STATS
                    elif action == "EXIT TO MENU":
                        self.state = GameState.MENU

            # ---------- UPDATE ----------
            if self.state == GameState.PLAYING:
                self.player.update(dt, self.level.tiles)

                # Terminal interaction (Level 1)
                if self.level.check_terminal(self.player.rect):
                    self.data.log("learning_speed")
                    self.dialogue.show("PROTOCOL: Boot sequence complete.")
                    self.state = GameState.DIALOGUE

            elif self.state == GameState.DIALOGUE:
                if self.dialogue.update():
                    self.state = GameState.LEVEL_COMPLETE

            elif self.state == GameState.LEVEL_COMPLETE:
                self.data.current_level += 1

                if self.data.current_level >= len(LEVELS):
                    self.state = GameState.ENDING
                else:
                    self.load_level()
                    self.state = GameState.PLAYING

            elif self.state == GameState.ENDING:
                self.draw_ending()
                pygame.display.flip()
                continue

            # ---------- DRAW ----------
            self.screen.fill((20, 20, 20))

            if self.state == GameState.MENU:
                self.menu.draw(self.screen)

            elif self.state == GameState.STATS:
                self.stats_screen.draw(self.screen)

            elif self.state == GameState.CONTROLS:
                self.controls_screen.draw(self.screen)

            elif self.state == GameState.CREDITS:
                self.credits_screen.draw(self.screen)

            elif self.state == GameState.PAUSED:
                if self.level:
                    self.level.draw(self.screen)
                if self.player:
                    self.player.draw(self.screen)
                self.pause_menu.draw(self.screen)

            else:
                if self.level:
                    self.level.draw(self.screen)
                if self.player:
                    self.player.draw(self.screen)
                self.dialogue.draw(self.screen)

            pygame.display.flip()

    # ---------- ENDING ----------
    def draw_ending(self):
        ending = get_ending(self.data.stats)
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 36)

        title = font.render("PROTOCOL DECISION", True, (0, 200, 200))
        result = font.render(f"Ending: {ending}", True, (200, 200, 200))
        hint = font.render("Press ESC to Exit", True, (120, 120, 120))

        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 230))
        self.screen.blit(result, (WIDTH//2 - result.get_width()//2, 280))
        self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 340))
