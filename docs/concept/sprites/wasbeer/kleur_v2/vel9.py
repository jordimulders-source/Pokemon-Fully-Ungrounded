"""Vergelijkingsvel kleur ronde 9 -> vel_ronde9.png. Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/vel9.py"""
import os
from PIL import Image, ImageDraw
from vel8 import echt, eigen, op, LICHT, DONKER, HERE, SP


def main():
    r9, r9b, r8 = (eigen(os.path.join(HERE, n + '.png')) for n in ('ronde9', 'ronde9b', 'ronde8'))
    oli = eigen(os.path.join(SP, 'olinguito_v2/af/olinguito.png'))
    coa = eigen(os.path.join(SP, 'coathief/af/coathief.png'))
    rijen = [
        ('ronde 9 | 9b | 8 (4x, licht)', [op(i, LICHT, 4) for i in (r9, r9b, r8)]),
        ('ronde 9 | 9b | 8 (4x, donker)', [op(i, DONKER, 4) for i in (r9, r9b, r8)]),
        ('ogen 8x: ronde 9 (zonder pupil) | 9b (pupil) | 8', [op(i, LICHT, 8, (9, 6, 27, 16), True) for i in (r9, r9b, r8)]),
        ('oren 8x: ronde 9 | 8', [op(i, LICHT, 8, (11, 0, 31, 9), True) for i in (r9, r8)]),
    ]
    lijn = [oli, coa, r9, r9b] + [echt(n) for n in ('zangoose', 'sneasel', 'linoone', 'mightyena', 'ursaring', 'furret')]
    t = 'olinguito, coathief, ronde 9, 9b, zangoose, sneasel, linoone, mightyena, ursaring, furret'
    rijen += [('1x: ' + t, [op(i, LICHT, 1) for i in lijn]), ('2x licht', [op(i, LICHT, 2) for i in lijn]),
              ('2x donker', [op(i, DONKER, 2) for i in lijn])]
    W = max(sum(i.size[0] + 10 for i in ims) for _, ims in rijen) + 10
    H = sum(max(i.size[1] for i in ims) + 26 for _, ims in rijen) + 10
    vel = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(vel); y = 6
    for t, ims in rijen:
        d.text((10, y), t, fill=(0, 0, 0)); y += 16; x = 10
        for i in ims:
            vel.paste(i, (x, y)); x += i.size[0] + 10
        y += max(i.size[1] for i in ims) + 10
    vel.save(os.path.join(HERE, 'vel_ronde9.png')); print('vel_ronde9.png', vel.size)


if __name__ == '__main__':
    main()
