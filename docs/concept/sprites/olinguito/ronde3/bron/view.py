"""Zoomweergave van anim_front.png (beide frames naast elkaar) voor eigen controle.
python3 view.py <anim_front.png> <uit.png> [zoom]"""
import sys
import numpy as np
from PIL import Image
im = Image.open(sys.argv[1]); z = int(sys.argv[3]) if len(sys.argv) > 3 else 6
a = np.array(im); p = im.getpalette()[:48]
rgb = np.array(p, np.uint8).reshape(16, 3)[a]; rgb[a == 0] = (205, 222, 205)
f = Image.fromarray(rgb)
w = Image.new('RGB', (128 * z + 16 + 128 + 8, 64 * z), (255, 255, 255))
w.paste(f.crop((0, 0, 64, 64)).resize((64 * z, 64 * z), Image.NEAREST), (0, 0))
w.paste(f.crop((0, 64, 64, 128)).resize((64 * z, 64 * z), Image.NEAREST), (64 * z + 8, 0))
w.paste(f.crop((0, 0, 64, 64)), (128 * z + 16, 0)); w.paste(f.crop((0, 64, 64, 128)), (128 * z + 16 + 64, 0))
w.save(sys.argv[2])
