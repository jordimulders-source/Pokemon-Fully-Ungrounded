"""Sunperor: poetsen per zone op onderlaag A (vogelrecept: S 0,36; kopgroep kroon+kop 1,2xS breed / 1,45xS hoog rond het halsgewricht;
romp 1,0xS; vleugel 0,95xS; poten 0,75xS lang; staf 1,55xS dik / 0,78xS lang; kroonpunt 0,6xS).
Elke pixel komt uit de onderlaag of uit een benoemde regel hieronder. python3 poets.py [stap] -> icon_f1.png (32x32)"""
import sys,os,numpy as np
from collections import Counter
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/'
STAP=int(sys.argv[1]) if len(sys.argv)>1 else 99
sys.argv=['bouw.py','A','0.36']; __file__=H+'bouw.py'
exec(open(H+'bouw.py').read().split("if __name__")[0])
c=np.array(Image.open(H+'A.png')); LOG=Counter()
def put(zone,pts,v):
    for x,y in pts:
        if c[y,x]!=v: c[y,x]=v; LOG[zone]+=1
def weg(zone,pts):
    for x,y in pts:
        if c[y,x]: c[y,x]=0; LOG[zone]+=1
def ic(x,y,n): p=naar_icoon(x+0.5,y+0.5,n); return int(np.floor(p[0])),int(np.floor(p[1]))
# REGEL 'dun deel': dunne onderdelen slijten bij de 45%-dekking weg. Zij worden voorwaarts afgebeeld: elke niet-donkere frontpixel
# van het deel naar zijn icoonpixel (meest voorkomende kleur per icoonpixel, via MAP), op minstens 2 px dik (REGELS_PER_BOUW:
# lang en dun >= 2 px, staf korter en dikker), daarna een omlijning van 1 px waar het deel aan leeg of aan een ander deel grenst.
def dun(n,zone,dik=(0,0),lijn=15,over=True):
    i=names.index(n); stem={}
    for y,x in zip(*np.nonzero((lab==i)&(fr>0)&~np.isin(fr,list(DONKER)))):
        X,Y=ic(x,y,n); stem.setdefault((X,Y),Counter())[MAP[int(fr[y,x])]]+=1
    pts={}
    for (X,Y),cn in stem.items():
        for dx in range(dik[0]+1):
            for dy in range(dik[1]+1):
                q=(X+dx,Y+dy)
                if q not in pts: pts[q]=cn.most_common(1)[0][0]
    for (X,Y),v in pts.items():
        if over or c[Y,X]==0: c[Y,X]=v; LOG[zone]+=1
    for (X,Y) in pts:
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            q=(X+dx,Y+dy)
            if q not in pts and c[q[1],q[0]]==0: c[q[1],q[0]]=lijn; LOG[zone]+=1
    return pts
def raster(zone,y,x0,rij):
    """rij als tekst: '.' leeg, ' ' ongemoeid, anders hex-index"""
    for i,ch in enumerate(rij):
        if ch==' ': continue
        v=0 if ch=='.' else int(ch,16)
        if c[y,x0+i]!=v: c[y,x0+i]=v; LOG[zone]+=1
