# Kale reductie natief (68x84 figuur) -> ~39x48: vlakgemiddelde per groep + dichtstbijzijnde modelkleur.
# Zwart (omlijning) wint als het >= ZW van het blok bedekt (lijnen blijven, ijskomeet-les). Niets getekend.
import sys, numpy as np; from PIL import Image
from groepen import masks, kmeans
OUT=sys.argv[1]; ZW=float(sys.argv[2]) if len(sys.argv)>2 else 0.30; BGT=float(sys.argv[3]) if len(sys.argv)>3 else 0.5
DY=float(sys.argv[4]) if len(sys.argv)>4 else 0.0; DX=float(sys.argv[5]) if len(sys.argv)>5 else 0.0
MODE=sys.argv[6] if len(sys.argv)>6 else 'dek'
ZWN=int(sys.argv[7]) if len(sys.argv)>7 else 1
MEER=len(sys.argv)>8 and sys.argv[8]=='meer'
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); m,lum=masks(a)
ys,xs=np.where(~m['bg']); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
H=48; s=(y1-y0)/H; W=int(np.ceil((x1-x0)/s))
PB=kmeans(a[m['brown']],4); PG=kmeans(a[m['green']],3); PS=kmeans(a[m['grey']],3)
# palet: 1 zwart, 2-5 bruin (donker->licht), 6-8 groen, 9-11 zilver
PAL=[(255,0,255),(16,8,6)]+[tuple(c) for c in PB]+[tuple(c) for c in PG]+[tuple(c) for c in PS]
grp={'brown':(2,PB),'green':(6,PG),'grey':(9,PS)}
o=np.zeros((H,W),int)
def wts(lo,hi,n):
    w=np.zeros(n); 
    for k in range(int(np.floor(lo)),int(np.ceil(hi))):
        if 0<=k<n: w[k]=min(hi,k+1)-max(lo,k)
    return w
for j in range(H):
    wy=wts(y0+DY+j*s,y0+DY+(j+1)*s,a.shape[0])
    for i in range(W):
        wx=wts(x0+DX+i*s,x0+DX+(i+1)*s,a.shape[1]); w=wy[:,None]*wx[None,:]; tw=w.sum()
        if (w*m['bg']).sum()/tw>=BGT: continue
        fg=tw-(w*m['bg']).sum()
        if MODE=='dek' and (w*m['blk']).sum()/fg>=ZW: o[j,i]=1; continue
        if MODE=='proj':
            # zwart als een zwart modelpixel met zijn middelpunt in dit spritepixel valt
            ly,hy=y0+DY+j*s,y0+DY+(j+1)*s; lx,hx=x0+DX+i*s,x0+DX+(i+1)*s
            cy=[k for k in range(int(ly)-1,int(hy)+2) if ly<=k+0.5<hy and 0<=k<a.shape[0]]
            cx=[k for k in range(int(lx)-1,int(hx)+2) if lx<=k+0.5<hx and 0<=k<a.shape[1]]
            if m['blk'][np.ix_(cy,cx)].sum()>=ZWN: o[j,i]=1; continue
        best=max(grp,key=lambda g:(w*m[g]).sum())
        base,P=grp[best]; ww=w*m[best]
        if ww.sum()==0: o[j,i]=1; continue
        col=(a*ww[...,None]).sum((0,1))/ww.sum()
        if MEER and best=='brown':
            # meerderheid: elk modelpixel eerst naar de dichtstbijzijnde bruintint, dan gewogen stemmen
            q=((a[...,None,:]-P[None,None])**2).sum(-1).argmin(-1); st=np.array([(ww*(q==t)).sum() for t in range(len(P))])
            o[j,i]=base+int(st.argmax()); continue
        o[j,i]=base+int(((P-col)**2).sum(1).argmin())
np.save(OUT+'.npy',o)
yy,xx=np.where(o>0); o2=o[yy.min():yy.max()+1,xx.min():xx.max()+1]; hh,ww_=o2.shape
full=np.zeros((64,64),int); fx=(64-ww_)//2; full[63-hh:63,fx:fx+ww_]=o2
p=Image.fromarray(full.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(OUT,transparency=0)
print(OUT,'s=%.3f'%s,ww_,hh,'zwart',(full==1).sum(),'kleuren',len(set(full.ravel()))-1, PAL)
