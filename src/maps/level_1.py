import random

from pygame import Vector2
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
            for i in range(1, 7)
        ]
        self.blocks.extend(self.generate_random_blocks(
            width=width,
            height=height,
            count=5,
        ))


    def generate_random_blocks(self, width: int, height: int, count: int) -> list[Block]:
        """Generate random blocks."""
        blocks = []
        for _ in range(count):
            while True:
                new_block = Block(
                    random.randint(0, width),  # noqa: S311
                    height - Block.height * 5
                )
                if all(not new_block.get_rect().colliderect(block.get_rect()) for block in  blocks):
                    blocks.append(new_block)
                    break
        return blocks

    def get_collition_resolution(self, rect: Rect) -> tuple[int, int]:
        """Return (dx, dy) to move given Rect out of the blocks."""
        for block in self.blocks:
            dx, dy = block.get_collition_resolution(rect)
            if dx != 0 or dy != 0:
                return dx, dy
        return 0, 0


    def draw(self, screen: Surface, cam_pos: Vector2) -> None:
        """Draw the map."""
        for block in self.blocks:
            block.draw(screen, offset=cam_pos)

