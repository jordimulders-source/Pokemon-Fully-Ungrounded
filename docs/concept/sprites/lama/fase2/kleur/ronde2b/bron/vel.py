"""Vel kleur ronde 2b (ronde 2 ernaast): lama 4x en 1x op licht en donker, naast de onderlaag, fase 1 (alpaca) en 5 echte Gen 3-sprites."""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(HERE, *['..'] * 8))
LIGHT, DARK = (236, 236, 236, 255), (40, 44, 56, 255)
def rgba(p):
    im = Image.open(p)
    if im.mode == 'P':
        t = im.info.get('transparency', 0); im = im.convert('RGBA'); px = im.load()
        src = Image.open(p)
        for y in range(im.height):
            for x in range(im.width):
                if src.getpixel((x, y)) == t: px[x, y] = (0, 0, 0, 0)
    return im.convert('RGBA').crop((0, 0, 64, 64))
def on(im, bg, s):
    b = Image.new('RGBA', (64, 64), bg); b.alpha_composite(im); return b.resize((64 * s, 64 * s), Image.NEAREST)
lama = rgba(os.path.join(OUT, 'lama.png'))
alp = rgba(os.path.join(ROOT, 'docs/concept/sprites/lama/referenties/fase1_alpaca.png'))
refs = []
for n in ['stantler', 'flaaffy', 'mareep', 'ponyta', 'girafarig']:
    d = os.path.join(ROOT, 'graphics/pokemon', n); p = os.path.join(d, 'anim_front_gba.png')
    refs.append((n, rgba(p if os.path.exists(p) else os.path.join(d, 'anim_front.png'))))
und = Image.open(os.path.join(ROOT, 'docs/concept/sprites/lama/fase2/silhouet/onderlaag_256.png')).convert('RGBA')
W = 256 * 4 + 64 * 2 + 16 * 7; H = 24 + 256 + 24 + 64 * 3 + 40 + 64 * 2 + 40
img = Image.new('RGBA', (W, H), (255, 255, 255, 255)); dr = ImageDraw.Draw(img)
x = 16
r1 = rgba(os.path.join(OUT, '../ronde2/lama.png'))
for lab, im in [('onderlaag', und), ('ronde 2b 4x licht', on(lama, LIGHT, 4)), ('ronde 2b 4x donker', on(lama, DARK, 4)), ('ronde 2 4x (vorige)', on(r1, LIGHT, 4))]:
    img.paste(im, (x, 24)); dr.text((x, 8), lab, fill=(0, 0, 0)); x += 256 + 16
img.paste(on(lama, LIGHT, 1), (x, 24)); img.paste(on(lama, DARK, 1), (x + 64 + 8, 24)); dr.text((x, 8), '1x', fill=(0, 0, 0))
img.paste(on(r1, LIGHT, 1), (x, 100)); dr.text((x, 168), 'ronde 2 1x', fill=(0, 0, 0))
y = 24 + 256 + 24; x = 16
dr.text((x, y - 16), 'op 3x: lama r2, alpaca, stantler, flaaffy, mareep, ponyta, girafarig (licht)', fill=(0, 0, 0))
for n, im in [('lama', lama), ('alpaca', alp)] + refs:
    img.paste(on(im, LIGHT, 3), (x, y)); x += 192 + 2
y += 192 + 40; x = 16
dr.text((x, y - 16), '1x op licht en donker (zelfde volgorde)', fill=(0, 0, 0))
for n, im in [('lama', lama), ('alpaca', alp)] + refs:
    img.paste(on(im, LIGHT, 1), (x, y)); img.paste(on(im, DARK, 1), (x, y + 64)); x += 72
img.save(os.path.join(OUT, 'vel.png')); print('vel.png', img.size)
