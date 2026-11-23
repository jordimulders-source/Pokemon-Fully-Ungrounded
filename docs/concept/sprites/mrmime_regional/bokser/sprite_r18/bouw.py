# r18 = r17 + (1) groot V-patroon = r7 'v_groot' (V_L, pixels 1-op-1), op de romp gelegd (alleen op rompwit/-grijs en
# de oude V, dus achter kop, schouderballen en borstvuist); variant 'groter' = dezelfde V met rij- en kolomherhaling;
# (2) verre schouderbal: vlakke zwarte bovenrand rond gemaakt door de hoekpixels 1 rij te verplaatsen.
import numpy as np, sys
sys.path.insert(0,'../sprite_r7'); from build import save
o=np.load('../sprite_r17/bokser.npy')
V_L={18:(32,33),19:(32,38),20:(32,37),21:(32,37),22:(31,36),23:(32,36),24:(33,36),25:(33,36),26:(34,35),27:(35,35)}
def vpix(V,dx,dy): return {(x+dx,y+dy) for y,(a,b) in V.items() for x in range(a,b+1)}
# groter: rij 19 en 22 herhaald (punt 2 rijen lager), kolom 34 herhaald (alles rechts ervan 1 px verder)
VG={}; ny=18
for y in sorted(V_L):
    for _ in range(2 if y in(19,21,23) else 1):
        a,b=V_L[y]; VG[ny]=(a,b+2 if b>=34 else (b+1 if b>=33 else b)); ny+=1   # kolom 33 en 34 herhaald
def maak(V,dx):
    a=o.copy()
    for x,y in vpix(V,dx,6):
        if 25<=y<=35 and a[y,x] in(7,8,3): a[y,x]=3
    # verre bal: bovenhoeken van de vlakke rand 1 rij omlaag/naar binnen
    assert a[22,19]==1 and a[22,23]==1 and a[23,19]==4 and a[23,23]==4
    a[22,19]=0; a[22,23]=0; a[23,19]=1; a[23,23]=1
    return a
g=maak(V_L,-5); save(g,'bokser'); gg=maak(VG,-6); save(gg,'bokser_groter')
for n,a in (('groot',g),('groter',gg)):
    print(n,'diff t.o.v. r17:',int((a!=o).sum()))
    for j in range(20,38): print('%2d '%j+''.join(str(v) if v else '.' for v in a[j,16:44]))
