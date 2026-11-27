# Zoekt rechte lijnstukken (>=4 px horizontaal, verticaal of 45 graden) in lijn- of donkere tint (1, 2, 13) in een sprite.
import numpy as np, sys
def runs(o,ks=(1,2),MIN=4):
    D=np.isin(o,ks); out=[]
    for (dy,dx) in ((0,1),(1,0),(1,1),(1,-1)):
        for Y in range(64):
            for X in range(64):
                if not D[Y,X]: continue
                py,px=Y-dy,X-dx
                if 0<=py<64 and 0<=px<64 and D[py,px]: continue
                n=0; y,x=Y,X
                while 0<=y<64 and 0<=x<64 and D[y,x]: n+=1; y+=dy; x+=dx
                if n>=MIN: out.append(((dy,dx),Y,X,n))
    return out
if __name__=='__main__':
    o=np.load(sys.argv[1])
    for r in runs(o): print(r)
