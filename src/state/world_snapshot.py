"""Snapshot of the world read once per tick."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Player:
    index: int
    health: int
    team: int
    origin: tuple[float, float, float]
    screen_box: tuple | None = None
    aim_delta: tuple[float, float] | None = None
    draw_box: bool = False
    draw_health: bool = False


@dataclass
class WorldItem:
    kind: str
    origin: tuple[float, float, float]
    screen_pos: tuple[int, int] | None = None
    label: str = ""


@dataclass
class WorldSnapshot:
    local_player: Player | None
    players: list[Player] = field(default_factory=list)
    world_items: list[WorldItem] = field(default_factory=list)
    view_matrix: list[float] = field(default_factory=list)
    screen: tuple[int, int] = (1920, 1080)

    @classmethod
    def empty(cls) -> "WorldSnapshot":
        return cls(local_player=None)