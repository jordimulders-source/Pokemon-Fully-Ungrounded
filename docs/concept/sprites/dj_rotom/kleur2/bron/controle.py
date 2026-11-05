"""Controle kleur2: open randen, losse pixels, omtrek t.o.v. silhouet3/s1.25, diff t.o.v. kleur1 buiten de zone."""
import sys, numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/dj_rotom/'
s=np.array(Image.open(D+'silhouet3/s1.25/silhouet.png'))>0
k1=np.array(Image.open(D+'kleur1/dj_rotom.png'))
for v in sys.argv[1:]:
    im=Image.open(D+'kleur2/dj_rotom_%s.png'%v); a=np.array(im)
    print('== variant',v,im.mode,im.size,'transparency',im.info.get('transparency'),'px',int((a>0).sum()))
    op=[];los=[]
    for y in range(64):
        for x in range(64):
            if not a[y,x]: continue
            n4=[a[yy,xx] if 0<=yy<64 and 0<=xx<64 else 0 for yy,xx in((y-1,x),(y+1,x),(y,x-1),(y,x+1))]
            if 0 in n4 and a[y,x]!=1: op.append((x,y,int(a[y,x])))
            n8=[a[yy,xx] for yy in range(max(0,y-1),min(64,y+2)) for xx in range(max(0,x-1),min(64,x+2)) if (yy,xx)!=(y,x)]
            if not any(n8): los.append((x,y))
    print(' open randen:',op); print(' losse pixels:',los)
    m=a>0; plus=m&~s; minus=s&~m
    print(' omtrek t.o.v. s1.25: +%d px (sprite, niet in s1.25), -%d px (s1.25, niet in sprite)'%(plus.sum(),minus.sum()))
    for nm,mm in (('+',plus),('-',minus)):
        ys,xs=np.nonzero(mm)
        if len(ys): print('   %s rijen %d-%d, kolommen %d-%d'%(nm,ys.min(),ys.max(),xs.min(),xs.max()))
    zone=np.zeros((64,64),bool); zone[:60,14:35]=True
    diff=(a!=k1)&~zone
    print(' pixels anders dan kleur1 buiten de zone x14-34/y0-59:',int(diff.sum()),list(zip(*np.nonzero(diff)))[:12])
    print(' pixels anders dan kleur1 totaal:',int((a!=k1).sum()))
