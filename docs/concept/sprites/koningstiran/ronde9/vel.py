"""vel.png ronde 9: kroon + kop 8x van ronde 8 en de 3 varianten, 1x licht/donker, stafkop 10x naast ronde 8 en ronde 7 (A). Draaien vanuit de repo-root."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(HERE)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12); INK = (20, 20, 24)
def on(im, c, size):
    b = Image.new('RGBA', size, c + (255,)); b.alpha_composite(im.resize(size, Image.NEAREST)); return b.convert('RGB')
op = lambda p: Image.open(p).convert('RGBA')
V = [(op(os.path.join(D, 'ronde8/sapa_inca.png')), 'huidig (ronde 8)'),
     (op(os.path.join(HERE, 'v1_een_boog_zwarte_rand.png')), '1: een gouden boog + zwarte randvlekken'),
     (op(os.path.join(HERE, 'v2_twee_bogen_gouden_rand.png')), '2: twee gouden bogen + gouden randvlekken'),
     (op(os.path.join(HERE, 'v3_een_boog_gouden_rand.png')), '3 (eigen keus): een boog + gouden randvlekken')]
kc = (8, 0, 50, 30); Z = 8
cw, ch = (kc[2] - kc[0]) * Z, (kc[3] - kc[1]) * Z
W = Image.new('RGB', (2 * (cw + 20) + 20, 2 * (ch + 110) + 290), (236, 232, 222)); d = ImageDraw.Draw(W)
for i, (im, lab) in enumerate(V):
    x, y = 10 + (i % 2) * (cw + 20), 10 + (i // 2) * (ch + 110)
    W.paste(on(im.crop(kc), (248, 248, 240), (cw, ch)), (x, y)); d.text((x, y + ch + 4), lab, font=F, fill=INK)
    for j, c in enumerate(((248, 248, 240), (40, 44, 52))):
        W.paste(on(im, c, (64, 64)), (x + j * 68, y + ch + 22))
y0 = 10 + 2 * (ch + 110)
tc = (8, 17, 24, 39)
T = [(op(os.path.join(D, 'ronde7/sapa_inca.png')), 'ronde 7 (A)'), (op(os.path.join(D, 'ronde8/sapa_inca.png')), 'ronde 8 (bol)'), (V[3][0], 'ronde 9 (puntig)')]
for i, (im, lab) in enumerate(T):
    W.paste(on(im.crop(tc), (248, 248, 240), (160, 220)), (10 + i * 175, y0)); d.text((10 + i * 175, y0 + 224), 'stafkop 10x ' + lab, font=F, fill=INK)
W.save(os.path.join(HERE, 'vel.png'))
