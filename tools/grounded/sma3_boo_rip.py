#!/usr/bin/env python3
"""Project Grounded: haalt de art voor de Boo-intro (tools/grounded/boo_intro.py) uit Super Mario Advance 3: Yoshi's Island.
- Boo (16 x 16, vier standen): LZ77-blok 0x2BFED8 van de ROM (sprite-tiles in SNES-volgorde: 16 tiles per rij, een
  16x16-sprite = tiles n, n+1, n+16, n+17), met het globale spritepalet op 0x2D2B9C (wit met lichtblauw, de spoken).
  Standen: 0 kijkt, 1 kijkt (andere mond), 2 bek open, 3 handen voor de ogen (verlegen).
- Kamek op zijn bezem: uit de openingsfilm (de 'shadow' die de ooievaar aanvalt), schoon gerenderd uit VRAM/OAM op
  frame 3590 na het aanzetten zonder invoer (alleen de sprites met OBJ-palet 1), net als warioware_rip.py.
- Kameks toverspreuk: de cirkel, driehoek en het vierkant (8 x 8, één kleur) uit LZ77-blok 0x2C06D0; de kleur wisselt in
  de intro zelf.
Uitvoer: graphics/grounded/yoshis_island/boo_intro/<naam>.png (RGBA).
Gebruik: python3.11 tools/grounded/sma3_boo_rip.py "<pad naar Super Mario Advance 3 - Yoshi's Island (USA).gba>"
(mgba: python3.11, zie CLAUDE.md; de ROM staat als zip op origin/master, nooit committen)"""
import os, sys, struct
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'maptools'))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(ROOT, 'graphics/grounded/yoshis_island/boo_intro')

BOO_GFX, MAGIC_GFX, GHOST_PAL = 0x2BFED8, 0x2C06D0, 0x2D2B9C
KAMEK_FRAME, KAMEK_PAL = 3590, 1


def lz77(rom, p):
    assert rom[p] == 0x10
    size = rom[p + 1] | rom[p + 2] << 8 | rom[p + 3] << 16
    out, q = bytearray(), p + 4
    while len(out) < size:
        flags = rom[q]; q += 1
        for b in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> b):
                v = rom[q] << 8 | rom[q + 1]; q += 2
                for _ in range((v >> 12) + 3):
                    out.append(out[-((v & 0xFFF) + 1)])
            else:
                out.append(rom[q]); q += 1
    return bytes(out[:size])


def sheet16(data):
    """4bpp-tiles, 16 per rij -> indexbeeld."""
    a = np.frombuffer(data, np.uint8)
    n = len(a) // 32
    t = a.reshape(n, 32)
    px = np.zeros((n, 64), np.uint8)
    px[:, 0::2], px[:, 1::2] = t & 15, t >> 4
    px = px.reshape(n, 8, 8)
    img = np.zeros(((n + 15) // 16 * 8, 128), np.uint8)
    for i in range(n):
        img[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = px[i]
    return img


def pal(rom, p):
    v = np.array(struct.unpack('<16H', rom[p:p + 32]))
    return np.stack([(v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3], 1).astype(np.uint8)


def rgba(idx, p):
    a = np.zeros(idx.shape + (4,), np.uint8)
    a[..., :3] = p[idx]
    a[..., 3] = (idx > 0) * 255
    return Image.fromarray(a, 'RGBA')


def kamek(rom_path):
    import warioware_rip as R
    from emu import Emu
    e = Emu(rom_path)
    for _ in range(KAMEK_FRAME + 1):
        e.core.run_frame()
    m = e.core.memory
    st = {'io': bytes(m.u8[0x04000000 + i] for i in range(0x60)),
          'pal': bytes(m.u8[0x05000000 + i] for i in range(0x400)),
          'vram': bytes(m.u8[0x06000000 + i] for i in range(0x18000)),
          'oam': bytes(m.u8[0x07000000 + i] for i in range(0x400))}
    ids = set()
    for i in range(128):
        a0, a1, a2 = struct.unpack('<3H', st['oam'][i * 8:i * 8 + 6])
        if (a2 >> 12) == KAMEK_PAL and ((a0 >> 8) & 3) != 2:
            ids.add(i)
    return R.group(st, None, ids)


def main():
    rom_path = sys.argv[1]
    rom = open(rom_path, 'rb').read()
    os.makedirs(OUT, exist_ok=True)
    gp = pal(rom, GHOST_PAL)
    b = sheet16(lz77(rom, BOO_GFX))
    for k, name in enumerate(['boo_look', 'boo_look2', 'boo_mouth', 'boo_shy']):
        rgba(b[:, k * 16:k * 16 + 16], gp).save(os.path.join(OUT, name + '.png'))
    m = sheet16(lz77(rom, MAGIC_GFX))
    shapes = {'magic_circle': m[0:8, 112:120], 'magic_triangle': m[0:8, 120:128], 'magic_square': m[8:16, 112:120]}
    for name, idx in shapes.items():
        Image.fromarray(((idx > 0) * 255).astype(np.uint8), 'L').save(os.path.join(OUT, name + '.png'))
    k = kamek(rom_path)
    k.save(os.path.join(OUT, 'kamek_broom.png'))
    print('klaar:', sorted(os.listdir(OUT)), k.size)


if __name__ == '__main__':
    main()
