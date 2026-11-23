# Krans-ogen . - . - . ^ . - . - . : stip = r6-pupilpositie (natief), rest van het streepje = vulling van het bolletje (boven/onder-buur).
import sys; sys.path.insert(0,'.'); sys.path.insert(0,'r4'); sys.path.insert(0,'r2')
import numpy as np
from PIL import Image
from natcoord import NY,NX
N6=np.asarray(Image.open('r5/natief_r6.png')).astype(float); L6=(N6*[0.299,0.587,0.114]).sum(2)
STIP={'L1':[(4,x) for x in range(20,24)],'L3':[(17,x) for x in range(7,10)],'L5':[(33,10),(33,11)],
      'R1':[(4,x) for x in range(39,43)],'R3':[(17,x) for x in range(54,58)],'R5':[(34,x) for x in range(51,55)]}
STREEP=['L2','L4','R2','R4']
# r6-stippen: donkere natieve pixel met lichte 4-buren
dots=[(y,x) for y in range(1,98) for x in range(1,98) if L6[y,x]<130 and all(L6[y+a,x+b]>165 for a,b in ((0,1),(0,-1),(1,0),(-1,0)))]
def ogen(S):
    S=S.copy(); log=[]
    for k,px in STIP.items():
        nat=[(NY[y,x],NX[y,x]) for y,x in px]
        best=min(((abs(dy-ny)+abs(dx-nx),i,(dy,dx)) for i,(ny,nx) in enumerate(nat) for dy,dx in dots))
        d,i,dot=best
        orig=S.copy()
        for j,(y,x) in enumerate(px):
            if j==i: S[y,x]=6
            else:
                a,b=orig[y-1,x],orig[y+1,x]
                S[y,x]=a if a==b or b in (6,7) else (b if a in (6,7) else min(a,b))
        log.append((k,'stip',px[i],'r6-stip natief',dot,'afstand',d))
    return S,log
if __name__=='__main__':
    E=np.array(Image.open('eindkeuring/claydol_eind.png')); S,log=ogen(E)
    for l in log: print(*l)
    for k,px in STIP.items():
        y=px[0][0]; xs=[x for _,x in px]; print(k,[ (int(E[y,x]),int(S[y,x])) for x in range(xs[0]-2,xs[-1]+3)])
