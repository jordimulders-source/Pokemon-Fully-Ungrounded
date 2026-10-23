# Maakt anim_front.png (64x128, twee frames), normal.pal en compare.png in de map erboven.
# Frame 2 = dezelfde handgetekende delen, kop/poten/klauwen/staart 1 pixel omhoog (ademhaling); lijf en voeten blijven staan.
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build
B = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(B)
REPO = os.path.abspath(os.path.join(OUT, '../../../../..'))

F1 = [('staart.txt',0,0),('lijf.txt',0,0),('arm_achter.txt',0,0),('voeten.txt',0,0),
      ('klauw_voor.txt',0,0),('arm_voor.txt',0,0),('kop.txt',12,16)]
F2 = [('staart.txt',0,-1),('lijf.txt',0,0),('arm_achter.txt',0,-1),('voeten.txt',0,0),
      ('klauw_voor.txt',0,-1),('arm_voor.txt',0,-1),('kop.txt',12,15)]

g1, g2 = build.compose(F1), build.compose(F2)
sheet = build.img(g1 + g2)
sheet.save(os.path.join(OUT, 'anim_front.png'), transparency=0)
with open(os.path.join(OUT, 'normal.pal'), 'w', newline='\r\n') as f:
    f.write('JASC-PAL\n0100\n16\n')
    for c in build.PAL:
        f.write('%d %d %d\n' % c)

def area(g):
    return sum(1 for r in g for v in r if v)
print('oppervlak frame 1:', area(g1), ' frame 2:', area(g2))

# vergelijkingsvel: onze sprite naast 5 echte Gen 3-sprites, op 1x en 3x
refs = ['teddiursa', 'zigzagoon', 'poochyena', 'sneasel', 'sandshrew']
ims = [('olinguito r8', build.img(g1).convert('RGBA'), build.PAL[0])]
for n in refs:
    im = Image.open(os.path.join(REPO, 'graphics/pokemon', n, 'anim_front_gba.png'))
    pal = im.getpalette()[:3]
    ims.append((n, im.crop((0, 0, 64, 64)).convert('RGBA'), tuple(pal)))
BG = (232, 232, 224)
W = 64 * 3 + 12
cv = Image.new('RGB', (W * len(ims), 64 + 64 * 3 + 40), BG)
d = ImageDraw.Draw(cv)
for i, (n, im, key) in enumerate(ims):
    px = im.load()
    for y in range(64):
        for x in range(64):
            if px[x, y][:3] == key:
                px[x, y] = BG + (255,)
    x0 = i * W
    cv.paste(im.convert('RGB'), (x0 + 70, 4))
    cv.paste(im.convert('RGB').resize((192, 192), Image.NEAREST), (x0 + 6, 72))
    d.text((x0 + 8, 268), n, fill=(40, 40, 40))
cv.save(os.path.join(OUT, 'compare.png'))
