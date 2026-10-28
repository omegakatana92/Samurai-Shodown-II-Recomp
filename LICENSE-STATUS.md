# Licence status

**Status: PolyForm Noncommercial 1.0.0 — confirmed by the repository owner.**

The full text is in `LICENSE`. It applies to the original code written for
this port.

## What the PolyForm licence covers

Only code in this repository that the project author wrote and has the right
to license:

- `src/` — the Samurai Shodown II ROM layout and the player entry point
- `scripts/`, `packaging/` — build, packaging, icon and ROM-validation helpers
- `CMakeLists.txt` — the project's build description
- `tests/` — scripted input
- the project documentation in `docs/` and the top-level `README.md`

## What it does not cover

- `neogeorecomp/` — the upstream toolkit, **MIT**. See `neogeorecomp/LICENSE`
  and `neogeorecomp/NOTICE`.
- Musashi, z80 and ymfm — MIT / MIT / BSD-3-Clause. Verbatim texts are in
  `neogeorecomp/LICENSES/`.
- SDL2 — zlib licence. See `packaging/SDL2.txt`.
- SNK game data, the Neo Geo BIOS, and anything generated from them. **None of
  that is distributed here.**

## Distribution caution

PolyForm Noncommercial is not an open-source licence and does not permit
commercial redistribution. Do not assume that a build of this project may be
sold, bundled with commercial hardware, or distributed for a fee. ROMs, BIOS
files and code generated from them are not covered by this licence at all;
users must supply their own legally obtained dumps.

Release binaries contain statically recompiled code produced from the
maintainer's own dump. They grant no rights in SNK's game code and are
provided for use with ROMs the recipient is legally entitled to use.
