"""Keuzevel: per optie 8x hand, 3x en 1x hele sprite; ernaast ronde 3, Sugimori-Drowzee en Mr. Mime."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from maak import *
R = os.path.abspath(os.path.join(H, '../../../../../..'))
def rgba(a):
    im = Image.fromarray(a, 'P'); im.putpalette(PAL); im.info['transparency'] = 0
    im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); return bg
def kolom(titel, a, onder=''):
    s = rgba(a)
    c8 = s.crop((1, 44, 25, 64)).resize((24 * 8, 20 * 8), Image.NEAREST)
    f3 = s.resize((192, 192), Image.NEAREST)
    k = Image.new('RGBA', (200, 410), (255, 255, 255, 255)); d = ImageDraw.Draw(k)
    d.text((4, 2), titel, fill=(0, 0, 0)); d.text((4, 14), onder, fill=(90, 90, 90))
    k.paste(c8, (4, 28)); k.paste(f3, (4, 194)); k.paste(s, (130, 340))
    return k
def ref():
    k = Image.new('RGBA', (260, 410), (255, 255, 255, 255)); d = ImageDraw.Draw(k)
    dz = Image.open(os.path.join(H, '../../referenties/drowzee_gen1_sugimori.png')).convert('RGBA')
    hand = dz.crop((430, 200, 660, 400)).resize((230, 200))
    d.text((4, 2), 'Sugimori-Drowzee (hand)', fill=(0, 0, 0)); k.paste(hand, (4, 16), hand)
    mm = Image.open(os.path.join(R, 'graphics/pokemon/mr_mime/anim_front_gba.png')); mm.info['transparency'] = 0
    mm = mm.convert('RGBA'); bg = Image.new('RGBA', mm.size, (255, 255, 255, 255)); bg.alpha_composite(mm)
    d.text((4, 222), 'Mr. Mime 8x / 3x', fill=(0, 0, 0))
    k.paste(bg.crop((40, 20, 60, 36)).resize((160, 128), Image.NEAREST), (4, 236))
    k.paste(bg.crop((0, 0, 64, 64)).resize((96, 96), Image.NEAREST).crop((50, 20, 96, 70)), (170, 236))
    return k
if __name__ == '__main__':
    import importlib
    cols = [kolom('ronde 3 (huidig)', A0, 'afgekeurd: handschoen')]
    for naam, onder in [a.split('=') for a in sys.argv[1:]]:
        m = importlib.import_module('opt' + naam)
        a = np.array(Image.open(os.path.join(H, 'optie_%s.png' % naam)))
        cols.append(kolom('optie ' + naam, a, onder))
    cols.append(ref())
    W = sum(c.width for c in cols) + 6 * len(cols)
    o = Image.new('RGBA', (W, 410), (255, 255, 255, 255)); x = 0
    for c in cols: o.paste(c, (x, 0)); x += c.width + 6
    o.convert('RGB').save(os.path.join(H, 'vel_opties.png'))
