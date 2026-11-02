# 7x-uitsneden van patronen (Game Freak) voor de patroonstudie
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import importlib.util
spec = importlib.util.spec_from_file_location('v', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vellen.py'))
src = open(spec.origin).read().split("vel(['NACHTAAP'")[0]
g = {'__file__': spec.origin}; exec(src, g); laad = g['laad']
crops = {'NACHTAAP': (16, 22, 52, 46), 'zigzagoon': (14, 14, 60, 50), 'seviper': (4, 4, 50, 50), 'raikou': (4, 20, 50, 60),
         'spinda': (10, 4, 46, 40), 'sigilyph': (14, 20, 44, 50), 'liepard': (10, 20, 50, 50), 'linoone': (20, 10, 60, 50), 'furret': (18, 8, 58, 48)}
S = 7; C = 46 * S
W = Image.new('RGB', (3 * C, 3 * C), (255, 255, 255))
for i, (n, c) in enumerate(crops.items()):
    s = laad(n); b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); b.alpha_composite(s)
    cc = b.crop(c).convert('RGB'); cc = cc.resize((cc.size[0] * S, cc.size[1] * S), Image.NEAREST)
    W.paste(cc, ((i % 3) * C, (i // 3) * C))
W.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patroon_crops_7x.png'))
