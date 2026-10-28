# Toolkit patches carried in `neogeorecomp/`

The vendored toolkit is NeoGeoRecomp 0.2.0 (MIT). It is kept close to
upstream so the project can be rebased. The deltas below are generic fixes
that apply to every game, not title hacks; they are also the ones shipped in
the other ports in this workspace.

## `src/audio.c` — YM2610 timer status and IRQ line

Upstream latched the timer overflow flags only while the corresponding IRQ was
enabled, and asserted the Z80 IRQ line whenever any flag was set. On a YM2610
the flag latches on overflow regardless of the enable bits, and only the
enable bits (register `$27` bits 2 and 3) put the flag on the IRQ line.

The driver polls status in both states, so the old combination could drop a
timer tick or inject an interrupt the driver had masked. Fixed by:

- `ym_update_timers()`: set status bit 0/1 on overflow unconditionally;
- `audio_sync()`: `int_pending = (status & 1 && ctrl & 4) || (status & 2 && ctrl & 8)`.

Earlier generic fixes already present in this copy:

- M1 window masking uses MAME's region-derived mask
  `(M1 size - 1) & 0x3FFFF`, so banked music data beyond the first window is
  read from the right offset.
- `audio_take_samples()` calls `audio_sync()` every frame, so the sequencer
  keeps running when the 68000 does not poll a sound port.

## `src/window_sdl.c` — SDL audio output

- Converted data is drained in whole destination frames. Queuing a partial
  frame swaps left/right for everything that follows.
- Queue high/low watermarks are computed in whole device frames; trimming a
  byte count that is not a multiple of the frame size shifts the sample
  alignment and turns the rest of the queue into noise.
- A >250 ms stall trims only the oldest excess (frame-aligned `SDL_DequeueAudio`)
  instead of clearing the queue.
- If the device runs dry between two frames, the 60 ms cushion is rebuilt once
  instead of leaving SDL to underrun on every following frame.
- `SDL_DequeueAudio`'s unsigned return is used correctly (it returns bytes
  dequeued, not a negative error code).

None of these change the emulated YM2610 samples; `--wav` output is unchanged
by the output-path fixes.

## Licensing

These patches are modifications of MIT-licensed upstream code and remain under
the upstream MIT terms. They are not covered by this project's PolyForm
licence.
