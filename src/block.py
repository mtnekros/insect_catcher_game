import pygame
from pygame import Rect
from pygame.surface import Surface


class Block:
    """The blocks on the ground.

    TODO: Eventually, I will create a map class that will hold all the blocks
    in the level & it will handle how the players and the other object interact with
    the map.
    """

    def __init__(self, left: int, top: int) -> None:
        """Initialize the block."""
        width = 80
        height = 80
        self.rect = Rect(left, top, width, height)
        _sprite = pygame.image.load("./assets/grass_block.png").convert_alpha()
        self.sprite = pygame.transform.scale(_sprite, (width, height))

    def get_rect(self) -> Rect:
        """Return the bounding box of the block."""
        return self.rect

    def get_collition_resolution(self, rect: Rect) -> tuple[int, int]:
        """Return (dx, dy) to move given Rect out of the block."""
        if not self.rect.colliderect(rect):
            return 0,0
        # Calculate the offset
        dx_left = self.rect.right - rect.left
        dx_right = self.rect.left - rect.right
        dy_top = self.rect.top - rect.bottom
        dy_bottom = self.rect.bottom - rect.top

        min_dx = dx_left if abs(dx_left) < abs(dx_right) else dx_right
        min_dy = dy_top if abs(dy_top) < abs(dy_bottom) else dy_bottom
        if abs(min_dx) < abs(min_dy):
            return min_dx, 0
        return 0, min_dy

    def draw(self, screen: Surface) -> None:
        """Draw the block."""
        screen.blit(self.sprite, self.rect.topleft)
