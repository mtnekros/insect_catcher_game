from typing import Literal

import pygame
from pygame.key import ScancodeWrapper
from pygame.rect import Rect

from src.animation import Animation, get_frame
from src.block import Block

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
        self.x_speed = 450
        self.y_speed = 10
        self.y_gravity = 60
        self.jumping_y_speed = -950

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
        block: Block,
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
            # TODO: Some refactoring needed here.
            self.state = "resting"

        if initial_key_presses.get(pygame.K_UP):
            self.i_frame = 0
            self.state = "jumping"
            self.y_speed = self.jumping_y_speed
            self.animations["jumping"].reset()

        self.y_speed = self.y_speed+self.y_gravity
        self.y += self.y_speed * dt

        if self.rect.colliderect(block.get_rect()):
            dx, dy = block.get_collition_resolution(self.rect)
            if dy < 0: # means the block is below & player needs to be moved up
                self.y_speed = 0
            self.x += dx
            self.y += dy
        self.current_animation.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the frame."""
        frame = pygame.transform.scale(self.current_animation.get_frame(), (self.width, self.height))
        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (self.x, self.y))
