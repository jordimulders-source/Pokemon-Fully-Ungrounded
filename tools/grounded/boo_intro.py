#!/usr/bin/env python3
"""Project Grounded: gevechtsintro van de Boos (Commander Boo in het spookhuis op Yoshi's Island, en Boo in het Battle
Stadium). Jordi: "bij Boo mag je een haunted house pakken uit de game waar Boo's hun ogen bedekken, Kamek langs komt
vliegen met zijn magische spreuk en van 1 Boo een Commander maakt waardoor die tegen je gaat battlen".
Het spookhuis uit Yoshi's Island (de SMA3-achtergrond, al in graphics/grounded/yoshis_island/), vijf verlegen Boos met
de handen voor de ogen, Kamek die op zijn bezem langs raast en zijn spreuk (cirkel, driehoek, vierkant) op de middelste
Boo afvuurt. Die zwelt op, draait zich om en is Commander Boo (zijn eigen trainerfoto, die al in de ROM staat).
De timing (op de beat van MUS_GROUNDED_VS_BROKEN_PIER) staat in src/data/boo_intro.h.

Art: de Boos, Kamek en zijn spreuk komen uit de ROM (tools/grounded/sma3_boo_rip.py ->
graphics/grounded/yoshis_island/boo_intro/). Uitvoer (graphics/battle_transitions/): boo_intro (het spookhuis, BG-palet
10-15), boo_yi (vier Boo-standen, 32 x 32), boo_kamek (64 x 32), boo_magic (drie vormen x vier kleuren, 8 x 8).
Gebruik: python3 tools/grounded/boo_intro.py [voorbeeldmap]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from gym_intro_lib import OUT, gba, ROOT
from legend_intros2 import EncoderN, quantize3, write_pal

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None
YI = os.path.join(ROOT, 'graphics/grounded/yoshis_island/')
RIP = YI + 'boo_intro/'
NPALS = 4

# het spookhuis: de houten wand met de boogvensters en het zwarte gras ervoor (SMA3-achtergrond, periode 256 px)
HOUSE_BOX = (6, 1080, 246, 1240)


def house():
    a = np.array(Image.open(YI + 'sma3_backgrounds_a.png').convert('RGB').crop(HOUSE_BOX))
    a[(a == 0).all(2)] = (8, 8, 8)       # zuiver zwart is in BG-beelden doorzichtig
    return Image.fromarray(a)


def rgba(name):
    return np.array(Image.open(RIP + name + '.png').convert('RGBA'))


def sheet(name, frames, w, h):
    """Kleine sprite (w x h), frames onder elkaar, één palet (index 0 doorzichtig)."""
    cols = []
    for a in frames:
        for c in map(tuple, (a[a[:, :, 3] > 0][:, :3] >> 3 << 3)):
            if c not in cols:
                cols.append(c)
    assert len(cols) <= 15, (name, len(cols))
    out = []
    for a in frames:
        c = np.zeros((h, w), np.uint8)
        fh, fw = a.shape[:2]
        y0, x0 = (h - fh) // 2, (w - fw) // 2
        rgb = (a[:, :, :3] >> 3) << 3
        for i, col in enumerate(cols):
            m = (rgb == np.array(col)).all(2) & (a[:, :, 3] > 0)
            c[y0:y0 + fh, x0:x0 + fw][m] = i + 1
        out.append(c)
    im = Image.fromarray(np.concatenate(out, 0), 'P')
    pal = [(0, 0, 0)] + cols + [(0, 0, 0)] * (15 - len(cols))
    im.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    im.save(OUT + 'boo_%s.png' % name)
    write_pal(OUT + 'boo_%s.pal' % name, pal)
    return im


def x2(a):
    return np.kron(a, np.ones((2, 2, 1), np.uint8))


# Kameks spreuk wisselt van kleur: rood, geel, groen, blauw (met een witte kern op de rand)
MAGIC = [(248, 56, 56), (248, 216, 32), (56, 200, 72), (64, 128, 248)]


def magic_frames():
    out = []
    for shape in ('magic_circle', 'magic_triangle', 'magic_square'):
        m = np.array(Image.open(RIP + shape + '.png')) > 0
        for col in MAGIC:
            a = np.zeros((8, 8, 4), np.uint8)
            a[m] = col + (255,)
            out.append(a)
    return out


def main():
    h = house()
    pals = quantize3([h], n=NPALS, shared=2)
    enc = EncoderN('intro', pals, 10, prefix='boo_')
    enc.add(h, None, 'spookhuis')
    enc.save()
    boos = [x2(rgba(n)) for n in ('boo_shy', 'boo_look', 'boo_look2', 'boo_mouth')]
    sheet('yi', boos, 32, 32)
    sheet('kamek', [rgba('kamek_broom')], 64, 32)
    sheet('magic', magic_frames(), 8, 8)
    if PREVIEW:
        bg = enc.render(enc.maps[0])
        bg = bg.convert('RGBA')
        for i, (x, y) in enumerate([(40, 84), (84, 70), (120, 92), (156, 70), (200, 84)]):
            im = Image.fromarray(boos[0 if i != 2 else 1])
            bg.alpha_composite(im, (x - 16, y - 16))
        k = x2(rgba('kamek_broom'))
        bg.alpha_composite(Image.fromarray(k), (150, 16))
        bg.convert('RGB').resize((480, 320), Image.NEAREST).save(os.path.join(PREVIEW, 'boo_intro_mock.png'))


if __name__ == '__main__':
    main()
