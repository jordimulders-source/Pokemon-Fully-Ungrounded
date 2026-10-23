"""Bouwt de alpaca (ronde 8) uit de met de hand getekende delen in delen.txt.
Alleen samenvoegen (voorste deel wint) en wegschrijven; geen automatische schaduw of omlijning.
Gebruik: python3 bouw.py <map met delen.txt> <uitvoermap>
"""
import sys, os
from PIL import Image

PAL = [
    ('.', (152, 208, 160)),  # 0 transparant
    ('K', (40, 32, 40)),     # 1 omlijning donker
    ('W', (255, 255, 248)),  # 2 wol hooglicht / glans
    ('w', (240, 230, 206)),  # 3 wol
    ('v', (208, 190, 158)),  # 4 wolschaduw
    ('V', (150, 126, 100)),  # 5 wolomlijning
    ('F', (246, 206, 152)),  # 6 vacht hooglicht
    ('f', (222, 164, 106)),  # 7 vacht
    ('e', (180, 116, 74)),   # 8 vachtschaduw
    ('E', (120, 72, 50)),    # 9 vachtomlijning
    ('R', (250, 150, 116)),  # 10 handschoen hooglicht
    ('r', (222, 92, 70)),    # 11 handschoen
    ('s', (170, 54, 56)),    # 12 handschoen schaduw
    ('S', (110, 32, 42)),    # 13 handschoen omlijning
    ('P', (240, 150, 160)),  # 14 roze
    ('B', (110, 120, 190)),  # 15 oogreflectie
]
IDX = {c: i for i, (c, _) in enumerate(PAL)}


def lees(pad):
    delen = []
    for regel in open(pad, encoding='utf-8'):
        regel = regel.rstrip('\n')
        if regel.startswith('## '):
            naam, x, y = regel[3:].split()
            delen.append([naam, int(x), int(y), []])
        elif regel.startswith('#') or not regel:
            continue
        else:
            delen[-1][3].append(regel)
    return delen


def samenvoegen(delen, extra=None):
    doek = [[0] * 64 for _ in range(64)]
    for naam, x0, y0, rijen in delen:
        breedtes = {len(r) for r in rijen}
        if len(breedtes) > 1:
            print('LET OP: ongelijke rijen in', naam, sorted(breedtes))
        for dy, rij in enumerate(rijen):
            for dx, c in enumerate(rij):
                if c == '.':
                    continue
                doek[y0 + dy][x0 + dx] = IDX[c]
    return doek


def afbeelding(doek):
    im = Image.new('P', (64, 64))
    flat = []
    for _, rgb in PAL:
        flat += list(rgb)
    im.putpalette(flat)
    im.putdata([v for rij in doek for v in rij])
    return im


def main():
    bron, uit = sys.argv[1], sys.argv[2]
    f1 = samenvoegen(lees(os.path.join(bron, 'delen.txt')))
    # frame 2: subtiel ademen = kop+kuif+oren 1 pixel omlaag (aparte, ook met de hand gecontroleerde regel)
    delen2 = lees(os.path.join(bron, 'delen.txt'))
    for d in delen2:
        if d[0] in ('gezicht', 'kuif', 'oor_links', 'oor_rechts'):
            d[2] += 1
    f2 = samenvoegen(delen2)
    for naam, doek in (('raster_f1.txt', f1), ('raster_f2.txt', f2)):
        with open(os.path.join(bron, naam), 'w') as fh:
            for rij in doek:
                fh.write(''.join(PAL[v][0] for v in rij) + '\n')
    im = Image.new('P', (64, 128))
    im.putpalette(afbeelding(f1).getpalette())
    im.paste(afbeelding(f1), (0, 0))
    im.paste(afbeelding(f2), (0, 64))
    im.save(os.path.join(uit, 'anim_front.png'), transparency=0)
    with open(os.path.join(uit, 'normal.pal'), 'w', newline='\r\n') as fh:
        fh.write('JASC-PAL\n0100\n16\n')
        for _, (r, g, b) in PAL:
            fh.write('%d %d %d\n' % (r, g, b))
    opp = sum(1 for rij in f1 for v in rij if v)
    rand = 0
    zwart = 0
    for y in range(64):
        for x in range(64):
            if not f1[y][x]:
                continue
            buren = [(x + a, y + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if any(not (0 <= u < 64 and 0 <= v < 64) or not f1[v][u] for u, v in buren):
                rand += 1
                zwart += f1[y][x] == 1
    print('oppervlak', opp, 'zwart-aandeel rand %.2f' % (zwart / rand))


if __name__ == '__main__':
    main()
