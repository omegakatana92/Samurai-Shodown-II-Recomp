# ROM layout

Source of truth: MAME `ROM_START( samsho2 )` (NGM-063) in
`src/mame/drivers/neogeo.cpp`. Every file below was checked against that entry
by size, CRC32 and SHA1. `scripts/validate-roms.py` performs the same check on
your copy.

## Game set `samsho2.zip`

| File | Size | CRC32 | SHA1 | Role |
|---|---|---|---|---|
| `063-p1.p1` | 2,097,152 | `22368892` | `0997f8284aa0f57a333be8a0fdea777d0d01afd6` | 68000 program |
| `063-s1.s1` | 131,072 | `64a5cd66` | `12cdfb27bf9ccd5a8df6ddd4628ef7cf2c6d4964` | fixed-layer tiles |
| `063-m1.m1` | 131,072 | `56675098` | `90429fc40d056d480d0e2bbefbc691d9fa260fc4` | Z80 sound driver |
| `063-v1.v1` | 2,097,152 | `37703f91` | `a373ebef4c33ba1d8340e826981a58769aada238` | ADPCM-A 0x000000 |
| `063-v2.v2` | 2,097,152 | `0142bde8` | `0be6c53acac44802bf70b6925452f70289a139d9` | ADPCM-A 0x200000 |
| `063-v3.v3` | 2,097,152 | `d07fa5ca` | `1da7f081f8b8fc86a91feacf900f573218d82676` | ADPCM-A 0x400000 |
| `063-v4.v4` | 1,048,576 | `24aab4bb` | `10ee4c5b3579865b93dcc1e4079963276aa700a6` | ADPCM-A 0x600000 |
| `063-c1.c1` | 2,097,152 | `86cd307c` | `0d04336f7c436d74638d8c1cd8651faf436a6bec` | sprites, plane 0/1 |
| `063-c2.c2` | 2,097,152 | `cdfcc4ca` | `179dc81432424d68cefedd20cc1c4b2a95deb891` | sprites, plane 2/3 |
| `063-c3.c3` | 2,097,152 | `7a63ccc7` | `49d97c543bc2860d493a353ab0d059088c6fbd21` | sprites, plane 0/1 |
| `063-c4.c4` | 2,097,152 | `751025ce` | `e1bbaa7cd67fd04e4aab7f7ea77f63ae1cbc90d0` | sprites, plane 2/3 |
| `063-c5.c5` | 2,097,152 | `20d3a475` | `28da44a136bd14c73c62c147c3f6e6bcfa1066de` | sprites, plane 0/1 |
| `063-c6.c6` | 2,097,152 | `ae4c0a88` | `cc8a7d11daa3821f83a6fd0942534706f939e576` | sprites, plane 2/3 |
| `063-c7.c7` | 2,097,152 | `2df3cbcf` | `e54f9022359963711451c2025825b862d36c6975` | sprites, plane 0/1 |
| `063-c8.c8` | 2,097,152 | `1ffc6dfa` | `acea18aca76c072e0bac2a364fc96d49cfc86e77` | sprites, plane 2/3 |

## System set `neogeo.zip`

| File | Size | CRC32 | SHA1 |
|---|---|---|---|
| `sp-s2.sp1` | 131,072 | `9036d879` | `4f5ed7105b7128794654ce82b51723e16e389543` |
| `sfix.sfix` | 131,072 | `c2ea0cfd` | `fd4a618cdcdbf849374f0a50dd8efe9dbab706c3` |
| `sm1.sm1` | 131,072 | `94416d67` | `42f9d7ddd6c0931fd64226a60dc73602b2819dcf` |
| `000-lo.lo` | 131,072 | `5a86cff2` | `5992277debadeb64d1c1c64b0a92d9293eaf7e4a` |

`--bios` accepts other system ROMs present in the same folder (for example
`sp-s3.sp1` or `sp-1v1_3db8c.bin`), but `sp-s2.sp1` is the tested default.

## Program image

`063-p1.p1` is stored 16-bit word-swapped (`ROM_LOAD16_WORD_SWAP`). MAME loads
the second 1 MB half into the fixed bank first and then `ROM_CONTINUE`s with
the first half:

```
file 0x000000–0x0FFFFF, word-swapped  -> 68k $100000–$1FFFFF  (banked image)
file 0x100000–0x1FFFFF, word-swapped  -> 68k $000000–$0FFFFF  (fixed bank)
```

After that transformation the fixed bank carries the `NEO-GEO` signature at
`$100` and the reset vectors `SSP=$0010F300`, `PC=$00C00402`.

Banking is the standard PROGBK1 scheme: the 1 MB window at `$200000` selects
one of the two halves of the banked image through the latch at
`$2FFFF0–$2FFFFF`. There is no encryption, SMA/CMC protection device or
daughterboard, and the S ROM is a plain 128 KB image (no VRAM bank bits).
