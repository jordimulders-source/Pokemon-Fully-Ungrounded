# r9.py: Gnometrotter Ice r9 uit r8 (23 nov). Jordi: "ijs is geen onderscheid meer tussen muts en rugijs, haar mag ook
# net iets meer. Lichaam moet nog ietsje meer ijsvorm". Logt elke gewijzigde pixel per zone (r9_log.txt). Silhouet gelijk.
import numpy as np, os; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(H,'../sprite_r8/gnometrotter_ice.png')); o=np.asarray(im).copy(); n=o.copy()
zone={}
def zet(x,y,v,z):
    if n[y,x]!=v: n[y,x]=v; zone[(x,y)]=z
ICE=(2,3,4,5)

# ---- 1. muts vs rugijs ----
# Model: de mutspunt eindigt rechts op x~44 (rij 8-15) en buigt onder rij 15 naar links; daarachter ligt de rugkam
# (lichtblauw doorschijnend, in de schaduw van de muts). Grens in de sprite: x44 op rij 9-14, x43 op rij 15-17.
GRENS={y:44 for y in range(9,15)}; GRENS.update({15:43,16:43,17:43})
RUG=np.zeros((64,64),bool)
for y in range(8,23):
    for x in range(40,53):
        if o[y,x] not in ICE: continue
        if y in GRENS and x>GRENS[y]: RUG[y,x]=True
        if y>=18 and x>=43: RUG[y,x]=True
for y,x in np.argwhere(RUG):      # rugijs in de schaduw: een tint donkerder (5->4, 4->3); lijnen (2) blijven
    zet(x,y,{5:4,4:3,3:3,2:2}[o[y,x]],'rugijs')
for y,x in np.argwhere(RUG):      # lichte rand linksboven op de rugkam (bovenkant van elke pegel), zodat hij volume houdt
    if o[y,x]==5 or (o[y,x]==4 and o[y-1,x] in (0,1,2)): zet(x,y,4,'rugijs')
# lichte facetribbe op de rugkam (model: heldere rand die van boven (47;9) schuin naar (45;26) loopt) in 4
for x,y in [(47,10),(47,11),(46,12),(46,13),(46,14),(46,15),(46,16),(45,17),(45,18),(45,19),(45,20)]:
    if RUG[y,x] and n[y,x]==3: zet(x,y,4,'rugijs')
for y,gx in GRENS.items():        # scheidingslijn in de donkerste ijstint (2) waar de muts vóór de rugkam ligt (mutszijde)
    if o[y,gx] in ICE: zet(gx,y,2,'muts')

# ---- 2. haar: eigen plukken met lichte kant (E) linksboven, D midden, C schaduwkant rechtsonder ----
HAAR={'haar L':(11,18,12,19),'haar R':(33,41,14,19)}
for nm,(x0,x1,y0,y1) in HAAR.items():
    P=[(x,y) for y in range(y0,y1+1) for x in range(x0,x1+1) if o[y,x] in (12,13,14)]
    xs=[p[0] for p in P]; ys=[p[1] for p in P]; a0,a1,b0,b1=min(xs),max(xs),min(ys),max(ys)
    for x,y in P:
        u=(x-a0)/max(1,a1-a0)+(y-b0)/max(1,b1-b0)
        zet(x,y,14 if u<0.7 else (13 if u<1.35 else 12),nm)

# ---- 3. romp: één facetgrens extra in het vlak rechtsonder (modelbarst (38,5;35)->(42;32,5)->(46,5;30,5)) als lichte naad 8 ----
for x,y in ((39,34),(40,33),(41,33),(42,32),(43,32),(44,31),(45,31),(46,30)):
    if o[y,x]==7: zet(x,y,8,'romp')

# ---- uitvoer + log ----
out=Image.fromarray(n.astype('uint8'),'P'); out.putpalette(im.getpalette())
out.save(os.path.join(H,'gnometrotter_ice.png'),transparency=0)
out.resize((512,512),Image.NEAREST).save(os.path.join(H,'gnometrotter_ice_8x.png'),transparency=0)
tel={}
with open(os.path.join(H,'r9_log.txt'),'w') as fh:
    for Y in range(64):
        for X in range(64):
            if n[Y,X]!=o[Y,X]:
                z=zone.get((X,Y),'rest'); tel[z]=tel.get(z,0)+1; fh.write('%s (%d,%d) %X -> %X\n'%(z,X,Y,o[Y,X],n[Y,X]))
print('t.o.v. r8 per zone:',tel,'| silhouet t.o.v. r8:',int(((n>0)!=(o>0)).sum()))
