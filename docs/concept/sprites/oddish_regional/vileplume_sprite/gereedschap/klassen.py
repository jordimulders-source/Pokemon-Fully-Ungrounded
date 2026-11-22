# Klassen per natieve modelpixel (alleen indelen van modelkleuren, niets tekenen).
import numpy as np
from PIL import Image
NAMEN=['bg','K','R0','R1','R2','R3','W0','W1','W2','W3','W4','G','KB','KO','KM','KG']
# R = anemonen (lijn, schaduw, midden, licht oranje), W = lijf/poten (lijn, 4 tinten donker->licht),
# G = kratergrijs (donkerder grijs < L60 telt als zwart), KB = bruine binnenrand krater, KO/KM/KG = kratergloed roodoranje/oranje/geel
KRATER=(99.5,57.0,17.5,9.5)   # ellips cx,cy,rx,ry natief: zwarte/grijze kraterrand (gemeten op het natieve raster)
def klassen(path='gereedschap/natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    H,W=L.shape; c=np.zeros((H,W),int)
    # achtergrond = vanaf de rand verbonden bijna-wit (min >= 240); het lijf is zelf bijna wit (e8f3eb), dus geen vaste drempel
    from collections import deque
    wit=a.min(2)>=240; bg=np.zeros((H,W),bool); q=deque()
    for y in range(H):
        for x in (0,W-1): q.append((y,x))
    for x in range(W):
        for y in (0,H-1): q.append((y,x))
    while q:
        y,x=q.popleft()
        if 0<=y<H and 0<=x<W and wit[y,x] and not bg[y,x]:
            bg[y,x]=True; q.extend(((y+1,x),(y-1,x),(y,x+1),(y,x-1)))
    yy,xx=np.mgrid[0:H,0:W]
    cx,cy,rx,ry=KRATER; kr=((xx-cx)/rx)**2+((yy-cy)/ry)**2<=1
    neutraal=(a.max(2)-a.min(2))<28
    koel=(B>=R-8)&~neutraal          # blauwig wit/grijs van lijf en poten
    for y,x in zip(*np.where(~bg)):
        l=L[y,x]; r,g,b=R[y,x],G[y,x],B[y,x]
        if l<36: c[y,x]=1
        elif kr[y,x] and r>215 and g>60 and (b<64 or (g>=148 and b<72)): c[y,x]=15 if g>=148 else 14 if g>=112 else 13
        elif kr[y,x] and neutraal[y,x]: c[y,x]=1 if l<60 else 11
        elif kr[y,x] and r<170 and r>g and g>15 and b<90 and r-g<110: c[y,x]=12
        elif koel[y,x] or (neutraal[y,x] and l>=100): c[y,x]=6 if l<105 else 7 if l<165 else 8 if l<196 else 9 if l<228 else 10
        elif neutraal[y,x] and y>=88: c[y,x]=6        # donkere grijsblauwe lijn van lijf/poten
        elif neutraal[y,x]: c[y,x]=2
        else: c[y,x]=2 if l<82 else 3 if l<113 else 4 if l<148 else 5
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN): print(n,(c==i).sum())
    ch='.K0123abcdeGuomy'
    for y in range(26,174): print('%3d '%y+''.join(ch[v] for v in c[y,34:166]))