# Plekken hieronder = frontpunten door bouw.naar_icoon (zie toelichting per zone); kleuren = MAP van de frontkleur ter plekke.
# KROON-ONDERRAND links: front rij 22 x9-20 (paarse rand + rood) -> rij 14,7 x7-12: rij 13-14 kroon, rij 15 omlijning; gat (9,13) dicht
raster('kroon',13,8,'cddd'); raster('kroon',14,7,'fcddd')
# KROONPUNT (lange veerpunt 0,6xS, >= 2 px dik): front x9-12 rij 23-31, rood met paarse punt -> x7-8 rij 15-16
raster('kroonpunt',15,6,'fadfff'); raster('kroonpunt',16,6,'fbbf'); raster('kroonpunt',17,7,'ff')
# KOP (kopgroep 1,2 x 1,45): front x21-33 rij 19-27 -> x12-17 rij 13-17 (x12 en x17 omlijning).
#  rij 13 = kopkruin front rij 19-20 (bruin '44' tussen donker) -> x14-15 bruin;
#  rij 14 = maskertop front rij 22: rood, snavelrug (26-27) -> x14 grijs (lichtgrijs zou een 12e kleur zijn; Gen 3 houdt 7-9 kleuren);
#  rij 15 = ogen front rij 23-24: wit (24,23) -> x13 met donker links (23,23) = x12; snavel grijsblauw (27,23) -> x14;
#           wit (29,23) -> x15 met donker (30-31,23) -> x16;
#  rij 16 = front rij 25: haaksnavel grijs (24-26) -> x13-14, rood (28-31) -> x15-16;
#  rij 17 = front rij 26: haakpunt (23,26) -> x13, kin rood (26-29) -> x14-16
raster('kop',13,12,'ff66ff')
raster('kop',14,12,'fa1aaf')
raster('kop',15,12,'f313ff')
raster('kop',16,12,'f11aaf')
raster('kop',17,12,'f1aaaf')
# NEK/LIJF onder de kop: front rij 27-30 donker (2/3 -> grijs) -> rij 18 x13-16 grijs, schouder links bruin (front '44' x21-23 rij 28-29)
raster('lijf',18,12,'e6111e')
# STAF (korter en dikker, 1,55 x 0,78): front x13-18; kop (ornament) rij 18-27 6 breed -> x9-11 rij 17-19; steel x14-17 -> x10-11 rij 20-22;
#  goud links (front b/c, licht), roodbruin rechts (front f) -> 8/9 links, 6 rechts; omlijning eromheen (rechts = lijfrand x12)
raster('staf',16,9,'fff')
raster('staf',17,8,'f896e')
raster('staf',18,8,'e896e')
raster('staf',19,8,'e896e')
raster('staf',20,9,'e86e')
raster('staf',21,9,'e86e')
raster('staf',22,9,'e86e')
# HAND (vleugelpunt om de staf): front x12-20 rij 40-47 bruin/donker -> x9-12 rij 23-25; stafvoet (16-18,47-48) -> (11,25)
raster('hand',23,8,'e66 ')
raster('hand',24,8,'e616')
raster('hand',25,9,'e66e')
raster('hand',26,10,'ee')
# VLEUGEL (geheven, 0,95xS): onderarm front x35-47 rij 28-33 -> x18-22 rij 18-19 (boven bruin = licht, onder grijs = schaduw);
#  handpennen front x47-55 rij 18-28 omhoog -> x22-24 rij 14-18, punt rond bovenaan (front (51-54,18))
raster('vleugel',13,23,'ff')
raster('vleugel',14,22,'f66f')
raster('vleugel',15,22,'f61f')
raster('vleugel',16,22,'f61f')
raster('vleugel',17,17,'effff61e')
raster('vleugel',18,17,'e66666e')
raster('vleugel',19,17,'e11111e')
raster('vleugel',20,18,'eeeee')
# POTEN (stompjes 2 px, 0,75xS lang): linkerpoot front x24-28 -> x13-14, rechterpoot x30-35 -> x16-17; rij 53-60 -> rij 27-28; tenen rij 61 -> rij 29
raster('poten',27,12,'e86e86e')
raster('poten',28,12,'e86e86e')
raster('poten',29,12,'eee.eee')
# BUIK (herkenningsteken, gouden ei): frontbuik (kleuren 10/11/12 in de romp) voorwaarts afgebeeld, meest voorkomende kleur per
#  icoonpixel binnen het lijf (x13-16): licht linksboven (c -> geel 9), goud (b -> 8), schaduw rechtsonder (a -> bruin 6)
i=names.index('romp'); st={}
for y,x in zip(*np.nonzero((lab==i)&np.isin(fr,[10,11,12]))):
    X,Y=ic(x,y,'romp'); st.setdefault((X,Y),Counter())[int(fr[y,x])]+=1
for (X,Y),cn in st.items():
    if 13<=X<=16 and c[Y,X] not in (0,14,15): put('buik',[(X,Y)],MAP[cn.most_common(1)[0][0]])
# LIJF RECHTS: de front-lijfrand is een ei (x41 bij rij 40-46 -> icoon x19-20); de onderlaag sleet 1 px in -> rand naar x19 op rij 21-23
put('lijf',[(18,21),(18,22),(18,23)],1); put('lijf',[(19,21),(19,22),(19,23)],14)
# KROONTOP rond (boller, geen recht stuk van 4): (14,3),(17,3) weg, (14,4),(17,4) worden rand
weg('kroontop',[(14,3),(17,3)]); put('kroontop',[(14,4),(17,4)],15)
# STIPPEN in de kroon: 15 gouden stippen in de front, Gen 3 dunt herhaalde patronen uit tot ±60 % -> 7 stippen van 1 px (geel 9),
#  op de afgebeelde plek van frontstippen, niet op de rand en niet naast elkaar: front (15,14),(19,10),(23,7),(29,6),(37,10),(42,14),(34,4)
put('stippen',[(9,10),(11,8),(13,6),(15,6),(19,8),(21,10),(17,5)],9)
if __name__=='__main__':
    im=Image.fromarray(c,'P'); im.putpalette(IP.flatten().tolist()); im.save(H+'icon_f1.png',transparency=0)
    print(dict(LOG))
