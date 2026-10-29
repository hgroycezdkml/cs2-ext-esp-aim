"""Opens a handle to cs2.exe with the minimum rights needed."""
from __future__ import annotations

from dataclasses import dataclass

import psutil
from loguru import logger


@dataclass
class Cs2Handle:
    pid: int
    client_base: int
    build: str
    dry_run: bool = False


def acquire_cs2_handle(dry_run: bool = False) -> Cs2Handle | None:
    if dry_run:
        return Cs2Handle(pid=0, client_base=0, build="dry-run", dry_run=True)

    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] == "cs2.exe":
            pid = proc.info["pid"]
            try:
                base = _client_base(pid)
            except Exception as exc:  # noqa: BLE001
                logger.error("failed to resolve client.dll base: {}", exc)
                return None
            return Cs2Handle(pid=pid, client_base=base, build="1.40.x")
    return None


def _client_base(pid: int) -> int:
    import pymem
    pm = pymem.Pymem(pid)
    for mod in pm.list_modules():
        if mod.name.lower() == "client.dll":
            return mod.lpBaseOfDll
    raise RuntimeError("client.dll not loaded")