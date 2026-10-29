"""External aim assist — moves the cursor toward the closest enemy bone."""
from __future__ import annotations

import math

from pynput.mouse import Controller

from src.core.config_loader import AimConfig
from src.core.memory_reader import MemoryReader
from src.handlers.base import Handler
from src.state.world_snapshot import WorldSnapshot


class AimHandler(Handler):
    name = "aim"

    def __init__(self, cfg: AimConfig, reader: MemoryReader) -> None:
        super().__init__(cfg.enabled)
        self.cfg = cfg
        self.reader = reader
        self.mouse = Controller()

    def handle(self, snap: WorldSnapshot) -> None:
        if not self.enabled or not snap.players:
            return
        target = self._closest(snap)
        if target is None:
            return
        dx, dy = target.aim_delta
        if math.hypot(dx, dy) > self.cfg.fov * 20:
            return
        self.mouse.move(int(dx / self.cfg.smooth), int(dy / self.cfg.smooth))

    def _closest(self, snap: WorldSnapshot):
        best = None
        best_d = float("inf")
        for p in snap.players:
            if snap.local_player and p.team == snap.local_player.team:
                continue
            if p.aim_delta is None:
                continue
            d = math.hypot(*p.aim_delta)
            if d < best_d:
                best, best_d = p, d
        return best