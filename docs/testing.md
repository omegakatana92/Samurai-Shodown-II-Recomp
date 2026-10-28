# Testing and compatibility

## What was measured (Windows x64, clang-cl 22.1.7, Release)

Commands were run from the project root with the ROM files in `roms/`.

| Test | Command | Result |
|---|---|---|
| ROM validation | `python scripts/validate-roms.py roms` | every file matches MAME (size, CRC32, SHA1) |
| Recompilation | `cmake --build build-windows` | 388,560 instructions, 21,260 routines, 28,551 dispatch entries after profiling |
| BIOS boot | `--headless --frames 600 --screenshot 600:bios.png` | NEO-GEO eyecatcher at frame 600 |
| Game boot | `--headless --frames 1800 --screenshot 1500:game.png` | intro sequence at frame 1500 |
| Coin → match | `--headless --frames 3600 --input tests/coin_start.txt` | HOW TO PLAY at 1300, stage/characters at 3550 |
| Correctness | `--headless --verify --frames 3000 --input tests/coin_start.txt` | **2,102,979 blocks, 0 mismatches** |
| Soak coverage | `--headless --frames 24000 --input tests/play_long.txt` | **100.00 % native, 0 interpreted instructions, 0 uncovered entry points** |
| Audio | `--headless --frames 4143 --wav attract.wav` | 70 s capture; per-second RMS matches MAME 0.242 attract playback |
| Windowed play | `Samsho2.exe --scale 3` | window opens, keyboard and gamepad input work |

The 24,000-frame soak is about 6 min 45 s of emulated time and walks coin,
start, HOW TO PLAY, character select and a match repeatedly. Coverage was
measured after one `profile` pass (`--dump-misses`). The entry list is a build
artifact and is not committed.

### Audio cross-check against MAME

A 70-second, no-input attract capture from this build and from MAME 0.242
(MVS, `sp-s2.sp1`, 48 kHz) were compared second by second. Example (left
channel RMS, sampled once per second):

```
MAME   597 633 629 476 611 694 280  50 427 1259 1467 2388 3061 2908 1898 1226
build  625 656 647 499 627 718 283  49 433 1270 1468 2443 3060 2923 1866 1211
```

The sequences track within a few percent for the whole capture, including the
quiet gaps while the game changes scene. There is no injected noise, no
clipping (peak 12,524 of 32,767) and no unexplained dropout.

## Steam Deck / Linux

Built with GCC 11 on Ubuntu 22.04 (glibc 2.35), packaged with appimagetool.
Artifact: `dist/steamdeck/Samsho2-SteamDeck-x86_64.AppImage` (10.6 MB).

Checked on a Linux x86_64 host:

- AppImage is executable and starts through `AppRun`
  (`--appimage-extract-and-run --headless --frames 700`): 28,551 entry
  points, 100.00 % native, 0 uncovered.
- Frame 600 rendered by the Linux binary is **byte-identical**
  (MD5 `57d476579f102cfb4f958464c5bfbee3`) to the Windows build's frame 600,
  so the recompiled CPU, video and timing agree across platforms.
- Windowed start with `SDL_VIDEODRIVER=dummy` opens the renderer (software
  fallback), runs 180 frames and exits cleanly.
- ROM/BIOS loading from `roms/` beside the AppImage, and via `--rom-path`.
- `ldd` resolves SDL2 from the AppImage's `usr/lib` when `AppRun` sets
  `LD_LIBRARY_PATH`; glibc, libstdc++ and the graphics/audio stack stay with
  the host.
- 1280×800 presentation: 320×224 scaled uniformly, letterboxed, not
  stretched (the code fits a 4:3 rectangle into the renderer output).

**Not tested:** a physical Steam Deck (LCD or OLED), SteamOS Gaming Mode
launch, Deck speakers/Bluetooth, and subjective listening on any device. The
AppImage targets SteamOS 3's glibc and uses only SDL2 + standard system
libraries, but that is a compatibility argument, not a hardware test.

## Known limitations

- The archive this port was developed against is the MVS/AES `samsho2` set.
  The Korean `samsho2k` program will not load with this layout (different
  program and S ROM names); add its files to `src/game.c` to support it.
- `--record` needs `ffmpeg` on `PATH`.
- Gamepad mapping is fixed (no remapping UI). SDL's
  `SDL_GAMECONTROLLERCONFIG` can describe unusual pads.
- Saves/NVRAM: the BIOS backup RAM is modelled, but there is no memory-card
  file manager.
- Native coverage is measured only over the profile scripts in `tests/`.
  Other modes (VS 2P, options, endings) still run correctly through the
  Musashi fallback, with lower native coverage until they are profiled.
