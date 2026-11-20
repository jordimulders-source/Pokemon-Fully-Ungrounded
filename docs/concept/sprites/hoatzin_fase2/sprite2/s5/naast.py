# naast.py [png...]: sprite(s) op 1x en 2x naast Honchkrow, Staraptor, Mandibuzz (frame 1) op licht en donker
import sys
from PIL import Image
G = '/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
ims = [Image.open(p) for p in (sys.argv[1:] or ['hoatzin.png'])] + [Image.open(G + n + '/anim_front.png').crop((0, 0, 64, 64)) for n in ('honchkrow', 'staraptor', 'mandibuzz')]
V = Image.new('RGB', (len(ims) * 140, 2 * 210), (255, 255, 255))
for r, bg in enumerate([(255, 255, 255), (64, 72, 80)]):
    V.paste(Image.new('RGB', (len(ims) * 140, 210), bg), (0, r * 210))
    for i, im in enumerate(ims):
        im = im.convert('RGBA')
        V.paste(im, (i * 140 + 38, r * 210 + 4), im)
        b = im.resize((128, 128), Image.NEAREST); V.paste(b, (i * 140 + 6, r * 210 + 74), b)
V.save(sys.argv[-1].replace('.png', '_naast.png') if False else 'naast.png')
