"""Base class for all feature handlers."""
from __future__ import annotations

from abc import ABC, abstractmethod

from src.state.world_snapshot import WorldSnapshot


class Handler(ABC):
    name: str = "handler"

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    @abstractmethod
    def handle(self, snap: WorldSnapshot) -> None: ...