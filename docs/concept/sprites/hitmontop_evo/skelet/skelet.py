"""Stap 1 van Jordi's werkwijze (6 nov): stick man / skelet van de pose, in opties.
Punten = gewrichten op de gespiegelde foto (referenties/pose_eenhandsstand.webp, geschaald naar 790 px breed).
Draaien vanuit de repo-root: python3 docs/concept/sprites/hitmontop_evo/skelet/skelet.py"""
import os, math
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(HERE, '../referenties/pose_eenhandsstand.webp')

# gewrichten op de gespiegelde foto (790x845)
P = dict(hand=(262, 735), pols=(298, 722), elleboog=(315, 625), schouder=(322, 522),
         nek=(300, 445), kop=(255, 405), heup=(440, 325),
         v_schouder=(365, 430), v_elleboog=(345, 330), v_pols=(430, 410), v_hand=(425, 458),
         knie1=(262, 238), enkel1=(165, 140), voet1=(78, 125),
         knie2=(560, 268), enkel2=(622, 180), voet2=(648, 122),
         koord=(500, 462))
PARENT = dict(pols='hand', elleboog='pols', schouder='elleboog', nek='schouder', kop='nek', heup='schouder',
              v_schouder='schouder', v_elleboog='v_schouder', v_pols='v_elleboog', v_hand='v_pols',
              knie1='heup', enkel1='knie1', voet1='enkel1', knie2='heup', enkel2='knie2', voet2='enkel2', koord='heup')
ORDER = ['pols', 'elleboog', 'schouder', 'nek', 'kop', 'heup', 'v_schouder', 'v_elleboog', 'v_pols', 'v_hand',
         'knie1', 'enkel1', 'voet1', 'knie2', 'enkel2', 'voet2', 'koord']
KOP_R = 48  # kopstraal op de foto


def bouw(lengte, draai=None, kop=1.0):
    """lengte: factor per gewricht (segment ouder->gewricht); draai: graden per gewricht (om de ouder)."""
    draai = draai or {}
    Q = {'hand': P['hand']}
    for j in ORDER:
        p = PARENT[j]
        dx, dy = P[j][0] - P[p][0], P[j][1] - P[p][1]
        a = math.radians(draai.get(j, 0)); f = lengte.get(j, 1.0)
        dx, dy = dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)
        Q[j] = (Q[p][0] + dx * f, Q[p][1] + dy * f)
    return Q, KOP_R * kop


BEEN = ['knie1', 'enkel1', 'knie2', 'enkel2']
OPTIES = {
    'A: zoals de foto': bouw({}),
    'B: Pokemon-maat (kop 1,3x, lijf 1,2x, benen 1,1x)': bouw(dict(heup=1.2, v_schouder=1.1, **{b: 1.1 for b in BEEN}), kop=1.3),
    'C: als B, bredere V, kop dichter bij de arm': bouw(dict(heup=1.2, v_schouder=1.1, kop=0.8, **{b: 1.1 for b in BEEN}),
                                                       draai=dict(knie1=-12, knie2=12, kop=-15), kop=1.3),
}
SEG = [('hand', 'pols', 'arm'), ('pols', 'elleboog', 'arm'), ('elleboog', 'schouder', 'arm'), ('schouder', 'nek', 'lijf'),
       ('nek', 'kop', 'lijf'), ('schouder', 'heup', 'lijf'), ('v_schouder', 'v_elleboog', 'arm2'), ('v_elleboog', 'v_pols', 'arm2'),
       ('v_pols', 'v_hand', 'arm2'), ('heup', 'knie1', 'been'), ('knie1', 'enkel1', 'been'), ('enkel1', 'voet1', 'voet'),
       ('heup', 'knie2', 'been'), ('knie2', 'enkel2', 'been'), ('enkel2', 'voet2', 'voet'), ('heup', 'koord', 'koord')]
KLEUR = dict(arm=(170, 110, 60), arm2=(210, 150, 90), lijf=(40, 40, 40), been=(60, 110, 220), voet=(60, 110, 220), koord=(200, 60, 40))
EIND = ['hand', 'v_hand', 'voet1', 'voet2']


