#!/usr/bin/env python3
"""Validate the Samurai Shodown II (MAME set `samsho2`) ROM files.

Checks every file the runtime loads against MAME's neogeo.cpp: size, CRC32
and SHA1.  The game set and the required `neogeo` system ROMs may live in
one directory or be passed as two.

Usage:
    python scripts/validate-roms.py ROM_DIR [BIOS_DIR]

Exit code 0 means every file matched; 1 means a problem was found.
No ROM data is read from or written anywhere except the paths given.
"""
import hashlib
import os
import sys
import zlib

# MAME src/mame/drivers/neogeo.cpp, ROM_START( samsho2 ) /* 063 */.
GAME = {
    "063-p1.p1": (0x200000, "22368892", "0997f8284aa0f57a333be8a0fdea777d0d01afd6"),
    "063-s1.s1": (0x020000, "64a5cd66", "12cdfb27bf9ccd5a8df6ddd4628ef7cf2c6d4964"),
    "063-m1.m1": (0x020000, "56675098", "90429fc40d056d480d0e2bbefbc691d9fa260fc4"),
    "063-v1.v1": (0x200000, "37703f91", "a373ebef4c33ba1d8340e826981a58769aada238"),
    "063-v2.v2": (0x200000, "0142bde8", "0be6c53acac44802bf70b6925452f70289a139d9"),
    "063-v3.v3": (0x200000, "d07fa5ca", "1da7f081f8b8fc86a91feacf900f573218d82676"),
    "063-v4.v4": (0x100000, "24aab4bb", "10ee4c5b3579865b93dcc1e4079963276aa700a6"),
    "063-c1.c1": (0x200000, "86cd307c", "0d04336f7c436d74638d8c1cd8651faf436a6bec"),
    "063-c2.c2": (0x200000, "cdfcc4ca", "179dc81432424d68cefedd20cc1c4b2a95deb891"),
    "063-c3.c3": (0x200000, "7a63ccc7", "49d97c543bc2860d493a353ab0d059088c6fbd21"),
    "063-c4.c4": (0x200000, "751025ce", "e1bbaa7cd67fd04e4aab7f7ea77f63ae1cbc90d0"),
    "063-c5.c5": (0x200000, "20d3a475", "28da44a136bd14c73c62c147c3f6e6bcfa1066de"),
    "063-c6.c6": (0x200000, "ae4c0a88", "cc8a7d11daa3821f83a6fd0942534706f939e576"),
    "063-c7.c7": (0x200000, "2df3cbcf", "e54f9022359963711451c2025825b862d36c6975"),
    "063-c8.c8": (0x200000, "1ffc6dfa", "acea18aca76c072e0bac2a364fc96d49cfc86e77"),
}

BIOS = {
    "sp-s2.sp1": (0x020000, "9036d879", "4f5ed7105b7128794654ce82b51723e16e389543"),
    "sfix.sfix": (0x020000, "c2ea0cfd", "fd4a618cdcdbf849374f0a50dd8efe9dbab706c3"),
    "sm1.sm1":   (0x020000, "94416d67", "42f9d7ddd6c0931fd64226a60dc73602b2819dcf"),
    "000-lo.lo": (0x020000, "5a86cff2", "5992277debadeb64d1c1c64b0a92d9293eaf7e4a"),
}


def check(name, expected, search):
    size, crc, sha1 = expected
    for d in search:
        p = os.path.join(d, name)
        if os.path.isfile(p):
            break
    else:
        print("MISSING   %-12s (looked in %s)" % (name, ", ".join(search)))
        return False
    data = open(p, "rb").read()
    got_crc = "%08x" % (zlib.crc32(data) & 0xFFFFFFFF)
    got_sha1 = hashlib.sha1(data).hexdigest()
    ok = len(data) == size and got_crc == crc and got_sha1 == sha1
    if ok:
        print("OK        %-12s %9d bytes  crc32 %s" % (name, len(data), got_crc))
    else:
        print("MISMATCH  %-12s size %d (want %d) crc32 %s (want %s)"
              % (name, len(data), size, got_crc, crc))
    return ok


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    game_dir = sys.argv[1]
    bios_dir = sys.argv[2] if len(sys.argv) > 2 else game_dir
    ok = True
    print("== game set samsho2 ==")
    for n, e in GAME.items():
        ok &= check(n, e, [game_dir])
    print("== system set neogeo ==")
    for n, e in BIOS.items():
        ok &= check(n, e, [bios_dir, game_dir])
    print("result:", "all files verified" if ok else "PROBLEMS FOUND")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
