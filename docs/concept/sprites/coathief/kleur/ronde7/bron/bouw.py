"""Zet raster.txt (met de hand getypt: 'y x0 pixels') om naar ../coathief.png en controleert tegen het bevroren silhouet.
Geen shading of filters: alleen letter -> paletindex."""
import os, sys
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
SIL = os.path.join(H, '../../../silhouet/ronde8.txt')
PAL = [('.', '98d0a0'),  # 0 transparant
       ('k', '140c0a'),  # omlijning (zwartbruin), schaduwkant
       ('m', '2a201c'),  # bivakmuts schaduw / selout donkere delen
       ('z', '40352f'),  # bivakmuts basis (kop, onderpoten, donkere staartringen)
       ('y', '5e5048'),  # bivakmuts licht
       ('Y', '8a7a6c'),  # bivakmuts hooglicht (randje linksboven)
       ('d', '5e3216'),  # vacht schaduw / selout
       ('b', '8e5226'),  # vacht basis (roodbruin)
       ('l', 'b87636'),  # vacht licht (goudbruin)
       ('h', 'd8a058'),  # vacht hooglicht
       ('n', 'a48660'),  # creme schaduw / selout lichte ringen
       ('c', 'dcc49a'),  # creme basis (ringen, vlekken, klauwen)
       ('w', 'f6eedc'),  # creme licht, glans
       ('r', '8c2418'),  # oog donker roodbruin (ronde 3: lichter, los van de kop)
       ('i', 'b04a2c'),  # iris licht (onderkant)
       ('x', '7c6448')]  # creme selout naast transparant (ronde 3, luma 104)
ORDER = ''.join(c for c, _ in PAL)
def lees(fp=os.path.join(H, 'raster.txt')):
    g = [['.'] * 64 for _ in range(64)]; fout = []
    for ln in open(fp):
        ln = ln.split('#')[0].strip() if not ln.startswith('#') else ''
        if not ln: continue
        y, x0, px = ln.split(); y = int(y); x0 = int(x0)
        for i, ch in enumerate(px):
            if ch not in ORDER: fout.append('onbekende letter %r op (%d,%d)' % (ch, x0 + i, y))
            if g[y][x0 + i] != '.': fout.append('dubbel op (%d,%d)' % (x0 + i, y))
            g[y][x0 + i] = ch
    return g, fout
if __name__ == '__main__':
    g, fout = lees()
    # handmatige reparaties (zelfde formaat, overschrijven raster.txt)
    pf = os.path.join(H, 'reparaties.txt')
    if os.path.exists(pf):
        for ln in open(pf):
            ln = ln.split('#')[0].strip()
            if not ln: continue
            y, x0, px = ln.split(); y = int(y); x0 = int(x0)
            for i, ch in enumerate(px):
                if ch not in ORDER: fout.append('onbekende letter op (%d,%d)' % (x0 + i, y))
                g[y][x0 + i] = ch
    sil = [l.rstrip('\n') for l in open(SIL) if l.strip()]
    diff = [(x, y) for y in range(64) for x in range(64) if (g[y][x] != '.') != (sil[y][x] == '#')]
    for f in fout: print(f)
    print('alpha-diff', len(diff), diff[:20])
    print('pixels', sum(ch != '.' for r in g for ch in r))
    open(os.path.join(H, 'raster_grid.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')
    flat = []
    for _, hx in PAL: flat += [int(hx[i:i + 2], 16) for i in (0, 2, 4)]
    im = Image.new('P', (64, 64)); im.putpalette(flat)
    im.putdata([ORDER.index(g[y][x]) for y in range(64) for x in range(64)])
    im.save(os.path.join(H, '../coathief.png'), transparency=0, bits=4)
