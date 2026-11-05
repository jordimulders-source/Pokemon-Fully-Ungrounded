"""Diff ronde 2b t.o.v. ronde 2: in de halszone (x16-33, y12-27, zonder kleding) en 0 erbuiten."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
a = Image.open(os.path.join(OUT, '../ronde2/lama.png')); b = Image.open(os.path.join(OUT, 'lama.png'))
ch = [(x, y) for y in range(64) for x in range(64) if a.getpixel((x, y)) != b.getpixel((x, y))]
inz = [p for p in ch if 16 <= p[0] <= 33 and 12 <= p[1] <= 27]
print('gewijzigd in de halszone:', len(inz), '| buiten de zone:', len(ch) - len(inz))
