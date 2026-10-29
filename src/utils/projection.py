"""World-to-screen using the CS2 view matrix."""
from __future__ import annotations


def world_to_screen(
    matrix: list[float],
    world: tuple[float, float, float],
    screen: tuple[int, int],
) -> tuple[int, int] | None:
    if len(matrix) != 16:
        return None
    x, y, z = world
    w = matrix[12] * x + matrix[13] * y + matrix[14] * z + matrix[15]
    if w < 0.001:
        return None
    sx = (matrix[0] * x + matrix[1] * y + matrix[2] * z + matrix[3]) / w
    sy = (matrix[4] * x + matrix[5] * y + matrix[6] * z + matrix[7]) / w
    return (int((screen[0] / 2) * (1 + sx)), int((screen[1] / 2) * (1 - sy)))