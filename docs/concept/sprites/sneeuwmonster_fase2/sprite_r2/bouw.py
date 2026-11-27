# Ronde 2 (= ronde 1 + randnormaal voor de selout): kale reductie + stenen-zone + omlijning + ontkorrelen + beschermde zones (ogen, mond). Gebruik vanuit sneeuwmonster_fase2.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *; from kaal import reduceer; from steen import stenen
o=reduceer(); kaal=o.copy(); opslaan(kaal,'sprite_r2/kaal.png')
o,info=stenen(o); print('stenen',info)
N4=((1,0),(-1,0),(0,1),(0,-1))
# 1. sneeuwkleurige randpixels boven op de emmer (antialias van de emmerrand) -> emmerrand
for Y in range(0,16):
    for X in range(64):
        if o[Y,X] in SNEEUW and Y<14 and X>=24: o[Y,X]=7
# 1b. inkeping in de bovenrand van de emmer (x30, rij 3) dicht: modelrand loopt daar recht door
o[3,30]=9
# r2: losse bultpixel (35,3) weg (model 54 % achtergrond, grensgeval); bovenrand loopt dan glad x30-33 -> rij 4
o[3,35]=0
# 2. ontkorrelen: clusters <3 px van vlaktinten nemen de meest voorkomende buurtint (zelfde groep); lijnen 2/3 alleen losse stippen
def ontkorrel(o,groep,tinten,minsize=3):
    for k in tinten:
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minsize: continue
            buren={}
            for Y,X in zip(*np.where(m)):
                for dy,dx in N4:
                    v=o[Y+dy,X+dx]
                    if v in groep and v!=k: buren[v]=buren.get(v,0)+1
            if buren: o[m]=max(buren,key=buren.get)
    return o
o=ontkorrel(o,SNEEUW,[4,5,6])
# losse lijnstippen: alleen een 2/3-pixel zonder enige lijnbuur (8-buren) verdwijnt
for Y,X in zip(*np.where(np.isin(o,[2,3]))):
    if not any(o[Y+dy,X+dx] in (1,2,3) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx):
        nb=[o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] in (4,5,6)]
        if nb: o[Y,X]=max(set(nb),key=nb.count)
o=ontkorrel(o,HOUT,[8,9]); o=ontkorrel(o,HOUT,[7],minsize=2)
# 3. buitenlijn: randpixel van de figuur -> lijn; lichtkant (lege buur alleen links/boven) = gekleurde selout, anders zwart
fg=o>0
def leeg(Y,X): return not(0<=Y<64 and 0<=X<64) or not fg[Y,X]
for Y,X in zip(*np.where(fg)):
    lb=[(dy,dx) for dy,dx in N4 if leeg(Y+dy,X+dx)]
    if not lb: continue
    # randnormaal uit alle lege 8-buren: wijst hij naar linksboven (nx+ny<0, of 0 met nx<0) -> lichtkant
    nx=sum(dx for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and leeg(Y+dy,X+dx))
    ny=sum(dy for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and leeg(Y+dy,X+dx))
    licht=nx+ny<0     # linksonder (nx+ny=0) = schaduwkant
    v=o[Y,X]
    if v in SNEEUW: o[Y,X]=2 if licht else 1
    elif v in HOUT or v in GRIJS: o[Y,X]=7 if licht else 1
# 3b. binnenlijnen in en onder de emmer niet zwart maar donkerste hout (zwart alleen op de buitenrand)
for Y,X in zip(*np.where(o==1)):
    if Y<20 and any(o[Y+dy,X+dx] in HOUT for dy,dx in N4) and not any(leeg(Y+dy,X+dx) for dy,dx in N4): o[Y,X]=7
# 4. ogen (beschermd): grijze schijf met zwarte spleet, maat/plek/spleetrij gemeten op het model (zie NOTITIES)
for Y in range(18,26):
    for X in range(19,37):
        if o[Y,X] in (1,10,11): o[Y,X]=6
L_OOG=[(19,'.gg.'),(20,'gGgg'),(21,'KKKK'),(22,'gggg'),(23,'.gg.')]
R_OOG=[(20,'.ggg.'),(21,'gGggg'),(22,'KKKKK'),(23,'ggggg'),(24,'.ggg.')]
for x0,oog in ((21,L_OOG),(30,R_OOG)):
    for Y,r in oog:
        for i,ch in enumerate(r):
            if ch!='.': o[Y,x0+i]={'g':10,'G':11,'K':1}[ch]
# 5. mond (beschermd): één lijn in de lijntint, krul links omhoog, zwart krulletje rechts zoals het model
for Y in (24,25,26,27):
    for X in range(19,36):
        if o[Y,X] in (2,3,1) and not (Y==24 and X in range(30,35)): o[Y,X]=6
for X in range(21,29): o[25,X]=2
for X in range(29,34): o[26,X]=2
o[24,20]=2; o[25,34]=1
opslaan(o,sys.argv[1] if len(sys.argv)>1 else 'sprite_r2/sneeuwmonster2_r1.png'); toon(o)
# 6. baardfranje (beschermd): de zigzaglijn valt bij de reductie uiteen (1 natieve cel = 0,47 spritepx).
#    Per spritekolom de rij met de meeste modellijn (profiel in halve rijen, zie NOTITIES) -> lijntint 2; tanden verticaal verbonden;
#    1 px lichtblauw (5) eronder zoals de schaduwrand onder de lijn in het model.
PAD={14:30,15:29,16:29,17:28,18:27,19:28,20:27,21:31,22:30,23:31,24:31,25:32,26:33,27:32,28:31,29:32,30:32,31:32,32:33,33:33,34:31,35:29,36:30,37:29,38:29,39:28,40:27}
for Y in range(27,34):
    for X in range(17,41):
        if o[Y,X] in (2,3): o[Y,X]=6
vorige=None
for X in sorted(PAD):
    Y=PAD[X]; o[Y,X]=2
    if vorige is not None and abs(Y-vorige)>1:
        for yy in range(min(Y,vorige)+1,max(Y,vorige)): o[yy,X]=2
    vorige=Y
for X in sorted(PAD):
    Y=PAD[X]
    if o[Y+1,X]==6: o[Y+1,X]=5
opslaan(o,sys.argv[1] if len(sys.argv)>1 else 'sprite_r2/sneeuwmonster2_r1.png'); toon(o,24,36,8,50)
