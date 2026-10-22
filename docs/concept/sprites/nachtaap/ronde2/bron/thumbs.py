"""Drie snelle silhouetten (zwart, 64x64) voor ronde 2 van de nachtaap.
A: mediterend, spiraalstaart rechtop naast de kop.
B: mediterend, spiraal als halo achter de kop.
C: zwevend druppellijf, spiraal als slinger eronder.
python3 thumbs.py <uit.png>"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../../../tools/concept/sprites'))
from layerlib import *


def head(cx=29, cy=24):
    m = ellipse(cx, cy, 15.5, 12.5)
    m |= ellipse(cx - 14, cy - 6, 4, 4) | ellipse(cx + 14, cy - 6, 4, 4)
    return m


def sil_A():
    m = head()
    m |= ellipse(29, 44, 10.5, 10)            # peerlijf
    m |= ellipse(29, 53, 14, 5)               # gevouwen benen
    m |= ellipse(17, 56, 4.5, 2.2) | ellipse(41, 56, 4.5, 2.2)   # voeten
    tail = bezier((38, 52), (50, 52), (51, 34)) + spiral(51, 23, 11, 3, 90, 90 - 630)
    m |= stroke(tail, 1.6)
    return m


def sil_B():
    m = head(29, 28)
    m |= ellipse(29, 47, 10.5, 9.5)
    m |= ellipse(29, 55, 14, 4.5)
    m |= ellipse(17, 58, 4.5, 2) | ellipse(41, 58, 4.5, 2)
    tail = spiral(29, 13, 11, 3, 90, 90 - 630)
    m |= stroke(tail, 1.6)
    return m


def sil_C():
    m = head(31, 22)
    m |= ellipse(31, 40, 9, 9) | polygon([(24, 42), (38, 42), (31, 52)])
    tail = bezier((31, 50), (31, 54), (36, 54)) + spiral(41, 54, 6, 2, 180, 180 + 450)
    m |= stroke(tail, 1.5)
    m |= ellipse(19, 41, 3, 4) | ellipse(43, 41, 3, 4)
    return m


if __name__ == '__main__':
    out = sys.argv[1]
    sils = [('A zittend, staart opzij', sil_A()), ('B halo', sil_B()), ('C zwevend', sil_C())]
    z = 4
    sheet = Image.new('RGB', (len(sils) * (64 * z + 70) + 10, 64 * z + 40), (250, 249, 244))
    d = ImageDraw.Draw(sheet)
    for i, (n, m) in enumerate(sils):
        a = np.where(m, 30, 250).astype(np.uint8)
        im = Image.fromarray(a).convert('RGB')
        x = 10 + i * (64 * z + 70)
        sheet.paste(im.resize((64 * z, 64 * z), Image.NEAREST), (x, 22))
        sheet.paste(im, (x + 64 * z + 4, 22))
        d.text((x, 6), n + '  (%d px)' % m.sum(), fill=(0, 0, 0))
    sheet.save(out)
