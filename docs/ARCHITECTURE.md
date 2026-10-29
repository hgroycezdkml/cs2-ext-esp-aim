# Architecture

```
src/main.py            entry — parses args, opens handle, boots Engine
src/core/              engine loop, memory reader, config loader
src/handlers/          feature handlers (esp_player, esp_bomb, aim_silent)
src/overlay/           transparent pygame + win32 layered window
src/state/             per-tick WorldSnapshot dataclasses
src/utils/             projection, matrix, handle guard, offset sync
src/native/            optional C++ input helper (SendInput wrapper)
scripts/               dev tools (offset dump, frame bench)
config/                default.toml + offsets.json
```

The loop is strictly read → dispatch → draw. Handlers never touch the
renderer directly; they annotate the `WorldSnapshot` and the renderer
consumes it. That keeps ESP and aim features testable against a synthetic
snapshot.