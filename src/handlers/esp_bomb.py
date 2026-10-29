"""Bomb + dropped weapon ESP (C4, defuse kit, primary)."""
from __future__ import annotations

from src.core.config_loader import ESPConfig
from src.handlers.base import Handler
from src.state.world_snapshot import WorldSnapshot
from src.utils.projection import world_to_screen


class ESPBombHandler(Handler):
    name = "esp_bomb"

    def __init__(self, cfg: ESPConfig) -> None:
        super().__init__(cfg.enabled)
        self.cfg = cfg

    def handle(self, snap: WorldSnapshot) -> None:
        if not snap.view_matrix:
            return
        for obj in snap.world_items:
            if obj.kind not in ("c4", "defuse_kit"):
                continue
            pt = world_to_screen(snap.view_matrix, obj.origin, snap.screen)
            if pt is None:
                continue
            obj.screen_pos = pt
            obj.label = "C4" if obj.kind == "c4" else "KIT"