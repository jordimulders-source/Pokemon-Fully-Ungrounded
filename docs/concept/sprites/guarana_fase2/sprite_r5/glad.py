# r4 stap 0b: buitenrand glad maken (Jordi r2: "De hele sprite is hoekig"; coordinator r4: trapjes weg, geen losse uitstekers,
# lijnsprongen 1-2-3, binnen +-1 px van het model). Masker licht vervaagd (gauss 0,8) en opnieuw op 0,5 gedrempeld, met beschermingen:
#  - weghalen alleen waar het deel breed is (>= 5 voorgrond-8-buren) of een losse uitsteker van 1 px op een brede rand; dunne ranken/klauwtjes blijven;
#  - erbij alleen in een inham (>= 5 voorgrond-8-buren) en met de kleurgroep van de meeste buren;
#  - het aantal samenhangende delen (8-buren) blijft gelijk, geen gat in een lus wordt dichtgemaakt (achtergrond blijft verbonden).
import numpy as np
N8=[(a,b) for a in (-1,0,1) for b in (-1,0,1) if a or b]
def gauss(m,s):
    r=int(np.ceil(3*s)); k=np.exp(-np.arange(-r,r+1)**2/(2*s*s)); k/=k.sum()
    p=np.pad(m.astype(float),r)
    p=np.apply_along_axis(lambda v:np.convolve(v,k,'same'),0,p); p=np.apply_along_axis(lambda v:np.convolve(v,k,'same'),1,p)
    return p[r:-r,r:-r]
def ncomp(m):
    lab=np.zeros(m.shape,int);k=0
    for y,x in zip(*np.where(m)):
        if lab[y,x]: continue
        k+=1; st=[(y,x)]; lab[y,x]=k
        while st:
            cy,cx=st.pop()
            for dy,dx in N8:
                yy,xx=cy+dy,cx+dx
                if 0<=yy<m.shape[0] and 0<=xx<m.shape[1] and m[yy,xx] and not lab[yy,xx]: lab[yy,xx]=k; st.append((yy,xx))
    return k
def bgcomp(m):   # achtergronddelen (4-buren) incl. gaten in lussen
    b=~m; lab=np.zeros(m.shape,int);k=0
    for y,x in zip(*np.where(b)):
        if lab[y,x]: continue
        k+=1; st=[(y,x)]; lab[y,x]=k
        while st:
            cy,cx=st.pop()
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=cy+dy,cx+dx
                if 0<=yy<m.shape[0] and 0<=xx<m.shape[1] and b[yy,xx] and not lab[yy,xx]: lab[yy,xx]=k; st.append((yy,xx))
    return k
def glad(o,s=0.8):
    M=o>0; G=gauss(M,s); n0=ncomp(M); b0=bgcomp(M); weg=[]; bij=[]
    def nb(m,y,x): return sum(1 for dy,dx in N8 if 0<=y+dy<64 and 0<=x+dx<64 and m[y+dy,x+dx])
    for y,x in sorted(zip(*np.where(M&(G<0.5))),key=lambda p:G[p]):
        f4=[(y+dy,x+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<64 and 0<=x+dx<64 and M[y+dy,x+dx]]
        def dik(q): return sum(1 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=q[0]+dy<64 and 0<=q[1]+dx<64 and M[q[0]+dy,q[1]+dx])>=3
        uitsteker=len(f4)==1 and dik(f4[0]) and nb(M,y,x)>=3
        if nb(M,y,x)>=5 or uitsteker:
            M[y,x]=False
            if ncomp(M)!=n0 or bgcomp(M)!=b0: M[y,x]=True
            else: weg.append((x,y))
    for y,x in sorted(zip(*np.where(~M&(G>=0.5))),key=lambda p:-G[p]):
        if nb(M,y,x)>=5:
            M[y,x]=True
            if ncomp(M)!=n0 or bgcomp(M)!=b0: M[y,x]=False
            else: bij.append((x,y))
    for x,y in weg: o[y,x]=0
    for x,y in bij:
        buren=[o[y+dy,x+dx] for dy,dx in N8 if 0<=y+dy<64 and 0<=x+dx<64 and o[y+dy,x+dx]>0]
        o[y,x]=max(set(buren),key=buren.count)
    return weg,bij
