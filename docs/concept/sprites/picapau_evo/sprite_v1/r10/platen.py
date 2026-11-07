"""r10-platen: bewijs.png (Swellows snavel, omgekleurd, en de onze in r10, op 16x), kop_closeup.png (kop r10, r9 en Swellow op 16x)
en vel.png (1x en 8x: r10, r9, Swellow). Draaien: python3.11 platen.py"""
from PIL import Image, ImageDraw
from ref_snavels import png, vel, G
from swellow_snavel import TABEL
from palet import RGB
sw = png(G + 'swellow/anim_front.png')
# omgekleurde Swellow: alleen de snavelpixels (zelfde selectie als swellow_snavel.py) met onze tinten, de rest van Swellow grijs gedempt
om = sw.copy(); px = om.load(); src = sw.load()
for y in range(64):
    for x in range(64):
        r, g, b, a = src[x, y]
        if not a: continue
        if (r, g, b) in TABEL and not (TABEL[(r, g, b)][0] == 'k' and (x >= 10 or not 11 <= y <= 19)) and 4 <= x <= 16 and 11 <= y <= 19:
            px[x, y] = RGB[TABEL[(r, g, b)][0]] + (255,)
        else:
            m = (r + g + b) // 3; px[x, y] = (m // 2 + 110, m // 2 + 110, m // 2 + 110, 255)
om.save('swellow_omgekleurd.png')
vel([('Swellow, snavel', G + 'swellow/anim_front.png', (3, 10, 18, 20)), ('Swellow omgekleurd (kleurtabel)', 'swellow_omgekleurd.png', (3, 10, 18, 20)),
     ('r10, onze snavel (x8, y-4 verschoven)', 'picapau_evo.png', (9, 6, 24, 16))], 16, 'bewijs.png')
vel([('kop r10', 'picapau_evo.png', (6, 0, 40, 18)), ('kop r9', '../r9/picapau_evo.png', (6, 0, 40, 18)),
     ('Swellow', G + 'swellow/anim_front.png', (3, 7, 31, 25))], 16, 'kop_closeup.png')
items = [('sprite r10', png('picapau_evo.png')), ('sprite r9', png('../r9/picapau_evo.png')), ('Swellow', sw)]
W8 = 512
v = Image.new('RGBA', (8 + len(items) * (W8 + 8), 16 + 72 + W8 + 8), (255, 255, 255, 255)); d = ImageDraw.Draw(v)
for i, (t, im) in enumerate(items):
    x = 8 + i * (W8 + 8)
    d.text((x, 2), t, fill=(0, 0, 0, 255)); v.alpha_composite(im, (x, 16)); v.alpha_composite(im.resize((W8, W8), Image.NEAREST), (x, 88))
v.convert('RGB').save('vel.png'); print('vel.png', v.size)
