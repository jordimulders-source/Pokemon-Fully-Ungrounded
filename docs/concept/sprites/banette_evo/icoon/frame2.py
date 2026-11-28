"""Frame 2 uit frame 1 (werkwijze stap 7): alles boven de voeten (rij 28-29) 1 px omlaag, de bovenste stofrij (27) vervalt
onder de verschoven romp, voeten blijven staan; gebaar: rechterhand met kruis blijft staan = 1 px omhoog t.o.v. het lijf.
python3 frame2.py f1.txt uit.txt"""
import sys
L=[list(l) for l in open(sys.argv[1]).read().split('\n')[:32]]
def STIL(x,y):  # rechterhand + kruis blijven staan (hand trekt 1 px op)
    return (x>=26 and 11<=y<=18) or (23<=x<=25 and 15<=y<=17)
F2=[['.']*32 for _ in range(32)]
for y in (28,29):
    F2[y]=L[y][:]
for y in range(0,28):
    for x in range(32):
        if L[y][x]=='.': continue
        if STIL(x,y): continue
        F2[y+1][x]=L[y][x]
for y in range(0,28):
    for x in range(32):
        if STIL(x,y) and L[y][x]!='.': F2[y][x]=L[y][x]
F2[18][23]='O'  # rand van de romp sluiten onder de opgetrokken hand
out=L+F2
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in out)+'\n')
for i in range(6,31): print('%2d'%i,''.join(L[i]),' ',''.join(F2[i]))
