"""External memory reader with per-tick snapshotting."""
from __future__ import annotations

from typing import Any

import pymem
from loguru import logger

from src.state.world_snapshot import Player, WorldSnapshot
from src.utils.matrix import read_view_matrix


class MemoryReader:
    def __init__(self, handle: Any, offsets: dict[str, int]) -> None:
        self.pm = pymem.Pymem(handle.pid) if not handle.dry_run else None
        self.client = handle.client_base
        self.offsets = offsets
        self._dry = handle.dry_run

    def _ptr(self, base: int, chain: list[int]) -> int:
        if self._dry:
            return 0
        addr = base
        for off in chain[:-1]:
            addr = self.pm.read_int(addr + off)
        return addr + chain[-1]

    def snapshot(self) -> WorldSnapshot:
        if self._dry:
            return WorldSnapshot.empty()

        local = self._ptr(self.client, self.offsets["dwLocalPlayer"])
        entity_list = self._ptr(self.client, self.offsets["dwEntityList"])
        vmatrix = read_view_matrix(self.pm, self.client + self.offsets["dwViewMatrix"])

        players: list[Player] = []
        for i in range(1, 33):
            try:
                ent = self.pm.read_int(entity_list + 0x8 * (i >> 9) + 0x10)
                if not ent:
                    continue
                hp = self.pm.read_int(ent + self.offsets["m_iHealth"])
                if hp <= 0:
                    continue
                pos = (
                    self.pm.read_float(ent + self.offsets["m_vecOrigin"]),
                    self.pm.read_float(ent + self.offsets["m_vecOrigin"] + 4),
                    self.pm.read_float(ent + self.offsets["m_vecOrigin"] + 8),
                )
                team = self.pm.read_int(ent + self.offsets["m_iTeamNum"])
                players.append(Player(index=i, health=hp, team=team, origin=pos))
            except Exception as exc:  # noqa: BLE001
                logger.debug("entity {} read failed: {}", i, exc)

        return WorldSnapshot(local_player=local, players=players, view_matrix=vmatrix)