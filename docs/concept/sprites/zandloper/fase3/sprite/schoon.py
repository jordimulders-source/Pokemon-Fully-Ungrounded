# Technisch opschonen op labelniveau: alleen tinten wisselen binnen een materiaal en losse lijnpixels weghalen.
import numpy as np
N4=[(0,1),(0,-1),(1,0),(-1,0)]; N8=N4+[(1,1),(1,-1),(-1,1),(-1,-1)]
def mat_of(l): return 0 if l==0 else (-1 if l==1 else l//10)   # zand 1x -> 1, glas 2x -> 2, hout 3x -> 3, lijn -> -1
def comps(mask):
    H,W=mask.shape; seen=np.zeros_like(mask,bool); out=[]
    for y in range(H):
        for x in range(W):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)]; seen[y,x]=1; c=[]
                while st:
                    p=st.pop(); c.append(p)
                    for dy,dx in N8:
                        q=(p[0]+dy,p[1]+dx)
                        if 0<=q[0]<H and 0<=q[1]<W and mask[q] and not seen[q]: seen[q]=1; st.append(q)
                out.append(c)
    return out
def comps4(mask):
    H,W=mask.shape; seen=np.zeros_like(mask,bool); out=[]
    for y in range(H):
        for x in range(W):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)]; seen[y,x]=1; c=[]
                while st:
                    p=st.pop(); c.append(p)
                    for dy,dx in N4:
                        q=(p[0]+dy,p[1]+dx)
                        if 0<=q[0]<H and 0<=q[1]<W and mask[q] and not seen[q]: seen[q]=1; st.append(q)
                out.append(c)
    return out
def buurtint(lab,p,mat,uitsluit):
    H,W=lab.shape; c={}
    for dy,dx in N8:
        y,x=p[0]+dy,p[1]+dx
        if 0<=y<H and 0<=x<W and mat_of(lab[y,x])==mat and (y,x) not in uitsluit:
            c[lab[y,x]]=c.get(lab[y,x],0)+1
    return max(c,key=c.get) if c else None
def tintclusters(lab,minpx=3,beschermd=None):
    """Tintvlakjes < minpx nemen de meest voorkomende buurtint van hetzelfde materiaal aan."""
    for _ in range(4):
        ch=0
        for t in np.unique(lab):
            if t<10: continue
            for c in comps4(lab==t):
                if len(c)>=minpx: continue
                if beschermd is not None and any(beschermd[p] for p in c): continue
                s=set(c)
                for p in c:
                    n=buurtint(lab,p,t//10,s)
                    if n is not None and n!=t: lab[p]=n; ch+=1
        if not ch: break
    return lab
def losse_lijnen(lab,minpx,zone=None):
    """Binnenlijn-componenten kleiner dan minpx weghalen (niet aan de buitenrand)."""
    H,W=lab.shape
    for c in comps(lab==1):
        if len(c)>=minpx: continue
        if zone is not None and not all(zone[p] for p in c): continue
        rand=any(lab[p[0]+dy,p[1]+dx]==0 for p in c for dy,dx in N4 if 0<=p[0]+dy<H and 0<=p[1]+dx<W)
        if rand: continue
        s=set(c)
        for p in c:
            for mat in (1,2,3):
                n=buurtint(lab,p,mat,s)
                if n: lab[p]=n; break
    return lab
