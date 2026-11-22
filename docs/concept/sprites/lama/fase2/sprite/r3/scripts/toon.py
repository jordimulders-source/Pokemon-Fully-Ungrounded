# hulpje: idx-array (.npy) + palet -> png (1x) en 8x op lichtgrijs
import sys, json, numpy as np
from PIL import Image
def png(a, pal, naam, k=1):
    im = Image.fromarray(a.astype('uint8'), 'P'); flat = []
    for c in pal: flat += list(c)
    im.putpalette(flat); im.save(naam, transparency=0)
    if k > 1:
        im = Image.open(naam).convert('RGBA'); bg = Image.new('RGBA', im.size, (235, 235, 240, 255)); bg.alpha_composite(im)
        bg.resize((64 * k, 64 * k), Image.NEAREST).save(naam)
if __name__ == '__main__':
    a = np.load(sys.argv[1]); pal = [tuple(c) for c in json.load(open(sys.argv[2]))]
    png(a, pal, sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 1)
