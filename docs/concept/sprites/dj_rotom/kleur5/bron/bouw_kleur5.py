"""kleur5 = kleur4 + reparaties 1-5 uit kleur4/CONSISTENTIE.md. Elke reparatie telt haar pixels."""
import sys, numpy as np
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/tools/concept/sprites')
from ascii_sprite import parse
CH='.123456789abcdef'
K=parse('../../kleur4/bron/dj_rotom.txt')[0].astype(int)
A=K.copy(); tel={}
def mark(naam,before):
    tel[naam]=tel.get(naam,0)+int((A!=before).sum())
GLOED={1,2,3}
# --- 2. bliksem 3 omhoog, spits vrij y23-32 (zone x17-31, y0-32)
b=A.copy()
bolt=np.zeros((64,64),bool); bolt[10:26,17:32]=(K[10:26,17:32]>0)
A[0:33,17:32]=np.where(K[0:33,17:32]>=4,K[0:33,17:32],0)   # alleen lijf houden (kop-bovenrand y32)
A[0:26,17:32]=0
for y in range(10,26):
    for x in range(17,32):
        if bolt[y,x]: A[y-3,x]=K[y,x]
A[22,25:29]=[1,2,2,1]                      # staarteinde dicht: kern stopt op y21, gloed sluit af
spits={23:{26:7},24:{26:5,27:7},25:{26:5,27:7},26:{25:6,26:4,27:7},27:{25:6,26:4,27:5,28:7},
       28:{25:6,26:4,27:5,28:7},29:{24:6,25:5,26:4,27:5,28:7},30:{24:6,25:5,26:4,27:5,28:6,29:7},
       31:{24:6,25:5,26:4,27:5,28:6,29:7},32:{24:6,25:5,26:4,27:5,28:6,29:6}}
for y,r in spits.items():
    for x,v in r.items(): A[y,x]=v
bm=np.zeros((64,64),bool); bm[7:23]=bolt[10:26]
lijf=(A>=4)&~bm
def d4(m):
    q=np.pad(m,1); return m|q[:-2,1:-1]|q[2:,1:-1]|q[1:-1,:-2]|q[1:-1,2:]
def d8(m):
    q=np.pad(m,1); r=m.copy()
    for dy in (0,1,2):
        for dx in (0,1,2): r|=q[dy:dy+64,dx:dx+64]
    return r
g=d8(d4(lijf))
for y in range(0,33):
    for x in range(17,32):
        if A[y,x]==0 and (g[y,x] or K[y,x] in GLOED and y>=26): A[y,x]=2
M=A>0
for y in range(0,34):
    for x in range(16,33):
        if A[y,x] in (1,2) and not (7<=y<=22 and bolt[y+3,x] and K[y+3,x]==A[y,x]):
            n=[(y-1,x),(y+1,x),(y,x-1),(y,x+1)]
            A[y,x]=1 if any(not M[a,c] for a,c in n) else 2
mark('2 bliksem + spits (x16-32, y0-33)',b)
# --- 3. losse tanden
b=A.copy(); A[43,24]=8; mark('3 tanden (24,43)',b)
# --- 4. hooglicht als vlekjes
b=A.copy()
houd=set()
for x in range(18,22): houd.add((x,33))
houd|={(17,34),(17,35)}
for x in range(36,43):
    for y in (31,32,33): houd.add((x,y))
houd|={(36,34),(36,35)}
for x in range(6,10):
    for y in (39,40): houd.add((x,y))
houd|={(5,41),(5,42)}
ogen=lambda x,y:(18<=x<=23 and 35<=y<=41) or (25<=x<=31 and 34<=y<=41)
for y in range(64):
    for x in range(64):
        if A[y,x]==4 and (x,y) not in houd and not ogen(x,y) and not (y<=32 and 24<=x<=29):
            A[y,x]=5
mark('4 hooglicht -> midden',b)
# --- 1. contour binnen de gloed
b=A.copy()
B=A.copy()
for y in range(64):
    for x in range(64):
        if y<=32 and 24<=x<=29: continue          # spits niet
        v=B[y,x]
        rn=B[y,x+1] if x<63 else 0; dn=B[y+1,x] if y<63 else 0
        ln=B[y,x-1] if x>0 else 0; un=B[y-1,x] if y>0 else 0
        if v==7 and (rn in GLOED or dn in GLOED): A[y,x]=8
        elif v==6 and (ln in GLOED or un in GLOED): A[y,x]=7
A[38,14]=7   # hoekpixel linkerspeaker: geen losse zwarte stip
mark('1 contour (7->8 schaduwzijde, 6->7 lichtzijde)',b)
with open('dj_rotom.txt','w') as f:
    f.write('== frame 1\n')
    for r in A: f.write(''.join(CH[v] for v in r)+'\n')
for k,v in tel.items(): print('%-50s %d px'%(k,v))
print('totaal t.o.v. kleur4:',int((A!=K).sum()))
