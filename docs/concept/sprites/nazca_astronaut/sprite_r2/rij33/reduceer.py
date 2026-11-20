# Natief model (100x100) -> klassenraster 2/3 (vlakgemiddelde: gewogen stem per klasse, geen tekenwerk).
import sys; from PIL import Image; import numpy as np
from klas import klas
Y0,Y1,X0,X1=7,94,29,76      # bbox figuur natief
DREMPEL=0.6
def reduceer(path, oy=0.0, ox=0.0, f=1.5, lijn=1.3):
    c=klas(np.asarray(Image.open(path).convert('RGB')))
    c[c=='?']='.'  # ? = antialias-rand van Gemini; telt als achtergrond (silhouetdrempel doet de rest)
    H=int(np.ceil((Y1-Y0)/f)); W=int(np.ceil((X1-X0)/f))
    out=np.full((H,W),'.',dtype='<U1')
    for j in range(H):
        for i in range(W):
            ya=Y0-oy+f*j; xa=X0-ox+f*i; sc={}
            tot=0
            for y in range(int(np.floor(ya)),int(np.ceil(ya+f))):
                wy=min(y+1,ya+f)-max(y,ya)
                if wy<=0: continue
                for x in range(int(np.floor(xa)),int(np.ceil(xa+f))):
                    wx=min(x+1,xa+f)-max(x,xa)
                    if wx<=0: continue
                    k=c[y,x] if 0<=y<100 and 0<=x<100 else '.'
                    w=wy*wx*(lijn if k in 'Ko' else 1); sc[k]=sc.get(k,0)+w; tot+=wy*wx
            if sc.get(".",0)>DREMPEL*tot: continue
            sc.pop('.',None); out[j,i]=max(sc,key=sc.get)
    return out
if __name__=='__main__':
    o=reduceer(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]))
    for j,r in enumerate(o): print('%2d '%j+''.join(r))
