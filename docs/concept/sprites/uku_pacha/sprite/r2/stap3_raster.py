# Uku Pacha r2 stap 3: klassekaart (M2) -> tekstraster raster_auto.txt; geest krijgt eigen lichte
# omlijning (modeltoon 13) en geen zwarte lijnen binnenin (het model heeft daar geen lijnen).
import numpy as np, geom
M=np.load('M2.npy'); GH=np.load('GH.npy'); cls=np.load('cls.npy')
LET={-1:'.',0:'K',2:'n',6:'d',8:'g',9:'s',11:'m',12:'b',13:'l',14:'p',15:'w',10:'B',7:'D',16:'Y',17:'P',18:'W'}
# geestgebied: vlakken opnieuw met meerderheid over alleen geestcellen
for j,i in zip(*np.where(GH)):
    x0,x1,y0,y1=geom.s2n(i,j); acc={}
    for cy in range(max(0,int(y0)),min(100,int(np.ceil(y1)))):
      for cx in range(max(0,int(x0)),min(100,int(np.ceil(x1)))):
        a=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy)); k=cls[cy,cx]
        if a>0 and k in (13,14,15): acc[k]=acc.get(k,0)+a
    if acc: M[j,i]=max(acc,key=acc.get)
    # rand van de geest (grenst aan transparant) = lichte omlijning 13
    if any(not(0<=j+a<64 and 0<=i+b<64) or M[j+a,i+b]<0 for a,b in ((0,1),(0,-1),(1,0),(-1,0))):
        M[j,i]=13
open('raster_auto.txt','w').write('\n'.join(''.join(LET[v] for v in r) for r in M)+'\n')
