"""Klauw los in 3D (Jordi: "draai een tekening van de klauw zodanig dat die recht voor ons staat").
Hand met 2 klauwen naast elkaar (Sneasel-achtig: dik aan de basis, gebogen naar de punt), tegen elkaar,
alleen bij de punten een kleine inkeping = koevoetkop. Weergaven: recht van voren, driekwart, opzij.
Draaien: python3 docs/concept/sprites/wasbeer/ontwerp/klauw3d.py"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pop3d_v2 as W
P = W.P


def klauw(gat=0.9):
    m = W.Model()
    m.axis = (np.zeros(3), np.array((0, 1.0, 0)), np.array((-1.0, 0, 0)))
    m.head = dict(c=np.array((0, 999.0, 0)), R=np.eye(3), hs=1.0, eyes=[np.array((0, 999.0, 0))])
    m.tube([(14, 12, 0, 4.2), (6, 8, 0, 4.6)], 'limb')                 # onderarm
    m.ell((3, 6, 0), (4.6, 4.2, 5.4), 'limb')                           # hand
    for sz in (1, -1):                                                   # 2 klauwen, z = naast elkaar
        z0 = sz * 1.5                                                    # tegen elkaar
        pts = []
        for i, t in enumerate(np.linspace(0, 1, 9)):
            ang = math.radians(10 + 95 * t)                              # buigt van vooruit naar omlaag
            r = 2.0 - 0.9 * t
            zc = z0 if t < 0.7 else z0 + sz * gat * (t - 0.7) / 0.3     # punten wijken een beetje = inkeping
            pts.append((0 - 6 * math.sin(ang) * t - 1.0 * t, 4 - 6 * (1 - math.cos(ang)) * t, zc, r))   # kort
        m.tube(pts, 'claw', 0.3)
    return m


def view(m, yaw, pitch):
    return W.view(m, yaw, pitch, 220)[0]


if __name__ == '__main__':
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    m = klauw()
    standen = [('recht van voren', 90, 0), ('driekwart', 50, 8), ('opzij (zoals nu in de sprite)', 0, 0)]
    vel = Image.new('RGB', (262 * 3 + 12, 300), 'white'); d = ImageDraw.Draw(vel)
    for i, (lab, yaw, pitch) in enumerate(standen):
        vel.paste(view(m, yaw, pitch), (12 + 262 * i, 10)); d.text((16 + 262 * i, 272), lab, font=F, fill=(40, 40, 40))
    vel.save(os.path.join(HERE, 'klauw3d.png'))
