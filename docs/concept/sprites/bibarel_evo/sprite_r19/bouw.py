# bouw.py ronde 19: pixelindeling (lijn/vlak) van r17 exact, kleuren van r18.
# Jordi: "je hebt sommige dingen nu overfixed, de lijnen moesten niet andere vormen alleen andere kleuren, verder prima wat je hebt gedaan"
# Dus: geen nieuwe lijnpixels (r18 stap 1, 1b, 3 vervallen); palet zie onder (vlakken = r16); bestaande silhouetrand b -> bijna-zwart K,
# oogrand D -> d (D is nu de donkere gouden lijnkleur; d heeft vrijwel de oude oograndkleur).
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r19/bouw.py
import numpy as np
from PIL import Image, ImageDraw
ch = '.KbcdfSCeLMogWwD'; I = {c: i for i, c in enumerate(ch)}
a = np.asarray(Image.open('sprite_r17/sprite.png')).astype(int); o = a.copy()
PAL17 = np.array(Image.open('sprite_r17/sprite.png').getpalette()[:48]).reshape(16, 3).astype('uint8')
r18 = Image.open('sprite_r18/sprite.png'); PAL18 = np.array(r18.getpalette()[:48]).reshape(16, 3).astype('uint8'); o18 = np.asarray(r18).astype(int)
im16 = Image.open('sprite_r16/sprite.png'); PAL16 = np.array(im16.getpalette()[:48]).reshape(16, 3).astype('uint8'); a16 = np.asarray(im16).astype(int)
# Jordi (correctie): "de kleur hoefde niet per se te veranderen van het geheel, het ging om de overgangen, hoe de sprite eruit zag"
# -> alle vlaktinten = r16 (de r10-kleuren); alleen de lijntinten harder/donkerder, in dezelfde tint als hun eigen vlak,
#    met de verhouding uit de studie (lijn L / basis L: Kangaskhan 0,39, Zapacha 0,45, Dundragoon 0,50, Skinguin 0,35-0,49):
#    b  = lijn van bruin d (188,128,74; h28, L140): (76,46,20) h28, L52 = 0,37 x d   (r16: 96,56,32 h22 L67 = 0,48)
#    D  = lijn van creme C (248,232,200; h40, L234): (148,114,48) h40, L117 = 0,50 x C (r16: 176,136,80... L141 = 0,60)
#    K  = buitenlijn bijna-zwart (40,20,12) zoals Zapacha (r16: 16,16,16)
PAL = PAL16.copy()
PAL[I['b']] = (76, 46, 20); PAL[I['D']] = (148, 114, 48); PAL[I['K']] = (40, 20, 12)
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1)); inb = lambda x, y: 0 <= x < 64 and 0 <= y < 64
rand = [(x, y) for y in range(64) for x in range(64) if a[y, x] == I['b'] and any(not inb(x+dx, y+dy) or a[y+dy, x+dx] == 0 for dx, dy in N4)]
for x, y in rand: o[y, x] = I['K']
oog = [(x, y) for y, x in np.argwhere(a == I['D']) if 14 <= y <= 18 and x >= 18]
for x, y in oog: o[y, x] = I['d']
def save(idx, pad, z=None):
    im = Image.new('P', (64, 64)); im.putpalette(PAL.ravel().tolist() + [0] * 3 * 240)
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad, transparency=0)
    if z: Image.fromarray(PAL[idx]).resize((64 * z, 64 * z), Image.NEAREST).save(pad.replace('.png', f'_{z}x.png'))
save(o, 'sprite_r19/sprite.png', 8)
# ---- bewijs
lijn = lambda x: np.isin(x, [I['K'], I['b']])
assert ((o > 0) == (a > 0)).all(), 'silhouet'
assert (lijn(o) == lijn(a)).all(), 'is-lijn-kaart (K/b) gelijk aan r17'
Dm = np.zeros((64, 64), bool)
for x, y in oog: Dm[y, x] = True
assert ((o == I['D']) == ((a == I['D']) & ~Dm)).all(), 'crème-lijn D: alleen bestaande D (oogrand naar d)'
diff = {(int(x), int(y)) for y, x in np.argwhere(o != a)}
assert diff == set(rand) | set(oog)
print('t.o.v. r16:', int((o != a16).sum()), 'px; pixels gewijzigd t.o.v. r17:', len(diff), '(silhouetrand b->K', len(rand), ', oogrand D->d', len(oog), ') ; t.o.v. r18:', int((o != o18).sum()))
# ---- vel: r19 | r18 | r17 8x ; 1x licht/donker
BG = (152, 208, 160)
def rgb(idx, pal, bg=BG):
    t = np.zeros((64, 64, 3), 'uint8'); t[:] = bg; m = idx > 0; t[m] = pal[idx[m]]; return Image.fromarray(t)
items = [('r19', o, PAL), ('r18', o18, PAL18), ('r17', a, PAL17)]
V = Image.new('RGB', (3 * 522 + 10, 22 + 512 + 34 + 64 + 34 + 512 + 10), 'white'); d = ImageDraw.Draw(V)
for i, (t, idx, p) in enumerate(items):
    V.paste(rgb(idx, p).resize((512, 512), Image.NEAREST), (10 + i * 522, 22)); d.text((10 + i * 522, 6), t + ' 8x', fill='black')
y = 22 + 512 + 34; d.text((10, y - 14), '1x licht / donker: r19 r18 r17', fill='black')
for j, bg in enumerate([(248, 248, 248), (24, 24, 32)]):
    for i, (t, idx, p) in enumerate(items): V.paste(rgb(idx, p, bg), (10 + j * 240 + i * 70, y))
y += 64 + 34
d.text((10, y - 14), 'r19 | r16 8x: vlakkleuren gelijk, alleen overgangen (r17) en lijntinten anders', fill='black')
for i, (idx, p) in enumerate([(o, PAL), (a16, PAL16)]): V.paste(rgb(idx, p).resize((512, 512), Image.NEAREST), (10 + i * 522, y))
V.save('sprite_r19/vel.png')
vlak = [c for c in ch[1:] if c not in 'bDK']
assert all((PAL[I[c]] == PAL16[I[c]]).all() for c in vlak), 'vlaktinten gelijk aan r16'
print('vlaktinten = r16:', vlak)
