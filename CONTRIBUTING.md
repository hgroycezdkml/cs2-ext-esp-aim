# Contributing to cs2-ext-esp-aim

Thanks for wanting to help. This project is an external CS2 ESP + aimbot
written in Python — no injection, no kernel driver, pure RPM/WPM via
`pymem` and an overlay window.

## Ground rules

- **External only.** PRs that inject DLLs into `cs2.exe` will be closed.
  We read memory with `ReadProcessMemory` and draw with a transparent
  overlay. That is the whole architecture.
- **Update offsets, not signatures.** When Valve ships a patch, bump
  `offsets/latest.json` and open a PR titled `offsets: <build>`.
- Keep the render loop under 2ms in the profiler. If your feature stalls
  the overlay, it goes behind a config flag.

## Local setup

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.main --dry-run
```

`--dry-run` runs the overlay against a synthetic memory backend so you
can iterate without CS2 open.

## Style

- `black` + `ruff`, line length 100.
- No global mutable state outside `state/`.
- Every new feature handler inherits from `handlers.base.Handler`.

## Reporting offset drift

Use `scripts/dump_offsets.py --compare offsets/latest.json` and attach
the diff to the issue. Do not paste raw `cs2.exe` dumps.