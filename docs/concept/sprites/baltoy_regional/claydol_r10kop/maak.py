# Claydol: kop van Gemini r10 (zonder zijn krans-rondjes en punt) op g3r5 palet B; krans, punt, lijf, staven diff 0.
import os, sys, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from lagen import G, PAL, masks
from pas import pas_z
TOON={'k':7,'d':5,'m':4,'l':3,'h':2,'c':1,'g':6,'r':9,'R':9}   # dichtstbijzijnde paletkleur; r (donkerrood) naar rood 9 i.p.v. lijn 7
OX,OY=11,6
def rand_k(R):
    """k-pixels van de r10-koprand (aan '.' grenzend, ook diagonaal) -> niet gebruiken, onze omlijning blijft"""
    h,w=R.shape; P=np.pad(R,1,constant_values='.'); out=np.zeros((h,w),bool)
    for y in range(h):
        for x in range(w):
            if R[y,x]=='k' and (P[y:y+3,x:x+3]=='.').any(): out[y,x]=True
    return out
def bouw(rz,cz,Y0=16,ox=None,oy=None):
    global OX,OY
    if ox is not None: OX=ox
    if oy is not None: OY=oy
    R,ri,ci,rw,cw=pas_z(rz,cz,Y0)
    rk=rand_k(R); geldig=(R!='.')&~rk
    kop,kin,bol,punt=masks()
    S=G.copy(); bron={}
    # buurvulling alleen met kopsteen, niet met de oogringen (ogen natief: links (25.5,44) r7.5, rechts (47,44.5) r8)
    ny=np.array(ri)[:,None]+0*np.array(ci)[None,:]; nx=0*np.array(ri)[:,None]+np.array(ci)[None,:]
    oog=((nx-25.5)**2+(ny-44)**2<=7.5**2)|((nx-47)**2+(ny-44.5)**2<=8**2)
    gy,gx=np.where(geldig&np.isin(R,list('hlmd'))&~oog)
    for y,x in zip(*np.where(kin)):
        ry,rx=y-OY,x-OX
        if 0<=ry<R.shape[0] and 0<=rx<R.shape[1] and geldig[ry,rx]:
            S[y,x]=TOON[R[ry,rx]]; bron[(y,x)]='r10'
        else:   # buiten de r10-kop of op zijn rand: dichtstbijzijnde r10-kopsteen
            d=(gy-ry)**2+(gx-rx)**2; i=d.argmin(); S[y,x]=TOON[R[gy[i],gx[i]]]; bron[(y,x)]='r10 buur'
    return S,bron,(R,ri,ci,rw,cw)
def check(S):
    assert ((S>0)==(G>0)).all(),'silhouet'
    kop,kin,bol,punt=masks()
    assert not ((S!=G)&~kin).any(),'buiten kop'
def save(S,pad):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad+'.png',transparency=0)
    im.resize((512,512),Image.NEAREST).save(pad+'_8x.png',transparency=0)
if __name__=='__main__':
    RZ=[(16,30,8),(31,53,4),(54,66,5)]; CZ=[(19,32,3),(33,40,2),(41,54,3),(55,80,10)]
    S,b,info=bouw(RZ,CZ); check(S); save(S,os.path.join(H,'proef'))
    print(sum(v=='r10 buur' for v in b.values()),'buur;',len(b))

RZ=[(16,30,9),(31,53,4),(54,66,5)]; CZ=[(19,32,3),(33,40,2),(41,54,3),(55,80,11)]   # gekozen: kop 1 rij lager (oy 7), 1 px naar rechts (ox 12)
def aa_weg(S):
    """r10-'d'-antialiaspixels op de rand van de rode band (losse 5 tegen rood) -> steen ernaast (meest voorkomende niet-rode buur)"""
    from lagen import masks
    kop,kin,bol,punt=masks(); T=S.copy(); log=[]
    for y,x in zip(*np.where(kin&(S==5))):
        nb=[S[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
        if 9 not in nb or sum(v==5 for v in nb)>0 or (y,x)==(21,25): continue   # (21,25) = bovenkant neus tussen de V-poten: blijft
        st=[v for v in nb if v not in (9,7,5)]
        if st: T[y,x]=max(set(st),key=st.count); log.append(((int(y),int(x)),int(T[y,x])))
    return T,log
def lever():
    S,b,info=bouw(RZ,CZ,ox=12,oy=7); check(S); save(S,os.path.join(H,'claydol_r10kop_ruw'))
    T,log=aa_weg(S); check(T); save(T,os.path.join(H,'claydol_r10kop'))
    return S,T,b,info,log
