"""Vel: meetlijnen op de 3/4-foto en op het poppetje, met de tabel. Draaien na fit_kop.py."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from potoo3d import *
from meten import FOTO, ratios, meet_model
HERE = os.path.dirname(os.path.abspath(__file__))
kp = json.load(open(os.path.join(HERE, 'kp_fit.json')))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
KL = dict(kruin=(220, 40, 40), oog=(40, 120, 220), mond=(200, 60, 200), kop=(40, 160, 60))


def lijnen(d, p, k, ox, oy):
    X = lambda x: ox + x * k; Y = lambda y: oy + y * k
    a, v = p['achter'][0], p['voor'][0]; t, b = p['kruin'][1], p['kaaktip'][1]
    d.rectangle((X(a), Y(t), X(v), Y(b)), outline=KL['kop'], width=2)
    d.line((X(a), Y(p['oog'][1]), X(v), Y(p['oog'][1])), fill=KL['oog'], width=2)
    d.line((X(p['oog'][0]), Y(t), X(p['oog'][0]), Y(b)), fill=KL['oog'], width=1)
    d.line((X(p['mond_l']), Y(p['mond_top']), X(p['mond_r']), Y(p['mond_top'])), fill=KL['mond'], width=2)
    d.line((X(p['mond_l']), Y(p['mond_top']), X(p['mond_l']), Y(b)), fill=KL['mond'], width=1)
    d.line((X(p['mond_r']), Y(p['mond_top']), X(p['mond_r']), Y(b)), fill=KL['mond'], width=1)


foto = Image.open(os.path.join(HERE, '..', 'referenties', 'jordi_great_potoo_bek_open_drieluik.webp')).convert('RGB')
fk = 1.6
fc = foto.crop((120, 0, 380, 260)).resize((int(260 * fk), int(260 * fk)))
m = potoo(0, kp=kp); yaw = 45
pm = meet_model(m, yaw)
v = view(m, yaw).transpose(Image.FLIP_LEFT_RIGHT).resize((416, 416), Image.NEAREST)
S = Image.new('RGB', (416 * 2 + 30 + 420, 470), 'white'); d = ImageDraw.Draw(S)
d.text((10, 6), '3/4-foto met meetlijnen', font=FB, fill=(30, 30, 30))
S.paste(fc, (10, 30)); lijnen(d, {kk: (vv if not isinstance(vv, tuple) else vv) for kk, vv in FOTO.items()}, fk, 10 - 120 * fk, 30)
d.text((436, 6), 'poppetje 45° (gespiegeld) met dezelfde lijnen', font=FB, fill=(30, 30, 30))
S.paste(v, (436, 30)); lijnen(d, pm, 416 / R, 436, 30)
f, r = ratios(FOTO), ratios(pm)
y = 40; d.text((870, 10), 'verhouding            foto   model', font=FB, fill=(30, 30, 30))
for kk in f:
    d.text((870, y), f'{kk[:26]:26s} {f[kk]:.2f}  {r[kk]:.2f}', font=F, fill=(30, 30, 30)); y += 20
S.save(os.path.join(HERE, 'meetlijnen.png'))
