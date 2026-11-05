"""Legt het zijaanzicht van het poppetje (gespiegeld) over de zijfoto, met de omrekening uit LM."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from potoo3d import *
m = potoo(0)
x0, x1, y0, y1 = bbox(m, 0, 0)
scale = R * (232 / 256) / max(x1 - x0, y1 - y0)
v = shade(*render(m, 0, 0, scale, ((x0 + x1) / 2, (y0 + y1) / 2))).transpose(Image.FLIP_LEFT_RIGHT)
foto = Image.open(os.path.join(HERE, '..', 'referenties', 'jordi_great_potoo_vooroverhangend_bek_open.webp')).convert('RGB')
k = (1 / 0.3) / (scale * 256 / R)
vv = v.resize((int(256 * k), int(256 * k)))
cx, cy = -((x0 + x1) / 2) / 0.3 + 250, -((y0 + y1) / 2) / 0.3 + 300
o = foto.convert('RGBA')
mask = vv.convert('L').point(lambda p: 110 if p < 252 else 0)
o.paste(Image.new('RGBA', vv.size, (140, 90, 255, 255)), (int(cx - vv.width / 2), int(cy - vv.height / 2)), mask)
S = Image.new('RGB', (foto.width * 2 + 10, foto.height), 'white')
S.paste(foto, (0, 0)); S.paste(o.convert('RGB'), (foto.width + 10, 0))
S.save(os.path.join(HERE, 'overlay_zijfoto.png'))
