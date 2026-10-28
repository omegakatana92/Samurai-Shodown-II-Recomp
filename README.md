# Samurai Shodown II — Neo Geo static recompilation

**Samurai Shodown II / Shin Samurai Spirits: Haohmaru Jigokuhen** (1994, NGM-063)
running as native C on Windows x64 and Linux x86_64 (Steam Deck), built with
[NeoGeoRecomp](https://github.com/sp00nznet/neogeorecomp).

The 68000 program is translated ahead of time into C, one routine per entry
point, and executed natively against a model of the MVS board: LSPC video,
palette, I/O, the Z80 sound CPU and the real `sp-s2.sp1` system ROM. It is not
an emulator wrapper. Addresses that the recompiler has not seen fall back to
the bundled Musashi interpreter.

## Status

| Area | State | Evidence |
|---|---|---|
| Build | Windows x64 Release, Linux x86_64 Release | clang-cl 22 / GCC 11 builds |
| Boot | Real MVS BIOS → game intro → title → match | screenshots in `shots/` (not committed) |
| Native coverage | **100.00 %** over a 24,000-frame scripted soak | `[exec] … interpreted instructions 0, 0 uncovered entry points` |
| Correctness | **0 mismatches** in 2,102,979 blocks | `--verify --frames 3000 --input tests/coin_start.txt` |
| Graphics | Sprites, fix layer, palettes, scrolling, raster IRQ | visual comparison against MAME |
| Audio | FM, SSG and ADPCM-A through YM2610 → SDL2 | 70 s attract capture matches MAME 0.242 per-second RMS |
| Controls | Keyboard and SDL2 gamepads | `--input` scripts plus windowed play |
| Steam Deck | AppImage built and smoke-tested under Linux x86_64 | frame-identical to Windows; see `docs/testing.md` |

Native coverage and `--verify` numbers are measured on this dump; they are not
guesses. Coverage is a property of the entry-point set used at build time:
`build-windows/entries.txt` is produced by the `profile` target and is not part
of the repository.

## ROM requirements

You must supply your own legally obtained dumps. Nothing derived from them is
in this repository or in the release assets.

Game set (`samsho2.zip`), unzipped:

```
063-p1.p1   2 MB   program (fixed 1 MB + 1 MB banked)    CRC32 22368892
063-s1.s1   128 KB fixed-layer tiles                     CRC32 64a5cd66
063-m1.m1   128 KB Z80 sound driver                      CRC32 56675098
063-v1..v4  7 MB   ADPCM-A samples                       CRC32 37703f91 0142bde8 d07fa5ca 24aab4bb
063-c1..c8  16 MB  sprite bitplanes (4 odd/even pairs)   CRC32 86cd307c cdfcc4ca 7a63ccc7 751025ce
                                                               20d3a475 ae4c0a88 2df3cbcf 1ffc6dfa
```

System set (`neogeo.zip`):

```
sp-s2.sp1   128 KB  MVS Asia/Europe BIOS v2 (default)
sfix.sfix   128 KB  fixed-layer tiles
sm1.sm1     128 KB  BIOS sound driver
000-lo.lo   128 KB  sprite shrink table
```

Verify a folder with `python3 scripts/validate-roms.py roms` (checks size,
CRC32 and SHA1 against MAME). Full table in `docs/rom-layout.md`.

The cartridge uses a plain PROGBK1 board: **no** NEO-SMA/NEO-CMC encryption, no
protection device, no extra sound ROM. The 2 MB program is the usual
second-half-first image: file `0x000000–0x0FFFFF` is the banked half and file
`0x100000–0x1FFFFF` is the fixed bank.

## Build

### Windows x64

Prerequisites: Visual Studio 2022/2026 with the C++ workload (or LLVM
clang-cl), CMake 3.21+, Ninja, and the official SDL2 VC development package
unpacked under `deps/sdl2/<version>/`.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build-windows.ps1 `
    -RomDir .\roms -Test
```

The script configures with Ninja + clang-cl (pass `-Msvc` for the MSVC toolset),
recompiles the program from your dump into `build-windows/generated/`, builds
`Samsho2.exe`, runs a headless smoke test and stages
`dist/windows/Samsho2-Windows-x64/`.

### Linux x86_64

Prerequisites: `gcc`, `g++`, `cmake`, `make`, `libsdl2-dev`, `pkg-config`,
`python3`.

```bash
./scripts/build-linux.sh                      # player only
./packaging/appimage/build-appimage.sh        # player + AppImage
```

Output: `dist/steamdeck/Samsho2-SteamDeck-x86_64.AppImage`.

### Manual CMake

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DSAMSHO2_ROM_DIR=$PWD/roms
cmake --build build --parallel
```

Without `SAMSHO2_ROM_DIR` the player still builds interpreter-only.

## Usage

```
Samsho2 --rom-path DIR [--bios-path DIR] [--bios FILE] [--fullscreen]
        [--scale N] [--headless] [--frames N] [--input FILE]
        [--screenshot N:FILE] [--record FILE.mp4] [--wav FILE] [--mute]
        [--interp] [--verify] [--dump-misses FILE]
```

Keyboard: arrows; **Z X C V** = A B C D; **5** coin; **1** start (P1);
**2** start (P2); **3** select; **9** service; **F2** test; **F11/Alt+Enter**
fullscreen; **Esc** quit.

Gamepad (SDL2, Xbox layout): D-pad/left stick, **A B X Y** = Neo Geo A B C D,
**Start** = start, **Back/View** = coin, **left shoulder** = select. The first
pad is player 1, the second player 2. On MVS you must insert a coin before
Start does anything.

### Steam Deck

1. Copy `Samsho2-SteamDeck-x86_64.AppImage` and a `roms/` folder beside it
   (for example `~/Games/Samsho2/`).
2. `chmod +x Samsho2-SteamDeck-x86_64.AppImage`, run it once in Desktop Mode.
3. Add it to Steam as a non-Steam game. The launcher starts fullscreen; the
   320×224 picture is pillarboxed on 1280×800, never stretched.
4. Steam Input: use the default gamepad template. Steam Input presents a
   standard controller to SDL2, which is what the player reads.

The AppImage bundles SDL2 (from the build host) and the player; it does not
bundle glibc, libstdc++ or the graphics stack. ROMs and BIOS are never inside.

## Testing

See `docs/testing.md` for the commands and the measured results of this build.
The short version:

```bash
Samsho2 --headless --rom-path roms --frames 600 --screenshot 600:bios.png
Samsho2 --headless --rom-path roms --frames 3600 --input tests/coin_start.txt
Samsho2 --headless --verify --rom-path roms --frames 3000 --input tests/coin_start.txt
cmake --build build-windows --target profile   # then rebuild for coverage
```

## Repository layout

```
src/game.c, game.h      ng_game_t: the verified ROM layout
src/main.c              player entry point (ng_main)
src/recomp_main.c       generator entry point (ng_recomp_main)
neogeorecomp/           upstream toolkit (MIT), vendored
tests/                  scripted input for headless runs
packaging/              AppImage and Windows staging helpers
scripts/                build and ROM validation helpers
docs/                   ROM layout, compatibility, testing, licensing notes
```

No `CMakeLists.txt`-generated state, ROMs, BIOS files or generated C is
committed. Build directories and `dist/` are ignored.

## Licence

- **Original project code** (`src/`, `scripts/`, `packaging/`, `docs/`,
  `CMakeLists.txt`, tests): **PolyForm Noncommercial 1.0.0**. Noncommercial
  use is free; commercial use requires a separate licence.
- **NeoGeoRecomp**: MIT. **Musashi**: MIT. **z80**: MIT. **ymfm**:
  BSD-3-Clause. **SDL2**: zlib. Their notices are kept verbatim in
  `neogeorecomp/` and `packaging/SDL2.txt`; see `THIRD_PARTY_NOTICES.md`.

No SNK ROM, BIOS or ROM-derived code is distributed. "Samurai Shodown",
"Samurai Spirits", "Neo Geo", "MVS" and "AES" are trademarks of SNK
Corporation; this project is not affiliated with or endorsed by SNK.
