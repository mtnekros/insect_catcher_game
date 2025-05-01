import math
import random

import pygame
from pygame import Rect, Surface, Vector2

from src.animation import Animation, get_frame


def get_random_vec(min_length: float, max_length: float) -> Vector2:
    """Get a random vector of a random magnitude."""
    length = random.random() * (max_length - min_length) + min_length  # noqa: S311
    random_vector = Vector2(
        random.choice([1, -1]) * random.random(), # noqa: S311
        random.choice([1, -1]) * random.random(), # noqa: S311
    )
    return random_vector.normalize() * length


class Butterfly:
    """Butterfly to catch."""

    width = 40
    height = 40

    __slots__ = ("pos", "velocity", "animation", "is_dead")

    def __init__(self, x: float, y: float) -> None:
        """Create butterfly instance."""
        self.pos = Vector2(x, y)
        self.velocity = get_random_vec(40, 60)
        sprite_sheet = pygame.image.load("./assets/butterfly.png").convert_alpha()
        frame_width = 15.5
        frame_height = 14
        self.is_dead = False
        self.animation = Animation(
            frames=[
                pygame.transform.scale(
                    get_frame(
                        sprite_sheet,
                        frame_width,
                        frame_height,
                        i,
                        0
                    ),
                    (Butterfly.width, Butterfly.height)
                )
                for i in range(3)
            ],
            duration_secs=0.75,
            cycle=True,
        )

    def get_rect(self) -> Rect:
        """Return the bbox rect."""
        return Rect(
            self.pos.x,
            self.pos.y,
            self.width,
            self.height,
        )

    def update(self, dt: float, bbox: Rect) -> None:
        """Update the position of walker."""
        self.pos += self.velocity * dt
        rect = self.get_rect()
        if rect.left < bbox.left or rect.right > bbox.right:
            self.velocity.x *= -1
        if rect.top < bbox.top or rect.bottom > bbox.bottom:
            self.velocity.y *= -1

        self.clamp(bbox)
        self.animation.update(dt)

    def clamp(self, bbox: Rect) -> None:
        """Clamp the walker inside the bounding box."""
        rect = self.get_rect()
        if rect.left < bbox.left:
            self.pos.x = bbox.left
        if rect.right > bbox.right:
            self.pos.x = bbox.right - self.width
        if rect.top < bbox.top:
            self.pos.y = bbox.top
        if rect.bottom > bbox.bottom:
            self.pos.y = bbox.bottom - self.height

    def mark_as_dead(self) -> None:
        """Mark the butterfly is dead."""
        self.is_dead = True

    def draw(self, screen: Surface, cam_pos: Vector2) -> None:
        """Draw the walker."""
        angle = self.velocity.angle_to(Vector2(0, -1))
        frame = self.animation.get_frame()
        frame = pygame.transform.rotate(frame, angle)
        screen.blit(frame, (self.pos + cam_pos))
        # pygame.draw.rect(screen, "Red", self.get_rect(), width=1)

