# r3 = r2 + Jordi's zes punten, met de hand (vanuit sprite/): python3 maker/r3_bouw.py [A|B]
# Blok x20..60, rij 19..44 volledig met de hand herschreven (bol, staart, aansluiting); kop/lijf als puntbewerkingen.
import sys
VAR=sys.argv[1] if len(sys.argv)>1 else 'A'
R=[list(l.rstrip('\n')) for l in open('maker/raster_r2.txt')]
BLOK={  # x20..60 (41 tekens)
19:"....d" + "."*33 + "d#.",
20:"...ded..d" + "."*28 + "de#.",
21:"." + "..decddeddddd##......." + "."*14 + "de#" + ".",
22:"." + "..decdecdeeeeee#####.." + "."*13 + "dec#" + ".",
23:"." + "...deeecccceeeeccce#.." + "."*12 + "deb#" + "..",
24:"." + "...dewcbbbbcceecbc#..." + "."*11 + "ddec#" + "..",
25:"." + "..dewweccbbbbcedcbc#.." + "."*7 + "d" + "." + "d#eecb#" + "..",
26:"." + "..dewweeecccbb#ecbc#.." + "."*7 + "d#e#ewcb#" + "..",
27:"." + ".deeweeecceecc#eecbc#." + "."*7 + "dec#eecbd#" + ".",
28:"." + ".deeeccbbceeec#eecbb#." + "."*7 + "dec#ecbde#" + ".",
29:"." + ".dccbbbceeeee#e#ecbb#." + "."*5 + "dddec#ecdec#" + ".",
30:"." + "dcbbbceeeee##ee#eecbb#" + ".." + "dd#eedecdedec#" + "..",
31:"." + "dcbbceeecc#eeeee#ecbb#" + ".." + "dedeccecdcdc#" + "...",
32:"." + "dcbceecbb#eeccee#ecbb#" + ".." + "deedcbecdbb#" + "....",
33:"." + ".dccecbbcdeeecce#ccb#." + ".." + "deecdbecbb#" + ".....",
34:"." + ".dceccceeeeeeec#ccbb#." + ".." + "deecdccbba#" + ".....",
35:"." + ".dcecbbbceeecbc#cbbb#" + "dddedecdddbb#" + "......",
36:"." + "#ceeeccbbbccbbccdcbb#" + "eeecdecceedb#" + "......",
37:".." + "#ceeeeeccbbbceecbb#" + "eeeccbdeeecbb#" + "......",
38:"ddc#ceeeeeeccceecbb#" + "eeeeccbdeccbbb#" + "......",
39:"bdcc##ceewwweeecc##sd" + "eeccbbdecbbba#" + "......",
40:"bbdctt###eeeeee##ssrdeeccbdecbbbba#" + "......",
41:"bbdcdsttt######ssrrdeeccbdecbbbaa#" + ".......",
42:"bbdccdssstttsssrrdddddcbdecbbbaaa#" + ".......",
43:"bbdcccdddsssrrrddeeeeeddaabbbbaa#" + "........",
44:"bbdccccccd####deeeeeccdbbbbbbaa#" + ".........",
}
for y,s in BLOK.items():
    assert len(s)==41,(y,len(s))
    for i,c in enumerate(s): R[y][20+i]=c
def P(x,y,c): R[y][x]=c
# rij 38-39 links van x20 (kop-achterkant): bovenrand licht
P(19,38,'e')
# kop: achterlijn licht gebogen (21,39) (22,40..45) (21,46..47)
P(21,39,'b'); P(20,39,'b'); P(22,39,'d'); P(23,39,'c')
for y in range(40,46): P(22,y,'d')
P(22,46,'c'); P(21,46,'d'); P(21,47,'d')
# oog
for (x,y) in [(10,45),(11,45),(12,45),(13,45),(10,46),(11,46),(12,46),(13,46),(10,47),(11,47),(12,47),(13,47),(11,48),(12,48)]:
    P(x,y,'c')
if VAR=='A':   # 3x3 naar het model: ooglid, donkere ring, lichtpunt
    E={(11,45):'b',(12,45):'b',(13,45):'#',(11,46):'#',(12,46):'w',(13,46):'#',(11,47):'#',(12,47):'#',(13,47):'#'}
else:          # 2x3 = oog C + ooglid
    E={(11,45):'b',(12,45):'#',(11,46):'#',(12,46):'w',(11,47):'#',(12,47):'#'}
for (x,y),c in E.items(): P(x,y,c)
# mondlijn (9,47)(8,48)(7,49) blijft d; kaakschaduw opgeschoond
for x,c in zip(range(5,15),"bbdcccccbb"): P(x,49,c)
for x,c in zip(range(6,14),"bccbbbba"): P(x,50,c)
# blauwe vin
F={(17,47):'v',(18,47):'v',(15,48):'v',(16,48):'v',(17,48):'u',(18,48):'u',(19,48):'b',
   (14,49):'v',(15,49):'u',(16,49):'u',(17,49):'u',(18,49):'u',(19,49):'b',
   (14,50):'u',(15,50):'u',(16,50):'u',(17,50):'u',(18,50):'a',(14,51):'a'}
for (x,y),c in F.items(): P(x,y,c)
# flap: bovenrand (28,45)(27,46)(26,47)(25,47), vouw (34,49)(35-37,48)(38-39,47)(40,46)(41,45)
for x,c in zip(range(22,52),"dcccccdeeeeeeecbbbbbdaaabbbaa#"): P(x,45,c)
for x,c in zip(range(22,51),"dccccdeeeeecbbbbbbbdaaaaaaaa#"): P(x,46,c)
for x,c in zip(range(22,50),"bbcddeeeeeeebbbbddbbaaaaaaa"+"#"): P(x,47,c)
for x,c in zip(range(20,49),"dbbbcceeebbbbbbddddbbbbbbaaa#"[:29]): P(x,48,c)
# onderrand flap gebogen: (25,50)(26,50) (27..29,51) (30..36,52) (37..39,51) (40,50)
for x in range(27,40): P(x,51,'b')
for x in (27,28,29,37,38,39): P(x,51,'d')
for x in range(30,37): P(x,52,'d')
P(25,50,'d'); P(26,50,'d'); P(40,50,'d'); P(40,51,'b')
# voorflipper: lichtkant omlijning gekleurd
P(13,53,'d'); P(12,54,'d'); P(11,55,'d')
# opschonen: tintvlakjes < 3 px (8-buren) samengevoegd, staartvouw doorlopend
for (x,y),c in {(25,21):'e',(25,22):'e',(57,23):'c',(39,23):'c',(29,31):'e',(30,31):'e',(29,33):'e',
    (54,31):'e',(50,34):'b',(29,35):'b',(25,38):'c',(44,43):'b',(45,43):'b',(40,44):'e',(41,44):'e',
    (36,45):'e',(33,46):'e',(31,53):'c',(32,53):'c',(54,34):'b',(53,27):'d',(53,28):'d',
    (40,46):'d',(41,46):'b',(41,45):'d',(42,45):'a'}.items(): P(x,y,c)
open(f'maker/raster_r3{"" if VAR=="A" else "_oogB"}.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
