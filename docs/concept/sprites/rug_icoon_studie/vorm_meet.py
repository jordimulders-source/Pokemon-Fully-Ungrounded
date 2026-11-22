"""Hoe simpel is een icoon t.o.v. de front? Maten per sprite:
- compact: omtrek^2/oppervlak van het silhouet (hoger = grilliger), icoon vs front verkleind tot icoonhoogte
- vlakken: aantal samenhangende kleurvlakken >= 2 px (zonder omlijning/donker), icoon vs front
- uitsteeksels: aantal 'armen' van het silhouet (eindpunten na opening), grof
python3 vorm_meet.py [icon.png front.png]  -> zonder argumenten: normen over alle GBA-iconen"""
import os,sys,numpy as np
from PIL import Image
from scipy import ndimage as nd
def stats(ix,P):
    m=ix>0
    if not m.any(): return None
    lum=P.mean(1)
    per=(m&~nd.binary_erosion(m)).sum(); comp=per**2/m.sum()
    light=m&(lum[ix]>=110); n=0
    for k in np.unique(ix[light]):
        lab,c=nd.label(ix==k); sizes=nd.sum(np.ones_like(lab),lab,range(1,c+1)); n+=(np.array(sizes)>=2).sum()
    holes=nd.label(nd.binary_fill_holes(m)&~m)[1]
    return comp,n,holes,m.sum()
def load(p,palfile=None):
    im=Image.open(p); ix=np.array(im)
    if palfile:
        L=open(palfile).read().split('\n'); P=np.array([[int(v) for v in L[3+k].split()[:3]] for k in range(16)])
    else: P=np.array(im.getpalette()[:48]).reshape(16,3)
    return ix,P
def shrink(ix,P,h):
    ys,xs=np.nonzero(ix>0); c=ix[ys.min():ys.max()+1,xs.min():xs.max()+1]; s=h/c.shape[0]
    w=max(1,round(c.shape[1]*s)); im=Image.fromarray(c.astype(np.uint8)).resize((w,h),Image.NEAREST); return np.array(im)
def pair(icon,front,ipal=None,fpal=None):
    ii,IP=load(icon,ipal); ii=ii[:32]; fi,FP=load(front,fpal); fi=fi[:64]
    ys,_=np.nonzero(ii>0); h=ys.max()-ys.min()+1
    a=stats(ii,IP); b=stats(shrink(fi,FP,h),FP); c=stats(fi,FP)
    return {'compact_ratio':a[0]/b[0],'vlakken_icoon':a[1],'vlakken_front64':c[1],'vlakken_ratio':a[1]/max(1,c[1]),'gaten_icoon':a[2],'gaten_front':c[2]}
if __name__!='__main__': pass
elif len(sys.argv)>2:
    print({k:round(float(v),2) for k,v in pair(sys.argv[1],sys.argv[2]).items()})
else:
    G='graphics/pokemon'; R=[]
    for sp in sorted(os.listdir(G)):
        d=f'{G}/{sp}'
        if os.path.exists(d+'/icon_gba.png') and os.path.exists(d+'/anim_front_gba.png'):
            try: R.append(pair(d+'/icon_gba.png',d+'/anim_front_gba.png',None,d+'/normal_gba.pal'))
            except Exception: pass
    for k in R[0]:
        v=np.array([r[k] for r in R],float); print(k,np.percentile(v,[10,25,50,75,90]).round(2))
