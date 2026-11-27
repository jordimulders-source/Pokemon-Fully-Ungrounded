# Eindkeuring stap 1: rechte lijnen (geest, rechtervleugel, linkerkop, onderste kronkel) + belijning.
# python3 e1_bewerk.py  -> raster_e1.txt, log op stdout
from lib import *
R=lees('raster_r7A.txt'); O=[r[:] for r in R]
LOG=[]
def zet(x,y,c,why):
    if R[y][x]!=c:
        LOG.append((x,y,R[y][x],c,why)); R[y][x]=c

# --- 1a geestvlam: bovenste sliert als boog (randlopen 1,1,1,2,3,2,1 i.p.v. 8 recht) ---
G='geest boog'
zet(56,18,'l',G)                       # haakpunt buigt naar links (model 40%)
zet(57,22,'l',G)
for x,c in zip(range(54,61),'lllwwwl'): zet(x,23,c,G)   # 54-56 erbij (model 40%)
for x,c in zip(range(52,60),'llwwwlll'): zet(x,24,c,G)  # kern in de sliert, geen 8 l op rij
# middenwisp boven de vleugelpunt: bult (model 40% op 55-57,r30), onderrand trapsgewijs
zet(56,30,'l','geest bult'); zet(57,30,'l','geest bult')
for x,c in zip(range(54,63),'llpplllll'): zet(x,31,c,'geest bult')
zet(60,31,'p','geest bult')
for x,c in zip(range(55,62),'ppplll.'): zet(x,32,c,'geest onderrand')   # (61,32) weg: model 50%
zet(56,33,'p','geest onderrand'); zet(57,33,'l','geest onderrand')      # (57,33) erbij: model 30%
# onderkant bij de staart: dubbele l-band (r42+r43) -> 1 px rand, kern uit model
for x,c in zip(range(50,58),'lppwwppp'): zet(x,43,c,'geest staart')
# --- 1b rechtervleugel: bovenrand met polsbult (model) i.p.v. 8 recht ---
V='vleugel boog'
zet(43,30,'.',V); zet(43,31,'D',V)
zet(49,30,'l',V); zet(50,30,'p',V)      # geestsliert loopt door tot de vleugel
for x in range(49,53): zet(x,31,'D',V)
# --- 1c linkerkop: bolle schedel i.p.v. hoek (randlopen 1,1,0,1,1,1,2,4,8) ---
H='kop links boog'
zet(7,10,'.',H)                          # model 60%
zet(12,9,'D',H); zet(13,9,'D',H)         # model 30%
zet(12,10,'B',H)                         # wordt binnen; 13-14 blijven D (wenkbrauwlijn uit model, lum 30)
zet(1,17,'D',H); zet(2,17,'B',H); zet(1,18,'B',H)   # snuit rond (model 40%)
# --- 1d onderste kronkel: lijn als doorhangende boog (model r59/60/59) ---
K='kronkel onder boog'
zet(34,59,'K',K); zet(33,60,'b',K); zet(34,60,'b',K); zet(41,59,'K',K); zet(41,60,'b',K)

# --- 2 belijning ---
def bg(x,y): return not(0<=x<64 and 0<=y<64) or R[y][x]=='.'
N4=((1,0),(-1,0),(0,1),(0,-1))
def gezicht(x,y): return (x<=16 and 14<=y<=28) or (30<=x<=50 and 3<=y<=11)
def vleugel(x,y): return 36<=x<=54 and 28<=y<=41
for y in range(64):
    for x in range(64):
        if R[y][x]!='K' or gezicht(x,y): continue
        buiten=any(bg(x+dx,y+dy) for dx,dy in N4)
        if buiten: continue
        if vleugel(x,y): zet(x,y,'D','binnenlijn niet zwart'); continue
        # diepste schaduw (DC: zwart alleen voor de diepste schaduw): lijn grenst aan schaduwtint d -> zwart blijft
        bur=[O[y+dy][x+dx] for dx,dy in N4]
        if 'd' in bur: continue
        zet(x,y,'n','binnenlijn niet zwart')
# lichtkant linkerkronkel: bovenrand in eigen donkerste tint
for x,y in [(12,43),(13,43),(14,43),(9,44),(10,44),(11,44),(8,45),(7,46),(6,47)]:
    zet(x,y,'n','buitenlijn lichtkant')
schrijf(R,'raster_e1.txt')
from collections import Counter
print(Counter(w for *_,w in LOG))
for l in LOG:
    if l[2]=='.' or l[3]=='.': print('ALPHA',l)
