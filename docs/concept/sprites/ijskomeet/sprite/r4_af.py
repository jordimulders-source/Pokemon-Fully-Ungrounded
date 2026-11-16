# r4 stap 4: kern-zwerfpixels, nevel-buitenrand bovenkant L->M, r4.txt + r4.png (palet r4: staart i/j lichter en paarser)
from gio import from_txt, to_txt, CH
import numpy as np; from PIL import Image
from pal import PAL
o=from_txt('r4_kern.txt'); C={c:i for i,c in enumerate(CH)}; H,W=o.shape
for (x,y) in [(26,30),(27,30)]: o[y,x]=C['j']
for y in range(0,30):
    for x in range(17,64):
        if o[y,x]==C['L'] and any(not(0<=y+a<H and 0<=x+b<W) or o[y+a,x+b]<0 for a,b in ((1,0),(-1,0),(0,1),(0,-1))): o[y,x]=C['M']
to_txt(o,'r4.txt')
P=list(PAL); P[CH.index('i')]=(58,54,112); P[CH.index('j')]=(88,80,150)
m=np.load('mask_r1.npy'); print('alpha-diff',int(((o>=0)!=m).sum()))
im=Image.fromarray((o+1).astype('uint8'),'P'); pal=[255,255,255]+[v for c in P for v in c]; im.putpalette(pal+[0]*(768-len(pal))); im.save('r4.png',transparency=0)
print('kleuren',len(set(np.asarray(Image.open('r4.png')).ravel())))
r=Image.open('r4.png').convert('RGBA').resize((512,512),0); b=Image.new('RGBA',(512,512),(255,255,255,255)); b.alpha_composite(r); b.convert('RGB').save('r4_8x.png')
a=np.asarray(Image.open('r4.png').convert('RGBA')).astype(float); tail=np.isin(o,[C['i'],C['j'],C['K'],C['n']])&(np.arange(64)[None,:]>=28)
print('staart gem.',a[tail][:,:3].mean(0).round())
