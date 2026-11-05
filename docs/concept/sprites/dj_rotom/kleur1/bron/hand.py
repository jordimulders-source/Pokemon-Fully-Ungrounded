"""Handwerk: per rij (x, tekens). Alles in het silhouet dat hier niet staat is gloed:
1 als het aan transparant grenst, anders 2. Schrijft dj_rotom.txt (daarna alleen nog
met de hand in dat bestand verder)."""
import numpy as np
from PIL import Image
G=np.array(Image.open('../../silhouet_af/silhouet.png'))>0
R={}
def p(y,x,s):
    R.setdefault(y,[]).append((x,s))
# bliksem met noot (plasma) + spits
p(21,24,'f'); p(22,24,'ff'); p(23,23,'f'); p(24,23,'f')
p(25,22,'ff'); p(25,25,'33'); p(26,22,'ff'); p(26,25,'333')
p(27,26,'3'); p(28,26,'33')
for y in range(29,33): p(y,27,'3')
p(33,27,'6'); p(34,26,'46'); p(35,26,'46'); p(36,26,'456'); p(37,25,'6456'); p(38,25,'64556')
# linker speaker
p(37,13,'6'); p(38,9,'6666'); p(38,13,'4'); p(38,14,'7777')
p(39,6,'666'); p(39,9,'4444'); p(39,13,'5'); p(39,14,'6666'); p(39,18,'777')
p(40,4,'66'); p(40,6,'444'); p(40,9,'9999'); p(40,13,'5'); p(40,14,'666666'); p(40,20,'77')
small=[" aaa ","a888a","a888a","a8b8a"," aaa "]
big=["  aaa  "," a888a ","a88888a","a88888a","a88b88a"," a8b8a ","  aaa  "]
for y in range(41,55):
    row='64'+'9'*7+'5'+'666666'+'7'
    if 42<=y<=46: s=small[y-42]; row=row[:3]+''.join(c if c!=' ' else row[3+i] for i,c in enumerate(s))+row[8:]
    if 47<=y<=53: s=big[y-47]; row=row[:2]+''.join(c if c!=' ' else row[2+i] for i,c in enumerate(s))+row[9:]
    p(y,4,row)
p(55,4,'7'+'5'*9+'666666'+'7'); p(56,4,'7777777'+'666'+'666666'+'7'); p(57,11,'777777777')
# kop x21..34
p(39,25,'6'); p(39,30,'6'); p(39,31,'7777')
p(40,24,'6'); p(40,25,'4'); p(40,30,'4'); p(40,31,'6666')   # spits-voet 26-29 op y39 staat al in spits? nee: y39 x26-29
p(39,26,'6666'); p(40,26,'4444')
p(41,21,'6664'); p(41,25,'44444'); p(41,30,'5'); p(41,31,'6666')
eyeN=[".ff.","fdcf","8cc8","fcdf",".ff."]; eyeF=["ff.","dcf","cc8","cdf","ff."]
disp=[".888888.","88888888","88e888e8","88ee88e8","8eee8ee8","8eeeeee8",".888888."]
for y in range(42,57):
    row=list('4'+'5'*9+'6666')
    if 42<=y<=46:
        for i,c in enumerate(eyeN[y-42]):
            if c!='.': row[1+i]=c
        for i,c in enumerate(eyeF[y-42]):
            if c!='.': row[6+i]=c
    if y==47: row[2:7]=list('7fff7')
    if y==48: row[3:6]=list('777')
    if 50<=y<=56:
        for i,c in enumerate(disp[y-50]):
            if c!='.': row[1+i]=c
    if y==53: row[0]='8'; row[9:14]=list('88888')
    p(y,21,''.join(row))
p(53,19,'88')
p(57,20,'777777777777777')
for y in range(40,58): 
    if y!=53: p(y,20,'7')
# rechter speaker
p(27,50,'66666'); p(27,55,'7')
p(28,46,'6666'); p(28,50,'44444'); p(28,55,'67')
p(29,43,'666'); p(29,46,'4444'); p(29,50,'9999'); p(29,54,'567')
p(30,39,'6666'); p(30,43,'444'); p(30,46,'9'*8); p(30,54,'5667')
p(31,36,'666'); p(31,39,'4444'); p(31,43,'9'*11); p(31,54,'5667')
p(32,35,'6'); p(32,36,'444'); p(32,39,'9'*15); p(32,54,'5667')
up=["  aaaaa  "," a88888a ","a8888888a","a8888888a","a8888888a","a8888888a","a888b888a"," a88b88a ","  aaaaa  "]
lo=["   aaaaa   "," aa88888aa "," a8888888a ","a888888888a","a888888888a","a888888888a","a888888888a","a8888b8888a"," a888b888a "," aa88888aa ","   aaaaa   "]
def RE(y): return 57 if y<=35 else (58 if y<=50 else 59)
for y in range(33,57):
    re=RE(y)
    row=list(('6' if y<39 else '7')+'4'+'9'*17+'5'+'6'*(re-55)+'7')
    if 34<=y<=42:
        for i,c in enumerate(up[y-34]):
            if c!=' ': row[6+i]=c
    if 45<=y<=55:
        for i,c in enumerate(lo[y-45]):
            if c!=' ': row[5+i]=c
    if y==53: row[0]='7'
    p(y,35,''.join(row))
p(57,35,'7'+'5'*19+'6666'+'7')
p(58,36,'777'+'6'*16+'6666'+'7')
p(59,39,'7'*12+'6'*7+'78')
p(60,51,'7777888')
CH='.123456789abcdef'
A=np.zeros((64,64),int)
for y in range(64):
    for x in range(64):
        if G[y,x]:
            n=[(y-1,x),(y+1,x),(y,x-1),(y,x+1)]
            A[y,x]=1 if any(not(0<=a<64 and 0<=b<64) or not G[a,b] for a,b in n) else 2
for y,l in R.items():
    for x,s in l:
        for i,c in enumerate(s):
            if c!=' ': A[y,x+i]=CH.index(c)
bad=[(y,x) for y in range(64) for x in range(64) if A[y,x] and not G[y,x]]
print('buiten silhouet:',bad)
with open('dj_rotom.txt','w') as f:
    f.write('== frame 1\n')
    for r in A: f.write(''.join(CH[v] for v in r)+'\n')
