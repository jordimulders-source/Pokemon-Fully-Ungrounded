# Ronde 5: scheiding van nabije vleugel (onderarm), dij/doorgetrokken poot, staart en beide poten (Jordi op r4:
# "niet goed te zien hier waar de ledematen los van elkaar zitten"). Alleen in het omcirkelde gebied, palet van r4, silhouet gelijk.
# Coördinaten 64x64. Indexen r4: 1 zwart, 5 (98,102,114), 8 (124,126,134), 9 (154,154,154), 10 (182,181,176), 12 (66,68,80) donkerste grijs.
import numpy as np
from PIL import Image
C=12
for src,dst in (('../r4/kuiken_r4_haarB.png','kuiken_r5.png'),):   # Jordi koos haren B
    im=Image.open(src); a=np.array(im); r4=a.copy(); n={}
    def zet(x,y,v,mid,oud):
        assert a[y,x] in oud,(mid,x,y,a[y,x])
        if a[y,x]!=v: a[y,x]=v; n[mid]=n.get(mid,0)+1
    # (1) scheidingslijnen waar natief_bewerkt een rand/toonsprong heeft, 1 px, donkerste grijs
    #  - onderrand onderarm over de dij: natief r44-45 '#' (45-46,44-45) -> rij 45 x35-39, sluit aan op de lijfonderlijn (28-34,45)
    for x in range(35,40): zet(x,45,C,'1 lijn onderarm/dij',(5,8,9,10))
    #  - dij/staart: natief donkere kolom x44-45 r45-50 -> kolom 39 r46-50 (was de M-sikkel in tint 5, viel weg tussen de veerlijnen)
    for y in range(46,51): zet(39,y,C,'1 lijn dij/staart',(5,))
    #  - verre poot/dij: natief '##' (38-39,47-48) -> kolom 33 r47-49, schaduwkant van de verre poot
    for y in (47,48,49): zet(33,y,C,'1 lijn poot/dij',(5,8,9))
    # (2) tintcontrast: staart ligt achter dij en onderarm -> een stap donkerder (9/10 -> 8), veerlijnen 5 blijven
    for y in range(45,51):
        for x in range(40,52):
            if a[y,x] in (9,10): zet(x,y,8,'2 staart donkerder',(9,10))
    # (3) schaduwrand: dij verdwijnt onder de onderarm -> bovenste rij dij een stap donkerder
    for x in range(35,39):
        v={10:9,9:8}.get(int(a[46,x]))
        if v: zet(x,46,v,'3 schaduwrand dij',(9,10))
    assert ((a>0)!=(r4>0)).sum()==0
    d=a!=r4; ys,xs=np.nonzero(d); print(dst,n,'totaal',int(d.sum()),'bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(),
        'zwart %',round((a==1).sum()/(a>0).sum()*100,1))
    out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save(dst,transparency=0)
