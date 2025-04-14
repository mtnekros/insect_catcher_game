import random

from pygame.rect import Rect
from pygame.surface import Surface

from src.block import Block


class MapLevel1:
    """Basic level 1 map."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize map with blocks."""
        self.blocks = [
            Block(
                i * Block.width,
                height - Block.height * 2,
            )
            for i in range(6)
        ]
        for _ in range(3):
            self.blocks.append(Block(
                random.randint(0, width),  # noqa: S311
                height - Block.height * 5
            ))


    def get_collition_resolution(self, rect: Rect) -> tuple[int, int]:
        """Return (dx, dy) to move given Rect out of the blocks."""
        for block in self.blocks:
            dx, dy = block.get_collition_resolution(rect)
            if dx != 0 or dy != 0:
                return dx, dy
        return 0, 0

    def draw(self, screen: Surface) -> None:
        """Draw the map."""
        for block in self.blocks:
            block.draw(screen)

