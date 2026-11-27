# Kale reductie van het natieve model (+ optioneel snavel vergroot als script op het model, vóór de reductie).
# Niets getekend: elke spritepixel komt uit zijn vlak modelpixels (oppervlakgewogen op een 4x-onderraster).
import numpy as np; from PIL import Image
from klassen import klassen, OOG, OOGR
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
K,LUM=klassen(N)
ANKER=(71.0,62.0)          # mondhoek (natief), gemeten op kop.png
SUB=4
def lab(mask):
    from scipy import ndimage; return ndimage.label(mask)
def snavelmasker():
    from morf import dil,closing
    yy,xx=np.mgrid[0:N.shape[0],0:N.shape[1]]
    s3=(K==3)
    M=(dil(s3,2)&((K==3)|(K==1)))&(xx<74)
    # gesloten vorm (mondopening = achtergrond binnen de snavel hoort erbij)
    C=closing(M,4)&(xx<74)
    P=M|(C&(K==0))
    return M,P
def fijn(f=1.0):
    """4x-onderraster (kleur, klasse); bij f>1 snavel (incl. mondopening) vergroot rond ANKER."""
    c=np.kron(N,np.ones((SUB,SUB,1),int)); k=np.kron(K,np.ones((SUB,SUB),int)); l=np.kron(LUM,np.ones((SUB,SUB)))
    if f==1.0: return c,k,l,None
    M,P=snavelmasker()
    H,W=k.shape; ty,tx=np.mgrid[-200:H,-200:W] if False else (None,None)
    # doelraster mag links/boven buiten het oude beeld groeien: vergroot het canvas links met PAD
    PAD=int(np.ceil((ANKER[0]-0)*(f-1)))*SUB+SUB*4
    H2,W2=H+PAD,W+PAD
    c2=np.full((H2,W2,3),255); k2=np.zeros((H2,W2),int); l2=np.full((H2,W2),255.)
    c2[PAD:,PAD:]=c; k2[PAD:,PAD:]=k; l2[PAD:,PAD:]=l
    yy,xx=np.mgrid[0:H2,0:W2]
    # doelpixel (fijn) -> natieve bronpositie
    u=((xx-PAD+0.5)/SUB-ANKER[0])/f+ANKER[0]; v=((yy-PAD+0.5)/SUB-ANKER[1])/f+ANKER[1]
    ui=np.floor(u).astype(int); vi=np.floor(v).astype(int)
    ok=(ui>=0)&(vi>=0)&(ui<N.shape[1])&(vi<N.shape[0])
    src=np.zeros_like(ok); src[ok]=P[vi[ok],ui[ok]]
    # oog nooit overschrijven
    nu=(xx-PAD+0.5)/SUB; nv=(yy-PAD+0.5)/SUB
    oogz=(nu-OOG[0])**2+(nv-OOG[1])**2<=(OOGR+1)**2
    zet=src&~oogz
    c2[zet]=N[vi[zet],ui[zet]]; k2[zet]=K[vi[zet],ui[zet]]; l2[zet]=LUM[vi[zet],ui[zet]]
    # oude snavelpixels die niet meer door de nieuwe snavel bedekt worden -> achtergrond (gemeld)
    oud=np.zeros((H2,W2),bool); oud[PAD:,PAD:]=np.kron(P,np.ones((SUB,SUB),bool))
    rest=oud&~zet&~oogz
    c2[rest]=255; k2[rest]=0; l2[rest]=255
    return c2,k2,l2,(PAD,int(rest.sum()))
# tintdrempels per groep op gemiddelde modelhelderheid: (lijn, donker, midden, licht)
DREMPEL={2:(70,102,124),3:(130,172,204),4:(None,158,None),5:(112,146,None)}
def reduceer(f=1.0,s=None,rechts=63,onder=63):
    """s = spritepx per natieve px. Rechterrand natief 175 -> X=rechts, onderrand natief 170 -> Y=onder."""
    c,k,l,info=fijn(f); PAD=info[0] if info else 0
    if s is None: s=62/154
    fs=s/SUB   # spritepx per fijne px
    # fijne coördinaat (zonder PAD) 175*SUB -> rechts ; 170*SUB -> onder
    H2,W2=k.shape
    X=np.floor(rechts+((np.arange(W2)-PAD+0.5)-175*SUB)*fs).astype(int)
    Y=np.floor(onder+((np.arange(H2)-PAD+0.5)-170*SUB)*fs).astype(int)
    o=np.zeros((64,64),int); g=np.zeros((64,64),int); cov={}
    tel=np.zeros((64,64,8)); lsum=np.zeros((64,64,8))
    for j in range(H2):
        yj=Y[j]
        if not 0<=yj<64: 
            if (k[j]>0).any(): raise SystemExit('buiten 64 (y) %d'%yj)
            continue
        row=k[j]; lr=l[j]
        for i in np.where(row>0)[0]:
            xi=X[i]
            if not 0<=xi<64: raise SystemExit('buiten 64 (x) %d'%xi)
            tel[yj,xi,row[i]]+=1; lsum[yj,xi,row[i]]+=lr[i]
    cel=np.zeros((64,64))
    for j in range(H2):
        if 0<=Y[j]<64:
            xs=X[(X>=0)&(X<64)]; np.add.at(cel[Y[j]],xs,1)
    return tel,lsum,cel,s,info
def indexeer(tel,lsum,cel,TB=0.28):
    """kale reductie -> (groep, tintklasse) per pixel. tint: 0 lijn,1 donker,2 midden,3 licht"""
    G=np.zeros((64,64),int); T=np.zeros((64,64),int)
    for y in range(64):
        for x in range(64):
            n=cel[y,x]
            if n==0: continue
            t=tel[y,x]; fig=t[1:].sum()
            if fig/n<0.5: continue
            zw=(t[1]+t[7])/n
            if zw>=TB: G[y,x]=1; continue
            gg=2+int(np.argmax(t[2:7])); G[y,x]=gg
            m=lsum[y,x,gg]/t[gg]
            if gg==6: T[y,x]=2; continue
            d=DREMPEL[gg]
            if gg==4: T[y,x]=1 if m<d[1] else 3; continue
            if gg==5: T[y,x]=0 if m<d[0] else (2 if m<d[1] else 3); continue
            T[y,x]=0 if m<d[0] else (1 if m<d[1] else (2 if m<d[2] else 3))
    return G,T
