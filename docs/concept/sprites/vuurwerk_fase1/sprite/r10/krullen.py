# r10 (laatste stap: patch.py -> overlay.py -> krullen.py): krullen-zone rijen 3-12, kol 18-29 (spritekader; canvas +1 rij, +17 kol).
# Jordi over r9: "de krullen hebben teveel rechte lijnen, kijk of je dat kan oplossen, anders doen we ze gewoon weg".
# A: krullen als curven (looplengtes 1-1-2-2 / 2-1-1 i.p.v. r9's 6 px rechte rechterrand en 1-1-1-trap), 1 px golvende ruimte
#    (5,25)(6,25)(7,24)(8,23)(9,23). Vlamtong: ronde top 2 breed, leunt naar rechts; halvemaan: gebogen band, punt naar rechts.
#    Omvang binnen het model: tong rij 4-9 / kol 19-24, halvemaan rij 5-12 / kol 23-28 (model: 4,3-9 / 21-23,5 en 5,6-12,5 / 23-28,6).
# B: krullen weg; kopomtrek als koepel (looplengtes 5,2,1,1,3), bovenrand-band k links (zoals (8,16-18)), schaduwsikkel k rechts.
import numpy as np
from txt import CH
from reduce2 import save
ZONE=(3,13,18,30)
A_TXT="""
............
....bb......
...bLLb..bb.
...bLLb.bLb.
bbbLLb.bLLb.
kbLLb.bLLb..
ccbbb.bLLb..
cccccbLLb...
cccccbLLb...
ccccccbb#dd.
"""
B_TXT="""
............
............
............
............
bbbbb.......
kkkkcbb.....
cccccccb....
ccccccckb...
cccccckkb...
cccccckk#dd.
"""
def build(base,txt):
    a=base.copy(); rows=txt.strip().splitlines(); r0,r1,c0,c1=ZONE
    assert len(rows)==r1-r0
    for i,s in enumerate(rows):
        assert len(s)==c1-c0
        for j,ch in enumerate(s): a[r0+i,c0+j]=CH.index(ch)
    return a
if __name__=='__main__':
    base=np.load('sprite_overlay.npy')   # = r9 sprite_A (keten patch.py -> overlay.py)
    A=build(base,A_TXT); B=build(base,B_TXT)
    np.save('sprite_A.npy',A); np.save('sprite_B.npy',B)
    r0,r1,c0,c1=ZONE; m=np.zeros(base.shape,bool); m[r0:r1,c0:c1]=True
    for n,x in (('A',A),('B',B)):
        d=(x!=base); print(n,'gewijzigd in zone:',int(d[m].sum()),'| buiten zone:',int(d[~m].sum()))