def naar64(Q, r):
    xs = [p[0] for p in Q.values()] + [Q['kop'][0] - r, Q['kop'][0] + r]
    ys = [p[1] for p in Q.values()] + [Q['kop'][1] - r, Q['kop'][1] + r]
    s = 58.0 / max(max(xs) - min(xs), max(ys) - min(ys))
    ox = (64 - (max(xs) - min(xs)) * s) / 2 - min(xs) * s
    oy = 62 - max(ys) * s
    return {k: (x * s + ox, y * s + oy) for k, (x, y) in Q.items()}, r * s, (s, ox, oy)


def teken(Q, r, Z, onder=None):
    im = Image.new('RGB', (64 * Z, 64 * Z), (255, 255, 255)) if onder is None else onder.copy()
    d = ImageDraw.Draw(im)
    w = max(1, Z)
    for a, b, t in SEG:
        d.line([tuple(c * Z for c in Q[a]), tuple(c * Z for c in Q[b])], fill=KLEUR[t], width=w * (2 if Z == 1 else 1) if Z > 1 else 1)
    cx, cy = Q['kop']
    d.ellipse([(cx - r) * Z, (cy - r) * Z, (cx + r) * Z, (cy + r) * Z], outline=(40, 40, 40), width=max(1, Z // 2))
    for k, p in Q.items():
        if k in ('kop', 'koord'):
            continue
        rr = (1.5 if k in EIND else 0.8) * Z
        d.ellipse([p[0] * Z - rr, p[1] * Z - rr, p[0] * Z + rr, p[1] * Z + rr], fill=(0, 0, 0) if k not in EIND else (230, 170, 40))
    d.line([(0, 63 * Z), (64 * Z, 63 * Z)], fill=(150, 150, 150))
    return im


def main():
    foto = Image.open(FOTO).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT).resize((790, 845))
    Z = 8
    tiles = []
    for naam, (Q, r) in OPTIES.items():
        q64, r64, (s, ox, oy) = naar64(Q, r)
        groot = teken(q64, r64, Z)
        if naam.startswith('A'):
            f = foto.resize((int(790 * s * Z), int(845 * s * Z)))
            onder = Image.new('RGB', (64 * Z, 64 * Z), (255, 255, 255))
            onder.paste(f, (int(ox * Z), int(oy * Z)))
            onder = Image.blend(onder, Image.new('RGB', onder.size, (255, 255, 255)), 0.45)
            fotovak = teken(q64, r64, Z, onder)
        klein = teken(q64, r64, 1)
        tiles.append((naam, groot, klein))
        klein.save(os.path.join(HERE, 'optie_%s.png' % naam[0]))
    W = 64 * Z
    vel = Image.new('RGB', (W * 4 + 50, W + 150), (235, 235, 240))
    d = ImageDraw.Draw(vel)
    vel.paste(fotovak, (10, 30)); d.text((10, 10), 'A over de foto (gespiegeld)', fill=(0, 0, 0))
    hm = Image.open(os.path.join(HERE, '../../../../../graphics/pokemon/hitmonlee/anim_front.png')).convert('RGBA').crop((0, 0, 64, 64))
    ht = Image.open(os.path.join(HERE, '../../../../../graphics/pokemon/hitmontop/anim_front.png')).convert('RGBA').crop((0, 0, 64, 64))
    for i, (naam, groot, klein) in enumerate(tiles):
        x = 20 + W * (i + 1) + 10 * i
        vel.paste(groot, (x, 30)); d.text((x, 10), naam, fill=(0, 0, 0))
        y = W + 45
        for j, z in enumerate((1, 2)):
            vel.paste(klein.resize((64 * z, 64 * z), Image.NEAREST), (x + j * 80, y))
        for j, ref in enumerate((ht, hm)):
            bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(ref)
            vel.paste(bg.convert('RGB'), (x + 230 + j * 70, y))
        d.text((x, y + 132), '1x en 2x | Hitmontop en Hitmonlee op 1x', fill=(0, 0, 0))
    vel.save(os.path.join(HERE, 'vel_skelet.png'))


main()
