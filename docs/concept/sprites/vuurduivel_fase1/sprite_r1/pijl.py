# pijl.py: de ENIGE toegestane afwijking (Jordi: "het is niet genoeg een pijl, maar dat kunnen we in de sprite doen"):
# staartpunt als klassieke duivelspijl (schoppenpunt), massief, in de vuurkleuren van het model
# (donkerrood bij de basis, oranje, geel bij de punt); plek en maat van het model (bbox x42-50, y36-46;
# stam komt linksonder binnen bij x44-45, punt rechtsboven bij x48-49). Rijen beginnen bij x41.
import os
X0=41
A={  # schuin, punt rechtsboven zoals het model
36:".......O...",
37:"......OYr..",
38:".....OYYr..",
39:".....OYYYr.",
40:"....OYYOOR.",
41:"...rOOOOOR.",
42:"..rOOOOrrR.",
43:".RrOOrrrrR.",
44:".RrrrrrrrR.",
45:".RRR#.RRR..",
}
B={  # recht, symmetrisch rond x46 (gekozen: leest het duidelijkst als schoppenpunt; A las als vlam/hart)
36:".....O.....",
37:"....OYr....",
38:"....OYr....",
39:"...OYYOr...",
40:"..rOYOOOR..",
41:".rOOOOOOOR.",
42:".rOOOOrrrR.",
43:".RrOrrrrrR.",
44:"..RrR#RrR..",
45:"...R##.R...",
}
def pijl():
    rij=B if os.environ.get('PIJL','B')=='B' else A
    return {(X0+i,y):c for y,r in rij.items() for i,c in enumerate(r) if c!='.'}
