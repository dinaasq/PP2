"""Entry point — wires screens together and runs the main loop."""
import sys
import pygame

from persistence import load_settings, add_score
from racer import Game, WIDTH, HEIGHT
from ui import (
    MainMenu, NameEntry, SettingsScreen,
    LeaderboardScreen, GameOverScreen,
)

FPS = 60


class App:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Advanced Racer")
        self.clock = pygame.time.Clock()
        self.settings = load_settings()
        self.player_name = "PLAYER"
        self.state = "menu"
        self.game = None
        self.last_summary = None
        self.screens = {
            "menu":        MainMenu(self),
            "name":        NameEntry(self),
            "settings":    SettingsScreen(self),
            "leaderboard": LeaderboardScreen(self),
        }
        self._apply_sound()

    def _apply_sound(self):
        # Hook for future sound effects — toggles mixer volume.
        try:
            vol = 1.0 if self.settings["sound"] else 0.0
            pygame.mixer.music.set_volume(vol)
        except pygame.error:
            pass

    def go(self, state):
        self.state = state
        if state == "name":
            self.screens["name"] = NameEntry(self)
        if state == "settings":
            self.screens["settings"] = SettingsScreen(self)
            self._apply_sound()
        if state == "leaderboard":
            self.screens["leaderboard"].refresh()
        if state == "menu":
            # Fresh menu each return so buttons are reset
            self.screens["menu"] = MainMenu(self)

    def start_game(self):
        self.game = Game(self.settings, self.player_name)
        self.state = "play"

    def quit(self):
        pygame.quit()
        sys.exit(0)

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()

                if self.state == "play":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.go("menu")
                        continue
                    if self.game:
                        self.game.handle_input(event)
                else:
                    self.screens.get(self.state, self.screens["menu"]).handle(event)

            if self.state == "play" and self.game:
                self.game.update()
                self.game.draw(self.screen)
                if self.game.game_over:
                    summary = self.game.summary()
                    self.last_summary = summary
                    add_score(summary["name"], summary["score"],
                              summary["distance"], summary["coins"])
                    self.screens["gameover"] = GameOverScreen(self, summary)
                    self.state = "gameover"
                    self.game = None
            else:
                screen = self.screens.get(self.state)
                if screen is None:
                    self.go("menu")
                    screen = self.screens["menu"]
                screen.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    App().run()
