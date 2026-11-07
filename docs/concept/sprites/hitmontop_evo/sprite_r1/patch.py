# Handmatige reparaties direct op raster.txt (eindcoordinaten): python3 patch.py <naam> ; segmenten staan in PATCHES.
import sys
P={}
def p(name,y,x0,s): P.setdefault(name,[]).append((y,x0,s))
# r1b: verre been + verre voet opnieuw. Voet = Hitmontop-rechtervoet (orig. x40-55, y14-22) 1:1, +8/-13 verschoven,
#      donkergrijs (e) -> d (klauwschaduw) of f; hielklauw ingekort. Been van heup schuin omhoog naar de enkel.
for y in range(0,15):
    p('r1b',y,46,'.'*18)
p('r1b',15,54,'.'*10)
p('r1b',1,53,"999")
p('r1b',2,51,"9966788dddff")
p('r1b',3,48,"ddf66666 79c1111f".replace(' ',''))
p('r1b',4,48,"cf7666667911 11f".replace(' ',''))
p('r1b',5,48,"cf7766677 7c1dff".replace(' ',''))
p('r1b',6,49,"97799777889cccf")
p('r1b',7,49,"98511978 88ccdf".replace(' ',''))
p('r1b',8,50,"f5ddf889fff")
p('r1b',9,50,"f511f99f")
p('r1b',10,50,"f9999f")
p('r1b',11,50,"96778f")
p('r1b',12,51,"96778f")
p('r1b',13,51,"967788f")
p('r1b',14,52,"967788f")
p('r1b',15,49,"99999677 8f".replace(' ',''))
p('r1b',16,49,"66666669 8888f".replace(' ',''))
p('r1b',17,44,"6666666666666988 8f".replace(' ',''))
# r1c: heup/zitvlak rechts ronder (geen rechte schuine kant)
p('r1c',22,58,"88f")
p('r1c',23,56,"788f")
p('r1c',24,56,"788f")
p('r1c',25,55,"788f")
p('r1c',26,54,"788f")
p('r1c',27,53,"788f")
# r1d: haarpunt rechts 1 px korter, zodat hij de vrije bovenarm niet raakt
p('r1d',31,32,".")
p('r1d',32,32,".")
name=sys.argv[1]
rows=[list(r.rstrip('\n')) for r in open('raster.txt')]
for y,x0,s in P[name]:
    for i,c in enumerate(s):
        if c!='_': rows[y][x0+i]=c
for r in rows: assert len(r)==64
open('raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
# r1e (rechtstreeks in raster.txt uitgevoerd): vrije bovenarm rijen 26-39 "52334" -> "52333",
#      zodat de donkere binnenlijn (5) tussen arm en borst los leest.
