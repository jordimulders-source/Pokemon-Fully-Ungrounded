"""Palet ronde 14 (C2, bijna wit met lila zweem; muil geestblauw/paars). Index 0 transparant."""
import sys
from PIL import Image
PAL = [
    (152, 208, 160),  # . transparant
    (28, 20, 44),     # 1 buitenlijn schaduwkant, mondlijn, oog-omgeving
    (90, 76, 124),    # 2 selout lichtkant, binnenlijnen (vleugelrand, takschaduw)
    (142, 130, 176),  # 3 diepe schaduw, halsrand, veerlijnen, staartbanden
    (186, 178, 214),  # 4 schaduw vacht, vleugel basis, hoornglans
    (226, 222, 240),  # 5 vacht basis, veerranden
    (250, 248, 255),  # 6 vacht licht
    (156, 136, 128),  # 7 hoorn (bovensnavel) en schorsstreepjes (grijsbruin)
    (8, 8, 12),       # 8 oog, puur zwart
    (44, 30, 96),     # 9 keel / slagschaduw in de muil (donkerst)
    (84, 64, 168),    # A muil donker-midden
    (122, 106, 214),  # B muil midden
    (166, 158, 240),  # C muil licht (verhemelte, kaakbodem)
    (234, 214, 242),  # D lip / kaakrand
    (80, 68, 80),     # E hoorn donker (haak, snijrand)
    (112, 98, 140),   # F vleugel schaduw, schors op de vleugel
]
CH = '.123456789ABCDEF'
def build(txt, out):
    rows = [l.rstrip('\n') for l in open(txt)][:64]
    im = Image.new('P', (64, 64), 0); im.putpalette([v for c in PAL for v in c])
    for y, r in enumerate(rows):
        for x, c in enumerate(r): im.putpixel((x, y), CH.index(c))
    im.save(out, transparency=0); return im
def pal(out):
    with open(out, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in PAL))
if __name__ == '__main__': build(sys.argv[1], sys.argv[2])
