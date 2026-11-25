# Jordi (25 nov): "A is het beste maar mag iets kleiner". Varianten: rijen/kolommen uit de Lombre-mond schrappen
# (Gengas-methode, niets hertekenen); rechterkant (onder het oog) en bovenrand blijven op hun plek.
from bouw import *
o=np.load('zonder_mond.npy')
def klein(drop_c=(),drop_r=()):
    m=[(r,c,k) for r,c,k in lombre_mond() if c not in drop_c and r not in drop_r]
    out=[]
    for r,c,k in m:
        nc=c+sum(1 for d in drop_c if d>c)        # links van een geschrapte kolom schuift 1 naar rechts
        nr=r-sum(1 for d in drop_r if d<r)        # onder een geschrapte rij schuift 1 omhoog
        out.append((nr,nc,k))
    return out
V={'A':((),()),'A1':((5,),()),'A2':((4,8),()),'A3':((5,),(27,)),'A4':((4,8),(27,))}
ims=[]
for n,(dc,dr) in V.items():
    v=sluit(plak(o,klein(dc,dr),17,4)); opslaan(v,'lombre_gaucho_%s.png'%n)
    print(n,'mondpixels',int((v!=o).sum()))

# Jordi: "a1 is de vorm van het mond het beste, a2 sluit die beter aan maar is de hele vorm van de mond weg"
# -> A5 = vorm A1, 1 px naar rechts (de punt staat dan waar die van A2 staat).
v=sluit(plak(o,klein((5,),()),18,4)); opslaan(v,'lombre_gaucho_A5.png'); print('A5 mondpixels',int((v!=o).sum()))
