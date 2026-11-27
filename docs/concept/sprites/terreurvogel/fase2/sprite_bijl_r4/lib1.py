# Gedeelde code (geen neveneffecten bij import): klassen op het natieve model en de kale reductie.
import numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
H,W=N.shape[:2]
L=N.mean(2); MX=N.max(2); MN=N.min(2)
R,G,B=N[...,0],N[...,1],N[...,2]
yy,xx=np.mgrid[0:H,0:W]
FIG=MN<225
ZW=FIG&(MX<40)                       # zwart (omlijning in het model)
grijs=FIG&~ZW&(np.abs(R-B)<22)&(np.abs(R-G)<16)
# groepen: 0 achtergrond, 1 zwart, 2 snavel, 3 lijf, 4 roest/kuif, 5 poten, 6 oog
GR=np.zeros((H,W),int)
GR[FIG]=3
warm=FIG&~ZW&(R-G>30)
GR[warm]=4
SNAVEL=grijs&(xx<=29)&(yy<=53)
GR[SNAVEL]=2
POOT=FIG&~ZW&~grijs&(yy>=55)&((xx<=50)|(xx>=70))
POOT|=FIG&~ZW&(yy>=60)&(xx>=72)          # rechterpoot ook donkere schubben
POOT|=FIG&~ZW&(yy>=62)&(xx<=50)
GR[POOT]=5
TEEN=POOT&(R-G>28)
GR[TEEN]=8
ORANJE=FIG&~ZW&(R-G>55)&(G>=85)&~POOT
GR[ORANJE]=7
# oog (gemeten op het natieve model): hooglicht + rode iris binnen het zwarte oogmasker
OOGPX=[(27,32),(27,33),(26,33),(25,34),(26,34)]
for (x,y) in OOGPX: GR[y,x]=6
GR[ZW]=1
GNAAM={1:'zwart',2:'snavel',3:'lijf',4:'roest',5:'poten',6:'oog',7:'oranje'}

S=63/94.0          # spritepx per natieve px (94 natieve px breed -> 63)
X0=2; Y0=22        # natieve bbox linksboven
OX=0; OY=62-int(np.ceil(59*S))+1   # onderrand figuur op y=62
SUB=8
def reductie(S=S,OX=OX,OY=OY):
    """per spritepixel: dekking per groep (oppervlak) + somkleur per groep."""
    cov=np.zeros((64,64,9)); col=np.zeros((64,64,9,3)); lum=np.zeros((64,64,9))
    cel=np.zeros((64,64))
    for j in range(H*SUB):
        ny=j//SUB; py=OY+((j+0.5)/SUB-Y0)*S; Y=int(np.floor(py))
        if not 0<=Y<64: continue
        for i in range(W*SUB):
            nx=i//SUB; px=OX+((i+0.5)/SUB-X0)*S; X=int(np.floor(px))
            if not 0<=X<64: continue
            g=GR[ny,nx]; cel[Y,X]+=1
            cov[Y,X,g]+=1; col[Y,X,g]+=N[ny,nx]; lum[Y,X,g]+=L[ny,nx]
    return cov,col,lum,cel

# Palet (modelkleuren via k-means per groep; Gen 3-tinten). Index -> (groep, rgb)
PAL=[(255,255,255),   # 0 transparant
     (16,16,16),      # 1 zwart (gedeeld)
     (240,236,232),   # 2 wit (gedeeld, ooghooglicht)
     (67,67,67),(94,90,95),(165,165,164),          # 3-5 snavel donker/midden/licht (staal, modelkleuren)
     (77,70,65),(126,109,88),(162,142,112),        # 6-8 lijf donker/midden/licht
     (107,61,51),(147,55,52),(158,111,90),(192,120,84),  # 9-12 roest donker/rood/tan(kuif)/oranje
     (78,68,57),(148,129,105),(224,189,149)]       # 13-15 poten donker/midden/licht(tenen)
GIDX={1:[1],2:[3,4,5],3:[6,7,8],4:[9,10,11],5:[13,14,15],6:[10,2],7:[12],8:[15]}
GROEP={1:1,2:0,3:2,4:2,5:2,6:3,7:3,8:3,9:4,10:4,11:4,12:4,13:5,14:5,15:5}  # index -> groep (2 wit = 0)
def dichtst(g,c):
    ids=GIDX[g]; d=[((np.array(PAL[i])-c)**2).sum() for i in ids]; return ids[int(np.argmin(d))]
def kaal(TB=0.34,FT=0.5):
    cov,col,lum,cel=reductie()
    S=np.zeros((64,64),int); G2=np.zeros((64,64),int)
    for y in range(64):
        for x in range(64):
            n=cel[y,x]
            if n==0: continue
            fig=cov[y,x,1:].sum()/n
            if fig<FT: continue
            if cov[y,x,1]/n>=TB: S[y,x]=1; G2[y,x]=1; continue
            g=2+int(np.argmax(cov[y,x,2:]))
            if g==5 and cov[y,x,8]/n>=0.3: g=8
            c=col[y,x,g]/cov[y,x,g]
            S[y,x]=dichtst(g if g!=6 else 4,c)
            G2[y,x]=g
    return S,G2
def opslaan(S,pad,pal=None):
    im=Image.fromarray(S.astype('uint8'),'P'); p=[]
    for c in (pal or PAL): p+=list(c)
    im.putpalette(p+[0]*(768-len(p))); im.save(pad,transparency=0)

def L_(i): return sum(PAL[int(i)])/3
