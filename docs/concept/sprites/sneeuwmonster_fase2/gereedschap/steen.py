# Stenen als eigen zone (geplakt op ±3,7 px, andere pixelmaat dan de rest): per steen de natieve klassen
# oppervlakgewogen verkleinen en per klasse het modelaandeel behouden (kwantiel-toewijzing), niets getekend.
# Vorm = spritepixels met >=45% steen; rand = omlijning (zwart) of gloed waar het model aan de rand gloeit;
# binnen: de pixels met het hoogste gloedaandeel worden scheur, zoveel als het modelaandeel gloed binnenin.
import numpy as np
from gemeen import *; from klassen import klassen
def stenen(o):
    o=o.copy(); a,c,L=klassen(); H,W=c.shape; yy,xx=np.mgrid[0:H,0:W]
    X=np.floor((xx-MX0)/F).astype(int); Y=np.floor((yy-MY0)/F).astype(int)
    x0,y0,x1,y1=STEENZONE; info=[]
    for ya,yb in ((300,380),(380,462)):
        sel=(yy>=ya)&(yy<yb)&(xx>=x0)&(xx<x1)
        Xs,Ys,cs,ls=X[sel],Y[sel],c[sel],L[sel]
        st=np.isin(cs,[1,5,6,7]); gl=np.isin(cs,[6,7]); ye=cs==7
        frac={}
        for Xv in range(Xs.min(),Xs.max()+1):
            for Yv in range(Ys.min(),Ys.max()+1):
                m=(Xs==Xv)&(Ys==Yv)
                if not m.any(): continue
                s=st[m].mean()
                if s>=0.45:
                    sm=m&st
                    frac[(Xv,Yv)]=(gl[sm].mean(),ye[sm].mean(),ls[sm&~gl].mean() if (sm&~gl).any() else 60)
        pts=set(frac)
        rand=[p for p in pts if any((p[0]+dx,p[1]+dy) not in pts for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))]
        binnen=[p for p in pts if p not in rand]
        gtot=gl[st].mean()
        for p in pts:
            if o[p[1],p[0]] in SNEEUW or o[p[1],p[0]] in (0,1) or True: o[p[1],p[0]]=12
        # rand: gloed waar >=35% gloed (rechts/onder in het model), anders zwart
        for p in rand:
            g,y,l=frac[p]; o[p[1],p[0]]=(15 if y>=0.18 else 14 if g>=0.5 else 13) if g>=0.35 else 1
        # binnen: kwantiel op gloedaandeel
        n=int(round(gtot*len(binnen))); rang=sorted(binnen,key=lambda p:-frac[p][0])
        for p in rang[:n]:
            g,y,l=frac[p]; o[p[1],p[0]]=15 if y>=0.15 else 14
        # lichtste facet (grijs in het model) op het donkere deel: hoogste modelhelderheid, 1 per steen
        rest=[p for p in binnen if p not in rang[:n]]
        if rest:
            q=max(rest,key=lambda p:frac[p][2])
            if frac[q][2]>=55: o[q[1],q[0]]=10
        info.append((len(pts),len(rand),n,round(gtot,2)))
    return o,info
