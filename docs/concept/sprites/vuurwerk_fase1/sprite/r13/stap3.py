# r13: C = B + kop meer als vlam (Jordi). Bron: kop van fase 3 (vlampunten op de achter-/bovenrand in de vorm 'p / pm / pmp',
# roze strepen die van achteren de creme in lopen). Achterkant van deze kop = rechts (kieuwen), bovenkant = rij 8.
# Ogen (11,33-34),(12,33-34),(15-18,39-41), mond (rij 19-21) en sprieten blijven pixelgelijk. Geen nieuwe kleuren.
import sys; sys.path.insert(0,'../r10'); from txt import CH
import numpy as np; from PIL import Image
S=Image.open('../r12/B.png'); a=np.array(S); pal=S.getpalette()
CH2=CH[:7]+'r'+CH[8:]; I={c:i for i,c in enumerate(CH2)}
def stamp(r,c):  # vlampunt van 2 rijen op de rand bij (r,c+1), punt naar boven (fase 3 rij 2-4, kol 14-16, verkleind)
    return [(r-2,c+1,'d'),(r-1,c,'d'),(r-1,c+1,'l'),(r-1,c+2,'d'),(r,c+1,'l')]
P=[]
P+=stamp(8,36)                                   # punt 1 op de bovenrand
P+=stamp(9,40)                                   # punt 2 op de achterhoek
P+=[(9,37,'l'),(10,37,'l'),(10,36,'l')]         # streep 1: van punt 1 schuin de creme in (aaneengesloten, smal uitlopend)
P+=[(10,41,'l'),(10,40,'l'),(11,40,'l'),(11,39,'l')]  # streep 2: van punt 2 schuin naar voren
P+=[(10,43,'d')]                                 # rafel: klein puntje op de achterrand boven de kieuwen
P+=[(9,42,'d'),          # sluit punt 2 aan de buitenkant (anders open rand)
    (11,41,'l'),          # streep 2 loopt door tot de achterrand (anders los creme-pixeltje)
    (9,38,'c')]           # los tan-pixeltje tussen streep 1 en de creme -> creme
C=a.copy()
for r,c,v in P: C[r,c]=I[v]
im=Image.fromarray(C,'P'); im.putpalette(pal); im.save('C.png',transparency=0)
print('gewijzigd',int((C!=a).sum()))
