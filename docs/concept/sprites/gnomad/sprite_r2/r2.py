# r2.py: sprite_r1 (A/B) -> r2. Alleen (1) riem met volume en (2) zwarte pixels rechts naast de neus ('oog'); verder diff 0 (assert).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r1'); from gemeen import lees, opslaan
R1='../sprite_r1/'
zone=np.load(R1+'zone_af.npy'); L=np.load(R1+'lijn.npy'); riem1=np.load(R1+'riem.npy')
zone[26,43]=5; L[26,43]=False   # zelfde reparatie als r1 (mutspixel in lijf)
L[43,26]=False
def top(X): u=(X-25.0)/14.0; return 40.6+3.4*(1-u*u)+0.8*u
body=(np.isin(zone,(5,8))|riem1)&~L
def bouw(var):
    im=Image.open(R1+'gnomad_%s.png'%var); pal=[tuple(im.getpalette()[3*k:3*k+3]) for k in range(16)]
    o=np.asarray(im).astype(int).copy(); r1=o.copy()
    LICHT,DONK,HOOG=(14,15,12) if var=='A' else (9,15,10)
    riem=np.zeros((64,64),bool); zone_riem={}
    # (1) riem: dikte 4 in het midden, 3 op de flanken (r1: 3/2), zelfde bovenrand; bovenrij licht met hooglicht links van het midden,
    #     onderrij 1 px donkere rand, rechter derde donker; broekrij direct onder de riem in schaduw (riem zit 'erom')
    for Y,X in zip(*np.where(body)):
        t=int(round(top(X))); u=(X-25)/14; dik=4 if abs(u)<0.55 else 3
        if t<=Y<t+dik:
            riem[Y,X]=True
            if Y==t+dik-1 or X>=33: o[Y,X]=DONK
            elif Y==t and 17<=X<=26: o[Y,X]=HOOG
            else: o[Y,X]=LICHT
        elif Y==t+dik:
            o[Y,X]=10 if X<30 else 9
    # randen links van de riem (buitenlijn naast de nieuwe riemrijen): blauwe selout -> riem donker
    # (2) 'oog' rechts naast de neus: zwarte ring om (25,29)-(26,30) openbreken naar het model (neusrand donkerroze, schaduw onder de mutsrand roze)
    OOG=[(24,29,6),(24,30,6),(27,30,7),(28,30,7),(25,31,7),(26,31,6)]
    for x,y,k in OOG: o[y,x]=k
    m=np.zeros((64,64),bool)
    for x,y,k in OOG: m[y,x]=True
    zone_mask=riem|riem1|np.isin(zone,(5,8))
    d=(o!=r1)
    assert not (d&~zone_mask&~m).any(), np.argwhere(d&~zone_mask&~m)
    opslaan(o,'gnomad_%s.png'%var,pal)
    print(var,'diff t.o.v. r1: riem/lijf/broek %d px, oog %d px, elders %d px'%((d&zone_mask&~m).sum(),(d&m).sum(),(d&~zone_mask&~m).sum()))
    print('   waarvan riem nieuw %d, schaduwrij onder de riem %d'%((d&riem).sum(),(d&~riem&zone_mask&~m).sum()))
bouw('A'); bouw('B')
