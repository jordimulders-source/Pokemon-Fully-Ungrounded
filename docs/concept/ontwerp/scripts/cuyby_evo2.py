"""Cuyby-evolutie ronde 2: langhaarcavia als wandelende hooiberg. Modeltekening, twee varianten.

A  Fontein-mantel: kop en lijf zijn een lange, lage bult; vanaf een kruin vlak boven het gezicht valt de vacht in
   grote golvende lokken omhoog-uit en dan omlaag naar achteren en opzij (de ichu-fontein). Een pony valt over het
   verre oog; het nabije oog zit in Cuyby's zwarte vlek met het zwarte oor.
B  Sleepmantel: lager en langer, de vacht valt vanaf een kleine kruinfontein naar achteren (zoals de foto), met
   een sleep van lokken achter; een pony valt over het verre oog.

Vlakke kleuren en basisvormen (ontwerptekening, niet de sprite). Vanuit de repo-root:
python3 docs/concept/ontwerp/scripts/cuyby_evo2.py docs/concept/ontwerp/cuyby_evo/ronde2
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdl import *
from PIL import Image, ImageDraw

C = dict(hi='#fbe9a8', straw='#eccb6a', strawd='#cf9f45', rust='#b8742c', white='#fbf6ea', whited='#ddd3bd',
         dark='#2f2830', pink='#f4909e', eye='#241a20', foot='#e8a59a')


def lock(cv, pts, w0, col, w1=1.0):
    cv.fill(cv.m_stroke(pts, w0, w1), col)


def foot(cv, x, y, col):
    cv.fill(cv.m_ellipse(x, y, 10, 6), col)


def face(cv, sx, sy, fringe):
    """Gezicht laag vooraan IN de vacht (geen aparte kop): witte bles/snuit, zwarte vlek met oor rond het nabije
    oog, en een pony die over het verre oog valt."""
    cv.fill(cv.m_blob([(sx + 2, sy - 20), (sx + 24, sy - 22), (sx + 32, sy - 4), (sx + 20, sy + 10),
                       (sx + 4, sy + 4)]), C['dark'], lw=1.6)
    cv.fill(cv.m_ellipse(sx + 28, sy - 26, 8, 10, rot=25), C['dark'])          # zwart oor
    cv.fill(cv.m_blob([(sx - 30, sy + 4), (sx - 18, sy - 12), (sx - 2, sy - 16), (sx + 6, sy - 2),
                       (sx + 2, sy + 16), (sx - 20, sy + 18)]), C['white'], lw=1.6)   # witte bles + snuit
    cv.fill(cv.m_ellipse(sx - 28, sy + 5, 4, 3.4), C['pink'], lw=1.2)          # neusje
    ex, ey = sx + 15, sy - 6
    cv.fill(cv.m_ellipse(ex, ey, 4.2, 5.0), C['eye'], lw=1.4)
    cv.dot(ex - 1.4, ey - 2.0, 1.6, '#ffffff')
    cv.dot(ex + 1.6, ey + 2.2, 1.0, '#9c624a')
    for pts, w, col in fringe:
        lock(cv, pts, w, col)


def hem(cv, x0, x1, y, col, n):
    """Zoom onderaan: een paar ongelijke lokpunten die naar achteren wijzen, geen vingers of taartrand."""
    step = (x1 - x0) / n
    for i in range(n):
        x = x0 + i * step
        k = 0.7 + 0.3 * ((i * 7) % 3) / 2
        lock(cv, [(x, y - 30), (x + step * 0.3, y - 10), (x + step * 0.9 * k, y + 2 * k)], step * 0.9, col, 1.5)


def variant_a():
    cv = Canvas(line='#4a3020', lw=2.2)
    foot(cv, 96, 214, C['rust']); foot(cv, 194, 212, C['rust'])                # verre pootjes
    # vacht valt naar achteren en omlaag (schaduwkant)
    lock(cv, [(120, 80), (196, 82), (236, 136), (230, 200)], 56, C['rust'], 10)
    cv.fill(cv.m_blob([(30, 196), (32, 150), (64, 104), (122, 84), (186, 104), (214, 160), (208, 206),
                       (120, 214)]), C['straw'])                               # kop + lijf in een
    hem(cv, 46, 216, 214, C['strawd'], 5)
    foot(cv, 70, 220, C['foot']); foot(cv, 168, 220, C['foot'])                # nabije pootjes
    # fontein: vanaf de kruin omhoog-uit en dan omlaag
    lock(cv, [(118, 86), (170, 50), (220, 84), (224, 150)], 46, C['straw'], 8)
    lock(cv, [(116, 92), (150, 68), (182, 104), (184, 170)], 40, C['hi'], 8)
    lock(cv, [(112, 84), (124, 46), (148, 36), (166, 50)], 22, C['hi'], 4)
    lock(cv, [(104, 92), (92, 60), (66, 66), (50, 104)], 30, C['straw'], 6)
    face(cv, 66, 172, [([(110, 88), (80, 100), (52, 130), (42, 160)], 34, C['hi'], ),
                       ([(102, 100), (84, 128), (80, 150)], 16, C['straw'])])
    return cv


def variant_b():
    cv = Canvas(line='#4a3020', lw=2.2)
    foot(cv, 96, 214, C['rust']); foot(cv, 200, 212, C['rust'])
    lock(cv, [(110, 96), (200, 104), (246, 150), (246, 206)], 54, C['rust'], 10)
    cv.fill(cv.m_blob([(30, 204), (34, 160), (66, 118), (130, 104), (200, 124), (226, 176), (210, 212),
                       (120, 218)]), C['straw'])
    hem(cv, 50, 236, 216, C['strawd'], 5)
    foot(cv, 66, 222, C['foot']); foot(cv, 176, 222, C['foot'])
    lock(cv, [(100, 124), (150, 122), (196, 150), (214, 196)], 38, C['straw'], 8)
    lock(cv, [(96, 108), (160, 92), (220, 118), (244, 170)], 40, C['hi'], 8)
    lock(cv, [(100, 104), (112, 76), (140, 70), (160, 92)], 26, C['straw'], 6)      # kruinfontein
    lock(cv, [(98, 106), (96, 80), (78, 80), (66, 100)], 18, C['hi'], 4)
    face(cv, 64, 180, [([(104, 106), (76, 118), (50, 146), (42, 168)], 30, C['hi'])])
    return cv


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    vs = [('A', 'fontein-mantel', variant_a()), ('B', 'sleepmantel', variant_b())]
    W = 16 + len(vs) * (256 + 16 + 140)
    sheet = Image.new('RGB', (W, 330), (236, 238, 242))
    d = ImageDraw.Draw(sheet)
    for i, (k, name, cv) in enumerate(vs):
        x = 16 + i * (256 + 16 + 140)
        im = cv.image()
        im.save(os.path.join(out, 'modeltekening_%s.png' % k))
        sheet.paste(im, (x, 40))
        sp = sprite_scale(cv, fill=0.72)
        sheet.paste(sp, (x + 264, 60), sp)
        big = sp.resize((128, 128), Image.NEAREST)
        sheet.paste(big, (x + 264, 140), big)
        sil = silhouette(sp).resize((64, 64))
        sheet.paste(sil, (x + 340, 60), sil)
        d.text((x, 12), '%s  %s' % (k, name), fill=(20, 20, 20), font=font(16, True))
    sheet.save(os.path.join(out, 'varianten.png'))
