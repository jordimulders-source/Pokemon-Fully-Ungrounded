# onderdelen.png (hoofd 16x, armen 12x, benen 12x: r5 | r4 | model) en vel.png (r5 | r4 | model; 1x en 2x naast Tyranitar/Aggron/Pinsir)
import sys, glob; sys.path.insert(0, 'sprite_v2_r5')
from kijk import *
R5 = 'sprite_v2_r7/pinsir_evo_v2_r7.png'; R4 = 'sprite_v2_r6/pinsir_evo_v2_r6.png'
L = ['r7', 'r6', 'model']
def stapel(bs, gap=16):
    w = max(b.width for b in bs); h = sum(b.height for b in bs) + gap * (len(bs) - 1)
    o = Image.new('RGB', (w, h), (255, 255, 255)); y = 0
    for b in bs: o.paste(b, (0, y)); y += b.height + gap
    return o
if __name__ == '__main__':
    stapel([vergelijk([R5, R4], 32, 17, 58, 47, 12, ['r7 rug', 'r6', 'model']), vergelijk([R5, R4], 5, 8, 38, 34, 12, L),
            naast([vergelijk([R5, R4], 28, 28, 47, 48, 12, ['r7 nabije arm', 'r6', 'model']),
                   vergelijk([R5, R4], 5, 38, 20, 49, 12, ['r7 verre arm', 'r6', 'model'])], gap=30),
            vergelijk([R5, R4], 12, 44, 48, 64, 12, ['r7 benen', 'r6', 'model'])]).save('sprite_v2_r7/onderdelen.png')
    k = 6
    groot = naast([sprite_crop(R5, 0, 0, 64, 64, k), sprite_crop(R4, 0, 0, 64, 64, k), model_crop(0, 0, 64, 64, k)], label=L)
    def p(f):
        im = Image.open(f).convert('RGBA'); a = np.array(im)
        if a[..., 3].min() == 255:  # geen alfa: kleur linksboven = achtergrond
            bg = a[0, 0, :3]; a[(a[..., :3] == bg).all(2), 3] = 0; im = Image.fromarray(a)
        return im.crop((0, 0, 64, 64))
    def zoek(n):
        c = glob.glob(f'/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/{n}/anim_front_gba.png') + glob.glob(f'/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/{n}/front.png')
        return c[0]
    refs = [R5, R4] + [zoek(n) for n in ('tyranitar', 'aggron', 'pinsir')]
    namen = ['r7', 'r6', 'Tyranitar', 'Aggron', 'Pinsir']
    rij = []
    for s in (1, 2):
        for bg in ((255, 255, 255), (48, 48, 64)):
            c = Image.new('RGB', (len(refs) * 64 * s + 8 * len(refs), 64 * s), bg)
            for i, f in enumerate(refs):
                im = p(f) if i >= 2 else Image.open(f).convert('RGBA')
                im = im.resize((64 * s, 64 * s), Image.NEAREST); c.paste(im, (i * (64 * s + 8), 0), im)
            rij.append(c)
    stapel([groot] + rij).save('sprite_v2_r7/vel.png')
