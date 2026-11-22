# maak.py r9 (vanaf r8): keurreparaties r8 (alleen herkleuren) + Jordi's gat in de tooi (enige silhouetwijziging).
# Elke wijziging is (x,y,oud,nieuw); oud wordt gecontroleerd. Kleurindices zie palet.py.
import numpy as np, json
from render import schrijf
H='.123456789abcdef'
a=np.load('../sprite_r8/samba_r8.npy'); r8=a.copy()
E={}
def z(naam,lst): E[naam]=lst
# 0 Jordi: tweede tooiveer van rechts onder (gele punt) 2 rijen dikker naar boven, gat naar het model (wig x48)
z('0_tooiveer_gat',[(45,14,0,5),(46,14,0,5),(47,14,0,1),
    (45,15,0,2),(46,15,0,3),(47,15,0,1),
    (44,16,5,2),(45,16,5,3),(46,16,8,6),(47,16,1,6),(44,15,1,5),(48,17,5,1),(48,19,5,1)])
# 1 rechtervleugel: per veer 2 | 3 3 (3) | 5 ; 4 alleen als sikkel achter/onder (x54-56,y18-25 en y25-26)
z('1_vleugel',[(50,21,4,3),(49,22,4,3),(53,22,4,3),(48,23,4,3),(52,23,4,3),(48,24,4,3),(52,24,4,3),(48,25,4,3),(54,24,3,2)])
# 2a tooiveren rechts (x33-41,y12-16)
z('2a_tooi_rechts',[(37,13,4,3),(37,14,4,3),(35,15,4,3),(36,15,4,3),(37,15,8,6),(39,14,8,7),(40,15,8,7),(40,16,8,7),(34,15,3,2),(37,12,3,5)])
# 2b meest linkse tooiveer (x15-21,y17-21): groen onderblad 2-rij licht / 3-rij vulling; losse gele pixels opnemen
z('2b_tooi_links',[(19,20,3,2),(19,21,4,3),(20,21,4,3),(16,19,6,7),(21,20,7,6)])
# 3 onderrand waaier: y24 doorlopend zwart, y25 slagschaduw 3 (linkerste 2 px blijven 2)
z('3_waaierrand',[(29,24,8,1),(31,24,8,1),(34,24,8,1)]+[(x,25,2,3) for x in range(29,35)])
# 4 franje/buik: 4 stroken (x26-27, 29-30, 34-35, 37-38), geel 6 links / 7 rechts, groen ertussen
z('4_franje',[(28,45,6,4),(29,45,7,6),(28,46,6,4),(29,46,7,6),(27,45,4,7),(26,46,7,6),(27,46,4,7),(27,47,4,7),
    (28,47,7,4),(28,48,8,4),
    (30,45,3,7),(30,46,3,7),(30,47,3,7),(29,47,7,6),(30,48,4,7),(29,48,8,7),
    (34,46,4,6),(35,46,6,7),(36,46,7,4),(34,47,8,6),(35,47,8,7),
    (37,46,4,6),(38,45,7,7),
    (39,43,8,7),(39,44,8,7),(40,43,5,4),(40,44,5,4),(32,42,4,3),(33,42,8,6)])
# 5 gele band linkervleugel: 8 = sikkel onderrand + 1 nerf (20,43)-(21,44)-(22,45); rest 7, lichtkant 6
z('5_band_links',[(16,42,7,6),(21,42,8,6),(22,42,8,6),
    (16,44,6,7),(17,44,6,7),(18,44,6,7),(19,44,6,7),(20,44,6,7),(15,44,8,7),
    (16,45,7,8),(18,45,7,8),(21,45,7,8),(25,42,7,6)])
# 6 borstband: gaatjes dicht, onderrand y38 doorlopend 8
z('6_borstband',[(29,34,7,6),(30,34,3,6),(31,34,3,6)]+[(x,38,7,8) for x in range(28,32)]+[(34,38,3,8)])
log={}
for k,l in E.items():
    n=0
    for x,y,o,nw in l:
        assert a[y,x]==o,(k,x,y,a[y,x],o)
        if o!=nw: a[y,x]=nw; n+=1
    log[k]=n
# alpha: alleen zone 0 mag veranderen
d=np.argwhere((a>0)!=(r8>0))
assert all((x,y) in {(45,14),(46,14),(47,14),(45,15),(46,15),(47,15)} for y,x in d), d
log['alpha_gewijzigd']=[(int(x),int(y)) for y,x in d]
np.save('samba_r9.npy',a); schrijf(a,'samba.png')
json.dump(log,open('log_r9.json','w'),indent=1)
print(log)
def show(x0,x1,y0,y1):
  print('   '+''.join(str(x%10) for x in range(x0,x1)))
  for y in range(y0,y1): print('%02d '%y+''.join(H[v] for v in a[y,x0:x1]))
show(10,60,10,50)
