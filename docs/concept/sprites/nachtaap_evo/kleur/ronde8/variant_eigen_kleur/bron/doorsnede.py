# kleinste doorsnede van het patroon: per patroonpixel de kortste van (rij-run, kolom-run) door die pixel
import sys, numpy as np
P=np.zeros((64,64),bool)
for l in open(sys.argv[1]): x,y=map(int,l.split()); P[y,x]=True
low=[]
for y,x in zip(*np.nonzero(P)):
    h=1;i=x-1
    while P[y,i]: h+=1;i-=1
    i=x+1
    while P[y,i]: h+=1;i+=1
    v=1;j=y-1
    while P[j,x]: v+=1;j-=1
    j=y+1
    while P[j,x]: v+=1;j+=1
    if min(h,v)<3: low.append((int(x),int(y),h,v))
print('pixels',int(P.sum()),'| onder 3 px:',len(low),low)
