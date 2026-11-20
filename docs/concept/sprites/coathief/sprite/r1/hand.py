# Handwerk op het startraster -> r1.txt. Elke regel: (y, x0, 'tekens'); '-' = laat staan.
# Indexen: 1 omlijning, 2/3/4 zwart schaduw/midden/licht, 5/6/7 bruin, 8/9/A creme, B/C oog.
import os; from PIL import Image; import numpy as np
D=os.path.dirname(os.path.abspath(__file__))
R=[list(l.rstrip('\n')) for l in open(os.path.join(D,'start.txt'))]
G=[l.rstrip('\n') for l in open(os.path.join(D,'groep.txt'))]
a=np.asarray(Image.open(os.path.join(D,'..','onderlaag_rgb.png'))).astype(int)
L=(a[...,0]*299+a[...,1]*587+a[...,2]*114)/1000

# KOP: tonen uit het model zelf (kruin en snuitrug licht, kaak donker), alleen naar 3 tinten gezet.
for y in range(29,50):
  for x in range(0,29):
    if G[y][x]=='K' and R[y][x]!='1':
      R[y][x]='4' if L[y,x]>=68 else ('3' if L[y,x]>=45 else '2')

E=[
# ---- LIJF (bruin), x27..48 ----
(33,29,'7--7777777777777776'),
(34,28,'6777777777667777776666'),
(35,28,'67777777776666777776 5'.replace(' ','5')),
(36,28,'677777777666666777655'),
(37,28,'67777777666666677765-'),
(38,28,'67777776666666777765-'),
(39,27,'6677777666666657777655'),
(40,27,'667777666666665777766 5'.replace(' ','5')),
(41,26,'56677766666666657777655'),
(42,26,'556776666666665777766555'),
(43,25,'55566666666666657776655'),
(44,24,'5555666666655557776665555'[:25]),
(45,22,'555555666666555556666666555'),
(46,20,'-55555556666655555666666655'),
(47,21,'5555555666665555555-666665555'),
(48,23,'55556666655555---5566655'),
(49,23,'555666666555------666555'),
(50,24,'55666666555-------5555'),
(51,24,'55666666555'),
(52,25,'5--6666555'),
(53,30,'6655'),
# rug: lichte vlak boven
(31,37,'77777'),
(32,35,'77777777777'),
(32,46,'76'),
# dijrand: schaduwwig van de buik omhoog langs de voorkant van de dij
(40,40,'55'),(41,40,'55'),(42,39,'55'),(43,38,'555'),
]
for y,x0,s in E:
  for i,c in enumerate(s):
    if c!='-': R[y][x0+i]=c

# ---- OOG (rood zoals de oude sprite, glans zoals het model) ----
for (x,y),c in {(18,39):'1',(19,39):'1',(20,39):'B',(21,39):'3',
                (18,40):'1',(19,40):'A',(20,40):'B',(21,40):'1',
                (18,41):'1',(19,41):'C',(20,41):'C'}.items(): R[y][x]=c
# creme rond het oog (wenkbrauwboog, onderstreep, wangvlek, verre vlek) uit het model
for (x,y),c in {(18,38):'9',(19,38):'A',(20,38):'A',(21,38):'9',(17,39):'9',(17,40):'9',
                (19,42):'9',(20,42):'9',(21,42):'8',(23,40):'9',(23,41):'9',(24,40):'8',
                (13,38):'9',(13,39):'8'}.items(): R[y][x]=c
# ---- OREN zwart (bivakmuts): creme rand -> zwart licht/midden, binnenkant donker ----
for (x,y),c in {(16,30):'4',(17,30):'3',(15,31):'3',
                (24,30):'4',(25,30):'4',(26,30):'3',(24,31):'4',(25,31):'3',(26,31):'3',(27,31):'2',
                (23,32):'3',(25,32):'2',(26,32):'2',(27,32):'2',(26,33):'2',(27,33):'2'}.items(): R[y][x]=c

# ---- POTEN ----
# geheven voorpoot (dichtbij): licht linksboven, donker rechts; klauwen creme (vorm = model)
for (x,y),c in {(22,48):'3',(20,49):'4',(21,49):'3',(22,49):'3',
                (18,50):'4',(19,50):'3',(20,50):'3',(21,50):'3',(22,50):'2',(23,50):'2',
                (17,51):'4',(18,51):'3',(19,51):'3',(20,51):'3',(21,51):'2',(22,51):'2',(23,51):'2',
                (17,52):'3',(18,52):'3',(19,52):'3',(20,52):'9',(22,52):'2',(23,52):'2',(24,52):'2',
                (17,53):'A',(18,53):'3',(19,53):'A',(20,53):'9',
                (17,54):'9',(18,54):'8',(19,54):'9',(18,55):'8',(19,55):'8'}.items(): R[y][x]=c
