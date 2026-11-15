# Bewijs: elke pixel die v3 anders heeft dan v2 ligt in een van de genoemde zones (keuring v2).
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
v2=[l.rstrip('\n') for l in open(D+'../sprite_v2/raster.txt')][:64]
v3=[l.rstrip('\n') for l in open(D+'raster.txt')][:64]
ZONES=[('P  paletruil: kern lichtvlek w->v',lambda y,x: v2[y][x]=='w' and v3[y][x]=='v'),
       ('M1 gat rookarm (rij 22, kol 51-52)',lambda y,x: y==22 and x in (51,52)),
       ('M2/M3/M5/MAG gezichtsnaden, wig, streep (rij 25-47, kol 8-33)',lambda y,x: 25<=y<=47 and 8<=x<=33),
       ('M4 krul (rij 32-39, kol 36-44)',lambda y,x: 32<=y<=39 and 36<=x<=44),
       ('MAG manen (binnenpixels van de vier manen)',lambda y,x: (0<=y<=10 and 24<=x<=38) or (39<=y<=53 and x<=12) or (18<=y<=33 and 50<=x) or (48<=y and 38<=x<=57))]
tel={z[0]:0 for z in ZONES}; buiten=[]
for y in range(64):
    for x in range(64):
        if v2[y][x]==v3[y][x]: continue
        for naam,f in ZONES:
            if f(y,x): tel[naam]+=1; break
        else: buiten.append((y,x,v2[y][x],v3[y][x]))
for k,v in tel.items(): print(f'{v:4d}  {k}')
print('BUITEN de zones gewijzigd:',len(buiten),buiten)
