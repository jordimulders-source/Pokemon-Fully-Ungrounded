# Vergelijkingsvel ronde 2: 4x licht/donker, 3x naast 1s en model, 1x, close-up palm 8x, Gen 3-referenties.
import os
from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HIER, '..')
ROOT = os.path.abspath(os.path.join(R, '..', '..', '..', '..', '..', '..'))
NA = os.path.join(R, 'nachtaap_fase3.png')
OUD = os.path.join(R, '..', 'ronde1s', 'nachtaap_fase3.png')
MODEL = os.path.join(R, '..', '..', 'silhouet', 'onderlaag_256.png')
REF = os.path.join(R, '..', '..', 'referenties')
LICHT, DONKER = (248, 248, 248, 255), (40, 44, 56, 255)

def rgba(p, frame=True):
    im = Image.open(p).convert('RGBA')
    if frame and im.size == (64, 128):
        im = im.crop((0, 0, 64, 64))
    return im

def op(im, k, bg):
    w, h = im.size
    b = Image.new('RGBA', (w * k, h * k), bg)
    b.alpha_composite(im.resize((w * k, h * k), Image.NEAREST))
    return b

nieuw, oud = rgba(NA), rgba(OUD)
model = Image.open(MODEL).convert('RGBA').resize((192, 192), Image.LANCZOS)
gen3 = [rgba(os.path.join(ROOT, 'graphics', 'pokemon', n, 'anim_front_gba.png')) for n in ('primeape', 'medicham', 'alakazam')]
deox = rgba(os.path.join(ROOT, 'graphics', 'pokemon', 'deoxys', 'anim_front_gba.png'))

W, H = 1050, 1012
vel = Image.new('RGBA', (W, H), (255, 255, 255, 255))
d = ImageDraw.Draw(vel)
y = 8
d.text((8, y), 'Nachtaap fase 3 - kleurronde 2 (4x licht / donker)', fill=(0, 0, 0)); y += 16
vel.alpha_composite(op(nieuw, 4, LICHT), (8, y)); vel.alpha_composite(op(nieuw, 4, DONKER), (8 + 256 + 16, y))
# 1x rij rechts
x = 8 + 512 + 48
d.text((x, y), '1x: 1s / ronde 2 / primeape / medicham / alakazam', fill=(0, 0, 0))
for i, im in enumerate([oud, nieuw] + gen3):
    vel.alpha_composite(op(im, 1, LICHT), (x + i * 72, y + 16))
    vel.alpha_composite(op(im, 1, DONKER), (x + i * 72, y + 88))
y += 256 + 16
d.text((8, y), '3x: ronde 1s  |  ronde 2  |  model (onderlaag)', fill=(0, 0, 0)); y += 16
vel.alpha_composite(op(oud, 3, LICHT), (8, y)); vel.alpha_composite(op(nieuw, 3, LICHT), (8 + 208, y))
mb = Image.new('RGBA', (192, 192), LICHT); mb.alpha_composite(model); vel.alpha_composite(mb, (8 + 416, y))
d.text((8 + 640, y), 'Gen 3 (3x): primeape, medicham, alakazam', fill=(0, 0, 0))
for i, im in enumerate(gen3[:2]):
    vel.alpha_composite(op(im, 3, LICHT), (8 + 640 + i * 200, y + 16))
y += 208
vel.alpha_composite(op(gen3[2], 3, LICHT), (8 + 640, y));
d.text((8, y), 'Palm 8x: ronde 1s | ronde 2 | Drowzee Gen 1 | Deoxys-hand 4x', fill=(0, 0, 0)); y += 16
box = (5, 45, 25, 63)
vel.alpha_composite(op(oud.crop(box), 8, LICHT), (8, y)); vel.alpha_composite(op(nieuw.crop(box), 8, LICHT), (8 + 176, y))
dr = Image.open(os.path.join(REF, 'drowzee_gen1_sugimori.png')).convert('RGBA').crop((540, 210, 720, 390)).resize((144, 144), Image.LANCZOS)
vel.alpha_composite(dr, (8 + 352, y))
vel.alpha_composite(op(deox.crop((0, 18, 22, 40)), 4, LICHT), (8 + 352, y + 150))
y += 160 + 100
d.text((8, y), 'Gen 3 (3x) donker', fill=(0, 0, 0)); y += 16
for i, im in enumerate([nieuw] + gen3):
    vel.alpha_composite(op(im, 3, DONKER), (8 + i * 200, y))
vel.convert('RGB').save(os.path.join(R, 'vel.png'))
print('vel.png')
