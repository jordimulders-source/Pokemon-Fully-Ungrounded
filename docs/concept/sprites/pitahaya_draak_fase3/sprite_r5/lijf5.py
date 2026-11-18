# Lijf r5: rustiger lijf. Werkt op r4 (geen nieuwe toonkaart): binnenvulling Z (niet buitenrand, niet naast zwart/roze,
# buiten de zones met eigen stappen). 1) g in Z die niet op een modelrib ligt (ribben.py, LMIN 25, lum<80) -> vulling;
# 2) G/h met modusfilter 3x3 (H blijft) -> brede schaduwvlakken i.p.v. vlekken; 3) ribben = modelribskelet in Z, alleen
# 8-samenhangende stukken >= MINRIB; 4) toonclusters < 3 px naar de buurmeerderheid.
import numpy as np; from ribben import ribkaart; from lijnen import zhang
N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def comp8(m):
    seen=np.zeros(m.shape,bool); out=[]
    for y0,x0 in zip(*np.where(m)):
        if seen[y0,x0]: continue
        st=[(y0,x0)]; seen[y0,x0]=1; cl=[]
        while st:
            a,b=st.pop(); cl.append((a,b))
            for dy,dx in N8:
                c,d=a+dy,b+dx
                if 0<=c<64 and 0<=d<64 and m[c,d] and not seen[c,d]: seen[c,d]=1; st.append((c,d))
        out.append(cl)
    return out
def comp4(m):
    seen=np.zeros(m.shape,bool); out=[]
    for y0,x0 in zip(*np.where(m)):
        if seen[y0,x0]: continue
        st=[(y0,x0)]; seen[y0,x0]=1; cl=[]
        while st:
            a,b=st.pop(); cl.append((a,b))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                c,d=a+dy,b+dx
                if 0<=c<64 and 0<=d<64 and m[c,d] and not seen[c,d]: seen[c,d]=1; st.append((c,d))
        out.append(cl)
    return out
def zone(o,uitsluit):
    groen=np.isin(o,[6,7,8,9]); p=np.pad(o,1)
    buur=lambda ks: np.any([np.isin(p[1+dy:65+dy,1+dx:65+dx],ks) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))],0)
    return groen&~buur([0])&~buur([1,2,3,4,5])&~uitsluit
def lijf(o,uitsluit,LMIN=25,lum=80,MINRIB=4,iters=2):
    o=o.copy(); Z=zone(o,uitsluit)
    R=zhang((ribkaart(LMIN,lum)[0]>0))&Z
    def vul_buren(y,x):
        nb=[o[y+dy,x+dx] for dy,dx in N8 if o[y+dy,x+dx] in (7,8,9)]
        return max(set(nb),key=nb.count) if nb else 8
    for y,x in zip(*np.where(Z&(o==6)&~R)): o[y,x]=vul_buren(y,x)
    for _ in range(iters):
        n=o.copy()
        for y,x in zip(*np.where(Z&np.isin(o,[7,8]))):
            nb=[o[y+dy,x+dx] for dy,dx in N8 if o[y+dy,x+dx] in (7,8)]+[o[y,x]]
            if nb.count(7)>nb.count(8): n[y,x]=7
            elif nb.count(8)>nb.count(7): n[y,x]=8
        o=n
    for cl in comp8(R):
        if len(cl)>=MINRIB:
            for y,x in cl: o[y,x]=6
        else:
            for y,x in cl: o[y,x]=vul_buren(y,x)
    for _ in range(3):
        for k in (7,8,9):
            for cl in comp4(Z&(o==k)):
                if len(cl)<3:
                    for y,x in cl:
                        nb=[o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[y+dy,x+dx] in (7,8,9) and o[y+dy,x+dx]!=k]
                        if nb: o[y,x]=max(set(nb),key=nb.count)
    return o,Z
