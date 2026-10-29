"""Bench overlay frame time against the dry-run backend."""
from __future__ import annotations

import time

from src.core.config_loader import load_config
from src.core.engine import Engine
from src.utils.handle_guard import acquire_cs2_handle


def main() -> None:
    cfg = load_config("config/default.toml")
    handle = acquire_cs2_handle(dry_run=True)
    engine = Engine(handle=handle, config=cfg, overlay=False)
    start = time.perf_counter()
    for _ in range(1000):
        engine._dispatch(engine.reader.snapshot())
    print(f"avg dispatch: {(time.perf_counter() - start) * 1000 / 1000:.3f}ms")


if __name__ == "__main__":
    main()