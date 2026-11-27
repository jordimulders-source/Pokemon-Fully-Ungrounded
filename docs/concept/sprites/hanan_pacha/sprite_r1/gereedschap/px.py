# Per spritepixel: modelklasse-aandelen (a=achtergrond l=lijn p=punt r=rood g=goud w=wit) en gemiddelde L van het model.
import sys,numpy as np; sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen('natief_r7.png'); x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]
N='alprgwo'
for Y in range(y0,y1):
    row=[]
    for X in range(x0,x1):
        f=np.zeros(7); lm=0; t=0
        for u,v,w in overlap(X,Y):
            if 0<=u<c.shape[1] and 0<=v<c.shape[0]: f[c[v,u]]+=w; lm+=w*L[v,u]; t+=w
        top=np.argsort(-f)[:2]
        row.append('%s%d%s%d/%3d'%(N[top[0]],int(f[top[0]]*9.99),N[top[1]],int(f[top[1]]*9.99),lm/t))
    print('%2d '%Y+' '.join(row))
print('   '+' '.join('%9d'%x for x in range(x0,x1)))
