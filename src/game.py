import pygame
from pygame import Rect, Vector2

from src.butterfly import Butterfly
from src.maps.level_1 import MapLevel1
from src.player import Player
from src.sounds import pause_bg_music, play_bg_music, stop_bg_music
from src.stats_overlay import StatsOverlay


class Game:
    """The game class used to run the game."""

    FRAME_RATE = 60
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 750
    CENTER_X = SCREEN_WIDTH // 2
    CENTER_Y = SCREEN_HEIGHT // 2
    GROUND_HEIGHT = 550
    BACKGROUND = (50, 50, 50)
    RECT = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    INITIAL_WALKER_COUNT = 10
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    WAVE_TIME_PERIOD = 10_000 # 10 secs

    def __init__(self) -> None:
        """Initialize the game."""
        self.cam_pos = Vector2(100, 0)
        self.is_running = True
        # self.road = Road(width=350)
        self.butterflies: list[Butterfly] = []
        self.next_wave_time = 0
        self.player = Player()
        self.add_butterfly(count=Game.INITIAL_WALKER_COUNT)
        self.map = MapLevel1(Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)
        self.clock = pygame.time.Clock()
        self.stats_overlay = StatsOverlay(5, 5)

    def add_butterfly(self, count: int=1) -> None:
        """Add butterfly into the game."""
        for _ in range(count):
            self.butterflies.append(
                Butterfly(Game.SCREEN_WIDTH/2, Game.SCREEN_HEIGHT/2)
            )

    def remove_walkers(self, count: int=1) -> None:
        """Remove walkers from the game."""
        for _ in range(count):
            if not self.butterflies:
                print("No walkers to remove")
                return
            self.butterflies.pop()

    def update(self, dt: float) -> None:
        """Update objects in the game.

        params dt(float): delta time passed since last time it was called.
        """
        initial_key_presses: dict[int, bool] = {}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    initial_key_presses[pygame.K_UP] = True
                elif event.key == pygame.K_SPACE:
                    self.add_butterfly(count=10)
                elif event.key == pygame.K_DELETE:
                    self.remove_walkers(count=10)
        self.next_wave_time += dt
        if self.next_wave_time >= Game.WAVE_TIME_PERIOD:
            self.add_butterfly(count=10)
        self.player.update(initial_key_presses, pygame.key.get_pressed(), self.map, dt)
        self.cam_pos.x += self.player.displacement.x
        for walker in self.butterflies:
            walker.update(dt, Game.RECT)
        self.stats_overlay.update(Game.FRAME_RATE, len(self.butterflies))

    def draw(self) -> None:
        """Render the objects in the game."""
        self.screen.fill(Game.BACKGROUND)
        # self.road.draw(self.screen)
        self.map.draw(self.screen, self.cam_pos)
        self.player.draw(self.screen, self.cam_pos)
        for walker in self.butterflies:
            walker.draw(self.screen, self.cam_pos)
        self.stats_overlay.draw(self.screen)

    def is_over(self) -> bool:
        """Return true if game is over."""
        return Game.RECT.bottom <= self.player.get_rect().bottom

    def run(self) -> None:
        """Run the game loop."""
        pygame.init()
        # play music
        play_bg_music()
        while self.is_running:
            if self.is_over():
                pause_bg_music()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                continue
            dt = self.clock.tick(Game.FRAME_RATE) / 1000.0
            self.update(dt)
            self.draw()
            pygame.display.flip()
        stop_bg_music()
        pygame.quit()



