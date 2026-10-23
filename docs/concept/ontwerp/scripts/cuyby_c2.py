"""Cuyby concept C2 (Langhaarbol, verfijnd naar Pokemon-stijl).

Verschil met C: een zuivere bol met een middenscheiding, weinig maar grote lokken
(zes, met een krul onderaan, zoals Swablu's wolk of Wooloo's wol), een pony van twee
lokken die het gezicht omlijst, grote glimmende ogen laag in de bol (Jigglypuff/Skitty),
een klein roze neusje met een omega-mondje en de driekleur als drie strakke vlakken.

Draaien vanuit de repo-root:
python3 docs/concept/ontwerp/scripts/cuyby_c2.py docs/concept/ontwerp/cuyby
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdl import *
from PIL import Image, ImageDraw

C = dict(fur='#fbf6ea', shade='#e6dcc6', accent='#f08a2a', dark='#2f2830', pink='#f4909e',
         line='#3a2a22', eye='#241a20')


def lock(cv, root, tip, w, curl=1):
    """Lok als druppel: brede wortel in de bol, valt omlaag naar een punt die iets naar buiten wijst."""
    (x0, y0), (x1, y1) = root, tip
    xm, ym = x0 * 0.45 + x1 * 0.55, y0 * 0.45 + y1 * 0.55
    return cv.m_blob([(x0 - w / 2, y0), (x0 + w / 2, y0), (xm + w * 0.38, ym), (x1, y1), (xm - w * 0.38, ym)])


def draw_C2():
    c = C
    cv = Canvas(line=c['line'], lw=2.6)
    # pootjes
    for x in (104, 148):
        cv.fill(cv.m_ellipse(x, 214, 12, 7), c['pink'])
        cv.stroke([(x - 3, y := 216), (x - 3, y + 4)], 1.4)
        cv.stroke([(x + 3, 216), (x + 3, 220)], 1.4)
    cx, cy = 128, 126
    ball = cv.m_ellipse(cx, cy, 68, 62)
    # zoom van lokken: brede, korte lokken die elkaar overlappen; de punten krullen naar buiten
    locks = [((72, 150), (52, 196), 34, -1), ((94, 166), (84, 208), 32, -1), ((116, 172), (112, 212), 30, -1),
             ((140, 172), (146, 212), 30, 1), ((162, 166), (174, 208), 32, 1), ((184, 150), (204, 196), 34, 1)]
    coat = ball.copy()
    for root, tip, w, cu in locks:
        coat |= lock(cv, root, tip, w, cu)
    cv.fill(coat, c['fur'])
    # driekleur: oranje rug (rechts), zwart vlak over het linkeroor tot om het linkeroog
    orange = cv.m_blob([(146, 58), (196, 76), (216, 130), (214, 200), (176, 214), (156, 180), (160, 128), (148, 92)])
    cv.fill(orange, c['accent'], line=False, clip=coat)
    black = cv.m_blob([(62, 82), (96, 62), (122, 74), (122, 112), (110, 148), (82, 150), (62, 124)])
    cv.fill(black, c['dark'], line=False, clip=coat)
    # loklijnen: alleen een korte lijn per lok, van de wortel naar de punt
    for (root, tip, w, cu) in locks:
        cv.stroke([(root[0] + (tip[0] - root[0]) * 0.25, root[1] + 8), (root[0] + (tip[0] - root[0]) * 0.6, root[1] + (tip[1] - root[1]) * 0.6)], 1.5)
    # middenscheiding met twee pony-lokken die het gezicht omlijsten
    cv.stroke([(128, 64), (128, 80)], 1.8)
    fl = cv.m_blob([(127, 80), (106, 84), (88, 98), (80, 118), (94, 108), (112, 96), (126, 92)])
    fr = cv.m_blob([(129, 80), (150, 84), (168, 98), (176, 118), (162, 108), (144, 96), (130, 92)])
    cv.fill(fl, c['dark'], lw=1.8)
    cv.fill(fr, c['accent'], lw=1.8)
    # gezicht: wit snuitvlak, grote ogen, roze neus, omega-mond
    eyeL, eyeR = (100, 134), (148, 132)
    for (ex, ey), r in ((eyeL, 11), (eyeR, 12)):
        cv.fill(cv.m_ellipse(ex, ey, r * 0.8 + 3, r + 3), c['fur'], line=False)
        cv.fill(cv.m_ellipse(ex, ey, r * 0.8, r), c['eye'], lw=1.6)
        cv.dot(ex + r * 0.25, ey - r * 0.4, r * 0.34, '#ffffff')
        cv.dot(ex - r * 0.28, ey + r * 0.45, r * 0.14, '#ffffff')
    cv.fill(cv.m_ellipse(124, 152, 7, 5), c['pink'], lw=1.8)
    cv.stroke([(124, 157), (124, 161)], 1.6)
    cv.stroke([(116, 160), (120, 164), (124, 161), (128, 164), (132, 160)], 1.6)
    # hangoortjes
    for (x, y, rot, col) in ((72, 74, -35, c['dark']), (182, 72, 35, c['accent'])):
        m = cv.m_ellipse(x, y, 13, 9, rot=rot)
        cv.fill(m, col)
        cv.fill(cv.m_ellipse(x + (2 if rot < 0 else -2), y + 2, 7, 4.5, rot=rot), c['pink'], line=False, clip=m)
    return cv


def sheet(cv, out):
    W, H = 660, 440
    img = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((16, 10), 'Cuyby (Normal, fase 1)  -  concept C2: Langhaarbol, verfijnd', fill=(20, 20, 20), font=font(15, True))
    img.paste(cv.image(256), (16, 40))
    d.rectangle([15, 39, 272, 296], outline=(200, 200, 200))
    sp = sprite_scale(cv, 64, 0.72)
    d.text((290, 40), 'sprite-formaat 1x / 2x', fill=(60, 60, 60), font=font(12))
    img.paste(sp, (290, 62), sp)
    sp2 = sp.resize((128, 128), Image.NEAREST)
    img.paste(sp2, (370, 62), sp2)
    d.text((290, 200), 'silhouet 1x / 2x', fill=(60, 60, 60), font=font(12))
    s = silhouette(sp)
    img.paste(s, (290, 220), s)
    s2 = s.resize((128, 128), Image.NEAREST)
    img.paste(s2, (370, 220), s2)
    d.text((16, 302), 'palet', fill=(60, 60, 60), font=font(12))
    for i, k in enumerate(['fur', 'shade', 'accent', 'dark', 'pink', 'eye']):
        d.rectangle([56 + i * 20, 302, 70 + i * 20, 316], fill=hexc(C[k]), outline=(0, 0, 0))
    txt = ('Idee van C (Peruaanse langhaarcavia = een bol vacht), gestileerd: zuivere bol met een\n'
           'middenscheiding, een zoom van zes brede lokken met krullende punten (Swablu/Wooloo),\n'
           'twee pony-lokken om het gezicht, grote glimmende ogen laag in de bol (Jigglypuff/Skitty),\n'
           'roze neusje + omega-mondje, hangoortjes. Driekleur als drie strakke vlakken. Geen blosjes.')
    d.multiline_text((16, 362), txt, fill=(30, 30, 30), font=font(12), spacing=4)
    img.save(out)


if __name__ == '__main__':
    out = sys.argv[1]
    cv = draw_C2()
    sheet(cv, os.path.join(out, 'concept_C2.png'))
    cv.image(256).save('/tmp/claude-0/-home-user/49b78f33-8da9-58c2-a8a1-539341a8b8f2/scratchpad/spr6/c2_raw.png')
