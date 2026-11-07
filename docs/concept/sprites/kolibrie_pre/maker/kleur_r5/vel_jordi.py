"""Vel voor Jordi: r5 (= r4 + 29 px uit de eindkeuring) 4x en 1x op licht en donker, naast Gen 3-vogels en de eindvorm."""
from PIL import Image, ImageDraw, ImageFont
R = '../../../../../../'
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
def spr(p, frame=True):
    im = Image.open(p).convert('RGBA')
    if frame:
        im = im.crop((0, 0, 64, 64)); bg = im.getpixel((0, 0))
        im.putdata([(0, 0, 0, 0) if px == bg else px for px in im.getdata()])
    return im
items = [('pre-evo r5', spr('kolibrie_pre.png', False)), ('r4', spr('../kleur_r4/kolibrie_pre.png', False))] + \
        [(n, spr(R + f'graphics/pokemon/{n}/anim_front.png')) for n in ('taillow', 'swablu', 'natu', 'pidgey')] + \
        [('eindvorm', spr('../../../kolibrie/af/kolibrie.png', False))]
LIGHT, DARK = (236, 236, 230, 255), (40, 40, 50, 255)
V = Image.new('RGBA', (20 + 2 * 276 + len(items) * 140, 600), (255, 255, 255, 255)); d = ImageDraw.Draw(V)
for i, bg in enumerate((LIGHT, DARK)):
    b = Image.new('RGBA', (256, 256), bg); b.alpha_composite(items[0][1].resize((256, 256), Image.NEAREST)); V.paste(b, (10 + i * 276, 30))
d.text((10, 8), 'kolibrie pre-evo r5 (4x, licht en donker)', font=F, fill=(0, 0, 0))
x0 = 20 + 2 * 276
for j, (n, im) in enumerate(items):
    for i, bg in enumerate((LIGHT, DARK)):
        b = Image.new('RGBA', (128, 128), bg); b.alpha_composite(im.resize((128, 128), Image.NEAREST)); V.paste(b, (x0 + j * 140, 30 + i * 136))
        b = Image.new('RGBA', (64, 64), bg); b.alpha_composite(im); V.paste(b, (x0 + j * 140 + 32, 320 + i * 72))
    d.text((x0 + j * 140, 470), n, font=F, fill=(0, 0, 0))
d.text((x0, 8), '2x en 1x op licht en donker', font=F, fill=(0, 0, 0))
V.convert('RGB').save('vel.png')
