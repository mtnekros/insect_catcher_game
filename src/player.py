from typing import Literal

import pygame
from pygame.key import ScancodeWrapper
from pygame.rect import Rect

from src.animation import Animation, get_frame
from src.block import Block
from src.maps.level_1 import MapLevel1

Direction = Literal["right", "left"]
AnimationType = Literal["resting", "running", "jumping", "shooting"]
class Player:
    """Animation: handles player animation."""

    def __init__(self) -> None:
        """Initialize animation."""
        frame_width = 85
        frame_height = 100
        self.state: AnimationType = "resting"
        self.direction: Direction = "right"
        sprite_sheet = pygame.image.load("./assets/player.png").convert_alpha()
        running_frames = [ get_frame(sprite_sheet, frame_width, frame_height, i, 0) for i in range(6) ]
        resting_frames = [ get_frame(sprite_sheet, frame_width, frame_height, i, 155) for i in range(2) ]
        self.animations: dict[AnimationType, Animation] = {
            "resting": Animation(resting_frames, 1),
            "jumping": Animation(resting_frames, .7),
            "running": Animation(running_frames, 1)
        }
        self.x = 100
        self.y = 400
        self.width = 68
        self.height = 80
        self.x_speed = 200
        self.y_speed = 0
        self.y_gravity = 30
        self.jumping_y_speed = -650

    @property
    def rect(self) -> Rect:
        """Return the bounding box of player."""
        return Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    @property
    def current_animation(self) -> Animation:
        """Return current animation based on state."""
        return self.animations[self.state]

    def update(
        self,
        initial_key_presses: dict[int, bool],
        key_presses: ScancodeWrapper,
        map: MapLevel1,
        dt: float,
    ) -> None:
        """Update animation."""
        if key_presses[pygame.K_RIGHT]:
            self.state = "running"
            self.direction = "right"
            self.x += self.x_speed * dt
        elif key_presses[pygame.K_LEFT]:
            self.state = "running"
            self.direction = "left"
            self.x -= self.x_speed * dt
        else:
            self.state = "resting"

        if initial_key_presses.get(pygame.K_UP):
            self.i_frame = 0
            self.state = "jumping"
            self.y_speed = self.jumping_y_speed
            self.animations["jumping"].reset()

        self.y_speed = self.y_speed+self.y_gravity
        self.y += self.y_speed * dt

        col_dx, col_dy = map.get_collition_resolution(self.rect)
        if col_dy < 0: # means the block is below & player needs to be moved up
            self.y_speed = 0
        self.x += col_dx
        self.y += col_dy
        self.current_animation.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the frame."""
        frame = pygame.transform.scale(self.current_animation.get_frame(), (self.width, self.height))
        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (self.x, self.y))
