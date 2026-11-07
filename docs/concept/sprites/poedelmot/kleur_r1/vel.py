"""vel.png: sprite op 8x naast de samengestelde bron (zelfde uitsnede en schaal), plus 1x en 2x op licht en donker."""
import os, sys
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, 'poedelmot.png')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(H, 'vel.png')
SRC = '/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/referenties/samengesteld.png'
p = Image.open(SP); rgba = p.convert('RGBA'); idx = p.load()
mask = Image.new('L', (64, 64), 0); m = mask.load()
for y in range(64):
    for x in range(64): m[x, y] = 255 if idx[x, y] != 0 else 0
def op(col, s=1):
    b = Image.new('RGBA', (64, 64), col); b.paste(rgba, (0, 0), mask)
    return b.resize((64*s, 64*s), Image.NEAREST)
S = 8
src = Image.open(SRC).convert('RGB'); k = (854-139)/62   # zelfde schaal als silhouet/sil.py
X0, Y0 = 139 - k*1, 150 - k*17
bron = src.crop((int(X0), int(Y0), int(X0+64*k), int(Y0+64*k))).resize((64*S, 64*S), Image.LANCZOS)
W = Image.new('RGB', (64*S*2 + 24 + 2*128 + 24, 64*S + 40), (255, 255, 255)); d = ImageDraw.Draw(W)
W.paste(op((152, 208, 160, 255), S), (0, 24)); d.text((4, 6), 'kleur_r1 (8x)', fill=(0, 0, 0))
W.paste(bron, (64*S + 12, 24)); d.text((64*S + 16, 6), 'bron: samengesteld.png (zelfde uitsnede, 8x)', fill=(0, 0, 0))
x0 = 64*S*2 + 36
d.text((x0, 6), '1x en 2x', fill=(0, 0, 0))
W.paste(op((232, 232, 224, 255)), (x0, 24)); W.paste(op((40, 40, 56, 255)), (x0 + 72, 24))
W.paste(op((232, 232, 224, 255), 2), (x0, 100)); W.paste(op((40, 40, 56, 255), 2), (x0 + 128 + 8, 100))
W.paste(op((248, 248, 248, 255), 2), (x0, 240)); W.paste(op((152, 208, 160, 255), 2), (x0 + 128 + 8, 240))
W.save(OUT)
