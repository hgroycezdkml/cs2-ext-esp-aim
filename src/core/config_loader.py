"""TOML config loader with pydantic validation."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import BaseModel, Field


class ESPConfig(BaseModel):
    enabled: bool = True
    box: bool = True
    health_bar: bool = True
    skeleton: bool = False
    max_distance: float = 5000.0
    team_filter: bool = True


class AimConfig(BaseModel):
    enabled: bool = True
    fov: float = 3.0
    smooth: float = 1.4
    bone: str = "head"
    key: str = "mouse5"


class OverlayConfig(BaseModel):
    target_frame_ms: int = 7
    frame_budget_ms: int = 12
    width: int = 1920
    height: int = 1080
    click_through: bool = True


@dataclass
class Config:
    esp: ESPConfig = field(default_factory=ESPConfig)
    aim: AimConfig = field(default_factory=AimConfig)
    overlay: OverlayConfig = field(default_factory=OverlayConfig)
    offsets: dict[str, int] = field(default_factory=dict)


class _Raw(BaseModel):
    esp: ESPConfig = Field(default_factory=ESPConfig)
    aim: AimConfig = Field(default_factory=AimConfig)
    overlay: OverlayConfig = Field(default_factory=OverlayConfig)


def load_config(path: str | Path) -> Config:
    p = Path(path)
    raw = tomllib.loads(p.read_text()) if p.exists() else {}
    parsed = _Raw(**raw)
    offsets_path = p.parent / "offsets.json"
    import json
    offsets = json.loads(offsets_path.read_text()) if offsets_path.exists() else {}
    return Config(esp=parsed.esp, aim=parsed.aim, overlay=parsed.overlay, offsets=offsets)