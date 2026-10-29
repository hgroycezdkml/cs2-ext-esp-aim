"""Draws boxes + health bars for visible enemy players."""
from __future__ import annotations

from src.core.config_loader import ESPConfig
from src.handlers.base import Handler
from src.state.world_snapshot import WorldSnapshot
from src.utils.projection import world_to_screen


class ESPPlayerHandler(Handler):
    name = "esp_player"

    def __init__(self, cfg: ESPConfig) -> None:
        super().__init__(cfg.enabled)
        self.cfg = cfg

    def handle(self, snap: WorldSnapshot) -> None:
        if not snap.view_matrix or snap.local_player is None:
            return
        local_team = snap.local_player.team
        for p in snap.players:
            if self.cfg.team_filter and p.team == local_team:
                continue
            head = world_to_screen(snap.view_matrix, p.origin, snap.screen)
            feet = world_to_screen(snap.view_matrix, (p.origin[0], p.origin[1], p.origin[2] - 72), snap.screen)
            if head is None or feet is None:
                continue
            p.screen_box = (head, feet)
            p.draw_health = self.cfg.health_bar
            p.draw_box = self.cfg.box