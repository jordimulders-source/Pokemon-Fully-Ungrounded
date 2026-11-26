# S1: Poliwhirls spiraalverloop (fit uit pw_spiraal.py: draairichting, fase, binnenbegin, buiteneinde-hoek) op modelmaat,
# spoed 2 px (1 px rood + 1 px geel). Pad bemonsterd, afgerond naar pixels, hoekpixels weggesnoeid tot een 1 px 8-verbonden lijn.
import numpy as np
cx0,cy0,d,p,ph,fmin,fmax=np.load('pw_fit.npy')
SP=2.0
def pad(cx,cy,fend):
    seq=[]
    for f in np.arange(fmin,fend+0.01,1.0):
        r=SP*f/360; deg=np.deg2rad(ph+d*f)
        q=(int(round(cx+r*np.cos(deg))),int(round(cy-r*np.sin(deg))))
        if not seq or seq[-1]!=q: seq.append(q)
    # dubbele terugkeer weg
    out=[]
    for q in seq:
        if q in out: continue
        out.append(q)
    # hoeken snoeien: pixel weg als vorige en volgende 8-buren zijn
    ch=True
    while ch:
        ch=False
        for i in range(1,len(out)-1):
            a,b=out[i-1],out[i+1]
            if max(abs(a[0]-b[0]),abs(a[1]-b[1]))==1:
                del out[i]; ch=True; break
    return out
FEND=fmax-360   # buiteneinde: zelfde hoek als bij Poliwhirl, een winding eerder (modelmaat)
if __name__=='__main__':
    print('buiteneinde fase',FEND,'straal',SP*FEND/360)
    for c in ((22.5,23.5),(22,23),(23,24),(22,24),(23,23)):
        P=pad(*c,FEND); s=set(P)
        # aanraken: pixels van verschillende windingen (ver in het pad) die 4-buren zijn
        idx={q:i for i,q in enumerate(P)}
        touch=sum(1 for q in P for n in ((q[0]+1,q[1]),(q[0],q[1]+1)) if n in idx and abs(idx[n]-idx[q])>3)
        xs=[q[0] for q in P]; ys=[q[1] for q in P]
        print(c,len(P),'raakt',touch,'bbox',min(xs),max(xs),min(ys),max(ys))
