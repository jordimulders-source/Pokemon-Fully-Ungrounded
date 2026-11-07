"""r7: met de hand, per onderdeel gemeten op het model (stappen/mg.py, zij.py, tab.py).
Basis: r6-raster (raster_r6.txt); kop/oren/gezicht/snorharen/pluk/wang/bef/voorpoten (x0-30) nieuw getekend,
rug, pluim, staart en tenen gerepareerd. Elke regel: seg(y, x, tekens)."""
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r7/'
G=[list(l.rstrip('\n').ljust(64,'.')[:64]) for l in open(D+'raster_r6.txt')][:64]
def seg(y,x,s):
    for i,c in enumerate(s):
        if c!=' ': G[y][x+i]=c
def clr(y,x0,x1):
    for x in range(x0,x1+1): G[y][x]='.'
# ---------- kop-zone: rij 14-38 x0-30 en rij 39-53 x0-24 eerst leeg (rest uit r6) ----------
for y in range(14,39): clr(y,0,30)
for y in range(39,54): clr(y,0,24)
def pts(c,L):
    for x,y in L: G[y][x]=c
# oor ver (top rij 15, buitenlijn x9 rij 19-22, terracotta onderin)
seg(15,11,'22')
seg(16,10,'2551')
seg(17,10,'2541')
seg(18,10,'2541')
seg(19, 9,'25541')
seg(20, 9,'25441')
seg(21, 9,'254331')
seg(22, 9,'243331')
# oor nabij (brede ronde schelp, donkere ring, bruine binnenkant)
seg(16,23,'222')
seg(17,22,'25551')
seg(18,21,'211151')
seg(19,20,'251CC51')
seg(20,19,'251BCC41')
seg(21,19,'251BBC41')
seg(22,19,'251BBC1')
# kopbovenkant tussen de oren, oorbasis
seg(23,10,'2333122215'); seg(23,20,'1BBBC1')
seg(24,10,'233455551');  seg(24,19,'51BBCB1')
seg(25,10,'244555551');  seg(25,19,'51BBB1')
seg(26,10,'2'+'5'*8+'44'+'1111')
seg(27, 9,'2'+'5'*11+'4331')
seg(28, 6,'8'); seg(28,9,'2'+'5'*11+'4333111')
# pluk (kroontje x5-8, rij 28-33), oog (Drowzee-lui uit r6), wangsikkel, nek
seg(29, 6,'8A2'+'5'*6+'2112'+'4'+'3333'+'8A91')
seg(30, 6,'8A2'+'5'*5+'11D112'+'33'+'8AA91'); seg(30,29,'12')
seg(31, 5,'89A9'+'5'*4+'21111'+'34'+'8AA91'+'33'+'11'+'34')
seg(32, 6,'199'+'5'*6+'5555'+'8AA91'+'3333'+'44'+'5')
seg(33, 7,'1'+'5'*10+'8AA91'+'333'+'4'+'5'*4)
seg(34, 7,'2'+'5'*10+'8A91'+'333'+'4'+'5'*5)
seg(35, 7,'2'+'5'*10+'889A1'+'3'+'4'+'5'*6)
seg(36, 7,'25'+'5555'+'5'*5+'4'+'8999'.replace('8999','899A')+'1'+'4'+'5'*6)
seg(37, 8,'14'+'3333'+'6'*6+'111'+'9'+'1'+'5'*6)
seg(38, 9,'1'+'76'+'11'+'6'*10+'1'+'5'*6)
seg(39,10,'11'); seg(39,14,'1'+'6666'+'7777'+'1')
seg(40,14,'1'+'6666'+'7777'+'1')
seg(41,15,'1'+'666'+'7777'+'5')
seg(42,16,'1'+'6'+'77777'+'55')
seg(43,15,'21'+'777777'+'55')
seg(44,13,'22331'+'77777'+'55')
# voorpoot ver (opgeheven wantje, terracotta onderarm) en bef-onderrand
seg(45,12,'2554331'+'1'+'66'+'2'+'55')
seg(46,12,'2554'+'333'+'1'+'11'+'2'+'55')
seg(47,12,'2544'+'111'); seg(47,21,'2555')
seg(48,12,'2423'+'1'); seg(48,20,'25554')
seg(49,12,'2423'+'1'); seg(49,20,'25544')
seg(50,13,'111');      seg(50,20,'25242')
seg(51,20,'24232')
seg(52,21,'1111')
# neus (Y): armen (8,34) (10,34), samen (9,35), steel (9,36-37)
pts('1',[(8,34),(10,34),(9,35)]); pts('2',[(9,36),(9,37)])
# snorharen nabij
pts('F',[(4,35),(5,35),(6,35),(1,36),(2,36),(3,36),(0,37)])
pts('F',[(6,36),(4,37),(5,37),(2,38),(3,38),(1,39),(0,40),(0,41)])
pts('F',[(7,37),(6,38),(5,39),(4,40),(4,41),(3,42)])
# snorharen ver (vanaf de wang achter de mond)
pts('F',[(13,35),(14,35),(15,36),(16,36),(17,36),(18,37),(19,38),(20,38),(21,38),(22,39)])
pts('F',[(13,36),(14,37),(15,37),(16,38),(17,38),(18,39),(19,40),(20,41),(21,42),(22,43)])
# ---------- lijf, achterpoten, staart, pluim: rij 14-38 x31-63 en rij 39-63 x25-63 nieuw ----------
for y in range(14,39): clr(y,31,63)
for y in range(39,64): clr(y,25,63)
for y in range(39,64):
    for x in range(64):
        if G[y][x]=='.' and False: pass
