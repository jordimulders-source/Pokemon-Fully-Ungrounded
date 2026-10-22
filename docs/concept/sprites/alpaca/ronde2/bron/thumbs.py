"""Drie snelle silhouetten (ronde 2, 'Wolbokser'): A viervoeter in dekking, B rechtop
in bokshouding, C zittende wolbal met handschoenen. Maakt thumbnails.png.
  python3 thumbs.py <uitmap>"""
import sys, os
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from PIL import Image, ImageDraw
from shapelib import Canvas

R = {'w': [1, 2, 3, 4], 'f': [5, 6, 7], 'r': [8, 9, 10]}

def ears(c, hx, hy):
    c.poly([(hx - 6, hy - 3), (hx - 9, hy - 12), (hx - 7, hy - 14), (hx - 4, hy - 6)], 'f')
    c.poly([(hx + 6, hy - 6), (hx + 9, hy - 14), (hx + 11, hy - 12), (hx + 8, hy - 3)], 'f')
    c.ellipse(hx - 8, hy - 14, 2, 2, 'r'); c.ellipse(hx + 10, hy - 14, 2, 2, 'r')

def head(c, hx, hy, neck=6):
    m, _ = c.m_cloud(hx + 2, hy + 8, 7, neck, 7, 3); c.fill(m, 'w')   # wollen hals
    ears(c, hx, hy)
    c.ellipse(hx, hy, 6, 6, 'f')
    c.ellipse(hx - 5, hy + 3, 4, 3, 'f')           # snoetje
    c.ellipse(hx + 1, hy - 9, 5, 4, 'w')           # bolhoedkuif (koepel)
    c.ellipse(hx + 1, hy - 5, 9, 2, 'w')           # rand

def A():
    c = Canvas(R)
    m, _ = c.m_cloud(38, 42, 16, 12, 9, 5); c.fill(m, 'w')
    c.ellipse(46, 56, 2, 3, 'f'); c.ellipse(53, 54, 2, 3, 'f')
    c.poly([(19, 40), (24, 40), (22, 50), (17, 50)], 'f'); c.ellipse(16, 51, 5, 5, 'r')
    c.poly([(28, 44), (32, 44), (31, 52), (27, 52)], 'f'); c.ellipse(28, 55, 5, 4, 'r')
    head(c, 22, 25)
    return c.finish()

def B():
    c = Canvas(R)
    c.ellipse(29, 58, 3, 3, 'f'); c.ellipse(41, 58, 3, 3, 'f')       # pootjes
    m, _ = c.m_cloud(36, 44, 13, 12, 9, 5, a0=0.3); c.fill(m, 'w')
    head(c, 30, 24)
    c.ellipse(42, 32, 5, 5, 'r')                                     # achterste handschoen bij de wang
    c.poly([(30, 40), (32, 37), (22, 34), (19, 38)], 'f'); c.ellipse(15, 37, 6, 6, 'r')  # jab
    return c.finish()

def C():
    c = Canvas(R)
    m, _ = c.m_cloud(33, 45, 17, 14, 10, 5); c.fill(m, 'w')
    head(c, 28, 25)
    c.ellipse(17, 52, 6, 5, 'r'); c.ellipse(45, 54, 6, 5, 'r')
    return c.finish()

out = sys.argv[1] if len(sys.argv) > 1 else '.'
sil = []
for name, f in (('A viervoeter', A), ('B rechtop', B), ('C wolbal', C)):
    a = f(); s = np.where(a[..., None] > 0, [20, 20, 20, 255], [0, 0, 0, 0]).astype(np.uint8)
    sil.append((name, Image.fromarray(s, 'RGBA')))
Z = 4
W = len(sil) * (64 * Z + 8) + 8 + 3 * 72
sheet = Image.new('RGB', (W, 64 * Z + 30), (246, 244, 236)); d = ImageDraw.Draw(sheet)
for i, (n, im) in enumerate(sil):
    x = 8 + i * (64 * Z + 8)
    d.text((x, 4), n, fill=(120, 20, 20))
    bg = Image.new('RGBA', (64 * Z, 64 * Z), (255, 255, 255, 255)); bg.alpha_composite(im.resize((64 * Z, 64 * Z), Image.NEAREST))
    sheet.paste(bg.convert('RGB'), (x, 18))
    x1 = len(sil) * (64 * Z + 8) + 8 + i * 72
    bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(im)
    sheet.paste(bg.convert('RGB'), (x1, 18)); d.text((x1, 86), n[0] + ' 1x', fill=(0, 0, 0))
sheet.save(os.path.join(out, 'thumbnails.png')); print('ok')
