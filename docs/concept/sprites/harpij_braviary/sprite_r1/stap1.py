# Stap 3: kale reductie -> letters van het eindpalet (zelfde vlakken). Zone-afhankelijk: snavel en poten = staal.
import numpy as np
k=np.load('kaal.npy'); H,W=k.shape
M={0:'.',1:'K',2:'K',3:'K',4:'n',5:'a',6:'a',7:'a',8:'b',9:'b',10:'b',11:'c',12:'g',13:'h',14:'u',15:'i',16:'W',17:'e',18:'e'}
g=[[M[v] for v in r] for r in k]
def snavel(y,x): return 13<=y<=21 and x<=8
def poot(y,x): return y>=48 and x<=25
ST={'a':'s','b':'t','c':'t','n':'s','g':'t','h':'u','i':'u','W':'W'}
for y in range(H):
    for x in range(W):
        if (snavel(y,x) or poot(y,x)) and g[y][x] in ST: g[y][x]=ST[g[y][x]]
open('stap1.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
print(open('stap1.txt').read())
