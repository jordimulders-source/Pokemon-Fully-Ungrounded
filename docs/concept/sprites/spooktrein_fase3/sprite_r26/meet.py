import sys
from PIL import Image
from collections import Counter
M={1,7,8,9,10,11,12,14}
def lum(c): return .299*c[0]+.587*c[1]+.114*c[2]
def meet(path,verbose=False):
    im=Image.open(path); p=im.getpalette(); A=im.load()
    pal=[tuple(p[3*i:3*i+3]) for i in range(16)]
    pc=Counter()
    for y in range(64):
        for x in range(64):
            a=A[x,y]
            for dx,dy in((1,0),(0,1)):
                if x+dx<64 and y+dy<64:
                    b=A[x+dx,y+dy]
                    if a!=b and a in M and b in M: pc[tuple(sorted((a,b)))]+=1
    tot=sum(pc.values()); weak=sum(n for k,n in pc.items() if abs(lum(pal[k[0]])-lum(pal[k[1]]))<20)
    if verbose:
        for k,n in pc.most_common(): print(k,n,round(abs(lum(pal[k[0]])-lum(pal[k[1]]))))
    return weak,tot,100*weak/tot
if __name__=='__main__':
    for f in sys.argv[1:]: print(f,meet(f,True))
