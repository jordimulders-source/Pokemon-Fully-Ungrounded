import os, json, collections
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'../../../../../..')
A=Image.open(os.path.join(D,'../../eindkeuring/capykart_r7.png')); B=Image.open(os.path.join(D,'capykart.png'))
a=A.load(); b=B.load(); W,H=A.size
ad=sum(1 for y in range(H) for x in range(W) if (a[x,y]==0)!=(b[x,y]==0))
fz={'oog':[(x,y) for x in range(28,32) for y in range(16,22)],'tanden':[(x,y) for x in range(17,24) for y in range(30,34)],
 'morrillo':[(x,y) for x in range(21,24) for y in (15,16)],'neusgaten':[(15,22),(16,22)],'mond':[(18,28),(19,28)],'kinlijn':[(x,30) for x in range(25,29)]}
def diff(ps):
    idx=sum(1 for p in ps if a[p]!=b[p])
    # vormdiff: zelfde partitie (pixel i en j gelijk in r7 <=> gelijk in r9)
    m={}; bad=0
    for p in ps:
        if a[p] in m and m[a[p]]!=b[p]: bad+=1
        m.setdefault(a[p],b[p])
    return idx,bad
pal=B.getpalette()[:48]; cnt=collections.Counter(B.get_flattened_data() if hasattr(B,'get_flattened_data') else B.getdata())
rol={1:'zwart (lijn)',2:'vacht licht',3:'vacht midden',4:'vacht donker = hout donkerst (outline base hout/vacht, sikkels, nerf op zijkant) — gedeeld warm roodbruin',
5:'hout hooglicht (bolling kap linksboven, randen, wielranden, naafknop) + bevel gele zijkant + bevel rood blok',6:'hout basis (kap, neus, wielen) = gele zijkant',
7:'rood donker (zijvlak + onderbevel rood blok); was lichtgrijs, vervalt',8:'blauwgrijs: hoepels, tandschaduw, morrillo, blauwe zijkant',9:'wit: tanden, glans hoepels, bevel geel/blauw blok',
10:'blauw',11:'groen donker',12:'rood',13:'hout midden-schaduw (zijkanten, kap achter, nerf op basis, sikkel-overgang)',14:'geel',15:'groen licht'}
w=json.load(open(os.path.join(D,'wijzigingen.json')))
L=['Capykart r8 -> r9: paletindeling coördinator (hout oranje en los van de vacht). Uitgangspunt r8.',
   f'alpha-diff t.o.v. r7: {ad}',
   'bevroren t.o.v. r7 (index-diff / vorm-diff): '+', '.join(f'{k} {diff(v)[0]}/{diff(v)[1]}' for k,v in fz.items()),
   '  tanden: alle lichtgrijze px (8 in het tandvak) -> blauwgrijs (lichtgrijs vervalt, zoals opgedragen); vorm-diff 0 (zelfde pixels, zelfde indeling).',
   f'index-wijzigingen t.o.v. r8: {len(w)}','', 'PALET']
for i in range(1,16): L.append(f'{i:2d}: {tuple(pal[i*3:i*3+3])}  {cnt[i]:4d} px  {rol[i]}')
lum=lambda c:round(.299*c[0]+.587*c[1]+.114*c[2])
L.append('helderheid hout 5/6/13/4: '+' / '.join(str(lum(pal[i*3:i*3+3])) for i in (5,6,13,4))+'; vacht 2/3/4: '+' / '.join(str(lum(pal[i*3:i*3+3])) for i in (2,3,4)))
L+=['','REGELS (per pixel, in maak_r9.py)',
'- vacht (kop/oren/nek/schouder): 2/3 blijven; r8-hooglicht 5 op de kop -> 2 (vacht heeft 3 tinten); 4 -> gedeeld donker.',
'- hout: 5 -> hooglicht, behalve op de motorkap: daar basis met hooglicht alleen linksboven (bolling; gids r.1376-1378 "highlighting color ... absolute closest to being perpendicular", klein houden).',
'- hout 6 -> basis op neus/kap/wielen; -> midden-schaduw op de zijkanten (middenpaneel, achterbak, zijvlak neus) en achter op de kap: neus (naar links) lichter dan zijkant (gids r.1315-1321: linkervlak meer belicht dan rechts).',
'- nerf: altijd één houttint donkerder dan het vlak (op basis -> midden-schaduw, op midden-schaduw -> donker), nooit vachttinten.',
'- sikkels uit r8: binnenste pixel -> midden-schaduw, pixel tegen de lijn -> donker (twee stappen sikkel; gids r.1374-1376 equator, r.515-516).',
'- blokken: gele zijkant = hout-basis, bevels = hout-hooglicht/wit, rood zijvlak = rood-donker. Hoepels: blauwgrijs + witte glans.','',
'GEWIJZIGDE PIXELS PER REGEL']
per=collections.defaultdict(list)
for k,(o,n,why) in w.items(): per[why].append(f'({k}) {o:X}->{n:X}')
for why,items in per.items(): L.append(f'== {why}: {len(items)} px'); L.append('   '+' '.join(items))
open(os.path.join(D,'log.txt'),'w').write('\n'.join(L)+'\n'); print('\n'.join(L[:26]))
