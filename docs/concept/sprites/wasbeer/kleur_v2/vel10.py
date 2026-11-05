"""Vergelijkingsvel kleur ronde 10 (neus, nabije klauwrand, staarthaak) -> vel_ronde10.png.
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/vel10.py"""
import os
from PIL import Image, ImageDraw
from vel8 import echt, eigen, op, LICHT, DONKER, HERE, SP


def render(box, k):
    r = Image.open(os.path.join(HERE, '../silhouet_v2/onderlaag_s1a_256.png')).convert('RGB')
    x0, y0, x1, y1 = box
    return r.crop((x0 * 4, y0 * 4, x1 * 4, y1 * 4)).resize(((x1 - x0) * k, (y1 - y0) * k), Image.LANCZOS)


def main():
    r10, r10b, r9 = (eigen(os.path.join(HERE, n + '.png')) for n in ('ronde10', 'ronde10b', 'ronde9'))
    kop, st, kl = (6, 4, 30, 22), (44, 16, 60, 36), (18, 22, 34, 36)
    rijen = [
        ('kop 8x: render | ronde 10 | 10b | 9', [render(kop, 8)] + [op(i, LICHT, 8, kop, True) for i in (r10, r10b, r9)]),
        ('neus 8x: ronde 10 | zigzagoon | linoone | raticate | teddiursa | mightyena',
         [op(r10, LICHT, 8, (6, 12, 18, 21), True), op(echt('zigzagoon'), LICHT, 8, (6, 31, 18, 40), True),
          op(echt('linoone'), LICHT, 8, (0, 24, 12, 33), True), op(echt('raticate'), LICHT, 8, (8, 26, 20, 35), True),
          op(echt('teddiursa'), LICHT, 8, (16, 18, 28, 27), True), op(echt('mightyena'), LICHT, 8, (2, 17, 14, 26), True)]),
        ('staart 8x: render | ronde 10 | 9 | sentret | furret', [render(st, 8)] + [op(i, LICHT, 8, st, True) for i in (r10, r9)]
         + [op(echt('sentret'), LICHT, 8, (14, 40, 30, 60), True), op(echt('furret'), LICHT, 8, (0, 20, 16, 40), True)]),
        ('nabije klauw 8x: render | ronde 10 | 9', [render(kl, 8)] + [op(i, LICHT, 8, kl, True) for i in (r10, r9)]),
        ('hele sprite 4x: ronde 10 | 10b | 9 (licht) | ronde 10 | 10b (donker)',
         [op(r10, LICHT, 4), op(r10b, LICHT, 4), op(r9, LICHT, 4), op(r10, DONKER, 4), op(r10b, DONKER, 4)]),
    ]
    lijn = [eigen(os.path.join(SP, 'olinguito_v2/af/olinguito.png')), eigen(os.path.join(SP, 'coathief/af/coathief.png')), r10, r10b]
    lijn += [echt(n) for n in ('zangoose', 'sneasel', 'linoone', 'mightyena', 'ursaring', 'furret')]
    t = 'olinguito, coathief, ronde 10, 10b, zangoose, sneasel, linoone, mightyena, ursaring, furret'
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
    vel.save(os.path.join(HERE, 'vel_ronde10.png')); print('vel_ronde10.png', vel.size)


if __name__ == '__main__':
    main()
