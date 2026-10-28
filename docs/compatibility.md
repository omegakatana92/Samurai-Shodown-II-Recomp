# Compatibility report — Samurai Shodown II (NGM-063)

## Hardware model exercised

| Component | Detail | State |
|---|---|---|
| 68000 | 12 MHz, static recompilation with Musashi fallback | working; 0 mismatches in `--verify` |
| BIOS | real `sp-s2.sp1` (MVS Asia/Europe v2), `sfix`, `sm1`, `000-lo` | boots, coin/credits, test mode |
| Program banking | PROGBK1, 1 MB window at `$200000`, latch `$2FFFF0` | working (2 MB program) |
| Fix layer | 128 KB S ROM, no VRAM bank bits | working |
| Sprites | 4 odd/even pairs, 16 MB, per-scanline LSPC rendering | working; no stray tiles or clipping |
| Palette | both banks, per-scanline switching | working |
| Raster IRQ | timer IRQ from the LSPC | working (status bars, screen shake) |
| Z80 | 4 MHz, M1 driver, NMI command latch, reply latch | working |
| YM2610 | FM, SSG, ADPCM-A via ymfm; timers and IRQ | working; matches MAME 0.242 attract audio |
| Input | keyboard + up to two SDL2 gamepads | working |
| Audio out | SDL2 stream, 55,555 Hz source resampled to the device format | working |

## What was compared, and how

- **Boot and menus** against MAME 0.242 with the same BIOS and set: BIOS
  eyecatcher, the "LONG LONG AGO…" intro, HOW TO PLAY, character select and
  the first stage render the same.
- **CPU** with `--verify`, which re-runs every native block in Musashi and
  compares registers, flags and bus writes: 2,102,979 blocks, 0 mismatches.
- **Coverage** with `--dump-misses` and one regeneration: 100.00 % native over
  the 24,000-frame soak.
- **Audio** by second-by-second RMS against a MAME capture of the same attract
  sequence.

## Not verified

- Actual Steam Deck hardware (LCD/OLED), Gaming Mode, Deck audio devices.
- Subjective listening: waveform comparison cannot tell whether a track is the
  *right* track, only that the mix behaves like the reference.
- VS 2-player, options menu and endings beyond the scripted soak (they run, but
  entry-point coverage for those modes was not separately profiled).
- Memory-card save/load UI.
- Korean `samsho2k` variant.
