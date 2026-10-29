# Security Policy

## Scope

This repository is an **external** CS2 ESP + aimbot. It does not inject
code, does not touch the kernel, and does not modify `cs2.exe` on disk.
Everything happens through `ReadProcessMemory` / `WriteProcessMemory`
against a handle opened with `PROCESS_VM_READ | PROCESS_VM_WRITE`.

## Threat model

- Malicious PRs that exfiltrate offsets or add network calls. We do not
  ship any networking code; `scripts/` and `src/overlay/` are the only
  places allowed to open sockets, and only for localhost debug.
- Supply chain: pin every dependency in `requirements.txt`. CI installs
  from the pinned file only.

## Reporting a vulnerability

Open a private security advisory. Do **not** file a public issue for
anything that could get users banned faster than usual (e.g. a broken
handle-close path that leaves `cs2.exe` with a stale handle).

## Disclaimer

Use at your own risk. VAC / Overwatch bans are permanent and this repo
makes no attempt to hide from them beyond `utils/handle_guard.py`.