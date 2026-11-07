"""Stap 2 (Jordi, 6 nov): stick man in Hitmonlee-verhoudingen ("niet langer dan een hitmonlee qua benen",
"geen menselijke verhoudingen", Hitmontop is "wimpy" t.o.v. Hitmonlee) + de onderdelen die vastliggen:
Hitmontops ronde handen en blauwe klauwvoeten, 1:1 geknipt (alleen gespiegeld/90 graden gedraaid).
Hoeken komen van de foto (skelet/skelet.py), lengtes in spritepixels.
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/stap2/stap2.py"""
import os, sys, math
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
sys.path.insert(0, os.path.join(HERE, '../skelet'))
import importlib.util
spec = importlib.util.spec_from_file_location('sk', os.path.join(HERE, '../skelet/skelet.py'))
src = open(os.path.join(HERE, '../skelet/skelet.py')).read().replace('\nmain()\n', '\n')
sk = {'__file__': os.path.join(HERE, '../skelet/skelet.py')}; exec(compile(src, 'skelet.py', 'exec'), sk)
P, PARENT, ORDER = sk['P'], sk['PARENT'], sk['ORDER']
# kleine correcties uit de keuring van stap 1
P = dict(P, enkel1=(140, 130), voet1=(95, 185), koord=(470, 440), knie2=(585, 250))

def laad(n):
    im = Image.open(os.path.join(ROOT, 'graphics/pokemon/%s/anim_front.png' % n)).convert('RGBA').crop((0, 0, 64, 64))
    bg = im.getpixel((0, 0))
    im.putdata([(0, 0, 0, 0) if px == bg else px for px in im.get_flattened_data()])   # achtergrondkleur (index 0) transparant
    return im


TOP, LEE = laad('hitmontop'), laad('hitmonlee')
HAND = TOP.crop((9, 27, 17, 36))
VOET = TOP.crop((40, 13, 56, 24))     # Hitmontops voet in zijaanzicht, klauwen naar rechts
VOET_L = TOP.crop((3, 6, 22, 27))      # Hitmontops linker bovenvoet; enkelstompje rechtsonder
VOET_L_ENKEL = (18, 13)                # plek van dat stompje in de uitsnede


def maak(L, hoofd_r):
    """L: lengte in px per gewricht (segment ouder->gewricht); hoeken van de foto."""
    Q = {'hand': (0.0, 0.0)}
    for j in ORDER:
        p = PARENT[j]
        dx, dy = P[j][0] - P[p][0], P[j][1] - P[p][1]
        n = math.hypot(dx, dy)
        Q[j] = (Q[p][0] + dx / n * L[j], Q[p][1] + dy / n * L[j])
    return Q, hoofd_r


BASIS = dict(pols=2, elleboog=7, schouder=7, nek=3, kop=7, heup=15, v_schouder=7, v_elleboog=6, v_pols=6, v_hand=3,
             knie1=11, enkel1=10, voet1=3, knie2=11, enkel2=10, voet2=3, koord=7)
BASIS = dict(BASIS, elleboog=8, schouder=8, nek=3, kop=9, heup=20, v_schouder=9, v_elleboog=7, v_pols=7)
BASIS = dict(BASIS, v_pols=9)   # vrije hand bij de riem (keuring stap 2)
OPTIES = {
    'D14: benen 24, romp 20, kop 14': maak(dict(BASIS, kop=6), 7),
    'D16: benen 24, romp 20, kop 16': maak(dict(BASIS, kop=7), 8),
    'E16: steviger: benen 22, romp 22, kop 16': maak(dict(BASIS, heup=22, knie1=11, enkel1=9, knie2=11, enkel2=9, kop=7), 8),
}
KLEUR = sk['KLEUR']; SEG = sk['SEG']


def plaats(Q, r):
    """schuif zo dat de hand op de grond staat (y=59) en het geheel horizontaal gecentreerd is."""
    xs = [p[0] for p in Q.values()] + [Q['kop'][0] - r]
    ox = 34 - (min(xs) + max(xs)) / 2
    oy = 58 - Q['hand'][1]
    return {k: (x + ox, y + oy) for k, (x, y) in Q.items()}


def plak(im, part, cx, cy):
    im.alpha_composite(part, (int(round(cx - part.width / 2)), int(round(cy - part.height / 2))))


def bouw(Q, r):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for a, b, t in SEG:
        d.line([Q[a], Q[b]], fill=KLEUR[t] + (255,), width=1)
    cx, cy = Q['kop']
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(40, 40, 40, 255))
    # vaste onderdelen
    plak(im, HAND, *Q['hand'])
    plak(im, HAND, *Q['v_hand'])
    # voet 1 (been naar linksboven): gespiegeld, klauwen naar links; voet 2 (rechtsboven): zoals bij Hitmontop, enkel onder
    ex, ey = Q['enkel1']
    im.alpha_composite(VOET_L, (int(round(ex - VOET_L_ENKEL[0])), int(round(ey - VOET_L_ENKEL[1]))))
    plak(im, VOET, *Q['voet2'])
    return im


def main():
    Z = 8; W = 64 * Z
    tiles = []
    for naam, (Q, r) in OPTIES.items():
        q = plaats(Q, r)
        im = bouw(q, r)

        im.save(os.path.join(HERE, 'optie_%s.png' % naam.split(':')[0]))
        a = im.getchannel('A').getbbox(); print(naam, 'bbox', a)
        tiles.append((naam, im))
    vel = Image.new('RGB', (20 + (W + 20) * 3, W + 220), (235, 235, 240))
    d = ImageDraw.Draw(vel)
    for i, (naam, im) in enumerate(tiles):
        x = 20 + i * (W + 20)
        bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(im)
        g = bg.resize((W, W), Image.NEAREST); gd = ImageDraw.Draw(g)
        gd.line([(0, 60 * Z), (W, 60 * Z)], fill=(150, 150, 150))
        vel.paste(g.convert('RGB'), (x, 30)); d.text((x, 10), naam, fill=(0, 0, 0))
        y = W + 45
        for j, ref in enumerate((im, TOP, LEE)):
            b2 = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); b2.alpha_composite(ref)
            vel.paste(b2.convert('RGB'), (x + j * 74, y))
            vel.paste(b2.resize((128, 128), Image.NEAREST).convert('RGB'), (x + 230 + (j - 1) * 0, y) if j == 0 else (0, 0)) if False else None
        b2 = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); b2.alpha_composite(im)
        vel.paste(b2.resize((128, 128), Image.NEAREST).convert('RGB'), (x + 240, y))
        d.text((x, y + 70), '1x: optie | Hitmontop | Hitmonlee', fill=(0, 0, 0))
        d.text((x + 240, y + 132), '2x', fill=(0, 0, 0))
    vel.save(os.path.join(HERE, 'vel_stap2.png'))


main()
