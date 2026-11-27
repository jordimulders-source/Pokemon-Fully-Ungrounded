# Manen A, ronde 2 (Jordi: "A is goed, alleen houd er rekening mee dat gemini die boog had gedaan omdat er een schouder zat,
# dus die boog hoeft geen boog meer te zijn"). Op modelniveau, alleen modelmateriaal:
# 1 verschoven kopie (+70,+30) zonder kamlokken (bron x>440 & y<530) -> geen dubbele kamrand op de schoft
# 2 boog = de oude schouderlijn van r3b (gebogen zwarte onderrand van de manen) die met de kopie mee is geschoven:
#   de kopie wordt aan de onder/rechterkant 16 px ingekort (boog weg; daar komt het origineel = lijf terug)
# 3 de onderkant krijgt lokpunten uit het model: per kolom een strook lokpunten (kolomsgewijs onder de ingekorte rand
#   gehangen, vorm van de punten ongewijzigd). Twee bronnen: a = keelfranjepunten r3b, b = lokpunten r3c.
# Uit: r2/model_A2a.png, r2/model_A2b.png
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from reduce import fgmask
Ld=lambda n:np.asarray(Image.open(n).convert('RGB')).astype(int)
M=Ld('../referenties/model_r3b.png'); R3C=Ld('../gemini/r3c/kudu_r3c.png'); fg=fgmask(M)
hb=np.load('haar_r3b.npy'); hc=np.load('haar_r3c.npy')
Hh,Ww=hb.shape; yy,xx=np.mgrid[:Hh,:Ww]
DX,DY=70,30
src=hb&~((xx>440)&(yy<530))                     # zonder kamlokken
S=np.zeros_like(hb); S[DY:,DX:]=src[:-DY,:-DX]   # verschoven masker
SV=np.zeros_like(M); SV[DY:,DX:]=M[:-DY,:-DX]    # verschoven pixels
basis=S|hb
def sh(m,dy,dx):
    o=np.zeros_like(m); o[max(dy,0):Hh+min(dy,0),max(dx,0):Ww+min(dx,0)]=m[max(-dy,0):Hh+min(-dy,0),max(-dx,0):Ww+min(-dx,0)]; return o
T=10
lumS=(SV*[.299,.587,.114]).sum(2)
rand=S&~(sh(basis,-T,0)&sh(basis,0,-T)&sh(basis,-T,-T))   # binnen 10 px van de onder/rechterrand van de kopie (boven het lijf)
boog=rand&(lumS<90)&~hb                                    # alleen de donkere lijn van de boog, niet waar het origineel haar ligt
boog=nd.binary_dilation(boog,iterations=2)&rand&~hb
keep=S&~boog
def strook(img,x0,x1,y0,y1,hm=None):
    """lokpuntstrook: per kolom de modelpixels van y0 tot het eind van het haar (+ zwarte puntlijn eronder)."""
    cols=[]
    lum=(img*[.299,.587,.114]).sum(2)
    for x in range(x0,x1):
        col=[]
        for y in range(y0,y1):
            if img[y,x].min()>=232: break
            if hm is not None and not hm[y,x] and lum[y,x]>=70: break
            col.append(img[y,x])
        cols.append(np.array(col))
    return cols
def maak(cols,naam):
    out=M.copy()
    out[S&keep]=SV[S&keep]
    xs=np.nonzero(keep.any(0))[0]
    n=0
    for x in xs:
        if not boog[:,x].any() and not S[:,x].any(): continue
        ys=np.nonzero(keep[:,x])[0]
        if not len(ys): continue
        yb=ys.max()                       # onderkant van de ingekorte kopie in deze kolom
        if yb<640: continue               # alleen aan de onderkant van de manen (geen punten midden op de schouder)
        if not boog[yb+1:yb+T+4,x].any(): continue   # alleen waar de boog zat
        c=cols[(x-xs.min())%len(cols)]
        for k,v in enumerate(c):
            y=yb+1+k
            if y<Hh and fg[y,x]: out[y,x]=v; n+=1
    hm=(S&keep)|hb
    tip=np.zeros_like(hb)
    tip[(out!=M).any(2)&~(S&keep)]=True
    np.save(f"r2/manen_{naam}.npy",hm|tip)
    Image.fromarray(out.astype("uint8")).save(f"r2/model_{naam}.png"); return out,n
import os; os.makedirs('r2',exist_ok=True)
a=strook(M,215,320,655,760)                         # keelfranjepunten r3b
b=strook(R3C,330,430,615,700,hc)                    # lokpunten r3c
for cols,nm in [(a,'A2a'),(b,'A2b')]:
    o,n=maak(cols,nm); print(nm,'puntpixels',n,'boogpixels weg',int(boog.sum()))
v=M.copy(); v[boog]=[255,0,0]; Image.fromarray(v[350:800,200:700].astype('uint8')).save('r2/boog_viz.png')
