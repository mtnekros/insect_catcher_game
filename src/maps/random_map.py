import random

from pygame import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from src.block import Block


class RandomMap:
    """Basic level 1 map."""

    def __init__(self, width: int, height: int, extra_blocks: int) -> None:
        """Initialize map with blocks."""
        self.blocks = [
            Block(
                i * Block.width,
                height - Block.height * 4,
            )
            for i in range(1, 7)
        ]
        # self.blocks.extend(self.generate_random_blocks(
        #     width=width,
        #     height=height,
        #     count=extra_blocks,
        #     offset=Vector2(7 * Block.width, 0),
        # ))
        for _ in range(extra_blocks):
            prev = self.blocks[-1]
            self.blocks.append(self.generate_next_block(prev, height))


    def generate_random_blocks(self, width: int, height: int, count: int, offset: Vector2) -> list[Block]:
        """Generate random blocks."""
        blocks = []
        for _ in range(count):
            while True:
                new_block = Block(
                    random.randint(int(offset.x), width),  # noqa: S311
                    int(offset.y + height - random.randint(0, 2) * Block.height * 2.5)  # noqa: S311
                )
                if all(not new_block.get_rect().colliderect(block.get_rect()) for block in  blocks):
                    blocks.append(new_block)
                    break
        return blocks

    def generate_next_block(self, current_block: Block, height: int) -> Block:
        """Generate next block within max jump."""
        max_jump_height = 200
        max_jump_length = 150
        next_x = current_block.get_rect().right + random.randint(0, max_jump_length)  # noqa: S311
        next_y = min(
            max(
                Block.height * 3,
                current_block.get_rect().top + random.randint(0, max_jump_height) * random.choice([1, -1])  # noqa: S311
            ),
            height - Block.height * 2
        )
        return Block(next_x, next_y)


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

