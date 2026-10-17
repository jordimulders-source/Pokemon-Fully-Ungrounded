"""Maakt graphics/pokedex/colors_label.png: de knop 'COLORS' voor de Pokédex-balk
(vervangt CANCEL; stijl en lettertype van AREA/CRY/SIZE)."""
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
menu = Image.open(os.path.join(ROOT, 'graphics/pokedex/menu.png'))

def glyph(x0, y0, mapc):
    return [''.join(mapc.get(menu.getpixel((x, y)), '?') for x in range(x0, x0 + 6)) for y in range(y0 + 4, y0 + 14)]

pink = {0xb: ' ', 0xf: '#', 0x2: 's'}
green = {0xc: ' ', 0xf: '#', 0xd: 's'}
G = {'C': glyph(66, 32, pink), 'L': glyph(96, 32, pink), 'R': glyph(22, 16, green), 'S': glyph(96, 16, green)}
G['O'] = [' ###s ', '#sss#s'] + ['#s  #s'] * 6 + ['s###ss', ' ssss ']

# Knop in de stijl van AREA/CRY/SIZE: linkerrand = tegel 0x20, daarna lege vulling (0x21)
label = Image.new('P', (48, 16))
label.putpalette(menu.getpalette())
label.paste(menu.crop((0, 16, 8, 32)), (0, 0))
for t in range(1, 6):
    label.paste(menu.crop((8, 16, 16, 32)), (8 * t, 0))
for k, ch in enumerate('COLORS'):
    for y, row in enumerate(G[ch]):
        for x, c in enumerate(row):
            label.putpixel((9 + 6 * k + x, 4 + y), {' ': 0xc, '#': 0xf, 's': 0xd}[c])
label.save(os.path.join(ROOT, 'graphics/pokedex/colors_label.png'))
