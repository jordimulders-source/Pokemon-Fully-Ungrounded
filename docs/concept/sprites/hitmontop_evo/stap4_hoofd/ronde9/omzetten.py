"""Ronde 9 (6 nov): het hoofd uit Jordi's Gemini-concept (referenties/hoofd_gemini_concept.webp) naar spritemaat.
Stap 1: uitsnede van het hoofd, verkleinen (gemiddelde per cel), per cel naar Hitmontops palet; omlijning waar het hoofd
aan de achtergrond grenst. Dit is de BRON voor het pixelwerk (zoals de render bij Picapau), nog geen eindsprite.
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap4_hoofd/ronde9/omzetten.py"""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../../..')
SRC = Image.open(os.path.join(HERE, '../../referenties/hoofd_gemini_concept.webp')).convert('RGB')
BOX = (140, 0, 712, 565)                     # hoofd + stekel + knot
HUID = [(255, 222, 156), (222, 189, 131), (180, 139, 90), (131, 90, 41)]
WIT, GRIJS, ZWART = (255, 255, 255), (205, 205, 205), (16, 16, 16)


def naar_palet(c, licht):
    r, g, b = c
    if r > 225 and g > 215 and b > 200:      # witte band, glans
        return WIT if r > 240 else GRIJS
    if r < 70 and g < 70 and b < 70:
        return ZWART
    # huid: kies tint op helderheid, verschoven zodat de middentoon het meeste krijgt
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    if lum > licht[0]: return HUID[0]
    if lum > licht[1]: return HUID[1]
    if lum > licht[2]: return HUID[2]
    return HUID[3]


def bouw(breed):
    crop = SRC.crop(BOX)
    h = round(crop.height * breed / crop.width)
    klein = crop.resize((breed, h), Image.BOX)
    # masker: niet-achtergrond (achtergrond is bijna wit/grijs met weinig verzadiging)
    m = crop.convert('RGB').resize((breed, h), Image.BOX)
    out = Image.new('RGBA', (breed, h), (0, 0, 0, 0)); px = out.load(); kp = klein.load()
    mask = set()
    for y in range(h):
        for x in range(breed):
            r, g, b = kp[x, y]
            achtergrond = (r > 225 and g > 225 and b > 225 and max(r, g, b) - min(r, g, b) < 12)
            if not achtergrond:
                mask.add((x, y))
    for (x, y) in mask:
        px[x, y] = naar_palet(kp[x, y], (175, 150, 120)) + (255,)
    for (x, y) in mask:                       # omlijning aan de buitenrand
        if any((x + dx, y + dy) not in mask for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            px[x, y] = ZWART + (255,)
    return out


def main():
    Z = 10
    vel = Image.new('RGB', (1400, 420), (235, 235, 240)); d = ImageDraw.Draw(vel); x = 10
    bron = SRC.crop(BOX); bron.thumbnail((300, 300)); vel.paste(bron, (x, 30)); d.text((x, 10), 'bron (Gemini, Jordi)', fill=(0, 0, 0)); x += 320
    for breed in (26, 29, 32):
        im = bouw(breed); im.save(os.path.join(HERE, 'omgezet_%d.png' % breed))
        bg = Image.new('RGBA', im.size, (152, 208, 160, 255)); bg.alpha_composite(im)
        vel.paste(bg.resize((im.width * Z, im.height * Z), Image.NEAREST).convert('RGB'), (x, 30))
        vel.paste(bg.convert('RGB'), (x, 30 + im.height * Z + 10))
        d.text((x, 10), 'breed %d px (8x niet, %dx) + 1x' % (breed, Z), fill=(0, 0, 0)); x += im.width * Z + 20
    vel.save(os.path.join(HERE, 'vel_omzetten.png'))


main()
