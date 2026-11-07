"""Probeersels kop (Jordi: "doe wat probeersels en toon me" · "puur van hoofd").
Basis = r9 zonder snavel (r9/basis.txt + r9/kop.txt zonder het snavelblok). Per variant P1-P6 een lijst met de hand getypte regels
"rij kolom pixels" in varianten.txt; '_' = transparant maken, '.' = overslaan. Uitvoer: P1.png ... P6.png, basis.png, vel.png.
Controle per variant: open randen (lichte kleur op de buitenrand) en losse pixels. Draaien: python3.11 probeer.py"""
from PIL import Image, ImageDraw
from palet import PAL, IDX, RGB
kop = open('../r9/kop.txt').read().split('\n')
a = kop.index('# snavel (Swellow: bovenrand in de donkere snaveltint, licht bovenop als vlek, mondlijn van de punt schuin omlaag naar de mondhoek,')
b = kop.index('# --- oren r9 (Jordi: "daarnaast is 1 van die slingers op zijn hoofd bijna een rechte lijn")')
regels = open('../r9/basis.txt').read().split('\n') + kop[:a] + kop[b:]
def zet(R, lijnen):
    for l in lijnen:
        if not l.strip() or l.startswith('#'): continue
        y, x, s = l.split(); y, x = int(y), int(x)
        for i, c in enumerate(s):
            if c == '.': continue
            R[y][x + i] = '.' if c == '_' else c
    return R
basis = zet([['.'] * 64 for _ in range(64)], regels)
var = {}; cur = None
for l in open('varianten.txt').read().split('\n'):
    if l.startswith('== '): cur = l[3:].split()[0]; var[cur] = []
    elif cur: var[cur].append(l)
def png(R, fn):
    im = Image.new('RGBA', (64, 64))
    for y in range(64):
        for x in range(64):
            if R[y][x] != '.': im.putpixel((x, y), RGB[R[y][x]] + (255,))
    im.save(fn); return im
def nb(x, y, d8):
    st = [(1,0),(-1,0),(0,1),(0,-1)] + ([(1,1),(1,-1),(-1,1),(-1,-1)] if d8 else [])
    return [(x+i, y+j) for i, j in st if 0 <= x+i < 64 and 0 <= y+j < 64]
LICHT = set('a b 1 y w c'.split())
out = []; ims = {'r9': Image.open('../r9/picapau_evo.png').convert('RGBA')}
png(basis, 'basis.png')
for n, l in var.items():
    R = zet([r[:] for r in basis], l)
    ims[n] = png(R, f'{n}.png')
    los = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and all(R[q][p] == '.' for p, q in nb(x, y, True))]
    rand = [(x, y, R[y][x]) for y in range(64) for x in range(64) if R[y][x] in LICHT and any(R[q][p] == '.' for p, q in nb(x, y, False))]
    tel = len({c for r in R for c in r} - {'.'})
    out.append(f'{n}: losse pixels {los}, lichte kleur op de buitenrand {rand}, {tel} kleuren + transparant')
open('controle_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
# vel: per kop 8x (boven) en 1x (onder), alleen het hoofd
C = (2, 0, 42, 20); Z = 8; W = (C[2] - C[0]) * Z; H = (C[3] - C[1]) * Z
namen = ['r9'] + list(var)
v = Image.new('RGBA', (8 + len(namen) * (W + 8), 16 + H + 8 + 24 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, n in enumerate(namen):
    x = 8 + i * (W + 8); k = ims[n].crop(C)
    d.text((x, 2), n if n != 'r9' else 'r9 (vergelijking)', fill=(0, 0, 0, 255))
    v.alpha_composite(k.resize((W, H), Image.NEAREST), (x, 16)); v.alpha_composite(k, (x, 16 + H + 8))
v.convert('RGB').save('vel.png'); print('vel.png', v.size)
