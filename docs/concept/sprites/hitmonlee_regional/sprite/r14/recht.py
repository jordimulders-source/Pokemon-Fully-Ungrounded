# Rechte-lijnencheck: runs in de omtrek (rand naar achtergrond) en in de binnenlijnen (index 1/2 binnenin).
# h: horizontale run >=5 met achtergrond erboven of eronder; v: verticale run >=5 met achtergrond links/rechts;
# d: regelmatige 45-graden-trap (1-1-1-1) van >=5 stappen; r: binnenlijn-run (index 1/2, niet aan de rand) >=4 horizontaal.
from PIL import Image; import numpy as np, sys
def runs(e,minh=5,minv=5,mind=5,minr=4):
    F=e>0; H,W=F.shape
    P=np.pad(F,1)
    up=F&~P[:-2,1:-1]; dn=F&~P[2:,1:-1]; lf=F&~P[1:-1,:-2]; rt=F&~P[1:-1,2:]
    out=[]
    def scan(B,axis,kind,mn):
        for i in range(B.shape[0] if axis==0 else B.shape[1]):
            line=B[i] if axis==0 else B[:,i]
            j=0
            while j<len(line):
                if line[j]:
                    k=j
                    while k<len(line) and line[k]: k+=1
                    if k-j>=mn: out.append((kind,i,j,k-j) )
                    j=k
                else: j+=1
    scan(up,0,'h-boven',minh); scan(dn,0,'h-onder',minh); scan(lf,1,'v-links',minv); scan(rt,1,'v-rechts',minv)
    # diagonale trappen: randpixels die (y+1,x+-1) ook rand zijn, ketens
    E=up|dn|lf|rt
    for sx in (1,-1):
        seen=set()
        for y in range(H):
            for x in range(W):
                if not E[y,x] or (y,x) in seen: continue
                ch=[(y,x)]; yy,xx=y,x
                while 0<=yy+1<H and 0<=xx+sx<W and E[yy+1,xx+sx] and not E[yy+1,xx] and not E[yy,xx+sx]:
                    yy+=1; xx+=sx; ch.append((yy,xx))
                for c in ch: seen.add(c)
                if len(ch)>=mind: out.append(('diag%+d'%sx,y,x,len(ch)))
    inner=(e==1)|(e==2)
    inner&=~E
    scan(inner,0,'binnen-h',minr)
    return out
if __name__=='__main__':
    e=np.array(Image.open(sys.argv[1]))
    for r in runs(e): print(r)
