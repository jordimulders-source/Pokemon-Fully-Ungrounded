# gen3.py: echte Gen 3-sprites uit graphics/pokemon (anim_front_gba + normal_gba.pal waar aanwezig)
from PIL import Image
import sys
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def ref(n):
    import os
    f=G+n+'/anim_front_gba.png'
    if not os.path.exists(f): f=G+n+'/anim_front.png'
    if not os.path.exists(f): f=G+n+'/front.png'
    im=Image.open(f); pf=G+n+('/normal_gba.pal' if f.endswith('_gba.png') else '/normal.pal'); pl=[l for l in open(pf).read().split('\n')[3:] if l.strip()]
    P=[tuple(map(int,l.split())) for l in pl]
    im=im.crop((0,0,64,64)); a=im.load()
    out=Image.new('RGBA',(64,64))
    for y in range(64):
        for x in range(64):
            i=a[x,y]; out.putpixel((x,y),(0,0,0,0) if i==0 else P[i]+(255,))
    return out,P,im
if __name__=='__main__':
    for n in sys.argv[1:]:
        o,P,im=ref(n)
        used=sorted(set(im.getdata()))
        print(n, [ (i,P[i], round(0.299*P[i][0]+0.587*P[i][1]+0.114*P[i][2])) for i in used])
