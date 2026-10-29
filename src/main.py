"""Entry point for cs2-ext-esp-aim."""
from __future__ import annotations

import argparse
import sys

from loguru import logger

from src.core.engine import Engine
from src.core.config_loader import load_config
from src.utils.handle_guard import acquire_cs2_handle


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="cs2-ext-esp-aim")
    p.add_argument("--dry-run", action="store_true", help="synthetic memory backend")
    p.add_argument("--config", default="config/default.toml")
    p.add_argument("--no-overlay", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    cfg = load_config(args.config)

    handle = acquire_cs2_handle(dry_run=args.dry_run)
    if handle is None:
        logger.error("cs2.exe not running or access denied")
        return 1

    logger.info("attached pid={} build={}", handle.pid, handle.build)
    engine = Engine(handle=handle, config=cfg, overlay=not args.no_overlay)
    try:
        engine.run()
    except KeyboardInterrupt:
        logger.info("shutdown requested")
    finally:
        engine.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())