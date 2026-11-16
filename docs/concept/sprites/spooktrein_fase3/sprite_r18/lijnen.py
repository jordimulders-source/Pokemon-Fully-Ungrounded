# Modellijnen koeienvanger: natieve lijnpixels (lum<THR, geen groen/wit), Zhang-Suen-skelet, per pixel geprojecteerd naar het spriteraster.
from proj import *
G=(N[...,1]>N[...,0]+20); WIT=N.min(2)>215
def zhang(m):
    m=m.copy().astype(np.uint8)
    while True:
        ch=False
        for st in (0,1):
            P=np.pad(m,1)
            p2,p3,p4,p5,p6,p7,p8,p9=P[:-2,1:-1],P[:-2,2:],P[1:-1,2:],P[2:,2:],P[2:,1:-1],P[2:,:-2],P[1:-1,:-2],P[:-2,:-2]
            B=p2+p3+p4+p5+p6+p7+p8+p9
            seq=[p2,p3,p4,p5,p6,p7,p8,p9,p2]
            A=sum(((seq[i]==0)&(seq[i+1]==1)).astype(int) for i in range(8))
            if st==0: c=(p2*p4*p6==0)&(p4*p6*p8==0)
            else: c=(p2*p4*p8==0)&(p2*p6*p8==0)
            d=(m==1)&(B>=2)&(B<=6)&(A==1)&c
            if d.any(): m[d]=0; ch=True
        if not ch: return m.astype(bool)
def lijnmasker(THR=52, ny0=63, ny1=84, nx0=9, nx1=42):
    L=np.zeros_like(G)
    sub=(LUM<THR)&~G&~WIT
    L[ny0:ny1,nx0:nx1]=sub[ny0:ny1,nx0:nx1]
    return L
def projecteer(S):
    out={}
    for ny,nx in zip(*np.where(S)):
        X,Y=n2s(nx+.5,ny+.5); out.setdefault((int(Y),int(X)),[]).append((ny,nx))
    return out
