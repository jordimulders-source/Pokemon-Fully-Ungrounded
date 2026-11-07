"""Keurvel silhouet ronde 3: tak-foto, vilt (hoofd/gezicht/oren), poppetje 5b, omtrek over het poppetje, silhouet en delen;
vak hoofd-gezicht-oren naast de vilt-foto; 1x en 2x naast tak-foto, poppetje, Butterfree en Venomoth (licht/donker).
Draaien: python3 docs/concept/sprites/poedelmot/silhouet/ronde3/keurvel.py (na silhouet.py)"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../../..'))
REF = os.path.join(HERE, '../../referenties')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
DY = 4   # silhouet.py schoof alles 4 px omlaag

S = np.array([[c == '#' for c in l.strip()] for l in open(os.path.join(HERE, 'ronde3.txt'))])
sil = Image.fromarray(np.dstack([np.zeros((64, 64, 3), np.uint8), (S * 255).astype(np.uint8)]), 'RGBA')
delen = Image.open(os.path.join(HERE, 'delen_8x.png')).convert('RGB')

def gen3(n):
    p = Image.open(os.path.join(ROOT, 'graphics/pokemon', n, 'anim_front.png')); idx = np.array(p)[:64, :64]
    rgba = np.array(p.convert('RGBA'))[:64, :64]; rgba[idx == 0, 3] = 0
    return Image.fromarray(rgba)
pop1 = Image.open(os.path.join(HERE, '../../poppetje/ronde5b/poppetje_45_1x.png')).convert('RGBA')
pop1 = Image.fromarray(np.roll(np.array(pop1), DY, 0))   # zelfde plek als het silhouet
foto = Image.open(os.path.join(REF, 'foto_tak_katoen.webp')).convert('RGB')
vilt = Image.open(os.path.join(REF, 'vilt_hoofd_gezicht_oren.png')).convert('RGB')
def wit(im, bg=(235, 235, 235)):
    b = Image.new('RGB', im.size, bg); b.paste(im, (0, 0), im if im.mode == 'RGBA' else None); return b

# onderlaag (poppetje 8x) met de omtrek van het silhouet in rood
ond = Image.open(os.path.join(HERE, 'onderlaag_512.png')).convert('RGB')
ond = Image.fromarray(np.roll(np.array(ond), DY * 8, 0))
o = np.array(ond)
rand = S & ~(np.roll(S, 1, 0) & np.roll(S, -1, 0) & np.roll(S, 1, 1) & np.roll(S, -1, 1))
for y, x in zip(*np.nonzero(rand)):
    o[y * 8:y * 8 + 8, x * 8:x * 8 + 8] = (o[y * 8:y * 8 + 8, x * 8:x * 8 + 8] * 0.35 + np.array((230, 30, 30)) * 0.65)
omtrek = Image.fromarray(o.astype(np.uint8))

W = 1340; out = Image.new('RGB', (W, 1230), 'white'); d = ImageDraw.Draw(out)
d.text((12, 10), 'Poedelmot silhouet ronde 3 (64x64): ronde 2 + vilt-oren, hoorntje weg, inkepingen lijf/vleugels, ronde pompons, verre voorpoot', font=FB, fill=(20, 20, 20))
y = 40; x = 12
rij = [(foto.resize((256, 256)), 'tak-foto (wol, pose, poten)'),
       (vilt.crop((60, 100, 720, 430)).resize((256, 128)), 'vilt (hoofd, gezicht, oren)'),
       (ond.resize((256, 256)), 'poppetje ronde 5b (8x -> 4x)'),
       (omtrek.resize((256, 256), Image.NEAREST), 'omtrek silhouet over poppetje'),
       (wit(sil).resize((256, 256), Image.NEAREST), 'silhouet 4x')]
for im, t in rij:
    out.paste(im, (x, y)); d.text((x, y + 260), t, font=F, fill=(60, 60, 60)); x += 264
y = 330
d.text((12, y), 'Hoofd, gezicht en oren naast de vilt-foto (Jordi 6 nov: "dit mag als inspiratie voor hoofd, gezicht en oren"; ogen "zoals in deze foto")', font=F, fill=(0, 0, 0))
vk = vilt.crop((200, 120, 580, 300)).resize((418, 198))
dk = delen.crop((0, 14 * 8, 50 * 8, 40 * 8)).resize((380, 198), Image.NEAREST)
sk = wit(sil).resize((512, 512), Image.NEAREST).crop((0, 14 * 8, 50 * 8, 40 * 8)).resize((380, 198), Image.NEAREST)
out.paste(vk, (12, y + 22)); out.paste(dk, (440, y + 22)); out.paste(sk, (830, y + 22))
d.text((12, y + 224), 'vilt-foto', font=F, fill=(60, 60, 60))
d.text((440, y + 224), 'delen: kop blauw, oren bruin, ogen rood', font=F, fill=(60, 60, 60))
d.text((830, y + 224), 'silhouet (zelfde uitsnede)', font=F, fill=(60, 60, 60))
y = 590
d.text((12, y), 'Delen 8x (groen = nabije poten, lichtgroen = verre poten)                 Poten: tak-foto-uitsnede', font=F, fill=(0, 0, 0))
out.paste(delen.resize((300, 300), Image.NEAREST), (12, y + 22))
out.paste(foto.crop((540, 880, 1280, 1330)).resize((380, 231)), (330, y + 22))
x0 = 730
d.text((x0, y), '1x en 2x, licht / donker:', font=F, fill=(0, 0, 0))
items = [('tak-foto', foto.resize((64, 64), Image.LANCZOS).convert('RGBA')), ('poppetje', pop1), ('silhouet', sil),
         ('butterfree', gen3('butterfree')), ('venomoth', gen3('venomoth'))]
for j, (t, im) in enumerate(items):
    xx = x0 + j * 120
    d.text((xx, y + 22), t, font=F, fill=(60, 60, 60))
    for k, bg in enumerate(((235, 235, 235), (60, 60, 70))):
        out.paste(wit(im, bg), (xx, y + 42 + k * 70))
    out.paste(wit(im).resize((128, 128), Image.NEAREST).crop((0, 0, 112, 128)), (xx, y + 186))
for j, n in enumerate(('butterfree', 'venomoth')):   # silhouetten van de referenties
    a = np.array(gen3(n))[..., 3] > 0
    im = Image.fromarray(np.dstack([np.zeros((64, 64, 3), np.uint8), (a * 255).astype(np.uint8)]), 'RGBA')
    out.paste(wit(im), (x0 + (3 + j) * 120, y + 322))
d.text((x0, y + 322 + 66), 'onder: silhouetten Butterfree / Venomoth op 1x', font=F, fill=(60, 60, 60))
# vak: omtrek op 1x (en 3x) naast Butterfree en Venomoth
y = 1010
d.text((12, y), 'Omtrek op 1x en 3x: poedelmot ronde 3, Butterfree, Venomoth (alleen de buitenrand, 1 px)', font=F, fill=(0, 0, 0))
def omtrek_van(a):
    r = a & ~(np.roll(a, 1, 0) & np.roll(a, -1, 0) & np.roll(a, 1, 1) & np.roll(a, -1, 1))
    im = np.full((64, 64, 3), 245, np.uint8); im[r] = (20, 20, 20); return Image.fromarray(im)
for j, a in enumerate([S] + [np.array(gen3(n))[..., 3] > 0 for n in ('butterfree', 'venomoth')]):
    o1 = omtrek_van(a); xx = 12 + j * 280
    out.paste(o1, (xx, y + 24)); out.paste(o1.resize((192, 192), Image.NEAREST), (xx + 74, y + 24))
out.save(os.path.join(HERE, 'vel.png')); print('vel.png', out.size)
