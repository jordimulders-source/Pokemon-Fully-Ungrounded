# Ponchovarianten A/B/C op basis0 (variant 0). ALLEEN binnen het ponchomasker, alleen het lijnenwerk (Jordi, 25 nov):
# "het enige waar je in afwijkt van het model is het lijnenwerk van de poncho ... dit betekent niet opnieuw tekenen,
#  hooguit de bladervorm met wat pixels schuiven omzetten en anders inkleuren".
# Lijnpixels = zwart (1) of rode lijn (2) binnen de poncho, niet op de rand van het masker (rand naar arm, gezicht, been
# blijft), en alleen in de wijkzone: rij 37-55, x <= 37 (de schaduwkant onder de hoedrand en de rechter schouderrand naar
# de arm blijven het model). Zones: boven (rij <= 41) = poncho, overgang (42-45), onder (>= 46) = bladpunten (model).
import numpy as np
from gemeen import opslaan
from ponchomasker import masker
o0=np.load('basis0.npy'); P=masker(o0)
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def is_lijn(o,y,x):
    if not P[y,x] or o0[y,x] not in (1,2): return False
    if not(37<=y<=55 and x<=37): return False
    return all(P[y+dy,x+dx] for dy,dx in N4)
LIJN=[(y,x) for y,x in zip(*np.where(P)) if is_lijn(o0,y,x)]
def vul(o,y,x):
    nb=[o0[y+dy,x+dx] for dy,dx in N8 if P[y+dy,x+dx] and o0[y+dy,x+dx] in (3,4,5,6,7)]
    return max(set(nb),key=nb.count) if nb else 4
def plooi(k): return max(3,k-1)   # één tint donkerder dan het vlak: plooi in de stof in plaats van een bladnerf
def maak(naam,boven,overgang,schuif=()):
    o=o0.copy()
    for y,x in LIJN:
        if y<=41: o[y,x]=boven(y,x)
        elif y<=45: o[y,x]=overgang(y,x)
    for (y,x),(y2,x2) in schuif:   # lijnpixel verschuiven: oude plek krijgt de vlaktint, nieuwe plek de lijntint
        k=o[y,x]; o[y,x]=vul(o,y,x); o[y2,x2]=k
    assert ((o>0)==(o0>0)).all() and (o[~P]==o0[~P]).all()
    n=int((o!=o0).sum()); print(naam,'gewijzigd t.o.v. variant 0:',n,'px (alle in de poncho); silhouet-diff 0')
    np.save(naam+'.npy',o); opslaan(o,'ludicolo_gaucho_%s.png'%naam); return o
print('lijnpixels in de wijkzone',len(LIJN))
# A: bovenaan verdwijnen de bladlijnen in het ponchovlak (één vlak, de bestaande schaduw van het model blijft);
#    in de overgang worden ze rode lijn (2), onderaan blijven de zwarte bladpunten van het model.
maak('A',lambda y,x:vul(o0,y,x),lambda y,x:2)
# B: bovenaan worden de bladlijnen plooien in de poncho (één tint donkerder dan het vlak, geen lijn), overgang rode lijn, onder zwart.
maak('B',lambda y,x:plooi(vul(o0,y,x)),lambda y,x:2)
# C: als A, en ook onderaan worden de bladlijnen binnen de poncho rode lijn (2) i.p.v. zwart: de poncho leest als één stuk
#    met een bladvormige zoom; zwart blijft alleen op de rand van de punten (maskerrand: tegen been, voet, arm, achtergrond).
def maakC():
    o=maak('C_tmp',lambda y,x:vul(o0,y,x),lambda y,x:2)
    for y,x in LIJN:
        if y>=46 and o[y,x]==1: o[y,x]=2
    n=int((o!=o0).sum()); print('C gewijzigd t.o.v. variant 0:',n,'px (alle in de poncho); silhouet-diff',int(((o>0)!=(o0>0)).sum()))
    np.save('C.npy',o); opslaan(o,'ludicolo_gaucho_C.png')
maakC()
import os; os.remove('C_tmp.npy'); os.remove('ludicolo_gaucho_C_tmp.png')
