# Vileplume r14 = r13_dunnepoten (Jordi: "poten zijn niet beter nee") + naad VL|VR naar het model.
# Jordi: "zwarte lijn tussen middenvoor en rechtsvoor". Draaien vanuit vileplume_sprite/: python3 r14/bouw.py
# Model (natief raster, uitsnede 6x, u92-126 v62-102): tussen VL en VR ligt geen anemoon duidelijk vóór de ander;
# het zijn twee bolle lobben die naar elkaar toe buigen (beide met een donkere R1-band onderaan) en samenkomen in een
# korte zwarte inkeping: zwart alleen op u108-109, v82-93 (sprite x35, rij 24-28), onderaan breed tegen het lijf
# (kale reductie rij 28: x34-36 zwart). Daarboven (v<82) is er geen zwarte naad; de tentakels lopen door, met een
# korte donkerrode streek (u106-108, v78-82 = sprite (35,23)).
# r13 had een rechte zwarte lijn op x36 van rij 20 t/m 26 en x37 rij 27-28. Tinten naast de lijn = kale reductie
# van het model (eigen lob: R2 boven, R1 in de onderband).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import opslaan
im=Image.open('r13/vileplume_r13_dunnepoten.png'); o0=np.asarray(im).astype(int); PAL=[tuple(c) for c in np.array(im.getpalette()[:48]).reshape(-1,3)]
o=o0.copy(); K,R0,R1,R2,R3=1,2,3,4,5
NAAD=[ # x,y,van,naar
 (36,20,K,R2),(36,21,K,R2),(36,22,K,R2),(36,23,K,R2),   # boven: geen zwarte naad in het model
 (35,23,R2,R0),                                         # korte donkerrode streek waar de inkeping begint
 (35,24,R2,K),(35,25,R1,K),(35,26,R1,K),(35,27,R1,K),   # zwarte inkeping op de modelplek (x35)
 (36,24,K,R2),(36,25,K,R2),(36,26,K,R1),                # VR-kant: tint van de eigen lob (R2, onderband R1)
 (37,27,K,R1),(37,28,K,R1),
 (34,28,R1,K),(35,28,R1,K),(36,28,R1,K)]                # onderaan de inkeping breed zwart tegen het lijf (model)
for X,Y,v,k in NAAD:
    assert o0[Y,X]==v,(X,Y,o0[Y,X],v); o[Y,X]=k
zone={(X,Y) for X,Y,v,k in NAAD}
# ---- poten (Jordi: "ga maar terug naar de vorige, zoveeel gespiegeled naar moddel"): dunne poten van r13_dunnepoten
# als basis; per rij plek, knik en tinten uit het verkleinde model (r14/poten.py), binnen de bestaande breedte (komt het
# model breder uit, dan valt de eindpixel met de minste modeldekking weg). Voetkappen (links rij 59, rechts rij 62)
# blijven: die zijn al gelijk aan het model (zwart x25-26 / x39-40).
sys.path.insert(0,'r14'); from poten import rij as modelrij, F
POTEN=set()
for Y in range(42,62):
    for xa,xb in ((19,31),(31,46)):
        if (xa==19 and Y==59): continue
        xs=[X for X in range(xa,xb) if o0[Y,X]>0]
        if not xs: continue
        n=len(xs); r=modelrij(Y,xa,xb)
        if r is None: continue
        x0,cols=r
        while len(cols)>n:
            covl=1-F[Y,x0,0]/F[Y,x0].sum(); covr=1-F[Y,x0+len(cols)-1,0]/F[Y,x0+len(cols)-1].sum()
            if covl<covr: x0+=1; cols=cols[1:]
            else: cols=cols[:-1]
            cols=list(cols); cols[0]=cols[0] if cols[0] in (1,6) else 6
            f=F[Y,x0+len(cols)-1]; cols[-1]=1 if f[1]>f[6]+f[7] else 6
        for X in xs: o[Y,X]=0; POTEN.add((X,Y))
        for j,k in enumerate(cols): o[Y,x0+j]=k; POTEN.add((x0+j,Y))
# linkervoet: de scheen staat in het model (rij 56-58) op x24-26, dus de kap volgt eronder over de volle breedte
# (model rij 59: zwart op x24-26, met lichte rest in het midden; de buitenrand houdt zwart, dus zwart x24-26)
for X in range(20,31): 
    if o0[59,X]>0 or X in (24,25,26): POTEN.add((X,59)); o[59,X]=0
for X in (24,25,26): o[59,X]=1
zone|=POTEN
assert all((X,Y) in zone for Y,X in np.argwhere(o!=o0)), 'buiten de naad en de poten'
opslaan(o,PAL,'r14/vileplume_r14.png')
print('naad %d px, poten %d px anders dan r13_dunnepoten'%(sum(o[Y,X]!=o0[Y,X] for X,Y,v,k in NAAD),sum(o[Y,X]!=o0[Y,X] for X,Y in POTEN)))
ch='.K0123abcdeGuomy'
for Y in range(40,64): print('%2d %s   r13dun %s'%(Y,''.join(ch[v] for v in o[Y,18:44]),''.join(ch[v] for v in o0[Y,18:44])))
