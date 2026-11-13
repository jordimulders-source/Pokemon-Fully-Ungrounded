# r3: bewerkt r2 (raster ../r2/raster.txt) per zone; ' ' = pixel houden
import sys,os; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D); sys.path.insert(0,D+'/..')
import pal,cfg,numpy as np
a=cfg.read(D+'/../r2/raster.txt'); r2=a.copy()
def R(y,x,s):
    for i,ch in enumerate(s):
        if ch!=' ': a[y,x+i]=cfg.CH.index(ch)

# ===== 1. MONDKANON: ovale opening met 1-px lip, 3 gebogen ribbels, taps =====
R(43,19,'.11111')                       # bovenrand opening
R(44,19,'199981')                       # bovenlip licht
LIPL={45:'9',46:'9',47:'9',48:'8',49:'8',50:'7'}
LIPR={45:'8',46:'7',47:'7',48:'7',49:'7',50:'f'}
BIN={45:'#11#',46:'11d1',47:'111e',48:'111e',49:'1d11',50:'#11#'}
for y in range(45,51):
    b=BIN[y].replace('#',LIPL[y] if y==45 else '7')
    b=b[:3]+(LIPR[y] if b[3]=='7' and y==45 else b[3])
    R(y,18,'1'+LIPL[y]+b+LIPR[y])   # hoekpixels binnen = lip -> ovale opening
R(51,19,'187771')                       # onderlip donkerder
R(45,23,'8')
# buis x25..31, taps (boven 43->44, onder 51->50)
SPAN={43:(25,27),44:(25,31),45:(25,31),46:(25,31),47:(25,31),48:(25,31),49:(25,31),50:(25,28)}
BAND={43:'9',44:'9',45:'9',46:'9',47:'8',48:'8',49:'8',50:'7',51:'7'}
RIB ={43:'8',44:'8',45:'7',46:'7',47:'7',48:'7',49:'7',50:'f',51:'1'}
ARC ={43:25,44:26,45:27,46:27,47:27,48:27,49:26,50:25}   # boogje ')'
for y,(x0,x1) in SPAN.items():
    for x in range(x0,x1+1): a[y,x]=cfg.CH.index(BAND[y])
    for c in (ARC[y],ARC[y]+3):
        if x0<=c<=x1: a[y,c]=cfg.CH.index(RIB[y])
R(43,28,'333f'); R(50,29,'11f'); R(51,25,'111111f'); R(50,18,'1')

# ===== 2. GEZICHT: rustig wangvlak, een zachte schaduwsikkel =====
for i,t in enumerate(['55554443','55544443','45444433','44444332','33344332']): R(45+i,33,t)   # x33-40
for i,t in enumerate(['4454433','4566433','5555432','4444332',' 344332']): R(50+i,33,t)       # x33-39 (x40 = lijn)

# ===== 3. RECHTER BOOG: ronde omgekeerde U, ovaal gat, regelmatige wratten =====
B={40:'.....1111.....',
   41:'...115554 11...'.replace(' ','')[:14],
   42:'..1544b4b431..',
   43:'.154b1111431..',
   44:'.1541...1431..',
   45:'15b1....1431..',
   46:'15541.....1431.',
   47:'154b1.....1431.',
   48:'15441.....1431.'}
for y,t in B.items(): R(y,50 if len(t)==14 else 49,t)
R(49,49,'15b1'); R(50,49,'144')

# ===== 5. MANTEL: segmentlijnen licht gebogen (boven vlakker, onder steiler) =====
R(28,43,'f'); R(30,45,'4f5'); R(32,46,'3f5')          # lijn A
R(34,39,'3f')                                          # lijn C

# ===== 4. ONDERKANT: rechter rupsband als lus (licht boven, donker onder, rol links), linker rol met zuignappen =====
# band bovenrand + bovenste baan (x41..53)
R(53,41,'11111')
R(54,41,'4555444444b31')
R(55,41,'4444444443321')
R(56,32,'45554433'); R(56,40,'f3333333fff222'); R(56,54,'1')
R(57,28,'43'); R(57,30,'1'); R(57,31,'455444333'); R(57,40,'ffffffff'); R(57,48,'33222'); R(57,53,'1')
# rol (opgerold eind van de rechter band) x30..39 + onderste baan x38..52 met twee roze zuignappen
R(58,26,'4443'); R(58,30,'f444ff3333'); R(58,40,'33333898333'); R(58,51,'22'); R(58,53,'1')
R(59,25,'44433'); R(59,30,'f44f33f332'); R(59,40,'998339783'); R(59,49,'332'); R(59,52,'1')
R(60,24,'998332'); R(60,30,'f33f22f222'); R(60,40,'9782222')
R(61,22,'13978298'); R(61,30,'f333ff2222'); R(61,40,'887')
R(62,23,'188728'); R(62,29,'7f33222222')


# ===== 6. OPRUIMEN: losse tintpixels =====
R(28,45,'6'); R(31,48,'5')                 # mantel: glans 3 px, lichte rand langs lijn A doorgetrokken
R(35,32,'6'); R(36,30,'4')                 # kopbovenkant
R(41,55,'5555'); R(42,57,'5'); R(43,53,'5'); R(48,61,'4')   # boog
R(50,35,'4'); R(53,33,'4444'); R(54,34,'333322')            # wang: onderrand als schaduw
R(54,52,'3'); R(55,50,'333'); R(56,32,'5')
R(57,39,'f'); R(58,36,'fff')                               # rol: binnenlijn van de lus loopt als spiraal de rol in                  # band / rol
R(60,29,'3'); R(61,22,'.1')                                  # linker rol
R(50,14,'13331'); R(51,13,'133221')                          # steel bovenste kanon achter de mond
R(42,32,'f'); R(44,53,'5')

cfg.write(a,D+'/raster.txt'); cfg.topng(a,D+'/octi.png')
d=(a!=r2); print('pixels veranderd totaal',d.sum())
