# Pitahaya-draak fase 2, r10 op sprite_r9/pitahaya2_r9A.png: reparatielijst eindkeuring/KEURING.md (A, E, B, C, D, F).
# Model = overnemen, nooit hertekenen: elke pixel hieronder heeft een reden (model-meting of benoemde Gen 3-sprite).
# Meetgereedschap: modeltoonkaart.py (gladde modelhelderheid binnen het roze, modeltoon per spritepixel),
# ../eindkeuring/dekking.py (modeldekking per spritepixel).
import numpy as np; from PIL import Image
import modeltoonkaart as mt
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
src=Image.open(B+'sprite_r9/pitahaya2_r9A.png'); a0=np.array(src).astype(int); pal0=src.getpalette()
N='.KdrpPgGhHwWsv'; I={c:i for i,c in enumerate(N)}
LOG=[]
def zet(a,lst,doel,oud,punt,why):
    for x,y in lst:
        assert N[a[y,x]] in oud,(punt,x,y,N[a[y,x]])
        if N[a[y,x]]!=doel: LOG.append((punt,x,y,N[a[y,x]],doel,why))
        a[y,x]=I[doel]
A=a0.copy()
# ---- A: bek-roze (Exploud/Croconaw/Totodile: donker achterin en bovenin, licht voorin-onder) ----
zet(A,[(18,44),(19,44),(18,45),(19,45),(20,45),(18,46),(19,46),(20,46),(18,47)],'p','P','A1','mondhoek onder de bovenkaak: geen lichtste tint (Exploud/Croconaw donker achterin)')
zet(A,[(16,48),(16,49),(17,49),(15,50),(16,50),(15,51)],'p','P','A1','verre lip: basistint, los van het vruchtvlees w')
zet(A,[(17,45)],'r','p','A1','modeltoon r; lijn onder de bovenlip (17,44-47) doorlopend r')
zet(A,[(9,54),(10,54),(11,54)],'r','pP','A2','onderkant onderkaak kijkt naar beneden: schaduw (Exploud, Gyarados)')
zet(A,[(9,53),(10,53)],'P','p','A3','voorste lipbocht naar het licht: modeltoon P')
zet(A,[(8,48),(8,49)],'r','d','A4','lipcontour één tint r tot (7,53)')
# ---- B: silhouet naar de modeldekking ----
zet(A,[(61,48),(61,49),(61,50),(61,51)],'K','.','B1','staart rechts: modeldekking 2,3,3,2/9 = bolling (Swampert/Salamence-krul)')
zet(A,[(60,48),(60,49),(60,50),(60,51)],'g','K','B1','oude lijn wordt donkerste groen langs de schaduwrand')
zet(A,[(12,58)],'K','g','B2','teenlijn uit het model (natief 4/9 zwart)')
zet(A,[(12,59),(15,59)],'.','K','B2','inkeping onder de modelteenlijnen (12,58) en (15,58): drie teenpunten (Feraligatr/Swampert)')
zet(A,[(12,56)],'g','.','B2','bolling op teen 1, modeldekking 2/9: bovenrand geen 1-1-1-trap')
zet(A,[(18,34),(19,34),(20,34)],'.','rd','B3','kopbovenkant: modeldekking 6/9 -> zadel tussen wenkbrauw en nekschub')
zet(A,[(18,35),(19,35),(20,35)],'d','p','B3','nieuwe bovenrand = selout d')
# ---- C: randen ----
zet(A,[(25,32),(26,32),(25,33),(27,33),(32,33),(49,38),(48,39),(51,43),(52,43),(57,43),(58,44),(12,57),(10,58),(29,59),(28,60)],'g','G','C1','vlaktint op de buitenrand -> selout (Feraligatr/Salamence: punten donker omlijnd)')
zet(A,[(31,34),(38,34)],'d','p','C1','top rugplaat op de buitenrand -> selout')
zet(A,[(10,34),(11,34),(17,34),(9,35)],'d','r','C2','kopselout één tint d')
# ---- D1: evenaar op de gladde modelhelderheid (sigma 1,5 spritepx, alleen roze). Alleen p->r (terminator) en r->d (sikkel);
#      r->p-wijzigingen die de kaart voorstelt zijn NIET gedaan: daar heeft het model een naad (modeltoon r).
T=mt.sample(mt.smooth(1.5))
D1r=[(45,37),(45,38),(28,43),(29,44),(44,43),(45,43),(46,43),(47,43),(44,44),(47,44)]
for x,y in D1r: assert T[y,x]<103,(x,y,T[y,x])
zet(A,D1r,'r','p','D1','gladde modelhelderheid < 103: terminator hoger aan de achterkant (romp) en bij de keel, laag waar het lijf bolt (Salamence/Shelgon)')
D1d=[(24,48),(25,48),(26,48),(27,48),(25,49),(26,49),(37,50),(38,51),(39,51)]
for x,y in D1d: assert T[y,x]<=78.5,(x,y,T[y,x])
zet(A,D1d,'d','r','D1','gladde modelhelderheid <= 78 (donkerste roze): sikkel waar het lijf achter de dijen verdwijnt')
# ---- D3: groen hooglicht op de modelrand (native pixels in H-kleur >= 4/9 per spritepixel) ----
zet(A,[(33,49),(34,50),(35,51)],'H','h','D3','middelste dij: modelrandlicht 5,6,4/9 (sluit aan op H (36,51)-(37,53))')
zet(A,[(48,51)],'H','h','D3','achterste dij: modelrandlicht 5/9 (sluit aan op H (47,48)-(48,49)); (46,47) 4/9 niet: gaf dambord met (47,48)')
zet(A,[(56,44),(57,44),(57,45),(57,48),(56,49),(54,50),(55,50)],'H','h','D3','staartkrul: modelrandlicht 5,6,7,4,6,7,9/9 (gele spiraalband in het model)')
# ---- F: losse pixels ----
zet(A,[(40,52)],'g','G','F','losse G; modeltoon g, buren h/g')
# ---- asserts ----
d=set((x,y) for y,x in zip(*np.where(A!=a0)))
assert d==set((x,y) for _,x,y,_,_,_ in LOG)
sil=set((x,y) for y,x in zip(*np.where((A>0)!=(a0>0))))
assert sil=={(61,48),(61,49),(61,50),(61,51),(12,59),(15,59),(12,56),(18,34),(19,34),(20,34)},sil
for (x,y) in [(9,44),(10,45),(11,46),(10,47),(9,48)]: assert A[y,x]==a0[y,x]   # V-rand bevroren
assert (A[44:52,9:15][a0[44:52,9:15]==13]==13).all()                            # gehemelte bevroren
def save(a,naam,pal):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(pal); im.save(naam,transparency=0)
# ---- E: palet ----
pal=list(pal0)
for i,c in {2:(0x68,0x18,0x38),5:(0xf8,0xa0,0xc0),6:(0x30,0x58,0x30),7:(0x4f,0x80,0x40),8:(0x78,0xa8,0x50),9:(0xb0,0xd0,0x68)}.items(): pal[3*i:3*i+3]=c
save(A,'pitahaya2_r10.png',pal)
# ---- D2-variant: rughooglicht P waar de gladde modelhelderheid >= 140 (top van de twee grote rugplaten) ----
V=A.copy(); n0=len(LOG)
D2=[(x,y) for y in range(34,42) for x in range(24,48) if A[y,x]==I['p'] and T[y,x]>=140]
zet(V,D2,'P','p','D2','variant: rughooglicht op de top van de rugplaat (gladde modelhelderheid >= 140); niet in het model')
save(V,'pitahaya2_r10_plaatlicht.png',pal)
# dambord-check (2x2, geen transparant)
def dam(a):
    n=[]
    for y in range(63):
        for x in range(63):
            q=a[y:y+2,x:x+2]
            if q[0,0]==q[1,1]!=q[0,1]==q[1,0] and 0 not in q: n.append((x,y))
    return n
print('dambord r9A',len(dam(a0)),'r10',len(dam(A)),'nieuw',sorted(set(dam(A))-set(dam(a0))))
print('r10 gewijzigd',n0,'variant extra',len(LOG)-n0, D2)
from collections import Counter
print(Counter(p for p,*_ in LOG))
open('pitahaya2_r10_afwijkingen.txt','w').write('punt\tx\ty\toud\tnieuw\treden\n'+'\n'.join('\t'.join(map(str,l)) for l in LOG)+'\n')
