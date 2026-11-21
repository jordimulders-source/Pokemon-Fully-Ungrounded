# Tentakelpunten van de achterste anemonen (L, R, T) in het model: lokale maxima van de silhouetrand t.o.v. het
# mondje (natief), boven de schijf. Geeft per anemoon [(hoek, x_sprite, y_sprite)].
import numpy as np
from klassen import klassen; from anemonen import *; from gemeen import *
def punten(venster=0.12, scheiding=0.10, tmax=0.2):
    a,c,L=klassen(); H,W=c.shape; fg=c>0
    own=np.full((H,W),-1)
    for v in range(110):
        for u in range(W):
            if fg[v,u]: own[v,u]=eigenaar(u+.5,v+.5)
    bd=fg&~(np.roll(fg,1,0)&np.roll(fg,-1,0)&np.roll(fg,1,1)&np.roll(fg,-1,1))
    out={}
    for i in (2,3,4):
        cx,cy=MOND[i][0],MOND[i][1]
        vs,us=np.where(bd&(own==i))
        t=np.arctan2(vs+.5-cy,us+.5-cx); r=np.hypot(us+.5-cx,vs+.5-cy)
        m=t<tmax; t,r,us,vs=t[m],r[m],us[m],vs[m]
        o=np.argsort(t); t,r,us,vs=t[o],r[o],us[o],vs[o]
        tips=[]
        for k in range(len(t)):
            w=np.abs(t-t[k])<venster
            if r[k]>=r[w].max()-1e-9 and r[k]>0.8*np.median(r) and (not tips or abs(t[k]-tips[-1][0])>scheiding):
                tips.append((t[k],X0+(us[k]+.5-U0)*S,Y0+(vs[k]+.5-V0)*S))
        # gat > 0,6 rad tussen twee punten (vlakke bovenrand: geen lokaal maximum in r): verste randpunt rond het midden
        extra=[]
        for (t0,_,_),(t1,_,_) in zip(tips,tips[1:]):
            if t1-t0>0.6:
                tm=(t0+t1)/2; w=np.abs(t-tm)<0.08
                if w.any():
                    k=np.where(w)[0][np.argmax(r[w])]; extra.append((t[k],X0+(us[k]+.5-U0)*S,Y0+(vs[k]+.5-V0)*S))
        out[i]=sorted(tips+extra)
    return out
if __name__=='__main__':
    import sys
    for i,tp in punten(*map(float,sys.argv[1:])).items(): print(AN[i][0],len(tp),[(round(np.degrees(q)),round(x,1),round(y,1)) for q,x,y in tp])
