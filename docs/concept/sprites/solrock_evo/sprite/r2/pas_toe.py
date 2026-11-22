# Ronde 2: MOET 1-5 + MAG (B onderpunten, A krasjes, kernrand) uit de keuring, per script.
from PIL import Image
import sys
def S(px,pts,c):
    for x,y in pts: px[x,y]=c
def rij(y,x0,x1): return [(x,y) for x in range(x0,x1+1)]
def ogen(px):
    S(px,rij(34,26,32),1)
    for x,c in zip(range(26,33),[1,12,5,12,12,12,1]): px[x,35]=c
    for x,c in zip(range(26,33),[1,12,12,11,11,12,1]): px[x,36]=c
    for x,c in zip(range(26,33),[1,1,12,11,12,1,1]): px[x,37]=c
    S(px,rij(38,27,31),1)
    S(px,rij(34,17,21),1)
    for x,c in zip(range(17,22),[1,12,5,12,1]): px[x,35]=c
    for x,c in zip(range(17,22),[1,12,11,12,1]): px[x,36]=c
    S(px,rij(37,18,20),1)
for v in 'AB':
    im=Image.open(f'r1/{v}.png'); px=im.load()
    ogen(px)
    if v=='A':
        px[22,33]=7;px[22,34]=7;px[22,35]=7;px[22,36]=8
        S(px,[(23,y) for y in range(33,37)],1)
        px[19,27]=7; px[22,39]=8
    else:
        S(px,[(22,y) for y in range(33,37)],3)
        S(px,[(23,y) for y in range(33,37)],1)
        px[23,42]=8;px[24,42]=8;px[25,42]=1;px[23,43]=8;px[24,43]=1;px[24,41]=8;px[22,42]=1;px[22,43]=1
        S(px,[(28,42),(29,42),(30,42),(32,42),(33,42)],8)
        S(px,[(28,43),(29,43),(30,43),(32,43),(33,43)],1)
    px[15,30]=3
    im.save(f'r2/{v}.png',transparency=0)
