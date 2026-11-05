"""Vergelijkvel: render naast de (gespiegelde) bronfoto. python3 vergelijk.py uit.png render1 foto1:crop:spiegel ..."""
import sys
from PIL import Image, ImageOps
REF = '../referenties/'
uit = sys.argv[1]; paren = sys.argv[2:]
tegels = []
for i in range(0, len(paren), 2):
    r = Image.open(paren[i]).convert('RGBA'); bg = Image.new('RGBA', r.size, (70, 90, 70, 255)); bg.alpha_composite(r)
    f, crop, sp = paren[i + 1].split(':')
    ph = Image.open(REF + f).convert('RGBA').crop(tuple(int(v) for v in crop.split(',')))
    if sp == '1': ph = ImageOps.mirror(ph)
    ph = ph.resize((int(ph.width * 600 / ph.height), 600))
    tegels += [bg.convert('RGB').resize((600, 600)), ph.convert('RGB')]
W = sum(t.width for t in tegels); o = Image.new('RGB', (W, 600)); x = 0
for t in tegels: o.paste(t, (x, 0)); x += t.width
o.save(uit)
