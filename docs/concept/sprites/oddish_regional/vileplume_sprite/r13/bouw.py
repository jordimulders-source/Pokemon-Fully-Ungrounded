# Vileplume r13 = r12 (bevroren) + Jordi op r12 (21 nov): "nee dit is prima, op wat details na, het gat linksbovenin
# tussen 2 anemonen in moet op een natuurlijke manier dicht, de zwarte lijnen tussen anemonen moet natuurlijker en de
# poten zien er niet mooi uit, misschien moeten we die 1 pixel dikker maken?"
# Draaien vanuit vileplume_sprite/: python3 r13/bouw.py. Alleen de drie zones hieronder; rest = r12 (assert).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import opslaan
im=Image.open('r12/vileplume_r12.png'); o12=np.asarray(im).astype(int); PAL=[tuple(c) for c in np.array(im.getpalette()[:48]).reshape(-1,3)]
o=o12.copy(); K,R0,R1,R2,R3=1,2,3,4,5
zones={}
def zet(zone,X,Y,k,van=None):
    if van is not None: assert o12[Y,X]==van, (zone,X,Y,o12[Y,X],van)
    o[Y,X]=k; zones.setdefault(zone,set()).add((X,Y))

# ---- 1. Gaten linksboven dicht: L loopt er doorlopend overheen, in de tinten van L; de rand tegen de krater blijft
# de zwarte kraterrand (x25, rij 11). L's eigen lijnen rond het gat worden L-tinten (anders dubbele lijn binnenin).
GAT=[ # (x,y, van, naar)
    (23,11,0,R1),(24,11,0,R0),(25,10,0,R0),          # gat tussen L en de krater (R0 = donkere kant van L tegen de kraterrand)
    (24,10,K,R1),(22,11,K,R1),(21,11,K,R2),          # L's oude rand rond dat gat -> L-tint (licht linksboven, schaduw rechts)
    (5,10,0,R3),(6,11,0,R3),                         # gaatje in de linkerrand van L
    (6,10,K,R2),(5,11,K,R2),(7,11,K,R0)]             # zwarte randjes eromheen -> L-tint, (7,11) blijft tentakelscheiding R0
for X,Y,v,k in GAT: zet('gat',X,Y,k,v)

# ---- 2. Lijnen tussen de anemonen ----
LIJN=[
    # T over L (na de verschuiving in r12): dubbele lijn (L-rand x21 + T-rand x22) -> één lijn (x21, zwart, schaduwkant
    # van L), de T-rand ernaast wordt T-tint (lichtkant van T); rij 8 sluit aan zodat de lijn doorloopt tot L's punt (20,9)
    (22,6,K,R3),(22,8,K,R2),(21,8,R0,K),
    # L tegen de krater, rij 12-14: trap van 2 px dik (KKK / KK / KK) -> 1 px (x24), L-kant schaduw R1
    (22,12,K,R1),(23,13,K,R1),(23,14,K,R1),
    # naad VL|VR boven (rij 18-19, x35): waar hij tegen de lichte rand van VR ligt -> selout R0
    (35,18,K,R0),(35,19,K,R0),
    # spleet tussen T en R (r12-opvulling R1, 3 px vlak) -> verloop naar R: buitenste kolom R2
    (41,5,R1,R2),(41,6,R1,R2),(41,7,R1,R2),(41,8,R1,R2)]
for X,Y,v,k in LIJN: zet('lijnen',X,Y,k,v)

base=o.copy()
# ---- 3. Poten 1 px dikker: elke 3-px-rij lijn - vulling - zwart wordt lijn - 2 vulling - zwart (extra pixel = kopie van
# de vulling, de rij groeit 1 px naar rechts); kap van 2 px wordt 3 px. Knik, plek en voeten blijven zoals r12.
def dik(a):
    a=a.copy(); ch=set()
    for Y in range(44,63):
        for xa,xb in ((18,31),(31,46)):
            xs=[X for X in range(xa,xb) if a[Y,X]>0]
            if not xs or xs[-1]-xs[0]+1!=len(xs): continue
            x0=xs[0]
            if len(xs)==3:
                p=[a[Y,x0],a[Y,x0+1],a[Y,x0+1],a[Y,x0+2]]
            elif len(xs)==2 and all(a[Y,x]==K for x in xs):      # voetkap
                p=[K,K,K]
            else: continue
            for j,k in enumerate(p):
                if a[Y,x0+j]!=k: a[Y,x0+j]=k; ch.add((x0+j,Y))
    return a,ch
odik,chd=dik(base)
for X,Y in chd: zones.setdefault('poten',set()).add((X,Y))

# ---- controle ----
for naam,a,extra in (('dun',base,set()),('dik',odik,chd)):
    toeg=set().union(*[s for z,s in zones.items() if z!='poten'])|extra
    d=np.argwhere(a!=o12); assert all((X,Y) in toeg for Y,X in d), naam
    assert len(set(a.ravel()))<=16
opslaan(odik,PAL,'r13/vileplume_r13.png'); opslaan(base,PAL,'r13/vileplume_r13_dunnepoten.png')
print('gewijzigd t.o.v. r12 (px echt anders): gat %d, lijnen %d, poten %d; totaal r13 %d, dunnepoten %d'%(
    sum(base[Y,X]!=o12[Y,X] for X,Y in zones['gat']),sum(base[Y,X]!=o12[Y,X] for X,Y in zones['lijnen']),len(chd),
    (odik!=o12).sum(),(base!=o12).sum()))
ch='.K0123abcdeGuomy'
for y in range(64): print('%2d '%y+''.join(ch[v] for v in odik[y]))
