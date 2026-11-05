# Eindkeuring ronde 7: vergelijkingsvel + patroonstudie (alleen lezen, geen sprite-wijziging)
import os, sys
from PIL import Image, ImageDraw
R = '/home/user/Pokemon-Fully-Ungrounded'
G = R + '/graphics/pokemon/'
HIER = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HIER)

def pal(path):
    l = open(path).read().split('\n')[3:19]
    return [tuple(int(v) for v in s.split()) for s in l if s.strip()]

def laad(naam):
    if naam == 'NACHTAAP':
        im = Image.open(OUT + '/nachtaap.png'); p = pal(OUT + '/normal.pal')
    else:
        f = G + naam + '/anim_front_gba.png'; pf = G + naam + '/normal_gba.pal'
        if not os.path.exists(f):
            f = G + naam + '/anim_front.png'; pf = G + naam + '/normal.pal'
        im = Image.open(f).crop((0, 0, 64, 64)); p = pal(pf)
    rgba = Image.new('RGBA', (64, 64))
    px = im.load(); o = rgba.load()
    for y in range(64):
        for x in range(64):
            i = px[x, y]
            if i: o[x, y] = p[i] + (255,)
    return rgba

def vel(namen, schaal, bestand, kol=6):
    cel = 64 * schaal + 8
    rijen = (len(namen) + kol - 1) // kol
    W = Image.new('RGB', (kol * (cel + 72), rijen * 2 * (cel + 14)), (255, 255, 255))
    d = ImageDraw.Draw(W)
    for i, n in enumerate(namen):
        s = laad(n)
        for bgi, bg in enumerate([(255, 255, 255), (40, 40, 52)]):
            x0 = (i % kol) * (cel + 72); y0 = ((i // kol) * 2 + bgi) * (cel + 14)
            b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(s)
            d.rectangle([x0, y0, x0 + cel + 70, y0 + cel + 12], fill=bg)
            W.paste(b.convert('RGB'), (x0 + 2, y0 + 12))
            W.paste(b.convert('RGB').resize((64 * schaal, 64 * schaal), Image.NEAREST), (x0 + 70, y0 + 12))
            d.text((x0 + 2, y0), n, fill=(200, 0, 0) if n == 'NACHTAAP' else (120, 120, 120))
    W.save(OUT + '/' + bestand)

vel(['NACHTAAP', 'lairon', 'sableye', 'misdreavus', 'aipom', 'grumpig', 'natu', 'abra',
     'mightyena', 'zigzagoon', 'umbreon', 'xatu'], 3, 'eindkeuring_vgl.png', kol=4)
vel(['NACHTAAP', 'zigzagoon', 'linoone', 'seviper', 'zangoose', 'mightyena', 'raikou', 'furret',
     'spinda', 'arbok', 'umbreon', 'sigilyph', 'cofagrigus', 'golett', 'claydol', 'xatu',
     'liepard', 'girafarig', 'entei', 'skuntank'], 4, 'patroonstudie.png', kol=4)
