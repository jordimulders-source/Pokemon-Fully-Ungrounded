# r12: paneelrecept van herstel10 (rand navy/zwart, lichte rand, vaktint per vak, rasterlijnen) als functie, per paneel.
import numpy as np
S=3.515625; TOP=13
SY,SX=np.mgrid[0:64,0:64]; MX=3+(SX+.5)*S; MY=3+(SY-TOP+.5)*S
TINT={'PD':[14,13,13,11],'PE':[14,13,13,11],'PA':[13,13,11,11],'PC':[13,13,11,11],'PB':[14,13,13],'PF':[14,13,11]}
LIJN={'PA':[.25,.5,.75],'PC':[.25,.5,.75],'PD':[.25,.5,.75],'PE':[.25,.5,.75],'PB':[1/3,2/3],'PF':[1/3,2/3]}
def uvf(g,mx,my):
    T,R,L=map(lambda p:np.array(p,float),g); Mx=np.array([R-T,L-T]).T; inv=np.linalg.inv(Mx)
    d=np.stack([mx-T[0],my-T[1]]); r=np.tensordot(inv,d,1); return r[0],r[1]
def ideaal(g):
    u,v=uvf(g,MX,MY); return (u>=0)&(u<=1)&(v>=0)&(v<=1)
def recept(k,g,P):
    """kleur per pixel van paneel k (P==k), geometrie g=(T,R,L) in modelcoordinaten."""
    T,R,L=map(np.array,g); d=L-T; vlak=abs(d[0])>=abs(d[1])
    u,_=uvf(g,MX,MY)
    du=np.abs(uvf(g,MX,MY+S)[0]-u) if vlak else np.abs(uvf(g,MX+S,MY)[0]-u)
    ID=ideaal(g); NEW={}
    def binnen(xx,yy): return 0<=xx<64 and 0<=yy<64 and ID[yy,xx] and P[yy,xx]!=''
    for y,x in zip(*np.where(P==k)):
        bo,on,li,re=binnen(x,y-1),binnen(x,y+1),binnen(x-1,y),binnen(x+1,y)
        if not(bo and on and li and re): NEW[(x,y)]=1 if (not on or (not re and bo)) else 2; continue
        uu=u[y,x]; i=int(np.clip(np.searchsorted(LIJN[k],uu),0,len(TINT[k])-1)); vt=TINT[k][i]
        if any(abs(uu-p)<=du[y,x]/2+1e-9 for p in LIJN[k]): NEW[(x,y)]=-(14 if vt==11 else 12); continue
        NEW[(x,y)]=vt
    own=lambda x,y: P[y,x] if 0<=x<64 and 0<=y<64 else ''
    for (x,y),c in list(NEW.items()):
        if c not in (14,13,11): continue
        for dy,dx in ((-1,0),(0,-1)):
            a,b=(x+dx,y+dy),(x-dx,y-dy)
            if own(*a)==k and NEW.get(a)==2 and own(*b)==k and (NEW.get(b,0) in (14,13,11) or NEW.get(b,0)<0):
                NEW[(x,y)]=12; break
    return {p:abs(c) for p,c in NEW.items()}
