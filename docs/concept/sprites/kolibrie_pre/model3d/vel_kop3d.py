"""Vel: model ronde 2 (ronde kop in 3D) in drie kopstanden naast Taillow en Starly, op 4x en 1x. python3 vel_kop3d.py"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import model as M, kop3d as K
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
BG = (236, 234, 228); INK = (40, 36, 50); GR = (95, 90, 105)
def sprite(p):
    im = Image.open(p); a = np.array(im.crop((0, 0, 64, 64))) != 0
    rgba = np.array(im.convert('RGBA').crop((0, 0, 64, 64))); rgba[..., 3] = a * 255
    return Image.fromarray(rgba)
def bg(im, k):
    v = Image.new('RGB', im.size, BG); v.paste(im, (0, 0), im); return v.resize((im.width * k, im.height * k), Image.NEAREST)
STANDEN = [('K1', 15, 14), ('K2', 25, 15), ('K3', 35, 17)]
cel = 256
V = Image.new('RGB', (24 + 5 * (cel + 14), 52 + cel + 40 + 110), 'white'); d = ImageDraw.Draw(V)
d.text((24, 14), 'Kolibrie pre-evo, model ronde 2: lijf B2, kop als ronde bol met het gezicht naar de kijker', font=FB, fill=INK)
ref = [('Taillow', sprite('../../../../../graphics/pokemon/taillow/anim_front.png')), ('Starly', sprite('../../../../../graphics/pokemon/starly/anim_front.png'))]
y = 48; x = 24
for naam, im in ref:
    V.paste(bg(im, 4), (x, y)); d.text((x, y + cel + 4), naam, font=F, fill=GR)
    V.paste(bg(im, 1), (x, y + cel + 30)); x += cel + 14
for naam, h, p in STANDEN:
    img, al = K.render(h, p)
    rgba = Image.fromarray(np.dstack([img, al * 255]).astype(np.uint8))
    V.paste(bg(rgba.resize((cel, cel), Image.LANCZOS), 1), (x, y))
    d.text((x + 6, y + 4), naam, font=FB, fill=INK)
    d.text((x, y + cel + 4), f'kop {32 + h} gr · {M.naar64(al).sum()} px', font=F, fill=GR)
    V.paste(bg(rgba.resize((64, 64), Image.LANCZOS), 1), (x, y + cel + 30))
    sil = Image.fromarray(np.where(M.naar64(al), 40, 236).astype(np.uint8)).convert('RGB')
    V.paste(sil, (x + 74, y + cel + 30))
    x += cel + 14
d.text((24, y + cel + 100), 'Onder elk: 1x (render verkleind) en het silhouet dat eruit komt. Oog = Starly-oog op de plek die de kop geeft (nu op de voorkant, niet de zijkant).', font=F, fill=GR)
V.save('vel_kop3d.png')
