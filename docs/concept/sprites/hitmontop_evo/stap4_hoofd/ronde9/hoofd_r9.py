"""Ronde 9: het hoofd op het silhouet van Jordi's Gemini-concept (omgezet_29.png = de omgezette bron).
1) silhouet en omlijning uit de bron; 2) vlakken: knot, band, stekel, kop apart; 3) schaduw per vlak met licht linksboven
(Hitmontops 4 huidtinten); 4) met de hand: ogen (Hitmontops oog: zwart rondje met wit puntje), de V (twee lijnen die
tussen de ogen in één punt samenkomen), mondstreepje.
Legenda raster: # omlijning, 0 licht, 1 basis, 2 schaduw, 3 donker, w wit, g grijs, . leeg."""
import os, math
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
KLEUR = {'#': (16, 16, 16), '0': (255, 222, 156), '1': (222, 189, 131), '2': (180, 139, 90), '3': (131, 90, 41),
         'w': (255, 255, 255), 'g': (205, 205, 205)}
TERUG = {v: k for k, v in KLEUR.items()}
src = Image.open(os.path.join(HERE, 'omgezet_29.png')).convert('RGBA'); sp = src.load()
W, H = src.size
G = {}
for y in range(H):
    for x in range(W):
        if sp[x, y][3]:
            G[(x, y)] = TERUG.get(sp[x, y][:3], '1')
binnen = {p for p, c in G.items()}
rand = {p for p in binnen if any((p[0] + dx, p[1] + dy) not in binnen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}

# knot als volle bal, kop ervoor; restvlak onder de knot weg
BAL_C, BAL_R = (23.5, 9.0), 5.3
in_bal = lambda x, y: (x - BAL_C[0]) ** 2 + (y - BAL_C[1]) ** 2 <= BAL_R ** 2
in_kop = lambda x, y: ((x - 12.5) / 12.9) ** 2 + ((y - 18.6) / 10.1) ** 2 <= 1.0 or y <= 9 and 9 <= x <= 17
binnen = {p for p in binnen if in_kop(*p)} | {(x, y) for x in range(W) for y in range(H) if in_bal(x, y)}
kopset = {p for p in binnen if in_kop(*p)}
rand = {p for p in binnen if any((p[0] + dx, p[1] + dy) not in binnen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
rand |= {p for p in kopset if any((p[0] + dx, p[1] + dy) not in kopset and in_bal(p[0] + dx, p[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
# vlakken
def is_knot(x, y): return in_bal(x, y) and not in_kop(x, y)
def is_stekel(x, y): return y <= 8 and 9 <= x <= 17
KOP_C, KOP_R = (12.5, 18.5), (12.5, 9.8)   # ellips van de kop (benadering van de omtrek)

def tint(u, v):
    """u,v: plek t.o.v. middelpunt, genormaliseerd (-1..1). Licht linksboven: licht waar -u-v groot is."""
    s = -0.55 * u - 0.75 * v
    r = math.hypot(u, v)
    if r > 0.93 and s < 0.25: return '3'
    if s > 0.78 and r > 0.45: return '0'
    if s < -0.35 or (r > 0.8 and s < 0.0): return '2'
    return '1'

R = {}
for (x, y) in binnen:
    if (x, y) in rand:
        R[(x, y)] = '#'; continue
    if is_knot(x, y):
        R[(x, y)] = tint((x - BAL_C[0]) / BAL_R, (y - BAL_C[1]) / BAL_R)
    elif is_stekel(x, y):
        R[(x, y)] = '0' if x <= 12 else ('1' if x <= 13 else '2')
    else:
        R[(x, y)] = tint((x - KOP_C[0]) / KOP_R[0], (y - KOP_C[1]) / KOP_R[1])

# grens knot/kop: omlijning tussen knot en kop (de knot ligt achter de kop), witte band ertussen
for (x, y) in []:
    if R[(x, y)] != '#' and is_knot(x, y):
        for dx, dy in ((-1, 0), (0, 1), (-1, 1)):
            q = (x + dx, y + dy)
            if q in R and R[q] != '#' and not is_knot(*q) and not is_stekel(*q):
                R[(x, y)] = '#'
BAND = [(19, 8), (20, 8), (19, 9), (20, 9), (20, 10), (21, 10), (21, 11), (22, 11), (22, 12), (23, 12)]
for i, p in enumerate(BAND):
    if p in R: R[p] = 'w' if i % 3 else 'g'

# ogen: Hitmontops oog (zwart rondje met wit puntje linksboven)
OOG = [".####.", "######", "##ww##", "##ww##", "######", ".####."]
for (ox, oy) in ((2, 16), (11, 16)):
    for j, rij in enumerate(OOG):
        for i, c in enumerate(rij):
            if c != '.': R[(ox + i, oy + j)] = '#' if c == '#' else 'w'
# de V: twee lijnen die tussen de ogen in één punt samenkomen (punt op (8,15))
V = [(5, 11), (6, 12), (7, 13), (8, 14), (9, 15),           # linkerarm
     (16, 10), (15, 11), (14, 11), (13, 12), (12, 13), (11, 14), (10, 14), (9, 15)]
for p in V: R[p] = '3'
# mond: één streepje, uiteinden 1 px hoger (een beetje blij)
for x in range(5, 14): R[(x, 23)] = '3'

def png(R, naam):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for (x, y), c in R.items(): im.putpixel((x, y), KLEUR[c] + (255,))
    im.save(os.path.join(HERE, naam)); return im

im = png(R, 'hoofd_r9.png')
with open(os.path.join(HERE, 'raster_r9.txt'), 'w') as f:
    for y in range(H): f.write(''.join(R.get((x, y), '.') for x in range(W)) + '\n')
# vel
Z = 12; bg = Image.new('RGBA', im.size, (152, 208, 160, 255)); bg.alpha_composite(im)
bron = Image.open(os.path.join(HERE, '../../referenties/hoofd_gemini_concept.webp')).convert('RGB').crop((140, 0, 712, 565)); bron.thumbnail((W * Z, H * Z))
vel = Image.new('RGB', (W * Z * 2 + 200, H * Z + 60), (235, 235, 240)); d = ImageDraw.Draw(vel)
vel.paste(bron, (10, 30)); vel.paste(bg.resize((W * Z, H * Z), Image.NEAREST).convert('RGB'), (W * Z + 30, 30))
vel.paste(bg.convert('RGB'), (W * Z * 2 + 50, 30)); vel.paste(bg.resize((W * 2, H * 2), Image.NEAREST).convert('RGB'), (W * Z * 2 + 50, 80))
d.text((10, 10), 'bron (Gemini, Jordi)', fill=(0, 0, 0)); d.text((W * Z + 30, 10), 'pixels (12x)', fill=(0, 0, 0)); d.text((W * Z * 2 + 50, 10), '1x / 2x', fill=(0, 0, 0))
vel.save(os.path.join(HERE, 'vel_r9.png'))
