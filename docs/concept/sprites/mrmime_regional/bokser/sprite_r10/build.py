# r10 (52 hoog): opgebouwd op de natieve 52-schaal (kaal52 = model, r9_52 = r9 op die schaal) met alle goedgekeurde
# bovenlagen r1-r9; per onderdeel (y, x0, pixels). '.' = achtergrond, ' ' = overslaan.
import numpy as np, sys
sys.path.insert(0,'../sprite_r7'); from build import save
H,W=52,35
a=np.zeros((H,W),int)
def p(y,x0,s):
    for i,ch in enumerate(s):
        if ch==' ': continue
        a[y,x0+i]=0 if ch=='.' else int(ch)
# --- kuiven: nabije kuif (rechts), verre kuif = dezelfde vorm ongespiegeld, 9 px naar links, achter de kop
KUIF=[(2,29,'11'),(3,28,'1421'),(4,26,'1144221'),(5,25,'224422221'),(6,25,'1244221'),(7,25,'122221'),(8,25,'12221'),(9,25,'1221'),(10,25,'111')]
for y,x0,s in KUIF:
    if y<=5: p(y,x0-9,s)                  # verre kuif eerst (kop gaat eroverheen); alleen het deel boven/achter de kop
a[5,16]=1                                 # rand van de verre kuif dicht
# --- kop (rond, modelmaat): omlijning, gezicht, wangschaduw rechts
KOP=[(3,21,'11111'),
     (4,19,'1188888'),
     (5,18,'18888888'),
     (6,18,'1888888'),
     (7,17,'18888888'),
     (8,17,'18888888'),
     (9,17,'188888888'),
     (10,17,'1888888871'),
     (11,17,'18888888771'),
     (12,17,'1888888771'),
     (13,17,'188888761'),
     (14,18,'18888761'),
     (15,19,'111111'),
     ]
for y,x0,s in KOP:
    for i,ch in enumerate(s):
        a[y,x0+i]=int(ch)
for y,x0,s in KUIF: p(y,x0,s)             # nabije kuif voor de kop
# verre kuif mag niet over de kop: kop-omlijning bovenaan herstellen
p(3,21,'11111')
# --- gezicht: ogen = modelraster (pupil zwart + 2 eronder, dunne lichtgrijze boog), snor (model), mond (r9)
for x,y in [(19,7),(18,10),(22,7),(23,7),(23,8),(23,9),(23,10)]: a[y,x]=7
for x in (19,22): a[8,x]=1; a[9,x]=2
p(11,19,'111'); p(12,18,'11811')     # snor = model (rij 24: 4 zwart; rij 25: zwart, licht, zwart)
# --- gestrekte vuist (r7/r8-vuist op 52): handrug linksboven licht, naad, glans, vingerplooi, vingers
p(7,2,'1111')
p(8,1,'155531')
p(9,0,'1552731')
p(10,0,'1331111')
p(11,0,'12531531')
p(12,1,'1221321')
p(13,2,'11111122')
# --- gestrekte arm naar de verre schouder
p(14,6,'1888222')
p(15,6,'1888888')
p(16,7,'178887')
p(17,8,'177777')
p(18,9,'1111111')
# --- verre schouder (Mr. Mime-bal, deels achter de borst; hooglicht linksboven, sikkel rechtsonder, één lijnkleur)
p(12,14,'111')
p(13,13,'17551')
p(14,13,'15554')
p(15,13,'155413')
p(16,13,'15441')
p(14,26,'6'); p(15,25,'66'); a[13,26]=1   # hals tussen kaak en nabije schouder
p(17,14,'111')
# --- romp + V (midden) + borstvuist + nabije schouder en arm
p(16,18,'333333')
p(17,17,'1'); p(17,18,'3333'); p(17,22,'8')
p(18,16,'4'); p(18,17,'8'); p(18,18,'333'); p(18,21,'8')
p(19,16,'4888'); p(19,19,'33'); p(19,21,'8')
p(20,16,'4888388')
for y in range(21,26): p(y,16,'4888887')
p(21,23,'7661'); p(22,23,'7661'); p(23,23,'7661'); p(24,22,'87661'); p(25,22,'87661')
# borstvuist
p(16,24,'1111')
p(17,23,'157531')
p(18,22,'15525321')
p(19,22,'13311111')
p(20,23,'1251531')
p(21,24,'11111')
# nabije schouder
p(12,28,'1111')
p(13,27,'175551')
p(14,27,'1555441')
p(15,27,'1555441')
p(16,28,'15441')
p(17,29,'1111')
# nabije arm (hangt, onderarm naar rechts)
p(18,29,'18871')
p(19,29,'18871')
p(20,29,'188871')
p(21,30,'18871')
p(22,30,'17871')
p(23,31,'1171')
p(24,33,'11')
# --- broek: tailleband met knik (midden-links 1 lager), Y-naad, hooglichten, schaduw rechts
p(26,16,'111776666111')
p(27,16,'1331666113331')
p(28,16,'1553111333331')
p(29,16,'13335533332221'); 
p(30,15,'133333253333321')
p(31,15,'133323533333321')
p(32,15,'1333313333333221')
p(33,15,'1333331333333221')
p(34,15,'1333332133333221')
p(35,16,'111111.1111111')
# --- benen: verre been schuin achter het nabije, nabije been smaller naar de enkel, knie-omtrek 1 rij
for y,x0,t in [(36,18,'1871'),(37,18,'1871'),(38,19,'1871'),(39,19,'18871'),(40,20,'18871'),(41,21,'18871'),(42,21,'18871'),(43,21,'18871'),(44,21,'1111')]: p(y,x0,t)
for y,x0,t in [(36,24,'18871'),(37,24,'18871'),(38,25,'1871'),(39,25,'18871'),(40,25,'1871'),(41,25,'1871'),(42,25,'1871'),(43,25,'1871'),(44,25,'1871'),(45,25,'1871')]: p(y,x0,t)
# --- schoenen: verre 1 rij hoger dan de nabije, hooglicht op de neus (model)
for y,x0,t in [(45,20,'13331'),(46,18,'1133331'),(47,17,'15333331'),(48,17,'15533331'),(49,17,'15333331'),(50,17,'11111111')]: p(y,x0,t)
for y,x0,t in [(46,25,'1111'),(47,24,'133331'),(48,24,'1333351'),(49,24,'1133551'),(50,25,'1333351'),(51,26,'111111')]: p(y,x0,t)
a[6,17]=0   # kop ronder: bovenste rij van de zijkant 1 px in
save(a,'bokser')
