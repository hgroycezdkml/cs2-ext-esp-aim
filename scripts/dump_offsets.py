"""Compare running cs2.exe offsets against the checked-in file."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.core.memory_reader import MemoryReader
from src.utils.handle_guard import acquire_cs2_handle


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--compare", default="offsets/latest.json")
    args = ap.parse_args()

    handle = acquire_cs2_handle()
    if handle is None:
        print("cs2.exe not running")
        return 1

    known = json.loads(Path(args.compare).read_text())["offsets"] if False else json.loads(Path(args.compare).read_text())
    reader = MemoryReader(handle, known)
    snap = reader.snapshot()
    print(f"players seen: {len(snap.players)}  local: {snap.local_player is not None}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())