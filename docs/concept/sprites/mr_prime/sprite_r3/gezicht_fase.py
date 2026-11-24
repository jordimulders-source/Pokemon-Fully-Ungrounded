# Gezichtsreductie op verschillende subpixel-fases (zelfde regels als reduceer_hyb) om de schoonste snor te kiezen.
import sys; from PIL import Image; import numpy as np; from bgmask import bgmask; from toon import rgb
TONES=np.array([1,47,63,77,116,150,208,253]); LIJN=0.28
import os
a=np.asarray(Image.open(os.environ.get('BRON','natief_kop.png')).convert('RGB')); b=bgmask(a); L=a.astype(float).mean(axis=2)
Lu=np.repeat(np.repeat(L,2,0),2,1); Bu=np.repeat(np.repeat(b,2,0),2,1)
def red(px,py,x0=7,y0=24,w=64,h=61):
    out=np.full((h,w),-1)
    for j in range(h):
        for i in range(w):
            ys=2*y0+py+j*5; xs=2*x0+px+i*5
            l=Lu[ys:ys+5,xs:xs+5]; m=~Bu[ys:ys+5,xs:xs+5]
            if l.size==0 or m.mean()<0.45: continue
            blk=(l<30)&m
            if blk.sum()/l.size>=LIJN or (m&~blk).sum()==0: out[j,i]=0; continue
            out[j,i]=np.abs(l[m&~blk].mean()-TONES).argmin()
    return out
if __name__=='__main__':
    tiles=[]
    for py in range(0,5,2):
        for px in range(0,5,2):
            o=red(px,py); np.save('fase_%d_%d.npy'%(px,py),o)
            tiles.append(Image.fromarray(rgb(o[10:26,20:50])).resize((30*10,16*10),0))
    W=Image.new('RGB',(310*3,170*3+170),(255,255,255))
    for k,t in enumerate(tiles): W.paste(t,((k%3)*310,(k//3)*170))
    m=Image.open('natief_kop.png').crop((7+20*2.5,24+10*2.5,7+50*2.5,24+26*2.5)).resize((300,160),Image.LANCZOS); W.paste(m,(0,510))
    W.save(sys.argv[1])

def red_mode(px,py,x0=7,y0=24,w=64,h=61,LIJN=0.28):
    """Zelfde raster, maar per cel de meest voorkomende modeltint (geen gemiddelde): houdt witte vlakken wit."""
    T=np.abs(Lu[...,None]-TONES).argmin(-1); T[Lu<30]=0
    out=np.full((h,w),-1)
    for j in range(h):
        for i in range(w):
            ys=2*y0+py+j*5; xs=2*x0+px+i*5
            t=T[ys:ys+5,xs:xs+5]; m=~Bu[ys:ys+5,xs:xs+5]
            if t.size==0 or m.mean()<0.45: continue
            f=t[m]
            if (f==0).sum()/t.size>=LIJN: out[j,i]=0; continue
            nz=f[f>0]; out[j,i]=np.bincount(nz).argmax() if nz.size else 0
    return out
