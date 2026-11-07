"""Vel kleur ronde 11 -> vel_ronde11.png. Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/vel11.py"""
import os
from PIL import Image, ImageDraw
from vel8 import echt, eigen, op, LICHT, DONKER, HERE, SP


def main():
    r11, r10b = eigen(os.path.join(HERE, 'ronde11.png')), eigen(os.path.join(HERE, 'ronde10b.png'))
    lijn = [eigen(os.path.join(SP, 'olinguito_v2/af/olinguito.png')), eigen(os.path.join(SP, 'coathief/af/coathief.png')), r11]
    lijn += [echt(n) for n in ('zangoose', 'sneasel', 'linoone', 'mightyena', 'ursaring', 'furret')]
    t = 'olinguito, coathief, ronde 11, zangoose, sneasel, linoone, mightyena, ursaring, furret'
    rijen = [('4x: ronde 11 | 10b (licht) | ronde 11 | 10b (donker)',
              [op(r11, LICHT, 4), op(r10b, LICHT, 4), op(r11, DONKER, 4), op(r10b, DONKER, 4)]),
             ('1x: ' + t, [op(i, LICHT, 1) for i in lijn]), ('2x licht', [op(i, LICHT, 2) for i in lijn]),
             ('2x donker', [op(i, DONKER, 2) for i in lijn])]
    W = max(sum(i.size[0] + 10 for i in ims) for _, ims in rijen) + 10
    H = sum(max(i.size[1] for i in ims) + 26 for _, ims in rijen) + 10
    vel = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(vel); y = 6
    for t, ims in rijen:
        d.text((10, y), t, fill=(0, 0, 0)); y += 16; x = 10
        for i in ims:
            vel.paste(i, (x, y)); x += i.size[0] + 10
        y += max(i.size[1] for i in ims) + 10
    vel.save(os.path.join(HERE, 'vel_ronde11.png')); print('vel_ronde11.png', vel.size)


if __name__ == '__main__':
    main()
