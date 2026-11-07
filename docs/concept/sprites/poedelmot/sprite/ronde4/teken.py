"""Poedelmot sprite ronde 4: raster.txt (met de hand, een teken per pixel, hex-index van PAL, '.' = transparant)
-> anim_front.png (64x64, geindexeerd) + normal.pal (JASC) + sprite_8x.png. Draaien vanuit deze map of de repo-root."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
PAL = [
    (152, 208, 160),  # 0 transparant
    (32, 24, 24),     # 1 omlijning schaduwkant, ogen
    (96, 88, 80),     # 2 selout wol/vleugel (lichtkant), binnenlijn schaduwkant
    (160, 148, 136),  # 3 wol diepe schaduw, binnenlijn vleugel over vleugel
    (208, 200, 184),  # 4 wol schaduw, plukbogen
    (232, 224, 216),  # 5 wol basis
    (248, 248, 240),  # 6 wol hooglicht, oogglans
    (240, 232, 208),  # 7 vleugel basis (creme)
    (208, 200, 168),  # 8 vleugel schaduw
    (168, 136, 104),  # 9 vleugeladers (lichtbruin)
    (120, 88, 56),    # a oor schaduw
    (72, 48, 32),     # b oor omlijning + strepen
    (184, 144, 96),   # c oor licht
    (152, 104, 64),   # d oor basis
]
def raster():
    return [l.rstrip('\n') for l in open(os.path.join(HERE, 'raster.txt'))][:64]
if __name__ == '__main__':
    R = raster()
    im = Image.new('P', (64, 64), 0)
    flat = [c for rgb in PAL for c in rgb] + [0] * (3 * (256 - len(PAL)))
    im.putpalette(flat)
    im.putdata([0 if ch == '.' else int(ch, 16) for r in R for ch in r])
    im.save(os.path.join(HERE, 'anim_front.png'), transparency=0)
    pal16 = PAL + [(0, 0, 0)] * (16 - len(PAL))
    open(os.path.join(HERE, 'normal.pal'), 'w', newline='\r\n').write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in pal16))
    rgb = im.convert('RGB'); rgb.resize((512, 512), Image.NEAREST).save(os.path.join(HERE, 'sprite_8x.png'))
