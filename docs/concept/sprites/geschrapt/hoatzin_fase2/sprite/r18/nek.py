# r18 stap 2: nek los van de vleugel, ALLEEN kleur binnen de bestaande r17-pixels (alpha-diff 0).
# Lijn doorlopend: per rij binnen 1 px van de rij erboven.
# Per rij y 23-40: xe = eerste lichte vleugelrandpixel (tint 5) in r17 (de vleugelvoorrand). De grenslijn ligt op de
# donkerste modelpixel (meeste natieve px met L<45) in xe-3..xe-1 -> lijn 1 (1 px). Tussen lijn en xe: vleugelrand -> 4.
# Links van de lijn (alleen y>=27, onder de kop): nek -> eigen tinten: model gem. L>=96 en weinig donker -> 4, anders 3 (was 2).
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../r1/natief.png').convert('RGB')).astype(float); L=a@[.299,.587,.114]; bg=a.min(2)>225
OX,OY,PX,PY=7,3,32,7
def meet(x,y):
    ny=PY+3*(y-OY); nx=PX+3*(x-OX); b=bg[ny:ny+3,nx:nx+3]; l=L[ny:ny+3,nx:nx+3]
    g=l[(~b)&(l>=45)]; return int(((~b)&(l<45)).sum()), (g.mean() if g.size else 0)
MAUVE=(1,2,3,4,5)
def nek(base):
    out=base.copy(); log=[]; lijn={}
    def zet(x,y,v,w):
        if base[y,x] not in MAUVE: return
        if out[y,x]!=v: log.append((w,x,y,int(out[y,x]),v)); out[y,x]=v
    for y in range(23,41):
        xs=[x for x in range(22,36) if base[y,x]==5]
        if not xs: continue
        xe=xs[0]
        kand=[x for x in range(xe-3,xe) if base[y,x] in MAUVE]
        if not kand: continue
        xl=max(kand,key=lambda x:(meet(x,y)[0],x))
        if y-1 in lijn and abs(xl-lijn[y-1])>1:            # doorlopend: binnen 1 px van de rij erboven, dan de donkerste daarvan
            k2=[x for x in kand if abs(x-lijn[y-1])<=1]
            if k2: xl=max(k2,key=lambda x:(meet(x,y)[0],x))
        lijn[y]=xl; zet(xl,y,1,'grenslijn')
        for x in range(xl+1,xe): zet(x,y,4,'vleugelrand')
        if y>=27:
            front=[x for x in range(10,xl) if base[y,x]>0][0]
            for x in range(front+1,xl):
                if base[y,x]==2:
                    d,g=meet(x,y); zet(x,y,4 if (g>=96 and d<=3) else 3,'nek')
    return out,log,lijn
if __name__=='__main__':
    r=np.array(Image.open('../r17/hoatzin.png')); o,log,lijn=nek(r)
    from collections import Counter; print(Counter(l[0] for l in log)); print(lijn)
    for y in range(20,42): print('%2d '%y+''.join('.' if v==0 else '%x'%v for v in o[y,14:37]),'  ',''.join('.' if v==0 else '%x'%v for v in r[y,14:37]))
