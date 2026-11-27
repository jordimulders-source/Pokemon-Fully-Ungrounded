# Gedeelde code fase 1 (geen neveneffecten bij import): groepen op het natieve model + kale reductie.
import numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
H,W=N.shape[:2]
L=N.mean(2); MX=N.max(2); MN=N.min(2)
R,G,B=N[...,0],N[...,1],N[...,2]
yy,xx=np.mgrid[0:H,0:W]
FIG=MN<225
ZW=FIG&(MX<45)
neutraal=(np.abs(R-G)<10)&(np.abs(G-B)<12)
# groepen: 0 achtergrond 1 zwart 2 snavel 3 bruin (kop+rug) 5 creme 6 poten 7 oog
GR=np.zeros((H,W),int)
GR[FIG]=3
GR[FIG&(L>=168)]=5
SNAVEL=FIG&~ZW&(yy<=50)&((xx<=28)|(neutraal&(xx<=40)&(yy>=32)&(L<130)))
GR[SNAVEL]=2
POOT=FIG&~ZW&(L<168)&(((yy>=71)&(xx<=45))|((yy>=70)&(xx>=53)&(xx<=61)))
POOT|=FIG&~ZW&(R-G>45)&(yy>=69)
GR[POOT]=6
OOG=FIG&~ZW&(R>170)&(G>140)&(B<140)&(xx>=44)&(xx<=50)&(yy>=31)&(yy<=37)
GR[OOG]=7
GR[ZW]=1
GNAAM={1:'zwart',2:'snavel',3:'bruin',5:'creme',6:'poten',7:'oog'}
KOP=(yy<=47)   # alleen informatief (zones in het rapport)

X0,Y0,X1,Y1=20,21,80,80      # natieve bbox (excl.)
S=0.75                       # 60 natief -> 45 sprite
OX=10; OY=18   # onderrand figuur op y=62
SUB=8
def reductie(S=S,OX=OX,OY=OY):
    cov=np.zeros((64,64,8)); col=np.zeros((64,64,8,3)); lum=np.zeros((64,64,8)); cel=np.zeros((64,64))
    for j in range(Y0*SUB,Y1*SUB):
        ny=j//SUB; py=OY+((j+0.5)/SUB-Y0)*S; Y=int(np.floor(py))
        if not 0<=Y<64: continue
        for i in range(X0*SUB,X1*SUB):
            nx=i//SUB; px=OX+((i+0.5)/SUB-X0)*S; X=int(np.floor(px))
            if not 0<=X<64: continue
            g=GR[ny,nx]; cel[Y,X]+=1; cov[Y,X,g]+=1; col[Y,X,g]+=N[ny,nx]; lum[Y,X,g]+=L[ny,nx]
    return cov,col,lum,cel

# Palet: eigen indices per groep (swaps triviaal). Tinten: k-means op de modelkleuren per groep (palet.py).
PAL=[(255,255,255),        # 0 transparant
     (16,16,16),           # 1 zwart
     (60,60,57),(104,100,94),(222,212,188),   # 2-4 snavel donker/midden/licht(punt)
     (60,50,47),(90,75,67),(132,113,95),      # 5-7 bruin (kop+rug) donker/midden/licht
     (170,152,124),(200,182,150),(239,229,204), # 8-10 creme donker/midden/licht
     (92,66,52),(150,104,80),(214,136,100),   # 11-13 poten donker/midden/licht(oranje)
     (240,236,232),(214,186,112)]             # 14 oog wit (glans), 15 oog geel (iris)
GIDX={1:[1],2:[2,3,4],3:[5,6,7],5:[8,9,10],6:[11,12,13],7:[14,15]}
GROEPIDX={'zwart':[1],'snavel':[2,3,4],'bruin':[5,6,7],'creme':[8,9,10],'poten':[11,12,13],'oog':[14,15]}
def dichtst(g,c,pal=None):
    pal=pal or PAL; ids=GIDX[g]; d=[((np.array(pal[i])-c)**2).sum() for i in ids]; return ids[int(np.argmin(d))]
def kaal(TB=0.34,FT=0.5,pal=None):
    cov,col,lum,cel=reductie()
    Sx=np.zeros((64,64),int); G2=np.zeros((64,64),int); ML=np.zeros((64,64))
    for y in range(64):
        for x in range(64):
            n=cel[y,x]
            if n==0: continue
            if cov[y,x,1:].sum()/n<FT: continue
            if cov[y,x,1]/n>=TB: Sx[y,x]=1; G2[y,x]=1; continue
            g=2+int(np.argmax(cov[y,x,2:]))
            c=col[y,x,g]/cov[y,x,g]; ML[y,x]=lum[y,x,g]/cov[y,x,g]
            Sx[y,x]=dichtst(g,c,pal); G2[y,x]=g
    return Sx,G2,ML
def opslaan(Sx,pad,pal=None):
    im=Image.fromarray(Sx.astype('uint8'),'P'); p=[]
    for c in (pal or PAL): p+=list(c)
    im.putpalette(p+[0]*(768-len(p))); im.save(pad,transparency=0)
def rgba(Sx,pal=None,k=1):
    pal=pal or PAL; a=np.zeros((64,64,4),'uint8')
    for i,c in enumerate(pal): a[Sx==i,:3]=c
    a[...,3]=np.where(Sx>0,255,0)
    im=Image.fromarray(a,'RGBA'); return im.resize((64*k,64*k),Image.NEAREST) if k>1 else im
