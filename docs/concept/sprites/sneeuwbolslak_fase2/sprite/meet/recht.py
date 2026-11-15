# python3 sprite/meet/recht.py raster.txt : rechte lijnstukken (omlijning '#' en binnenlijn 'd') van >= 4 px horizontaal/verticaal
# en >= 5 px exact diagonaal. In Gen 3 zijn rondingen trapjes; lange rechte stukken lezen als "te recht" (Jordi).
import sys
R=[l.rstrip('\n') for l in open(sys.argv[1])]; L=lambda y,x: 0<=y<64 and 0<=x<64 and R[y][x] in '#d'
out=[]
for dy,dx,mn,naam in ((0,1,4,'horizontaal'),(1,0,4,'verticaal'),(1,1,5,'diagonaal \\'),(1,-1,5,'diagonaal /')):
    for y in range(64):
        for x in range(64):
            if L(y,x) and not L(y-dy,x-dx):
                n=0
                while L(y+n*dy,x+n*dx): n+=1
                if n>=mn: out.append((n,naam,x,y))
for n,naam,x,y in sorted(out,reverse=True): print(f'{n:2d} px {naam:12s} vanaf (x {x}, y {y})')
print('totaal',len(out))
