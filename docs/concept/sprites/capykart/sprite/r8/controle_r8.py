"""Controle r8 t.o.v. r7: alpha-diff, bevroren zones, kleine clusters, wijzigingen per zone -> log.txt"""
import os, json, collections
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
A=Image.open(os.path.join(D,'../../eindkeuring/capykart_r7.png')); B=Image.open(os.path.join(D,'capykart.png'))
a=A.load(); b=B.load(); W,H=A.size
ad=sum(1 for y in range(H) for x in range(W) if (a[x,y]==0)!=(b[x,y]==0))
frozen={'oog':[(x,y) for x in range(28,32) for y in range(16,22)],'tanden':[(x,y) for x in range(17,24) for y in range(30,34)],
 'morrillo':[(x,y) for x in range(21,24) for y in (15,16)],'neusgaten':[(15,22),(16,22)],'mond':[(18,28),(19,28)],'kinlijn':[(x,30) for x in range(25,29)]}
fz={k:sum(1 for p in v if a[p]!=b[p]) for k,v in frozen.items()}
W8=json.load(open(os.path.join(D,'wijzigingen.json')))
pal=B.getpalette()[:48]; palA=A.getpalette()[:48]
cnt=collections.Counter(B.getdata())
rol={1:'zwart: buitenlijn schaduwkant, binnenlijnen schaduwkant',2:'vacht basis; nerf op licht hout (5) (een stap)',3:'vacht midden/schaduw; nerf op hout (6) (een stap); spaak achterwiel',
4:'vacht diepe schaduw + hout schaduw (sikkels) + outline base hout/vacht + naafring',5:'hout licht (bovenvlakken, wielrand, naafknop) = vacht-hooglicht (voorhoofd/snuitrug) = bovenbevel zijvlak geel blok = bovenbevel rood blok (warme hue shift)',
6:'hout midden = zijvlak geel blok (schaduw, oker)',7:'hoepel basis, tandschaduw',8:'hoepel schaduw + outline base hoepel, zijvlak blauw blok + outline base blauw, morrillo',
9:'tanden + glans hoepels + bovenbevel geel en blauw blok',10:'blauw voorvlak + bovenbevel blauw zijvlak',11:'groen schaduwvlak + outline base driehoek',12:'rood voorvlak + bovenbevel rood zijvlak',
13:'rood zijvlak + outline base rood blok + onderbevel rood',14:'geel voorvlak',15:'groen lichtvlak'}
L=[]
L.append('Capykart r7 -> r8: schaduwronde (Dragonfly Cave). Alleen tinttoewijzing per pixel + 1 paletwaarde.')
L.append(f'alpha-diff t.o.v. r7: {ad}  (silhouet identiek)')
L.append('bevroren zones (pixeldiff t.o.v. r7): '+', '.join(f'{k} {v}' for k,v in fz.items()))
L.append(f'gewijzigde pixels: {len(W8)}; kleuren in gebruik: {len(cnt)} (incl. transparant)')
L.append('')
L.append('PALET (index: rgb; rol, gedeeld waar het kan)')
for i in range(1,16):
    rgb=tuple(pal[i*3:i*3+3]); old=tuple(palA[i*3:i*3+3])
    L.append(f'{i:2d}: {rgb}{"  (r7: "+str(old)+")" if rgb!=old else ""}  {cnt[i]:4d} px  {rol[i]}')
L.append('Geen vrije slot: een extra houttint of crème-hooglicht zou een andere functie kosten. Gekozen voor delen: vacht 2/3 doen dienst als "een-stap"-nerf op het hout,')
L.append('5 (iets minder verzadigd: (246,170,102)->(244,178,116)) is hout-licht, vacht-hooglicht en blokbevel tegelijk, 6 is ook de schaduwzijde van het gele blok.')
L.append('')
cit={
'groene driehoek':'gids r.1311-1321 (Shading Flat Surfaces): "each surface simply has one shade, proportional to the angle at which the light hits the surface" + r.96 "The \\"outline shadows\\" are always black"',
'geel blok':'gids r.1311-1321: top/links meest belicht, rechts minder; r.1344-1346: afgeronde ribbe = "cut all the corners and edges off" -> smalle lichte bevel',
'rood blok':'gids r.1311-1321 (zie geel blok); r.1344-1346 bevel',
'blauw blok':'gids r.1311-1321; r.1379-1381 "Shadows cast by other objects ... should always be fully colored with the shadow color" (bovenrand onder het rode blok)',
'rechterhoepel':'gids r.1423-1425 shine op glanzend materiaal, "Don\'t overdo shine": kort, alleen boven en op de bolling; r.506-513 licht linksboven',
'linkerhoepel':'gids r.1423-1425 shine; r.506-513 licht linksboven',
'kop hooglicht':'gids r.1376-1378 "The highlighting color should be used on those areas that are lit and are the absolute closest to being perpendicular" (voorhoofd/snuitrug), klein houden',
'kop sikkel':'gids r.515-516 "the shading should also curve around the shape of the body"; r.1374-1376 grens basis/schaduw op de "equator"',
'kaak/nek':'gids r.1379-1381 slagschaduw van de kop op de nek "fully colored with the shadow color"; r.506-513',
'schouder in kart':'SPRITE_KERN Coathief-les: elk groot vlak volume; gids r.1374-1376 equator',
'kart neus bovenvlak':'opdracht: nerf een stap van het vlak; gids r.1311-1321 bovenvlak meest belicht (5 blijft)',
'kart neus voorvlak':'gids r.1311-1321 linkervlak belicht; nerf een stap (3 op 6) i.p.v. 4: minder hard, korter',
'kart neus sikkel':'gids r.515-516 + r.1374-1376: schaduw onderlangs (van het licht af), dikker naar rechts/onder',
'kart neus zijvlak':'nerf een stap; gids r.1374-1376',
'voorwiel':'gids r.1350-1374 bol: licht linksboven (rand 5), schaduwvlak rechtsonder vanaf de equator, naaf als een knop',
'kart midden':'gids r.1379-1381 slagschaduw van het voorwiel; r.1374-1376 onderrand in schaduw; nerf een stap',
'kart achterbak':'gids r.1311-1321 rechterzijde minder belicht; nerf een stap, korter',
'achterwiel':'gids r.1350-1374 (zie voorwiel)'}
per=collections.OrderedDict()
for k,(o,n,z,r) in W8.items(): per.setdefault(z,[]).append((k,o,n,r))
for z,items in per.items():
    L.append(f'== {z}: {len(items)} px')
    L.append(f'   waarom: {items[0][3]}')
    L.append(f'   gids:   {cit.get(z,"")}')
    L.append('   '+' '.join(f'({k}) {o:X}->{n:X}' for k,o,n,r in sorted(items, key=lambda t:(int(t[0].split(",")[1]),int(t[0].split(",")[0])))))
open(os.path.join(D,'log.txt'),'w').write('\n'.join(L)+'\n')
print('\n'.join(L[:12]))
