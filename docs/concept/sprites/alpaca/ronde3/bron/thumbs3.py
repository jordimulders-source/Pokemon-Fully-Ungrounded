"""Drie silhouetten voor ronde 3 (viervoeter): A staand op de handschoenen (gekozen),
B één handschoen omhoog in de dekking, C liggend (kush, zoals een rustende alpaca) met
de handschoenen voor zich. Maakt thumbnails.png.  python3 thumbs3.py <uitmap>"""
import sys, os
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import alpaca3 as A
from shapelib import Canvas

def C():
    c = Canvas(A.R, thresholds=A.TH)
    c.fill(c.m_ellipse(38, 50, 15, 7), 'wol')
    A.puffs(c, [(27, 52, 4), (33, 54, 4), (40, 54, 4), (47, 53, 4), (52, 48, 3.4), (33, 46, 4.2), (41, 45, 4.4), (48, 46, 3.8)], (36, 46, 17, 10))
    A.puffs(c, [(27, 44, 4.2), (25, 39, 4.0)], (24, 40, 8, 9))
    hx, hy = 23, 30
    c.poly([(hx - 5, hy - 4), (hx - 7, hy - 11), (hx - 5, hy - 12), (hx - 3, hy - 5)], 'vacht')
    c.poly([(hx + 4, hy - 5), (hx + 7, hy - 12), (hx + 9, hy - 11), (hx + 7, hy - 4)], 'vacht')
    c.ellipse(hx, hy, 6.5, 5.8, 'vacht'); c.ellipse(hx - 5, hy + 2.6, 3.6, 2.7, 'vacht')
    c.ellipse(hx + 0.5, hy - 7.4, 3.6, 2.4, 'wol'); c.ellipse(hx, hy - 5.4, 5.6, 1.3, 'wol')
    A.glove(c, 15, 55, 4.6); A.glove(c, 24, 57, 4.4, far=True)
    c.outline(); return c.idx

frames = np.array(Image.open(os.path.join(sys.argv[1], 'anim_front.png')))
sil = [('A staand op handschoenen', frames[:64]), ('B handschoen omhoog', frames[64:]), ('C liggend (kush)', C())]
Z = 4
W = 3 * (64 * Z + 8) + 8 + 3 * 72
sheet = Image.new('RGB', (W, 64 * Z + 30), (246, 244, 236)); d = ImageDraw.Draw(sheet)
for i, (n, a) in enumerate(sil):
    s = np.where(a[..., None] > 0, [20, 20, 20, 255], [255, 255, 255, 255]).astype(np.uint8)
    im = Image.fromarray(s, 'RGBA')
    x = 8 + i * (64 * Z + 8)
    d.text((x, 4), n, fill=(120, 20, 20))
    sheet.paste(im.resize((64 * Z, 64 * Z), Image.NEAREST).convert('RGB'), (x, 18))
    x1 = 3 * (64 * Z + 8) + 8 + i * 72
    sheet.paste(im.convert('RGB'), (x1, 18)); d.text((x1, 86), n[0] + ' 1x', fill=(0, 0, 0))
sheet.save(os.path.join(sys.argv[1], 'thumbnails.png')); print('ok')
