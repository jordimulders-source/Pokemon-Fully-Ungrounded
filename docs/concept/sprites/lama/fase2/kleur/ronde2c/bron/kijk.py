"""Kijkvel (alleen kijken): 2b en 2c op 1x, 3x en 6x, licht en donker."""
import sys
from PIL import Image
A = Image.open('ronde2b/lama.png').convert('RGBA'); B = Image.open('ronde2c/lama.png').convert('RGBA')
W = Image.new('RGBA', (64*(1+1+3+3+6+6)+80, 64*6*2+20), (240, 238, 230, 255))
for row, bg in enumerate([(240, 238, 230, 255), (40, 40, 56, 255)]):
    y = row * (64*6+10)
    W.paste(Image.new('RGBA', (W.width, 64*6), bg), (0, y))
    x = 4
    for s in (1, 1, 3, 3, 6, 6):
        pass
    for im, s in ((A, 1), (B, 1), (A, 3), (B, 3), (A, 6), (B, 6)):
        b = im.resize((64*s, 64*s), Image.NEAREST); W.paste(b, (x, y), b); x += 64*s + 12
W.save(sys.argv[1])
