"""kapgrens_8x.png: de drie kapgrens-varianten (hoger | zoals r7b | lager), koppen op 8x en hele sprite op 1x, licht en donker."""
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
def on(p, bg=(236, 236, 230)):
    im = Image.open(p); c = im.crop((0, 0, 64, 64)); a = c.convert('RGBA'); px = a.load(); idx = c.load()
    for y in range(64):
        for x in range(64):
            if idx[x, y] == 0: px[x, y] = (0, 0, 0, 0)
    b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(a); return b.convert('RGB')
vs = [('kapgrens 1 px hoger', 'kolibrie_pre_hoger.png'), ('kapgrens zoals r7b (r8)', 'kolibrie_pre.png'), ('kapgrens 1 px lager', 'kolibrie_pre_lager.png')]
Z, box = 8, (8, 7, 36, 26)
W, H = (box[2] - box[0]) * Z, (box[3] - box[1]) * Z
out = Image.new('RGB', (3 * (W + 20) + 20, H + 40 + 2 * 74 + 20), 'white'); d = ImageDraw.Draw(out)
for i, (n, p) in enumerate(vs):
    x = 20 + i * (W + 20); out.paste(on(p).crop(box).resize((W, H), Image.NEAREST), (x, 28)); d.text((x, 6), n, fill='black', font=F)
    for j, bg in enumerate(((236, 236, 230), (44, 44, 52))): out.paste(on(p, bg), (x + W // 2 - 32, H + 40 + j * 74))
out.save('kapgrens_8x.png')
