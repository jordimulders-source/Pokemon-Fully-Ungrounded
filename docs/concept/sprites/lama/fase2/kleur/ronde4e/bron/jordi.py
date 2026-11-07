"""Kijkvel voor Jordi (zelfde opbouw als ronde4c/jordi_4c.png): 4x, kop+hals 8x en 1x, op wit."""
import os
from PIL import Image
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = Image.open(os.path.join(OUT, 'lama.png')).convert('RGBA')
s.putdata([(0, 0, 0, 0) if p[:3] == (152, 208, 160) else p for p in s.getdata()])
w = Image.new('RGBA', s.size, (255, 255, 255, 255)); w.alpha_composite(s)
big = w.resize((256, 256), Image.NEAREST); kop = w.crop((8, 4, 34, 34)).resize((208, 240), Image.NEAREST)
c = Image.new('RGB', (256 + 208 + 64 + 40, 256), (255, 255, 255))
c.paste(big, (0, 0)); c.paste(kop, (266, 8)); c.paste(w, (266 + 218, 96))
c.save(os.path.join(OUT, 'jordi_4e.png'))
