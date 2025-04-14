from typing import Literal

import pygame
from pygame.key import ScancodeWrapper
from pygame.rect import Rect

from src.animation import Animation, get_frame
from src.maps.level_1 import MapLevel1

Direction = Literal["right", "left"]
AnimationType = Literal["resting", "running", "jumping", "shooting"]
class Player:
    """Animation: handles player animation."""

    __slots__ = (
        "state",
        "direction",
        "animations",
        "x",
        "y",
        "width",
        "height",
        "x_speed",
        "y_speed",
        "y_gravity",
        "jumping_y_speed",
        "jump_count",
        "max_jump_count",
        "inner_padding",
    )

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
        self.jumping_y_speed = -750
        self.jump_count = 0
        self.max_jump_count = 2
        self.inner_padding = 5

    def get_rect(self) -> Rect:
        """Return the bounding box of player."""
        inner_padding = self.inner_padding
        return Rect(
            int(self.x) + inner_padding * 2.5,
            int(self.y) + inner_padding,
            self.width - inner_padding * 3.5,
            self.height - inner_padding
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

        if (
            initial_key_presses.get(pygame.K_UP) and
            self.jump_count < self.max_jump_count
        ):
            self.state = "jumping"
            self.y_speed = self.jumping_y_speed
            self.animations["jumping"].reset()
            self.jump_count += 1

        self.y_speed = self.y_speed+self.y_gravity
        self.y += self.y_speed * dt

        col_dx, col_dy = map.get_collition_resolution(self.get_rect())
        if col_dy < 0: # means the block is below & player needs to be moved up (player touches the ground)
            self.y_speed = 0
            self.jump_count = 0
        self.x += col_dx
        self.y += col_dy
        self.current_animation.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the frame."""
        frame = pygame.transform.scale(self.current_animation.get_frame(), (self.width, self.height))
        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)
        pygame.draw.rect(screen, "Red", self.get_rect(), 1)
        screen.blit(frame, (self.x, self.y))
