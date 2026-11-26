# Bouwt poliwag_regional_r1 uit de kale reductie (reduceer.py). Lagen:
#  A tinten per materiaal uit de modelhelderheid (lijf/geel licht gladgestreken = opschoning van de spikkels)
#  B omlijning (technisch)   C reparaties per pixel naar het model: spiraal, ogen, mond (rood = Jordi), kristallen
import numpy as np; from PIL import Image
from palet import PAL
z=np.load('reductie.npz'); cls=z['cls'].copy(); lum=z['lum']; col=z['col']
kaal=np.load('kaal.npy'); H,W=cls.shape
def blur(v,m,s):
    r=int(3*s); k=np.exp(-np.arange(-r,r+1)**2/(2*s*s))
    num=np.where(m,v,0.0); den=m.astype(float)
    for ax in (0,1):
        num=np.apply_along_axis(lambda x:np.convolve(x,k,'same'),ax,num)
        den=np.apply_along_axis(lambda x:np.convolve(x,k,'same'),ax,den)
    return num/np.maximum(den,1e-6)
out=np.zeros((H,W),'uint8')
Y=cls==1; K=cls==4; IR=(cls==2)|(cls==3)
jj,ii=np.mgrid[0:H,0:W]
disc=IR&(ii<=19)&(jj>=17)&(jj<=34)
tail=IR&(ii>=27)&(jj>=13)&~((ii<=32)&(jj<=20))
crys=IR&(jj<=20)&~disc&~tail&~((ii<=14))
feet=K&(jj>=35)&(((ii<=9))|((ii>=20)))
# --- A: lijf (zwart): helderheid gladgestreken over sigma 1.5 cel
sb=blur(lum,K,1.5)
out[K]=np.where(sb[K]>=54,3,2)
out[K&(sb>=67)]=4
sf=blur(lum,feet,1.0)
out[feet]=np.where(sf[feet]>=55,4,np.where(sf[feet]>=42,3,2))
# geel
sy=blur(lum,Y,1.0)
out[Y]=np.where(sy[Y]>=212,5,np.where(sy[Y]>=185,6,7))
# ijs: schijf/staart/kristal per cel (licht gladgestreken), rood blijft rood
for m,s in ((disc,0.45),(tail,0.45),(crys,0.45)):
    ice=m&(cls==3); si=blur(lum,ice,s)
    out[ice]=np.select([si[ice]>=214,si[ice]>=196,si[ice]>=168],[8,9,10],11)
red=IR&(cls==2); out[red]=np.select([lum[red]>=125,lum[red]>=95],[12,13],14)

# --- spiraal: rood in de schijf eerst terug naar ijs (tint uit de ijsomgeving), dan de spiraal 1 px langs het modelpad
ice=disc&(cls==3); si=blur(lum,ice,1.2)
dr=disc&(cls==2); out[dr]=np.select([si[dr]>=214,si[dr]>=196,si[dr]>=168],[8,9,10],11)
SPIRAAL={  # (x,y): index ; pad uit de modelcellen (cls), van het buiteneinde naar binnen
 (12,31):14,(13,30):14,(14,29):13,(15,28):13,(15,27):13,(15,26):13,(15,25):13,(14,24):13,(14,23):13,(13,22):13,
 (12,21):13,(11,21):13,(10,20):13,(9,20):13,(8,20):13,(7,20):12,(6,21):12,(5,22):12,(4,23):12,
 (4,24):13,(4,25):13,(4,26):13,(4,27):13,(5,28):13,(6,29):13,(7,30):13,(8,30):13,(9,30):13,(10,30):13,(11,29):13,(12,28):13,
 (12,27):13,(12,26):13,(12,25):13,(12,24):13,(11,23):13,(10,23):13,(9,23):13,(8,23):13,(7,23):13,(6,24):13,(6,25):13,(6,26):13,
 (7,27):13,(8,28):13,(9,28):13,(10,27):13,(10,26):13,(10,25):13,(9,25):13,(8,25):13}
for (x,y),v in SPIRAAL.items(): out[y,x]=v

out[21,7]=9   # grijze modelcel midden in de schijf (ruis) -> ijs
def put(rows):
    for y,(x0,r) in rows.items():
        for dx,ch in enumerate(r):
            if ch!=' ': out[y,x0+dx]=0 if ch=='.' else int(ch,16)
