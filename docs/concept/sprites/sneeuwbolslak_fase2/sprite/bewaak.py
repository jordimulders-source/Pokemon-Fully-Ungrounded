# python3 sprite/bewaak.py RASTER.txt  (methode Krassault): silhouet-diff (moet 0) + afwijking van onderlaag56 per zone.
import sys,numpy as np
S=np.load('sprite/sil56_rond.npy'); O=[l.rstrip('\n') for l in open('sprite/onderlaag56.txt')]; R=[l.rstrip('\n') for l in open(sys.argv[1])]
sd=sum((R[y][x]!='.')!=S[y,x] for y in range(64) for x in range(64)); print('silhouet-diff:',sd)
Z={'bol':0,'kop':0,'staart':0,'lijf/flap/ring':0}
for y in range(64):
    for x in range(64):
        if O[y][x]!=R[y][x]:
            k='bol' if (x-31.5)**2+(y-31)**2<=12.5**2 and y<=36 else 'kop' if x<=22 and y>=35 else 'staart' if x>=43 and y<=50 else 'lijf/flap/ring'
            Z[k]+=1
print('afwijking van onderlaag56:',Z,'totaal',sum(Z.values()),'van',int(S.sum()))
print('OK' if sd==0 else 'FAIL'); sys.exit(0 if sd==0 else 1)
