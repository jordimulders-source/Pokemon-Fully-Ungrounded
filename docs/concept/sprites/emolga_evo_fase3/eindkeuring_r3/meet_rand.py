# meet_rand.py: kleur van de buitenrandpixels per kant (links/boven = lichtkant, rechts/onder = schaduwkant). Gebruik: python3 meet_rand.py <png>...
from PIL import Image
import sys, collections
def load(f):
    im=Image.open(f)
    if im.mode!='P': print('mode',im.mode); 
    w,h=im.size
    if h==128: im=im.crop((0,0,64,64))
    return im
for f in sys.argv[1:]:
    im=load(f); px=im.load(); w,h=im.size; p=im.getpalette()
    L=lambda i: sum(p[i*3:i*3+3])//3
    lt=collections.Counter(); rb=collections.Counter()
    for y in range(h):
        for x in range(w):
            if px[x,y]==0: continue
            def tr(a,b): return not(0<=a<w and 0<=b<h) or px[a,b]==0
            if tr(x-1,y) or tr(x,y-1): lt[px[x,y]]+=1
            if tr(x+1,y) or tr(x,y+1): rb[px[x,y]]+=1
    fmt=lambda c: ' '.join('%x(%d):%d'%(k,L(k),v) for k,v in c.most_common())
    print(f.split('/')[-2] if 'anim' in f else f); print('  links/boven:',fmt(lt)); print('  rechts/onder:',fmt(rb))
