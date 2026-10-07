# Credits & Attribution

Re-Cherry (Linux port) stands on a tall stack of other people's work.
This file credits every project, library and tool the port uses, and
the license each one is under. License texts live in `licenses/`.
This project's own code is BSD 3-Clause (see `LICENSE`).

## The game

- **Lollipop Chainsaw** (Xbox 360, 2012) — developed by
  **Grasshopper Manufacture**, published by **Warner Bros. Interactive
  Entertainment**; © Grasshopper Manufacture / Warner Bros.
  No game data is bundled with this port; supply your own disc image.

## The recompilation

- **Re-Cherry** — the original ReXGlue recompilation project by
  **MaxDeadBear** (game config, function annotations, midasm hooks:
  fps unlock, frame counter, costume switcher, Xbox Live prompt
  bypass). Linux/SDK groundwork by **ufoex** (fork), incl. wiring the
  Xbox Live bypass into the build and the assets-next-to-exe fallback.
- **ReXGlue SDK** — static recompilation runtime and codegen
  (BSD 3-Clause; `licenses/ReXGlue-SDK-BSD-3-Clause.txt`), with
  house patches.
- **Re-Cherry Launcher** — the house TP-style Qt launcher (themed
  variant), BSD 3-Clause.

## Tools & libraries

- **Qt 6** (LGPL-3.0) — launcher UI.
- **FFmpeg** (LGPL-2.1) — media decoding in the runtime.
- **extract-xiso** — ISO extraction for the launcher's ISO import
  (optional system tool, not bundled; or import an already-extracted
  folder instead).
- **linuxdeploy / appimagetool** — AppImage packaging.
