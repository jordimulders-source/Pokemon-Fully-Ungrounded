"""Snel kijkvel: sprite 8x met raster | C3-render | sprite 1x. python3.11 kijk.py [png] [uit]"""
import sys
from PIL import Image, ImageDraw
fn = sys.argv[1] if len(sys.argv) > 1 else 'picapau_evo.png'
uit = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/4639ce03-6e5e-57a6-83bc-e54e06dafbeb/scratchpad/k.png'
im = Image.open(fn).convert('RGBA')
v = Image.new('RGBA', (512 * 2 + 140, 530), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
v.alpha_composite(im.resize((512, 512), Image.NEAREST), (0, 0))
for i in range(0, 65, 8):
    d.line([(i * 8, 0), (i * 8, 512)], fill=(200, 200, 255)); d.line([(0, i * 8), (512, i * 8)], fill=(200, 200, 255))
v.alpha_composite(Image.open('../blender/r3/C3_8x.png').convert('RGBA'), (520, 0))
v.alpha_composite(im, (1040, 10)); v.alpha_composite(im.resize((128, 128), Image.NEAREST), (1036, 90))
v.save(uit)
