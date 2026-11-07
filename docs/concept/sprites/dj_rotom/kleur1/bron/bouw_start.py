"""Startraster (eenmalig): plaatst de onderdelen met handgekozen coördinaten en stempels.
Daarna wordt alleen nog dj_rotom.txt met de hand bewerkt."""
import numpy as np
from PIL import Image
G=np.array(Image.open('../../silhouet_af/silhouet.png'))>0
def er(m):
    p=np.pad(m,1); return m&p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:]
E1=er(G); E2=er(E1)
A=np.zeros((64,64),int)
A[G]=2; A[G&~E1]=1
B=E2.copy(); B[:37]&=False; B[:,33:]|=E2[:,33:]  # lichaam: boven y37 alleen rechterspeaker
B[:37,:33]=False
def put(x0,y0,st):
    for dy,row in enumerate(st):
        for dx,ch in enumerate(row):
            if ch!=' ': A[y0+dy,x0+dx]='.123456789abcdef'.index(ch)
# lichaam basis oranje
A[B]=5
# --- linker speaker x4..19
for y in range(38,58):
    for x in range(4,20):
        if B[y,x]: A[y,x]=5
A[np.ix_(range(40,56),range(5,13))]=9
for y in range(38,58):
    for x in range(13,20):
        if B[y,x] and A[y,x]==5: A[y,x]=6
# --- kop x21..34
for y in range(39,58): A[y,20]=7
for y in range(39,58):
    for x in range(31,35):
        if B[y,x]: A[y,x]=6
# --- rechter speaker x35..
for y in range(26,61):
    for x in range(35,59):
        if B[y,x]:
            A[y,x]= 6 if x>=54 else 5
    if B[y,35] or B[y,36]: A[y,35]=7
for y in range(32,58):
    top=33-(np.arange(37,54)-37)//4
    for i,x in enumerate(range(37,54)):
        if y>=top[i]: A[y,x]=9
# conussen
small=[" aaa ","a888a","a888a","a8b8a"," aaa "]
big=["  aaa  "," a888a ","a88888a","a88888a","a88888a"," a8b8a ","  aaa  "]
put(6,41,small); put(5,47,big)
up=["  aaaaa  "," a88888a ","a8888888a","a8888888a","a8888888a","a8888888a","a888b888a"," a8bbb8a ","  aaaaa  "]
lo=["   aaaaa   ","  a88888a  "," a8888888a ","a888888888a","a888888888a","a888888888a","a888888888a","a888888888a"," a88bbb88a ","  a8bbb8a  ","   aaaaa   "]
put(41,34,up); put(40,45,lo)
# ogen, grijns, display
eyeL=[" f8 ","fcc8","fcdf","8ddf"," ff "]
eyeR=[" 8f ","8ccf","fdcf","fdd8"," ff "]
put(21,42,eyeL); put(26,42,eyeR)
put(23,47,["7fff7"," 777 "])
disp=[" 8 888 8 ","888888888","888888888","8e88e888e","8ee8ee8ee","8eeeeeeee"," eeeeeee "]
put(21,50,disp)
for x in range(30,35): A[53,x]=8
CH='.123456789abcdef'
with open('dj_rotom.txt','w') as f:
    f.write('== frame 1\n')
    for r in A: f.write(''.join(CH[v] for v in r)+'\n')