# --- ogen: per cel uit de modelsamenstelling (celinhoud.py: Z zwart, W wit, I ijs, G grijs)
OOG_VER={7:(5,"77"), 8:(5,"111"), 9:(4,"1911"), 10:(3,"19181"), 11:(3,"18311"), 12:(3,"19116"), 13:(2,"77887"), 14:(3,"671")}
OOG_NABIJ={7:(16,"72"), 8:(14,"611992"), 9:(14,"1911992"), 10:(13,"61881991"), 11:(14,"1111981"), 12:(14,"1333981"),
           13:(14,"1118816"), 14:(14,"771116")}
put(OOG_VER); put(OOG_NABIJ)
# --- mond: vorm uit het model, kleur rood (Jordi); spleet en stip zwart zoals in het model
MOND={12:(8,"eee"), 13:(6,"7eccce6"), 14:(6,"ec11cce1"), 15:(6,"1cdd1cc1"), 16:(6,"11dddde1"), 17:(8,"1111")}
put(MOND)
out[1,21]=0   # losse ijscel naast de kristalpunt (ruis)

# --- B: omlijning (technisch). Rand = pixel naast lucht (4-buren).
o=out.copy()
def lucht(y,x): return y<0 or x<0 or y>=H or x>=W or out[y,x]==0
for y in range(H):
    for x in range(W):
        v=out[y,x]
        if v==0: continue
        up=lucht(y-1,x); lf=lucht(y,x-1); dn=lucht(y+1,x); rt=lucht(y,x+1)
        if not (up or lf or dn or rt): continue
        if v in (2,3,4): o[y,x]=1
        elif v in (5,6): o[y,x]=7 if (up or lf) and not (dn or rt) else 1
        elif v in (8,9,10,11) and x<=19: o[y,x]=1            # schijf tegen lucht: zwart zoals het model
        elif v in (8,9,10,11): o[y,x]=11 if (up or lf) and not (dn or rt) else 15   # staart (kristallen zijn met de hand)
        elif v in (12,13): o[y,x]=14 if (up or lf) and not (dn or rt) else 1
out=o
# --- staart: rode kern per rij uit celinhoud.py (linksboven d, midden c licht, rechtsonder e); grijze ruiscellen -> vin; rand f
STAART={18:(49,"f"),19:(43,"de"),20:(42,"dce"),21:(41,"dce"),22:(39,"dcce"),23:(38,"dce"),24:(36,"dcce"),
 25:(34,"ddcde"),26:(31,"aadcdea"),27:(31,"eddde"),28:(29,"eddde"),29:(28,"ddeaaaa"),}
put(STAART)
for (x,y) in ((49,19),(49,20),(43,27),(41,28),(39,29)): out[y,x]=15
# kristallen na de omlijning (met de hand gezette lijnen blijven staan)
# --- kristallen: silhouet en rood uit celinhoud.py; lichte kant b, schaduwkant f (ijs-selout), vulling 8/9/a
KRISTAL1={0:(23,"b"), 1:(22,"b8f"), 2:(20,".b8af"), 3:(20,"bc9af"), 4:(20,"b8daf"), 5:(19,"1d9aaf"), 6:(20,"bdeaf"), 7:(20,"1bb1")}
KRISTAL2={6:(26,"bb"), 7:(25,"b89f"), 8:(24,"b8daf"), 9:(25,"bef"), 10:(25,"11")}
KRISTAL3={14:(30,"bb"), 15:(29,"b89f"), 16:(29,"bdaf"), 17:(29,"bdf"), 18:(29,"1ef"), 19:(29,"1f")}
for k in (KRISTAL1,KRISTAL2,KRISTAL3): put(k)
# --- ruis in vlakken (losse tintcellen) -> buurtint; onderrand schijf uit het model (donkerblauw, rij 34)
FIX={(1,23):10,(39,21):9,(37,22):9,(41,23):10,(35,24):10,(33,24):10,(39,27):10,(40,27):9,(40,18):8,
     (9,34):15,(10,34):15,(11,34):15,(12,34):15,(13,34):2,(14,34):2}
for (x,y),v in FIX.items(): out[y,x]=v

# --- uitvoer: 64x64 geindexeerd, index 0 transparant
OX,OY=7,19
S=np.zeros((64,64),'uint8'); S[OY:OY+H,OX:OX+W]=out
im=Image.fromarray(S,'P'); im.putpalette([c for t in PAL for c in t]); im.save('poliwag_regional_r1.png',transparency=0)
np.save('r1.npy',out)