# stappende voorpoot (onder het lijf): 3 links, 2 rechts; klauwen
for y in range(53,61):
  for x in range(22,34):
    if G[y][x]=='K' and R[y][x] not in '1':
      R[y][x]='2'
for (x,y) in [(29,53),(29,54),(30,54),(29,55),(30,55),(28,56),(29,56),(28,57),(29,57),(27,58),(28,58),(27,59),(26,59),(26,60)]:
  R[y][x]='3'
for (x,y),c in {(24,59):'8',(23,60):'8',(24,60):'A',(25,60):'9',(22,61):'8',(23,61):'9',(24,61):'8',(25,61):'1',
                (26,61):'9',(27,61):'9',(28,61):'2',(22,62):'1',(23,62):'1',(24,62):'1',(25,62):'9',(26,62):'8',
                (27,60):'3',(28,60):'2'}.items(): R[y][x]=c
# verre achterpoot: geheel in de schaduw
for y in range(48,59):
  for x in range(35,42):
    if G[y][x]=='K' and R[y][x]!='1': R[y][x]='2'
for (x,y) in [(36,51),(36,52),(37,53),(37,54)]: R[y][x]='3'
# dichte achterpoot: lichte linkerrand, midden, schaduw rechts
for y in range(47,62):
  for x in range(42,54):
    if G[y][x]=='K' and R[y][x]!='1': R[y][x]='3'
for y in range(47,62):
  xs=[x for x in range(42,54) if G[y][x]=='K' and R[y][x]!='1']
  if not xs: continue
  if y>=51: R[y][xs[0]]='4'
  R[y][xs[-1]]='2'
for (x,y),c in {(48,48):'2',(47,49):'2',(48,49):'2',(46,50):'3',(47,50):'2',(48,50):'2',(49,50):'2',
                (50,59):'2',(48,59):'2'}.items(): R[y][x]=c


# kruin: afgeronde lichtvlek i.p.v. blok (vorm volgt de kop)
for (x,y),c in {(20,32):'3',(20,33):'3',(19,34):'3',(17,35):'3',(18,35):'3',(14,40):'3'}.items(): R[y][x]=c
# stappende voorpoot: dubbele buitenlijn rechts terug naar 1 px
R[54][33]='2'; R[55][33]='2'
# dichte achterpoot: teenlijn doorgetrokken naar de onderlijn
R[60][49]='1'
# hak rechts: (51,52) en (52,54) zijn reductieresten buiten de buitenlijn (dubbele lijn in de traphoek) -> weg
R[52][51]='0'; R[54][52]='0'

# ---- opruimen kleine tintvlakjes (ronde 1, zelfcontrole) ----
for (x,y),c in {(53,9):'4',(48,30):'3',(49,33):'2',(21,51):'3',(39,44):'5',(40,44):'6',(49,53):'2',(20,53):'9',
   (16,30):'3',(17,30):'3',(15,31):'4',(15,32):'4',(17,31):'3',(22,31):'3',
   (25,30):'3',(24,31):'3',(23,32):'1',(25,40):'3',(9,47):'2',
   (21,49):'4',(19,50):'4',(20,50):'4',(18,51):'4',
   (36,50):'3',(37,55):'3',
   (43,51):'3',(45,52):'3',(46,53):'3',(47,54):'3',(48,54):'4',(47,58):'3',(46,59):'4',(48,59):'3',
   # klauwen: twee tinten (9 licht, 8 schaduw), vorm = model
   (17,53):'9',(17,54):'9',(19,53):'9',(19,54):'9',(20,52):'9',
   (24,60):'9',(25,60):'9',(23,61):'9',(24,61):'9',(26,61):'9',(27,61):'9',(25,62):'9',(26,62):'9',
   # creme tekening rond het oog: een tint (9), glans A blijft
   (18,38):'9',(19,38):'9',(20,38):'9',(21,38):'9',(21,42):'9',(24,40):'9',(13,39):'9'}.items(): R[y][x]=c
# randregel opnieuw (na het handwerk): schaduwkant zwart, lichtkant selout
def T(x,y): return not(0<=x<64 and 0<=y<64) or R[y][x]=='0'
for y in range(64):
  for x in range(64):
    if R[y][x]=='0': continue
    nb=[(dx,dy) for dx,dy in [(0,-1),(-1,0),(1,0),(0,1)] if T(x+dx,y+dy)]
    if not nb: continue
    c=R[y][x]
    if any(d in [(1,0),(0,1)] for d in nb): R[y][x]='1'
    elif c in '567': R[y][x]='5'
    elif c in '89A': R[y][x]='8'
    else: R[y][x]='1'

open(os.path.join(D,'r1.txt'),'w').write('\n'.join(''.join(r) for r in R)+'\n')
# controle: silhouet gelijk aan de onderlaag
bad=[(x,y) for y in range(64) for x in range(64) if (R[y][x]!='0')!=(G[y][x]!='.') and (x,y) not in [(51,52),(52,54)]]
print('alpha-afwijkingen:',bad)
