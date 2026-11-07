"""Vel silhouet fase 3 ronde 3: onderlaag | ronde 3 4x | ronde 3 (omtrek) over de onderlaag | ronde 3 1x, met daaronder
Gen 3-silhouetten van zware viervoeters (1x en 2x) het silhouet van fase 2 en ronde 2. Draaien: python3 vel_ronde3.py -> vel_ronde3.png;
schrijft ook ronde3_1x.png (zwart op wit)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '../../../../../..')
S = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, 'ronde3.txt')) if l.strip()])
M = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, 'model50.txt')) if l.strip()])
a = np.zeros((64, 64), np.uint8) + 255; a[S] = 0; Image.fromarray(a).save(os.path.join(HERE, 'ronde3_1x.png'))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
def sil(m, bg=(250, 250, 250)):
    b = np.full(m.shape + (3,), bg, np.uint8); b[m] = (38, 30, 48); return Image.fromarray(b)
def outline(img, m, s):
    dd = ImageDraw.Draw(img)
    for y, x in np.argwhere(m):
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < 64 and 0 <= xx < 64 and m[yy, xx]: continue
            X, Y = x * s, y * s
            if dy: dd.line([(X, Y + (s if dy > 0 else 0)), (X + s, Y + (s if dy > 0 else 0))], fill=(120, 0, 200), width=1)
            else: dd.line([(X + (s if dx > 0 else 0), Y), (X + (s if dx > 0 else 0), Y + s)], fill=(120, 0, 200), width=1)
def mask(path, frame=True):
    im = Image.open(path); arr = np.array(im)
    if frame: arr = arr[:64]
    return arr != 0 if im.mode == 'P' else arr[..., 3] > 0
W = Image.new('RGB', (1490, 520), (250, 250, 250)); d = ImageDraw.Draw(W)
d.text((10, 6), f'Lama fase 3, silhouet ronde 3, spritebron (kop 1,2x, bombín 1,3x links, vlechten 1,3x naar buiten) ({int(S.sum())} px; model {int(M.sum())} px; +{int((S & ~M).sum())} / -{int((M & ~S).sum())} px, alle <= 1 px)', fill=0, font=F)
U = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGB')
W.paste(U, (10, 30)); d.text((10, 290), 'onderlaag (spritebron K3)', fill=0, font=F)
W.paste(sil(S).resize((256, 256), Image.NEAREST), (280, 30)); d.rectangle([280, 30, 535, 285], outline=(210, 210, 210)); d.text((280, 290), 'ronde 3, 4x', fill=0, font=F)
u = U.copy(); outline(u, S, 4); W.paste(u, (550, 30)); d.text((550, 290), 'ronde 3 (omtrek) over de onderlaag', fill=0, font=F)
W.paste(sil(S), (820, 60)); W.paste(sil(S, (120, 160, 120)), (900, 60)); d.text((820, 130), 'ronde 3, 1x', fill=0, font=F)
refs = [('camerupt', 'graphics/pokemon/camerupt/anim_front_gba.png', True), ('tauros', 'graphics/pokemon/tauros/anim_front_gba.png', True),
        ('donphan', 'graphics/pokemon/donphan/anim_front_gba.png', True), ('rhyhorn', 'graphics/pokemon/rhyhorn/anim_front_gba.png', True),
        ('lama fase 2', 'docs/concept/sprites/lama/fase2/af/lama.png', False)]
x = 10
for n, p, fr in refs:
    m = mask(os.path.join(ROOT, p), fr)
    W.paste(sil(m), (x, 330)); W.paste(sil(m).resize((128, 128), Image.NEAREST), (x + 70, 330))
    d.text((x, 465), f'{n} ({int(m.sum())} px)', fill=0, font=F); x += 205
R1 = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, 'ronde2.txt')) if l.strip()])
W.paste(sil(R1), (x, 330)); W.paste(sil(R1).resize((128, 128), Image.NEAREST), (x + 70, 330)); d.text((x, 465), f'fase 3 r2 ({int(R1.sum())} px)', fill=0, font=F); x += 205
W.paste(sil(S), (x, 330)); W.paste(sil(S).resize((128, 128), Image.NEAREST), (x + 70, 330)); d.text((x, 465), f'fase 3 r3 ({int(S.sum())} px)', fill=0, font=F)
d.text((10, 490), 'onder: Gen 3-silhouetten (1x en 2x) van zware viervoeters, het silhouet van fase 2, ronde 2 (W3, goedgekeurd) en ronde 3 (spritebron) op dezelfde schaal', fill=(90, 90, 90), font=F)
W.save(os.path.join(HERE, 'vel_ronde3.png'))
