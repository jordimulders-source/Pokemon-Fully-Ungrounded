# Pitahaya-draak fase 2, r4 op r3 (hoofd) en r3-lipB. Alles gemeten op het model (natief.png, 3x3-blok per spritepixel).
#  A BOVENLIP/KAAKLIJN: r2 maakte rij 42 x3-9 recht zwart. Model: tandvlees (roze) boven elke tand op (4,42) en (8,42)
#    (blok 7 resp. 6 roze px, 1 resp. 0 zwart); de lijn zakt bij x7 naar rij 43 (blok (7,43): 5 zwart). -> tandvlees terug
#    in de roze modeltoon van het blok (gemiddelde roze px -> dichtstbijzijnde toon). Silhouet blijft (model bevestigt het).
#  B SCHEIDING GEHEMELTE / VLEES ONDERKAAK: model scheidt ze met de verre lip, een diagonale roze strook (r) met
#    donkere onderrand (d = (113,43,55)) van (9,45) via (10,46),(11,46),(12,45) naar de zwarte lijn (14,44)-(16,44).
#    Hoofdversie: de strookpixels waar het model de donkere onderrand heeft ((11,46): 1 d-px, (12,45): 2 d-px) -> d (schaduw).
#    lipB: die pixels zijn al r (dominante strooktoon); het model heeft onder de strook geen aparte schaduw (blokken
#    (12,46),(11,47) zijn 100 % vlees), dus verder niets.
import sys,numpy as np; from PIL import Image
from groepen import laad
LIPB='--lipB' in sys.argv
BRON='pitahaya2_r3_lipB.png' if LIPB else 'pitahaya2_r3.png'; UIT='pitahaya2_r4_lipB.png' if LIPB else 'pitahaya2_r4.png'
R=Image.open(BRON); r3=np.asarray(R).astype(int); pal=R.getpalette(); P=np.array(pal[:39]).reshape(13,3)
a,lum,g=laad(); o=r3.copy(); log=[]; ZONE=set()
N={0:'.',1:'K',2:'d',3:'r',4:'p',5:'P',6:'g',7:'G',8:'h',9:'H',10:'w',11:'W',12:'s'}
def blok(Y,X): return slice(3*(Y-13),3*(Y-13)+3),slice(2+3*X,5+3*X)
def zet(y,x,v,stap,reden):
    ZONE.add((y,x))
    if o[y,x]!=v: log.append((stap,x,y,N[o[y,x]],N[v],reden)); o[y,x]=v
def info(y,x):
    gb=g[blok(y,x)]; return f"model: {(gb==2).sum()} roze, {(gb==1).sum()} zwart, {((gb==6)|(gb==7)).sum()} vlees, {(gb==0).sum()} achtergrond"
# A
for y,x in ((42,4),(42,8)):
    sl=blok(y,x); gb=g[sl]; c=a[sl][gb==2].mean(0); t=[2,3,4,5][int(((P[[2,3,4,5]]-c)**2).sum(1).argmin())]
    zet(y,x,t,'A tandvlees',info(y,x)+f'; roze gemiddelde {tuple(int(v) for v in c)}')
# B
if not LIPB:
    for y,x in ((46,11),(45,12)):
        zet(y,x,2,'B schaduw verre lip',info(y,x)+'; donkere onderrand (113,43,55) van de strook ligt in dit blok')
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(UIT,transparency=0)
diff=set(zip(*np.where(o!=r3))); assert diff<=ZONE; assert ((o>0)==(r3>0)).all()
BEK=lambda y,x: 2<=x<=20 and 42<=y<=56
assert all(BEK(y,x) for y,x in diff)
print(UIT,'gewijzigd t.o.v.',BRON,len(diff),'(alle in de bek; buiten 0; silhouet gelijk)')
for l in log: print(' ',l)
open(UIT[:-4]+'_afwijkingen.txt','w').write('\n'.join('\t'.join(map(str,l)) for l in log)+'\n')
