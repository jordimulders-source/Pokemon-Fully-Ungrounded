#!/usr/bin/env python3
"""Project Grounded: grijze stenen standbeelden als overworld-objecten (48x48, 1 frame, rij voor rij zoals de truck).

Zelfde techniek als de Regi-beelden in Ashfrost (`regi_statue.statue`: frame 0 van de overworld-sprite in 6 grijstinten
op een sokkel), maar dan als object in plaats van als metatiles: zo kost een beeld geen tileset-ruimte. Alle beelden
delen één palet (`stone_statue.pal`, tag OBJ_EVENT_PAL_TAG_STONE_STATUE). Het object staat op het vak van de sokkel;
de sprite steekt een half vak links/rechts en twee vakken omhoog uit.

Nieuw beeld: soort in STATUES zetten, script draaien, en in C een OBJ_EVENT_GFX_STATUE_* toevoegen (zie TAPU_KOKO).
Gebruik: python3 tools/grounded/statue_sprites.py [voorbeeld.png]"""
import os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
os.chdir(ROOT)
from regi_statue import statue, STONE

BG = (115, 197, 164)
STATUES = ['tapu_koko', 'tapu_lele', 'tapu_bulu', 'tapu_fini', 'celebi']
PICS = 'graphics/object_events/pics/misc'
PAL = 'graphics/object_events/palettes/stone_statue.pal'


def sprite(species):
    """48x48 met palet-indexen: 0 = transparant, 1-6 = STONE."""
    rgba = statue(species)                              # 32x48, sokkel onderaan
    out = Image.new('P', (48, 48), 0)
    px, src = out.load(), rgba.load()
    for y in range(48):
        for x in range(32):
            r, g, b, a = src[x, y]
            if a:
                px[x + 8, y] = STONE.index((r, g, b)) + 1
    flat = list(BG)
    for c in STONE:
        flat += c
    out.putpalette(flat + [0] * (768 - len(flat)))
    return out


def main():
    imgs = []
    for sp in STATUES:
        im = sprite(sp)
        im.save('%s/statue_%s.png' % (PICS, sp))
        imgs.append(im)
    cols = [BG] + STONE + [(0, 0, 0)] * (15 - len(STONE))
    with open(PAL, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in cols:
            f.write('%d %d %d\n' % c)
    if len(sys.argv) > 1:
        o = Image.new('RGB', (len(imgs) * 52, 48), (90, 160, 120))
        for i, im in enumerate(imgs):
            mask = Image.new('L', im.size, 0)
            mask.putdata([255 if v else 0 for v in im.tobytes()])
            o.paste(im.convert('RGB'), (i * 52, 0), mask)
        o.resize((o.width * 4, o.height * 4), Image.NEAREST).save(sys.argv[1])
    print('klaar:', ', '.join(STATUES))


if __name__ == '__main__':
    main()
