"""r15-platen: vel.png. Boven op 8x: r15, r14, Pidgeot, Staraptor, Picapau, Raichu Gen 1 (Jordi). Onder dezelfde op 1x (licht en donker).
Draaien: python3.11 platen.py"""
from PIL import Image, ImageDraw
G = '../../../../../../graphics/pokemon/'
def eerste(fn): return Image.open(fn).convert('RGBA').crop((0, 0, 64, 64))
def zonder_achtergrond(im):
    bg = im.getpixel((0, 0)); d = im.getdata()
    im.putdata([(0, 0, 0, 0) if p[:3] == bg[:3] else p for p in d]); return im
rai = Image.open('../../referenties/jordi_inspiratie_raichu_gen1.png').convert('RGBA').resize((64, 64), Image.NEAREST)
ims = [('r15', Image.open('picapau_evo.png').convert('RGBA')), ('r14', Image.open('../r14/picapau_evo.png').convert('RGBA')),
       ('Pidgeot', zonder_achtergrond(eerste(G + 'pidgeot/anim_front.png'))), ('Staraptor', zonder_achtergrond(eerste(G + 'staraptor/anim_front.png'))),
       ('Picapau', Image.open('../../../picapau/af/picapau.png').convert('RGBA')), ('Raichu Gen 1 (Jordi)', rai)]
Z = 8; W = 64 * Z
v = Image.new('RGBA', (8 + len(ims) * (W + 8), 16 + W + 8 + 72), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im) in enumerate(ims):
    x = 8 + i * (W + 8)
    d.text((x, 2), t + ' (8x, eronder 1x licht/donker)', fill=(0, 0, 0, 255))
    v.alpha_composite(im.resize((W, W), Image.NEAREST), (x, 16))
    v.alpha_composite(im, (x, 16 + W + 8))
    donker = Image.new('RGBA', (64, 64), (40, 40, 48, 255)); donker.alpha_composite(im); v.alpha_composite(donker, (x + 72, 16 + W + 8))
v.convert('RGB').save('vel.png'); print('vel.png', v.size)
