# blokken.py: r4-tekening per rij; R(y,x,s) zet pixels vanaf x ('~' = houden, '.' = transparant)
def R(y,x,s):
    for i,ch in enumerate(s):
        if ch!='~' and x+i<64: a[y,x+i]=cfg.CH.index(ch)
def clear(y,x0,x1): a[y,x0:x1+1]=0
# ===== MANTEL + VIN (punt 2, 6): lijnen donkerrood, selout boven, lichter =====
R(24,44,'222222222')
R(25,43,'2'+'998998888'+'2222')
R(26,42,'2'+'88888888888877'+'222')
R(27,42,'2'*16+'981')
R(28,38,'2222'+'5'+'22'+'666'+'55'+'2'+'655544'+'2'+'981')
R(29,36,'22'+'5566555'+'2'+'65554'+'2'+'5544'+'2'+'9881')
R(30,34,'222'+'555555444'+'2'+'55544'+'2'+'444'+'2'+'8981')
R(31,32,'22'+'555'+'2'+'55544444'+'2'+'555444'+'2'+'4'+'2'+'89881')
R(32,31,'2'+'555443'+'2'+'54444443'+'2'+'5444433'+'2'+'888881')
R(33,26,'222222'+'5544443'+'2'+'4444433'+'2'+'444433'+'2'+'888871')
R(34,24,'22'+'5665'+'2'+'665444433'+'2'+'444443'+'2'+'44433'+'2'+'88888771')
R(35,23,'2'+'5554'+'22'+'6654444433'+'2'+'4444433'+'2'+'4433'+'2'+'88877771')
R(36,22,'2'+'554'+'22'+'555444444333'+'2'+'4444333'+'2'+'333'+'2'+'877777771')
# ===== KRUL (haak), VERRE OOG, NABIJE OOG, ONDERKANT MANTEL (punt 4, 5, 6, 7) =====
R(37,19,'2cb544'+'2'+'5544'+'44444'+'3333'+'44'+'2'+'443333332'+'1'*10+'...')
R(38,19,'2ba442'+'55'+'44444'+'3'+'566555'+'4'+'3'+'2'+'33333322'+'1'+'.'*13)
R(39,18,'..2543'+'2'+'4'+'111'+'444'+'3'+'5555'+'4'+'1111'+'2'+'33322'+'1'+'.'*15)
R(40,18,'..2543'+'2'+'1'+'ccb'+'1'+'44'+'3'+'44'+'111'+'ccb'+'1'+'2'+'3322'+'1'+'......'+'2222'+'......')
R(41,18,'..2cb3'+'2'+'2'+'b1a'+'2'+'4'+'33'+'11'+'cb1bba'+'2'+'2'+'322'+'1'+'.....'+'22'+'5665'+'1'+'.....')
R(42,18,'..2ba33'+'222222'+'2'+'33'+'2'+'bbaba'+'2'+'4'+'1'+'22'+'1'+'.....'+'2'+'5554444'+'1'+'....')
# ===== WANG, KIN, BOOG, TENTAKELS RECHTS (punt 1, 5) =====
import json
for k,v in json.load(open(D+'/blok2.json')).items(): R(int(k),32,v)
# ===== LICHT (punt 2): 3 -> 4 in mantel, kop, wang, kin, tentakels; 3 blijft als sikkel boven een lijn/rand =====
def zone(x0,y0,x1,y1,frm,to,keep_edge=True):
    b=a.copy()
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if b[y,x]!=frm: continue
            dn=b[y+1,x] if y<63 else 0; rt=b[y,x+1] if x<63 else 0
            if keep_edge and (dn in (0,1,2,15) or rt in (0,1)): continue
            a[y,x]=to
zone(22,28,55,37,3,4)      # mantel + kopbovenkant
zone(32,38,41,55,3,4)      # wang + kin
zone(41,50,62,54,3,4)      # middelste tentakel
zone(42,37,49,43,2,3,False) # schaduwvlak onder de mantel: 2 -> 3
# ===== minder zwart: binnenlijnen tussen twee vormen -> donkerrood =====
for (y,x0,x1) in [(53,49,54),(54,45,48),(55,39,44),(56,33,37)]:
    for x in range(x0,x1+1):
        if a[y,x]==1: a[y,x]=2
for y in range(49,54):
    if a[y,40]==1: a[y,40]=2
# ===== meer licht linksboven per vorm =====
def sw(pts,frm,to):
    for (y,x0,x1) in pts:
        for x in range(x0,x1+1):
            if a[y,x]==frm: a[y,x]=to
sw([(29,38,44),(30,37,44),(31,38,42),(32,39,43),(33,40,42),(29,46,50),(30,47,50),(31,47,50),(32,48,50),(33,48,49)],4,5)  # mantelsegmenten
sw([(34,31,36),(35,32,36),(36,28,34),(37,28,33)],4,5)        # kopbovenkant
sw([(44,35,38),(45,37,38),(46,36,37)],4,5)                   # wang onder het oog
sw([(42,55,58),(43,51,53),(44,51,53),(45,50,52),(46,51,52),(47,50,51),(48,50,51),(49,49,50)],4,5)  # bovenste tentakel
# ===== correcties na kijken =====
sw([(42,56,58)],5,4)                          # bovenste tentakel: schaduw rechts terug
sw([(50,34,37)],4,3)                          # kin: plooi boven de kin terug
# gat-randen die naar het licht kijken: donkerrood i.p.v. zwart
for (y,x) in [(48,45),(48,46),(48,47),(46,48),(47,48),(45,58),(46,59),(47,60)]:
    if a[y,x]==1: a[y,x]=2
# ===== opschonen: losse tintpixels, lichte buitenrand =====
for (x,y,c) in [(51,28,'5'),(54,32,'2'),(53,33,'2'),(40,38,'4'),(25,39,'2'),(37,39,'5'),
                (43,44,'1'),(49,38,'1'),(50,38,'.'),(44,42,'1'),(45,42,'.'),(52,35,'4'),(53,54,'4'),(52,54,'4'),
                (55,56,'2'),(49,59,'2')]:
    a[y,x]=cfg.CH.index(c)
# gat in de donkere boog: bovenrand zwart, gat 3x2, onderrand donkerrood
for (x,y,c) in [(45,42,'1'),(45,46,'1'),(46,46,'1'),(47,46,'1'),(45,47,'.'),(46,47,'.'),(47,47,'.'),
                (45,48,'.'),(46,48,'.'),(47,48,'.'),(44,48,'1'),(48,48,'2')]:
    a[y,x]=cfg.CH.index(c)
# ===== punt 9: kanonopeningen (klein) =====
a[42,3]=cfg.CH.index('1')     # bovenste kanon: opening 1 px hoger (2x3 zoals het model)
a[58,11]=cfg.CH.index('1')    # onderste kanon: losse grijze pixel in de opening weg
# ===== losse tintpixels krul, wang, kin samenvoegen =====
for (x,y,c) in [(29,34,'6'),(26,35,'4'),(24,36,'4'),(22,37,'4'),(38,48,'3'),(37,49,'3'),
                (39,51,'3'),(39,52,'3'),(39,53,'3'),(33,54,'4'),(36,54,'3')]:
    a[y,x]=cfg.CH.index(c)
for (x,y,c) in [(26,34,'6'),(23,36,'4')]: a[y,x]=cfg.CH.index(c)
# ===== rupsband: binnenlijn krult links omhoog (spiraal zoals het model), zuignappen erlangs =====
R(57,32,'2344444333')
R(58,32,'233b433333')
R(59,32,'32333b3322')
R(60,32,'3322222239')
