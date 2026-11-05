"""Salticonda kleurronde 3c: vanaf kleur3b. (1) De kuif groeit naar achteren en rechtsboven met een kraag van
zoutplaten (2-4 px over de oude achterrand); (2) neusgaten weer zichtbaar in de neuskap, kap zachter in de snuit.
Bewerkt worden alleen: de kraagzone (rij 3-19, x >= oude buitenrand-1) en het snuitfront (x 4-14, y 5-10).
Al het andere is letterlijk kleur3b (check_kleur3c.py)."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'
I=CH.index
# nieuwe buitenrand (x) per rij; rij 12 = inkeping tussen twee kraagplaten
NOX={2:34,3:37,4:40,5:42,6:45,7:45,8:47,9:48,10:49,11:50,12:49,13:50,14:50,15:50,16:49,17:48,18:46,19:45}
RADIAAL=(7,12,16)
# voorkant en top van de kuif (rij 1-5) opnieuw met de hand: weer hoog over het voorhoofd zoals kleur3,
# met twee plaattoppen en een inkeping (25,1) waar de voorhoofdnaad begint. (x0, tekens); '.' = transparant
TOP={
 1:(21,"hhhh.hhhhhK"),
 2:(18,"hhhaabahaababbKKK"),
 3:(16,"hhaabbbbcgabbbccgbcKKK"),
 4:(14,"hhaabbbbbccgabbbcgabccgaKKK"),
 5:(13,"heeeeeeebbbb"),
 6:(13,"aa"),
}          # naad dwars door de kraag (Y op de kraagnaad)
KORREL=set()  # lichte zoutkorrels op de bovenrand van de kraag
# snuitfront: (x, y, teken), met de hand
SNUIT=[
 # dip achter de kap ondieper (1 tint, geen gat meer)
 (12,6,'h'),(11,7,'b'),(12,7,'b'),
 # kap: licht linksboven, iets donkerder rechtsonder
 (10,7,'b'),(11,8,'b'),(12,8,'b'),(13,8,'a'),
 # neusgaten: dichtbij 3 px (OO/O) tegen de voorrand, veraf 1x2 (K/K), kleiner
 (5,8,'O'),(6,8,'O'),(7,8,'a'),(8,8,'a'),(9,8,'K'),(10,8,'b'),
 (5,9,'O'),(6,9,'a'),(7,9,'a'),(8,9,'a'),(9,9,'K'),(10,9,'b'),(11,9,'b'),(12,9,'a'),(13,9,'a'),
 # schaduwrand onder de kap: 1 tint (b), loopt naar achter uit in a
 (6,10,'b'),(7,10,'b'),(8,10,'b'),(9,10,'b'),(10,10,'b'),(11,10,'a'),(12,10,'a'),(13,10,'a'),
]
def oud_ox(P,y):
    return max(x for x in range(48) if P[x,y]!=0)
def build():
    B=Image.open(D+'kleur3b/salticonda.png'); P=B.load()
    out=B.copy(); Q=out.load()
    old={y:oud_ox(P,y) for y in range(1,20)}
    old13=P[45,13]!=0
    if old13: old[13]=44          # het oude opkrulrandje (45,13) hoort bij de rand op x 44
    S={(x,y) for x in range(64) for y in range(64) if P[x,y]!=0}
    for y in range(2,20):
        for x in range(old[y]+1,NOX[y]+1): S.add((x,y))
    if old13: S.discard((45,13)) if NOX[13]<45 else None
    zone=lambda x,y: 2<=y<=19 and x>=old[y]-1
    for y in range(2,20):
        o=old[y]; n=NOX[y]
        for x in range(o-1,n+1):
            if (x,y) not in S: continue
            rand=any(q not in S for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)])
            if rand: Q[x,y]=I('K') if y<=9 else I('O'); continue
            if x<o:
                if CH[P[x,y]] in 'KO': Q[x,y]=I('c')
                continue
            if x==o: Q[x,y]=I('g'); continue
            t=(x-o)/max(1,n-o)
            if y in RADIAAL: ch='g'
            elif x-o==1: ch='a' if y<=8 else 'b'
            elif (y-1) in RADIAAL and x-o==2: ch='b'
            else: ch=('c' if t<0.5 else 'd') if y<=8 else ('d' if t<0.6 else 'e')
            Q[x,y]=I(ch)
    for y,(x0,t) in TOP.items():
        for i,ch in enumerate(t):
            x=x0+i
            if y==5 and 25<=x<=27: continue
            Q[x,y]=I(ch)
    # dwarsnaden in de kraag schuin laten aflopen (geen rechte streep van 4-5 px): buitenste helft 1 rij lager
    for y in RADIAAL:
        o=old[y]; n=NOX[y]
        for x in range(o+1,n):
            if x-o>(n-o)/2 and (x,y+1) in S and Q[x,y+1] not in (I('K'),I('O')):
                Q[x,y]=I('d'); Q[x,y+1]=I('g')
    for (x,y) in KORREL: Q[x,y]=I('a')
    for x,y,ch in SNUIT: Q[x,y]=I(ch)
    return out, old
if __name__=='__main__':
    im,old=build(); im.save(D+'kleur3c/salticonda.png',transparency=0)
    Q=im.load()
    open(D+'kleur3c/salticonda_raster.txt','w').write('\n'.join(''.join(CH[Q[x,y]] for x in range(64)) for y in range(64))+'\n')
