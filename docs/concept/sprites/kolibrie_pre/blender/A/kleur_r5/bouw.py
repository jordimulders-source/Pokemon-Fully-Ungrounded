"""kleur_r4/raster.txt -> r5: Starly-oog terug (uit maker/kleur_r10, x21-25 y14-18 -> y17-21), vleugel eigen tinten (8/A) + zachte rand E.
Alles buiten oogvak en vleugel blijft pixel voor pixel r4 (controle.py bewijst dat)."""
import sys
H='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/'
A=H+'blender/A/'
g=[list(l.rstrip('\n')) for l in open(A+'kleur_r4/raster.txt')][:64]
r10=[l.rstrip('\n') for l in open(H+'maker/kleur_r10/raster.txt')][:64]
# 1. oogvak r4 (Latias, x21-26 y16-21) terug naar gezicht, dan het Starly-oog uit r10 erop (5x5, 3 omlaag)
GEZICHT={(23,16):'5',(24,16):'5',(25,16):'5',(21,17):'5',(25,17):'4',(21,21):'4',(25,21):'3'}
for (x,y),c in GEZICHT.items(): g[y][x]=c
OOG=[(x,y) for y in range(14,19) for x in range(21,26) if r10[y][x] in '1257' and not (x in (21,25) and y in (14,18))]   # oogpixels in r10: zwart, rand 2, glans 7, onderglans 5
for x,y in OOG: g[y+3][x]=r10[y][x]
# 2. vleugel: eigen tinten (B->8 basis, E->A schaduw) in het vleugelvak; kap (y<=22) blijft B/E
for y in range(27,43):
    for x in range(31,42):
        g[y][x]={'B':'8','E':'A'}.get(g[y][x],g[y][x])
# zachte rand (E) langs boven- en voorkant van de vleugel; bovenrand rond gemaakt (x33-34 op rij 27 wordt lila)
for x,y,c in [(33,27,'4'),(34,27,'4'),(35,27,'E'),(36,27,'E'),(37,27,'E'),(38,27,'E'),
              (33,28,'E'),(34,28,'E'),(32,29,'E'),(32,30,'E'),(31,31,'E'),(31,32,'E'),(31,33,'E'),(32,34,'E'),(32,35,'E')]:
    g[y][x]=c
open(A+'kleur_r5/raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
sys.path.insert(0,A+'kleur_r5'); import palet; palet.build(A+'kleur_r5/raster.txt',A+'kleur_r5/kolibrie_pre.png')
