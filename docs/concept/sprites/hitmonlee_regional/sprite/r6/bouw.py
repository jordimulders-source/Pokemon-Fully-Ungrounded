# r6 = r5 + reparaties per zone (alle pixels gelogd in r6/log.txt):
#  A. trapbeen-ringen rij 11-22: rijtype uit het model (M_donker: lijnrijen 11*,13,15,17,20,22; *11 = de lijn onder de voet
#     die in geschrapte 2x-rij 10.5 zat), lijnrij binnenin = 2, bandrij binnenin = M_2e (op een na lichtste natieve pixel = de verlichte ringkleur)
#     binnen de ringtinten. Buitenrand blijft 1/2 zoals r5.
#  B. oog en verre oog per pixel uit M_gem/M_donker (zie lijst).
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/hitmonlee_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64, lab
PAL=eval(open(D+'r4/bouw.py').read().split('PAL=')[1].split(']')[0]+']'); PL=lab(np.array(PAL[1:],float))
L5=np.load(D+'r5/idx.npy'); L=L5.copy()
Mg=np.load(D+'M_gem.npy'); Md=np.load(D+'M_donker.npy'); Ml=np.load(D+'M_licht.npy'); Mz=np.load(D+'M_zonderlijn.npy'); M2=np.load(D+'M_2e.npy')
log=open(D+'r6/log.txt','w')
def zet(x,y,k,why):
    if L[y,x]!=k: log.write(f'({x},{y}) {L[y,x]}->{k} {why}\n'); L[y,x]=k
RING=[15,8,7,6,5,4,3]
def in_ramp(k,ramp):
    if k in ramp: return k
    return ramp[int(((PL[np.array(ramp)-1]-PL[k-1])**2).sum(1).argmin())]
# A
LIJN={11,13,15,17,20,22}
for y in range(11,23):
    xs=[x for x in range(30,50) if L5[y,x]>0]; a,b=xs[0],xs[-1]
    for x in range(a+1,b):
        if y in LIJN: zet(x,y,2,'A ringlijn')
        else: zet(x,y,in_ramp(M2[y,x],RING),'A ringband M_2e')
# B. oog (per pixel uit de natieve 2x2-blokken, zie NOTITIES): bovenlijn r29, dikke zwarte linkerhoek, rode iris,
#    glans (20,30) met bleke reflectie eronder, oranje onderkant, onderlijn r32-33.
OOG={29:{18:2,19:1,20:1,21:1,22:1,23:2},
     30:{16:5,17:1,18:1,19:3,20:10,21:2,22:3,23:2},
     31:{16:6,17:1,18:2,19:3,20:8,21:6,22:5,23:2},
     32:{17:6,18:1,19:3,20:5,21:6,22:6},
     33:{19:2,20:2}}
VER={24:{27:2,28:2},25:{27:1,28:2,29:1},26:{27:2,28:3,29:1},27:{27:1,28:10,29:2},28:{27:1,28:1,29:2}}
for y,row in OOG.items():
    for x,k in row.items(): zet(x,y,k,'B oog')
for y,row in VER.items():
    for x,k in row.items(): zet(x,y,k,'B ver oog')
# C. standbeen-ringen rij 44-53 (verticale deel): lijnrijen uit de natieve donkerrijen (44,46,48,51,53),
#    bandrijen = M_2e binnen de ringtinten (zoals A).
LIJN2={44,46,48,51,53}
for y in range(44,54):
    xs=[x for x in range(46,59) if L5[y,x]>0]; a,b=xs[0],xs[-1]
    for x in range(a+1,b):
        if y in LIJN2: zet(x,y,2,'C ringlijn standbeen')
        else: zet(x,y,in_ramp(M2[y,x],RING),'C ringband standbeen M_2e')
np.save(D+'r6/idx.npy',L)
save_p64(L,PAL,D+'r6/sprite.png'); save_idx(L,PAL,D+'r6/r6_10x.png',10)
