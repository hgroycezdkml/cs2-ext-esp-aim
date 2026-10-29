"""Reads the 4x4 view matrix out of cs2 memory."""
from __future__ import annotations


def read_view_matrix(pm, addr: int) -> list[float]:
    return [pm.read_float(addr + 4 * i) for i in range(16)]