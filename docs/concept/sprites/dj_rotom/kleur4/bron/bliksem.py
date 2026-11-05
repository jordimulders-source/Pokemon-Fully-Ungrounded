"""kleur4: bliksem opnieuw (zone x17-31, y0-25). Vorm per rij met de hand (L/R = randkolommen),
opbouw: rand 1, daarbinnen 2, kern 3; noot wit met een rand 1 eromheen. Rest = kleur3."""
import sys, numpy as np
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/tools/concept/sprites')
from ascii_sprite import parse
CH='.123456789abcdef'
A=parse('../../kleur3/bron/dj_rotom.txt')[0].astype(int)
A[0:26,17:32]=0
S=np.zeros((64,64),bool)
ROWS={10:(25,30),11:(24,30),12:(23,29),13:(23,29),14:(22,28),15:(21,28),16:(21,27),
      17:(20,30),18:(20,30),19:(24,29),20:(24,29),21:(25,29),22:(25,28),23:(25,28),24:(25,28),25:(25,28)}
for y,(l,r) in ROWS.items(): S[y,l:r+1]=True
   # bovenrand van de uitsteker hoort bij de vorm
def edge(m):
    q=np.pad(m,1); return m&~(q[:-2,1:-1]&q[2:,1:-1]&q[1:-1,:-2]&q[1:-1,2:])
S2=S.copy(); S2[26,25:29]=True
E1=edge(S2)&S; I1=S2&~edge(S2); E2=edge(I1)&I1
# spitsaansluiting: rij 25 grenst aan de gloed van de spits (rij 26) -> niet als rand tellen
for y in range(8,26):
    for x in range(17,32):
        if S[y,x]: A[y,x]=1 if E1[y,x] else (2 if (E2[y,x] or y<=16) else 3)
# staart: kern van 2 px (x26-27) tot in de spits
for y in range(20,26):
    for x in (26,27):
        if S[y,x] and not E1[y,x]: A[y,x]=3
# rij 18: onderrand van het blok links (19-23) rand; uitsteker-onderkant
NOTE=[(26,11),(26,12),(26,13),(26,14),(26,15),(27,11),(28,12),(24,15),(25,15),(24,16),(25,16)]
for x,y in NOTE: A[y,x]=15
if len(sys.argv)<2 or sys.argv[1]!='zonderrand':
    for x,y in NOTE:
        for dx,dy in((1,0),(0,1),(-1,0),(0,-1)):
            xx,yy=x+dx,y+dy
            if A[yy,xx] in (2,3) and (xx,yy) not in NOTE: A[yy,xx]=1
with open('dj_rotom.txt','w') as f:
    f.write('== frame 1\n')
    for r in A: f.write(''.join(CH[v] for v in r)+'\n')
