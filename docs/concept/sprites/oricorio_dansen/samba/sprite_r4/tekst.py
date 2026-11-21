# tekstraster van de modelmeting per spritepixel: vulmodus (letter) en lijnaandeel (cijfer 0-9 = tienden) voor zone y0 y1 x0 x1
import numpy as np, sys, json
from reduce import cl, LIJN, FAM, grenzen
from palet import NAMEN
F,OY,OX=2.9,0,0.97; pl=json.load(open('plaats.json'))
gy=grenzen(200,F,OY); gx=grenzen(200,F,OX)
y0,y1,x0,x1=map(int,sys.argv[1:5])
LET={'_':'.','O':'#','G1':'a','G2':'b','G3':'c','G4':'d','Y1':'y','Y2':'z','Y3':'x','B1':'B','B2':'C','K1':'p','K2':'q','K3':'r','W':'w'}
print('     '+''.join(str((x//10)%10) for x in range(x0,x1))); print('     '+''.join(str(x%10) for x in range(x0,x1)))
for Y in range(y0,y1):
    s1='';s2=''
    for X in range(x0,x1):
        j=Y-pl['dy']; i=X-pl['dx']
        if not(0<=j<len(gy)-1 and 0<=i<len(gx)-1): s1+='.'; s2+='.'; continue
        sl=(slice(gy[j],gy[j+1]),slice(gx[i],gx[i+1])); b=cl[sl].ravel(); l=LIJN[sl].ravel()
        if (b>0).sum()<0.45*len(b): s1+='.'; s2+='.'; continue
        v=b[(b>0)&~l]
        if len(v)==0: s1+='#'
        else:
            u,c=np.unique(v,return_counts=True); s1+=LET[NAMEN[u[c.argmax()]]]
        s2+=str(min(9,int(10*l.sum()/len(b))))
    print('%3d  %s   %s'%(Y,s1,s2))
