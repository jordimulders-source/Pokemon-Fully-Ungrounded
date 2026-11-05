"""kleur2: kleur1 buiten de zone x14-34 ongewijzigd; in de zone een grotere kop (x1,25, leidraad
silhouet3/s1.25) met de hand, de bliksem uit kleur1 5 rijen omhoog (zelfde maat), gloed 2 px rond het lijf.
Gebruik: python3 bouw_kleur2.py <variant> -> dj_rotom_<variant>.txt"""
import sys, numpy as np
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/tools/concept/sprites')
from ascii_sprite import parse
V=sys.argv[1] if len(sys.argv)>1 else 'A'
CH='.123456789abcdef'
K=parse('../../kleur1/bron/dj_rotom.txt')[0].astype(int)
X0,X1,YB=14,34,57
A=K.copy(); A[:YB+1,X0:X1+1]=0
body=np.zeros((64,64),bool)
def p(y,x,s):
    for i,c in enumerate(s):
        if c!='_' and c!=' ':
            A[y,x+i]=CH.index(c)
            if c not in '123': body[y,x+i]=True
# bliksem: kleur1 rijen 19-30 (x20-29) 5 rijen omhoog
bolt=np.zeros((64,64),bool)
for y in range(19,31):
    for x in range(20,30):
        if K[y,x]: A[y-5,x]=K[y,x]; bolt[y-5,x]=True
# spits (kleur1-opbouw, 1 rij langer)
p(26,27,'6'); p(27,26,'46'); p(28,26,'46'); p(29,26,'456'); p(30,25,'6456'); p(31,25,'64556')
# kop: bovenrand
p(32,18,'66666666'); p(32,26,'455'); p(32,29,'66'); p(32,31,'7777')
p(33,17,'6'+'4'*14+'6666')
# linkerspeaker-zijvlak x14, naad x15
p(38,14,'7'); 
for y in range(39,57): p(y,14,'67')
p(57,14,'77')
# kop voorvlak x16-30, zijvlak x31-34
for y in range(34,57):
    p(y,16,'6'+('4' if y<=44 else '5')+'5'*13+'6666')
p(57,16,'7'*19)
# ogen (opbouw kleur1, 6 hoog, schuin: bovenkanten naar buiten, verre oog 1 rij hoger)
eye=[".ff.","fccf","8fc8","8cd8","fddf",".ff."]
for i,r in enumerate(eye):
    p(36+i,18 if i<3 else 19,r.replace('.','_'))
    p(35+i,27 if i<3 else 26,r.replace('.','_'))
# grijns met tandjes (mondhoeken omhoog)
p(42,21,'8'); p(42,27,'8'); p(43,22,'8fff8'); p(44,23,'888')
# display
if V=='A':   # 4 brede blokjes (2 px), display x17-29
    p(46,18,'88'); p(46,27,'88')
    p(47,17,'8'*13); p(48,17,'8'*13)
    H=[2,4,1,3]
    for y in range(49,54):
        row=['8']*13
        for k,h in enumerate(H):
            top=54-h
            for dx in (0,1):
                if y>=top: row[1+3*k+dx]='2' if (y==top and h>1) else 'e'
        p(y,17,''.join(row))
    p(54,18,'8'*11)
else:        # 5 smalle staafjes, midden van de bovenrand lager
    p(46,18,'88'); p(46,28,'88'); p(47,18,'888'); p(47,27,'888')
    p(48,18,'8'*12)
    H=[1,3,4,2,4]
    for y in range(49,54):
        row=['8']*12
        for k,h in enumerate(H):
            top=54-h
            if y>=top: row[1+2*k]='2' if y==top and h>1 else 'e'
        p(y,18,''.join(row))
    p(54,19,'8'*10)
# snoer
p(51,14,'888'); p(51,30,'88888')
# rechterspeaker linkerrand naast de kop: naad
for y in range(32,39): A[y,35]=7
# gloed: 2 px rond alle lijfpixels, alleen in de zone
lijf=(K>=4)&~((np.arange(64)[None,:]>=X0)&(np.arange(64)[None,:]<=X1)&(np.arange(64)[:,None]<=YB))
allb=lijf|body
def d4(m):
    q=np.pad(m,1); return m|q[:-2,1:-1]|q[2:,1:-1]|q[1:-1,:-2]|q[1:-1,2:]
def d8(m):
    q=np.pad(m,1); r=m.copy()
    for dy in (0,1,2):
        for dx in (0,1,2): r|=q[dy:dy+64,dx:dx+64]
    return r
g=d8(d4(allb))
zone=np.zeros((64,64),bool); zone[:YB+3,X0:X1+1]=True
for y in range(64):
    for x in range(64):
        if zone[y,x] and g[y,x] and A[y,x]==0: A[y,x]=2
# gloedtinten opnieuw: buitenste ring 1, rest 2 (behalve plasma-kern 3 en de bliksem zelf)
M=A>0
for y in range(64):
    for x in range(64):
        if A[y,x] in (1,2) and not bolt[y,x]:
            n=[(y-1,x),(y+1,x),(y,x-1),(y,x+1)]
            A[y,x]=1 if any(not(0<=a<64 and 0<=b<64) or not M[a,b] for a,b in n) else 2
with open('dj_rotom_%s.txt'%V,'w') as f:
    f.write('== frame 1\n')
    for r in A: f.write(''.join(CH[v] for v in r)+'\n')
