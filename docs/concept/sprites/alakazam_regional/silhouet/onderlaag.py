# automatische onderlaag (alleen als start; daarna met de hand)
import numpy as np
d=np.load('meet.npz'); mean,p15,dark,red,m=d['mean'],d['p15'],d['dark'],d['red'],d['m']
L=mean.mean(2); out=[]
for Y in range(64):
    r=''
    for X in range(64):
        if not m[Y,X]: r+='.'; continue
        l=L[Y,X]
        if red[Y,X]>0.35: r+='r' if l>80 else 's'
        elif l<24 or (dark[Y,X]>0.3 and p15[Y,X]<20 and l<140): r+='o'
        elif l<48: r+='m'
        elif l<70: r+='n'
        elif l<100: r+='e'
        elif l<135: r+='d'
        elif l<170: r+='c'
        elif l<200: r+='b'
        elif l<232: r+='a'
        else: r+='w'
    out.append(r)
open('../kleur_r1/onderlaag.txt','w').write('\n'.join(out)+'\n')