# pluim: 4 slanke vlammen, punten (59,14) (54,16) (60,20) (50,22); zwarte kerven ertussen
for y in range(14,29): clr(y,48,63)
seg(14,58,'81')
seg(15,57,'8A1')
seg(16,54,'8 8A1')
seg(17,53,'818A91')
seg(18,52,'8A1A91')
seg(19,52,'8A9A91')
seg(20,52,'8AAA91A1')
seg(21,51,'8AAAA18A1')
seg(22,50,'88A9CA1A1')
seg(23,50,'81AC4AA91')
seg(24,50,'89A4C4A1')
seg(25,50,'8A9C4C91')
seg(26,50,'8A9C4C91')
seg(27,50,'89C44CC1')
seg(28,51,'1C444CC1')
seg(29,51,'1C4444C1')
# staart: binnenrand zwart/bruin, lichte tan (4), bruine band (C), oranje rand rechts (4/3), onderboog B/3
seg(30,52,'14444CC11')
seg(31,52,'B44444C141')
seg(32,53,'B4444C441')
seg(33,54,'B4444541')
seg(34,55,'B4444541')
seg(35,55,'B4444541')
seg(36,56,'B444441')
seg(37,56,'1444C41')
seg(38,57,'1CCC41')
seg(39,57,'1CC431')
seg(40,56,'1CCC431')
seg(41,56,'1CCC331')
seg(42,56,'1CC3331')
seg(43,55,'1CCC331')
seg(44,55,'1CC4331')
seg(45,54,'1BB3331')
seg(46,52,'11BB3331')
seg(47,47,'11111BBC3331')
seg(48,47,'1BBBBC33311')
seg(49,47,'111111111')
# rug: bovenlijn met vachtpuntje (40,29), rechterrand met tweede puntje (45,34), bil-puntje (49,44)
seg(29,34,'222222'+'1')
seg(30,31,'222'+'5555'+'211')
seg(31,31,'5'*10+'1')
seg(32,31,'5'*11+'11')
seg(33,31,'5'*12+'41')
seg(34,31,'5'*12+'421')
seg(35,31,'5'*12+'431')
seg(36,31,'5'*12+'431')
seg(37,31,'5'*12+'4431')
seg(38,31,'5'*8+'4'+'555'+'4431')
# rij 39+: voorpoot nabij (x25-29), schouderlijn x30, buikvlek 7/6, dijlijn, dij, bil
seg(39,25,'55555'+'5'*8+'4'+'5'*4+'44331')
seg(40,25,'55555'+'2'+'5'*6+'4'+'5'*5+'43331')
seg(41,25,'55555'+'2'+'5'*6+'2'+'5'*5+'433331')
seg(42,25,'55555'+'1'+'66'+'555'+'2'+'5'*7+'43331')
seg(43,25,'55555'+'1'+'777'+'5'+'2'+'5'*8+'43331')
seg(44,25,'55555'+'1'+'7777'+'2'+'5'*8+'433331')
seg(45,25,'5555'+'11'+'7777'+'2'+'5'*8+'43331')
seg(46,25,'555'+'11'+'66776'+'2'+'5'*8+'4331')
seg(47,25,'55'+'11'+'666666'+'2'+'5'*8+'4331')
seg(48,25,'11'+'66666666'+'2'+'5'*7+'4333')
seg(49,26,'111'+'6666666'+'2'+'4'+'55555'+'4333')
seg(50,26,'1EEE'+'11'+'6666'+'1'+'4'+'555'+'4'+'33333'+'1')
seg(51,27,'1EEEEE'+'1111'+'3'*11+'1')
seg(52,28,'13EEEEEE1'+'1'+'3'*11+'1')
seg(53,29,'13EEEE1'+'  '+'11'+'3'*10+'1')
seg(54,29,'1EEEEE1'+'    '+'111111'+'43331')
seg(55,28,'11EEEE1'+' '*11+'14331')
seg(56,25,'2221EEEE1'+' '*12+'14331')
seg(57,24,'2332E2EE1'+' '*13+'14331')
seg(58,24,'1EE2E2E1'+' '*12+'2245541')
seg(59,25,'111111'+' '*12+'25555551')
seg(60,43,'25525241')
seg(61,43,'14424231')
seg(62,44,'111111')
# naden: x24 rij 39-41 (lijf achter de bef), nabije pootrand x25 rij 49-51
for y in (39,40,41): G[y][24]='5'
for y in (49,50,51): G[y][25]='1'
# ---------- ronde 7b: na meting met stappen/tab.py (dekking/donker per pixel) ----------
# oor ver: top smaller (r16 rand x12), aansluiting oorbasis
seg(16,10,'251.'); G[16][13]='.'
G[22][10]='3'; G[24][13]='3'; seg(25,11,'444')
# oor nabij: rechterrand x25 (r17), ring op x23 (r18), lichte rand x25/x24 rechts, bruin B links C rechts
seg(17,22,'2551.')
seg(18,21,'251141')
seg(19,20,'251CC41')
seg(20,19,'251BCC41')
seg(21,19,'251BCC41')
seg(22,18,'251BCC41')
seg(23,18,'151BCC41')
seg(24,18,'151BBC41')
seg(25,18,'151B141')
seg(26,19,'551111'[:5]); G[26][24]='.'
seg(26,19,'55111')
# nek achter het oor: contour x23 (r26-28), terracotta x21-22
seg(27,20,'5431'); G[27][24]='.'
seg(28,20,'5331...1'); 
# wangsikkel volgens meting: punt (25-27,28-29), rand x22 (r30), x21 (r31), onderpunt (22,37-38)
seg(29,19,'3'+'3333'+'88A1')
seg(30,19,'24'+'48AA11')
seg(31,18,'544'+'8A91'+'33'+'11'+'3'+'44')
seg(32,15,'5554'+'8AA91'+'333'+'4'+'444')
seg(33,18,'8AA91'+'333'+'444'+'5')
seg(34,18,'8AA91'+'333'+'44'+'5')
seg(35,18,'8999'+'1'+'3'+'44'+'5')
seg(36,18,'48199'+'1'+'4'+'5')
seg(37,19,'441'+'9'+'1'+'5')
seg(38,18,'6'); seg(38,22,'1'+'5')
seg(37,16,'66')
# bef: rechterrand x22, x23 oranje; linkerrand x15 op r40; kin x14 donker op r38
seg(39,19,'766'); seg(39,23,'5')
seg(40,14,'.'); seg(40,15,'1'); seg(40,23,'5')
seg(38,14,'1')
seg(42,31,'77')
seg(44,23,'2')
seg(45,20,'77')
seg(38,10,'66')
# pluk: bovenrand (7,29) dicht, A-cluster
G[29][7]='8'; G[31][6]='A'
# staartrand en -onderboog netter
seg(32,60,'5'); seg(33,59,'45'); 
seg(38,60,'4')
G[44][58]='3'
seg(47,53,'CC'); seg(48,52,'CC')
# dij-onderkant: 4-band aaneen; onderbeen voorkant
seg(50,37,'444444'); G[49][42]='4'
seg(54,46,'44')
G[52][30]='3'
# nabije voet: bovenkant 5
seg(58,46,'5'); seg(58,49,'5'); seg(60,49,'5'); seg(61,49,'4')
# pluim F3-punt dicht
G[20][58]='8'
# sikkelpunt boven dicht, r29 kleuren, r34 kerf op x21
seg(28,26,'81')
seg(29,19,'5543')
seg(34,18,'8AA1'+'333'+'44'+'5')
# ---------- poten volgens meting (tab.py) ----------
# voorpoot ver: wantje x12-15, rechterrand x15 op r48-49, teenlijn (14,49)
for y in range(44,51): clr(y,12,19)
seg(44,14,'2331')
seg(45,13,'233331')
G[45][19]='1'
seg(46,12,'2554333'); G[46][19]='1'
seg(47,12,'2544111')
seg(48,12,'2451')
seg(49,12,'2321')
seg(50,13,'11')
# voorpoot nabij: rechterrand x24, teenlijn x22
for y in range(48,53): clr(y,20,25)
seg(48,20,'255541')
seg(49,20,'25541')
seg(50,20,'25241')
seg(51,20,'24231')
seg(52,21,'111')
# verre achterpoot en voet (rand en voet 1 px naar rechts)
for y in range(52,60): clr(y,24,37)
seg(52,28,'133EEEE11')
seg(53,30,'112EEE1')
seg(54,31,'1EEEE1')
seg(55,29,'11EEEE1')
seg(56,26,'221EEEEE1')
seg(57,25,'232E2EEE1')
seg(58,25,'1E2E2EE1')
seg(59,26,'111111')
seg(44,18,'77'); G[52][37]='1'; G[52][29]='1'
G[16][53]='8'; G[29][33]='2'; G[30][33]='5'; G[46][48]='1'; G[46][47]='3'
# ---------- opschonen kleine tintvlakjes (controle.py) ----------
seg(22,50,'88AAAA1A1'); seg(23,50,'81ACC9991'); seg(24,50,'8AAC4491')
seg(25,50,'8A9C4491'); seg(26,50,'8A9C4491'); seg(27,50,'899C44C1')
G[17][57]='A'; G[19][54]='A'
G[25][23]='C'; G[27][21]='3'
seg(31,22,'AA'); seg(32,20,'AAA'); G[33][21]='A'
G[31][18]='4'; G[31][29]='4'
G[37][60]='4'; G[37][44]='3'
G[39][19]='6'
seg(48,13,'44'); G[49][13]='4'
G[48][23]='4'
G[52][30]='E'
G[21][57]='9'; G[22][51]='A'
open(D+'raster.txt','w').write('\n'.join(''.join(r) for r in G)+'\n')
