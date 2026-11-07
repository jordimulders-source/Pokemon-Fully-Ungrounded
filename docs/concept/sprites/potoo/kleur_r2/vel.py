"""vel.png: sprite 8x | model op 8x | 1x op licht en donker (+ vorige ronde 8x als die er is)."""
import os, sys, json
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); P = '/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
k = json.load(open(P + 'gereedschap/kader.json')); X0, Y0, s = k['x0'], k['y0'], k['s']
sp = Image.open(os.path.join(H, 'potoo.png')).convert('RGBA')
def op(bgc, im, z):
    b = Image.new('RGBA', im.size, bgc); b.alpha_composite(im); return b.convert('RGB').resize((im.width * z, im.height * z), Image.NEAREST)
m = Image.open(P + 'model/model_lijf_30.png'); mb = Image.new('RGBA', m.size, (255, 255, 255, 255)); mb.alpha_composite(m)
m8 = mb.convert('RGB').crop((int(X0), int(Y0), int(X0 + 64 * s), int(Y0 + 64 * s))).resize((512, 512), Image.LANCZOS)
prev = sys.argv[1] if len(sys.argv) > 1 else None
cols = [op((255, 255, 255, 255), sp, 8), m8] + ([op((255, 255, 255, 255), Image.open(prev).convert('RGBA'), 8)] if prev else [])
W = 512 * len(cols) + 8 * (len(cols) - 1); o = Image.new('RGB', (W, 512 + 8 + 128), (200, 200, 200))
for i, c in enumerate(cols): o.paste(c, (i * 520, 0))
o.paste(op((255, 255, 255, 255), sp, 2), (0, 520)); o.paste(op((40, 40, 48, 255), sp, 2), (136, 520))
o.paste(op((255, 255, 255, 255), sp, 1), (272, 520)); o.paste(op((40, 40, 48, 255), sp, 1), (344, 520))
mm = mb.convert('RGB').crop((int(X0), int(Y0), int(X0 + 64 * s), int(Y0 + 64 * s))).resize((64, 64), Image.LANCZOS)
o.paste(mm.resize((128, 128), Image.NEAREST), (520, 520)); o.paste(mm, (656, 520))
o.save(os.path.join(H, 'vel.png'))
