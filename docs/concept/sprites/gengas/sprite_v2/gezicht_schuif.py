# Hybride gezicht (Jordi: "oog en mond grootte van model is beter en van jouw versie de positionering"):
# het modelgezicht (blok rij 28-45, kolom 8-27 van het gekwantiseerde model, ALLE modelpixels incl. de donkere
# maskerband ertussen) schuift als één blok dx=+5, dy=+1 naar de r3-plek (gemeten middelpunten t.o.v. r3:
# linkeroog +4,6/+3,2, rechteroog +4,1/+1,0, grijns +5,6/-0,1). Randpixels van het silhouet (omlijning/maan links)
# schuiven niet mee en blijven staan. Vrijgekomen gezichtspixels krijgen de modelband uit dezelfde rij.
import sys
src,dst=sys.argv[1],sys.argv[2]
R=[list(l.rstrip('\n')) for l in open(src)][:64]
O=[r[:] for r in R]
Y0,Y1,X0,X1,DX,DY=28,45,8,27,5,1
RANDSET=set('KgGhHW')
rim=set()
for y in range(Y0,Y1+1):
    x=X0
    while x<12 and R[y][x] in RANDSET: rim.add((y,x)); x+=1
def bandwaarde(y): return 'b' if y<=37 else 'l'
gezicht=lambda y,x: R[y][x] in set('KERWHhGgv') or (x>X0 and R[y][x] in 'ra')
# 1) vrijgekomen gezichtspixels -> band
for y in range(Y0,Y1+1):
    for x in range(X0,X1+1):
        if (y,x) in rim: continue
        if gezicht(y,x): O[y][x]=bandwaarde(y)
# 2) blok plakken
for y in range(Y0,Y1+1):
    for x in range(X0,X1+1):
        ty,tx=y+DY,x+DX
        O[ty][tx]=bandwaarde(ty) if (y,x) in rim else R[y][x]
open(dst,'w').write('\n'.join(''.join(r) for r in O)+'\n')
