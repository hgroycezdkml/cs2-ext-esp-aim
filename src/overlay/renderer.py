"""Transparent click-through overlay using pygame + win32 layered window."""
from __future__ import annotations

import pygame
import win32api
import win32con
import win32gui

from src.core.config_loader import OverlayConfig
from src.state.world_snapshot import WorldSnapshot


class OverlayRenderer:
    def __init__(self, cfg: OverlayConfig) -> None:
        self.cfg = cfg
        pygame.init()
        self.surface = pygame.Surface((cfg.width, cfg.height), pygame.SRCALPHA)
        self.hwnd = self._create_window()
        self._init_done = True

    def _create_window(self) -> int:
        hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST,
            "STATIC", "cs2-ext-esp-aim", win32con.WS_POPUP,
            0, 0, self.cfg.width, self.cfg.height,
            None, None, None, None,
        )
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        return hwnd

    def draw(self, snap: WorldSnapshot) -> None:
        self.surface.fill((0, 0, 0, 0))
        for p in snap.players:
            if getattr(p, "draw_box", False) and p.screen_box:
                (hx, hy), (fx, fy) = p.screen_box
                pygame.draw.rect(self.surface, (255, 40, 40), (hx - 20, hy, 40, fy - hy), 1)
            if getattr(p, "draw_health", False) and p.screen_box:
                (hx, hy), (fx, fy) = p.screen_box
                pygame.draw.rect(self.surface, (40, 255, 40), (hx - 26, hy, 3, int((fy - hy) * p.health / 100)))

    def close(self) -> None:
        pygame.quit()
        if self.hwnd:
            win32gui.DestroyWindow(self.hwnd)