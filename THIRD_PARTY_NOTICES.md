# Third-party notices

This project is a game-specific host for **NeoGeoRecomp**, a static
recompilation toolkit for SNK Neo Geo games. It contains several kinds of code
with different terms:

| Part | Path | Licence | Copyright |
|---|---|---|---|
| Original project code (ROM layout, player, scripts, packaging, docs) | `src/`, `scripts/`, `packaging/`, `docs/`, `CMakeLists.txt`, `tests/` | PolyForm Noncommercial 1.0.0 (see `LICENSE`) | the Samurai-Shodown-II-Recomp authors |
| NeoGeoRecomp 0.2.0 | `neogeorecomp/` | MIT (see `neogeorecomp/LICENSE`) | © 2026 sp00nznet |
| Musashi 68000 core | `neogeorecomp/ext/musashi/` | MIT | © 1998-2001 Karl Stenerud |
| z80 core | `neogeorecomp/ext/z80/` | MIT | © 2019 Nicolas Allemand |
| ymfm (YM2610 synthesis) | `neogeorecomp/ext/ymfm/` | BSD 3-Clause | © 2021 Aaron Giles |
| SDL2 (development package, Windows) | `deps/sdl2/` (not committed) | zlib | © 1997-2025 Sam Lantinga |

The verbatim licence texts ship beside this file: `neogeorecomp/LICENSE`,
`neogeorecomp/NOTICE`, `neogeorecomp/LICENSES/Musashi.txt`,
`neogeorecomp/LICENSES/z80.txt`, `neogeorecomp/LICENSES/ymfm.txt` and
`packaging/SDL2.txt`. Release bundles repeat them under `LICENSES/`.

## What the PolyForm licence covers

PolyForm Noncommercial 1.0.0 applies **only** to the original code in the first
row. The vendored toolkit and the emulation cores keep their MIT/BSD terms;
nothing in `neogeorecomp/` is relicensed. The generic audio fixes listed in
`docs/toolkit-patches.md` modify MIT-licensed upstream code and remain under
the upstream MIT terms. If you redistribute a build, keep those notices with
it.

## Game data

No SNK game ROM, system BIOS, recompiled C generated from a game ROM, or
entry-point list is included in this repository or in the release assets. The
recompiler runs on your own dump at build time.

Screenshots that show SNK artwork are not part of the repository; the `shots/`
folder used during testing is ignored by Git.

## Trademarks

"Samurai Shodown", "Samurai Spirits", "Neo Geo", "MVS" and "AES" are
trademarks of SNK Corporation. This project is not affiliated with or endorsed
by SNK. It ships no game data and no SNK code.

## Legal status

The PolyForm Noncommercial licence grants rights in the original code only. It
does not grant any right to SNK's game data, and it does not make distribution
of ROM-derived material lawful where it otherwise would not be. Whether you
may distribute a build that contains recompiled code generated from a game ROM
depends on your rights in that ROM; this project does not assert that such
distribution is permitted. If in doubt, distribute source and let each user
build against their own dump.
