"""Vel: nieuw silhouet (3/4) op 4x en 1x naast de silhouetten van Taillow, Starly, Pidgey, Natu, Fletchling en het oude
profielsilhouet (maker/silhouet_r2), elk op 3x en 1x; onderste rij de echte sprites in kleur (houding)."""
from PIL import Image, ImageDraw, ImageFont
G = '/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
BG, INK = (236, 236, 230), (40, 30, 60)
def sil_txt(p): return [[c == '#' for c in l.rstrip('\n')] for l in open(p)][:64]
def sil_png(n):
    im = Image.open(G + n + '/anim_front.png'); a = im.load()
    return [[a[x, y] != 0 for x in range(64)] for y in range(64)]
def kleur(n):
    im = Image.open(G + n + '/anim_front.png').crop((0, 0, 64, 64)); a = im.load(); c = im.convert('RGB'); b = c.load()
    for y in range(64):
        for x in range(64):
            if a[x, y] == 0: b[x, y] = BG
    return c
def img(M):
    im = Image.new('RGB', (64, 64), BG); p = im.load()
    for y in range(64):
        for x in range(64):
            if M[y][x]: p[x, y] = INK
    return im
nieuw = img(sil_txt('silhouet.txt'))
refs = [('Taillow', img(sil_png('taillow')), kleur('taillow')), ('Starly', img(sil_png('starly')), kleur('starly')),
        ('Pidgey', img(sil_png('pidgey')), kleur('pidgey')), ('Natu', img(sil_png('natu')), kleur('natu')),
        ('Fletchling', img(sil_png('fletchling')), kleur('fletchling')),
        ('oud profiel r2', img(sil_txt('../../maker/silhouet_r2/silhouet.txt')), None)]
W = 256 + 30 + 7 * 200 + 20
out = Image.new('RGB', (W, 30 + 256 + 40 + 200 + 90), 'white'); d = ImageDraw.Draw(out)
d.text((10, 6), 'Kolibrie pre-evo, silhouet maker3 r1 (3/4, foto 5 gespiegeld): 4x en 1x, naast echte Gen 3/4-vogels op 3x en 1x', fill='black', font=FB)
out.paste(nieuw.resize((256, 256), Image.NEAREST), (10, 30)); out.paste(nieuw, (10, 296))
out.paste(nieuw.resize((128, 128), Image.NEAREST), (90, 296))
d.text((10, 430), 'nieuw: 4x, 1x, 2x', fill='black', font=F)
x = 296
cols = [('nieuw (3x)', nieuw, None)] + refs
for name, s, k in cols:
    out.paste(s.resize((192, 192), Image.NEAREST), (x, 30)); out.paste(s, (x, 228))
    if k is not None: out.paste(k.resize((192, 192), Image.NEAREST), (x, 300)); out.paste(k, (x + 128, 300 + 192 - 64))
    d.text((x, 498), name, fill='black', font=FB); x += 200
out.save('vel.png')
