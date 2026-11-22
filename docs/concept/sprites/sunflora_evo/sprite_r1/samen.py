# Zet kop (kale reductie + 1 px buitenlijn erbuiten) en Sunflora-lijf samen op 64x64. Lijf achter de kop.
import sys, numpy as np; from PIL import Image; from pal import PAL
kop=np.load(sys.argv[1] if len(sys.argv)>1 else 'kop_kaal.npy'); lijf=np.load(sys.argv[2] if len(sys.argv)>2 else 'lijf_kaal.npy')
OUT=sys.argv[3] if len(sys.argv)>3 else 'samen'
SEL={2:4,3:4,4:4,5:6,6:6,7:9,8:9,9:9,10:6}   # lichtkant-selout per kleur
def omlijn(k):
    h,w=k.shape; p=np.zeros((h+2,w+2),'uint8'); p[1:-1,1:-1]=k; o=p.copy()
    for y in range(h+2):
        for x in range(w+2):
            if p[y,x]: continue
            nb={}
            for dy,dx in ((1,0),(0,1),(-1,0),(0,-1)):
                yy,xx=y+dy,x+dx
                if 0<=yy<h+2 and 0<=xx<w+2 and p[yy,xx]: nb[(dy,dx)]=p[yy,xx]
            if not nb: continue
            # lichtkant = de vorm ligt rechts/onder van deze lijnpixel (lijn zit links/boven)
            if set(nb)<= {(1,0),(0,1)}: o[y,x]=SEL.get(nb.get((1,0),nb.get((0,1))),1)
            else: o[y,x]=1
    return o
K=omlijn(kop)
C=np.zeros((64,64),'uint8')
kx=(64-K.shape[1])//2; ky=0
lh,lw=lijf.shape
lx=kx+1+round(0.506*kop.shape[1])-round(0.45*lw); ly=64-lh
C[ly:ly+lh,lx:lx+lw]=np.where(lijf>0,lijf,C[ly:ly+lh,lx:lx+lw])
reg=C[ky:ky+K.shape[0],kx:kx+K.shape[1]]; C[ky:ky+K.shape[0],kx:kx+K.shape[1]]=np.where(K>0,K,reg)
print('kop incl. lijn',K.shape[1],'x',K.shape[0],'op',kx,ky,'| lijf',lw,'x',lh,'op',lx,ly)
np.save(OUT+'.npy',C)
im=Image.fromarray(C,'P'); im.putpalette([v for c in PAL for v in c]); im.save(OUT+'.png',transparency=0)
Image.open(OUT+'.png').convert('RGBA').resize((512,512),Image.NEAREST).save(OUT+'_8x.png')
