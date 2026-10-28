/*
 * game.c - Samurai Shodown II (MAME set `samsho2`, NGM-063) ROM layout,
 * shared by the player and the generator so both load the program
 * identically.
 *
 * Source of truth is MAME's ROM_START( samsho2 ) in
 * src/mame/drivers/neogeo.cpp.  Every file in the supplied archive matches
 * that entry's size and CRC32:
 *
 *   P ROM  063-p1.p1  2 MB  TC5316200, 16-bit word-swapped.  MAME loads the
 *          second 1 MB half into the fixed bank first and then continues
 *          with the first half into the banked image (ROM_LOAD16_WORD_SWAP
 *          at 0x100000 + ROM_CONTINUE at 0x000000), which is the usual
 *          layout for a 2 MB program:
 *            file 0x000000-0x0FFFFF -> 68k $100000-$1FFFFF (banked image)
 *            file 0x100000-0x1FFFFF -> 68k $000000-$0FFFFF (fixed bank)
 *   C ROMs 063-c1..c8  8 x 2 MB, four odd/even bitplane pairs (planes 0/1
 *          in the odd file, 2/3 in the even file) = 16 MB interleaved.
 *   S ROM  063-s1.s1  128 KB fixed-layer tiles.
 *   M1     063-m1.m1  128 KB Z80 sound driver.
 *   V ROMs 063-v1..v4 7 MB ADPCM-A samples (2+2+2+1 MB), concatenated.
 *
 * The cart is a normal PROGBK1 MVS/AES board: one 1 MB bank behind the
 * $200000 window, selected at $2FFFF0-$2FFFFF.  There is no program
 * encryption, no NEO-SMA/NEO-CMC protection and no extra sound ROM.  The
 * fixed bank carries the "NEO-GEO" signature at $100 once word-swapped,
 * which is what the loader assumes.
 */
#include "game.h"

const ng_game_t k_samsho2 = {
    .name = "samsho2",
    .title = "Samurai Shodown II - Haohmaru Jigokuhen",
    .prom_size = 0x200000,
    .prom = {
        /* file        file offset  dest       length    swap */
        {"063-p1.p1", 0x000000,    0x100000,  0x100000, 1},
        {"063-p1.p1", 0x100000,    0x000000,  0x100000, 1},
    },
    .crom_size = 0x1000000,
    .crom_pairs = {
        {"063-c1.c1", "063-c2.c2"},
        {"063-c3.c3", "063-c4.c4"},
        {"063-c5.c5", "063-c6.c6"},
        {"063-c7.c7", "063-c8.c8"},
    },
    .srom = "063-s1.s1",
    .m1 = "063-m1.m1",
    .vrom = {"063-v1.v1", "063-v2.v2", "063-v3.v3", "063-v4.v4"},
};
