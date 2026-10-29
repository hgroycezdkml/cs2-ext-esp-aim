"""Core render + tick loop. Owns the overlay and the feature bus."""
from __future__ import annotations

import time
from dataclasses import dataclass

from loguru import logger

from src.core.config_loader import Config
from src.core.memory_reader import MemoryReader
from src.handlers.base import Handler
from src.handlers.esp_player import ESPPlayerHandler
from src.handlers.esp_bomb import ESPBombHandler
from src.handlers.aim_silent import AimHandler
from src.overlay.renderer import OverlayRenderer
from src.state.world_snapshot import WorldSnapshot


@dataclass
class Engine:
    handle: object
    config: Config
    overlay: bool = True

    def __post_init__(self) -> None:
        self.reader = MemoryReader(self.handle, self.config.offsets)
        self.renderer = OverlayRenderer(self.config.overlay) if self.overlay else None
        self.handlers: list[Handler] = [
            ESPPlayerHandler(self.config.esp),
            ESPBombHandler(self.config.esp),
            AimHandler(self.config.aim, self.reader),
        ]
        self._running = False

    def run(self) -> None:
        self._running = True
        logger.info("engine started with {} handlers", len(self.handlers))
        while self._running:
            t0 = time.perf_counter()
            snap = self.reader.snapshot()
            self._dispatch(snap)
            if self.renderer:
                self.renderer.draw(snap)
            elapsed = (time.perf_counter() - t0) * 1000
            if elapsed > self.config.overlay.frame_budget_ms:
                logger.warning("frame over budget: {:.2f}ms", elapsed)
            time.sleep(max(0.0, (self.config.overlay.target_frame_ms - elapsed) / 1000))

    def _dispatch(self, snap: WorldSnapshot) -> None:
        for h in self.handlers:
            if h.enabled:
                h.handle(snap)

    def shutdown(self) -> None:
        self._running = False
        if self.renderer:
            self.renderer.close()
        logger.info("engine stopped")