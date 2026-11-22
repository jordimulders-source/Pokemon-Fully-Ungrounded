# Lijf r4: overwegend middengroen (h), schaduw G rechtsonder (volume-toonkaart), licht H alleen in een band van 2 px langs
# boven-/linkerranden, en ribben (g) als dunne lijnen uit de lange donkergroene modellijnen (ribben.py, skelet >= 14 px,
# lum < 85), op spriteniveau nogmaals verdund tot 1 px.
import numpy as np, sys; sys.path.append('../sprite_r2')
from lijnen import zhang
def comp(m):
    lab=np.zeros(m.shape,int); n=0
    for y in range(64):
        for x in range(64):
            if m[y,x] and not lab[y,x]:
                n+=1; st=[(y,x)]; lab[y,x]=n
                while st:
                    a,b=st.pop()
                    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        c,d=a+dy,b+dx
                        if 0<=c<64 and 0<=d<64 and m[c,d] and not lab[c,d]: lab[c,d]=n; st.append((c,d))
    return lab,n
def lijf(o,V,R,uitsluit,pct_schaduw=30,pct_licht=80,band=2,minrib=3):
    groen=np.isin(o,[6,7,8,9]); lab,n=comp(groen)
    groot=max(range(1,n+1),key=lambda i:(lab==i).sum()); body=(lab==groot)
    p=np.pad(o==0,1); rand=body&(p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:])
    Z=body&~rand&~uitsluit
    # buitenrand-pixels die g/G/h/H zijn blijven; Z = binnenvulling
    pos=[(y,x) for y,x in zip(*np.where(Z)) if not np.isnan(V[y,x])]
    vals=np.array([V[y,x] for y,x in pos]); qs,ql=np.percentile(vals,[pct_schaduw,pct_licht])
    niet=~body|(o==1)   # niet-lijf: achtergrond, roze, zwart
    pn=np.pad(niet,2,constant_values=True)
    for (y,x),v in zip(pos,vals):
        boven=any(pn[2+y-d,2+x] or pn[2+y,2+x-d] or pn[2+y-d,2+x-d] for d in range(1,band+1))
        o[y,x]=7 if v<qs else (9 if (v>=ql and boven) else 8)
    # ribben
    rm=zhang((R>0)&Z)
    l2,n2=comp(rm)  # 4-samenhang; korte stukjes weg
    lab8=np.zeros_like(l2)
    for y,x in zip(*np.where(rm)):
        o[y,x]=6
    # rib-stukjes korter dan minrib (8-samenhang) terug naar de vulling eromheen
    seen=np.zeros((64,64),bool)
    for y0,x0 in zip(*np.where(rm)):
        if seen[y0,x0]: continue
        st=[(y0,x0)]; seen[y0,x0]=1; cl=[]
        while st:
            a,b=st.pop(); cl.append((a,b))
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    c,d=a+dy,b+dx
                    if 0<=c<64 and 0<=d<64 and rm[c,d] and not seen[c,d]: seen[c,d]=1; st.append((c,d))
        if len(cl)<minrib:
            for a,b in cl:
                nb=[o[a+dy,b+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[a+dy,b+dx] in (7,8,9)]
                o[a,b]=max(set(nb),key=nb.count) if nb else 8
    # toonclusters < 3 px (G/h/H, zonder ribben) naar de buurmeerderheid
    from lijf import clusters
    o=clusters(o,Z&np.isin(o,[7,8,9]))
    return o,Z
