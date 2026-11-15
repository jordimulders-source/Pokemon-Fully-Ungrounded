# r5: pieken rechtsonder (x34-49, y30-53) opnieuw als lange spitse punten (gemeten op model_12x)
import numpy as np
from gio import from_txt, to_txt, CH
def run(o):
    C={c:i for i,c in enumerate(CH)}; H,W=o.shape
    def inpoly(px,py,P):
        c=False; n=len(P)
        for i in range(n):
            x1,y1=P[i]; x2,y2=P[(i+1)%n]
            if (y1>py)!=(y2>py) and px < x1+(py-y1)*(x2-x1)/(y2-y1): c=not c
        return c
    B=[(30,56),(32.6,56),(33.3,52),(44.6,41.2),(38.6,41.8),(46.7,34.2),(40.6,35.4),(46.0,30.1),(42.5,29.5),(30,29.5)]
    SP=[]
    dark=np.zeros_like(o,bool)
    win=[(y,x) for y in range(30,54) for x in range(33 if y>=47 else 34,50) if o[y,x]>=0]
    for y,x in win:
        px,py=x+0.5,y+0.5
        dark[y,x]=inpoly(px,py,B) or any(inpoly(px,py,p) for p in SP)
    out=o.copy()
    def isd(y,x):
        if (y,x) in S: return dark[y,x]
        return o[y,x]>=0 and CH[o[y,x]] in 'ijKnv'
    S=set(win)
    for y,x in win:
        edge=any(o[y+a,x+b]<0 for a,b in((1,0),(-1,0),(0,1),(0,-1)))
        if dark[y,x]:
            if not isd(y+1,x) or not isd(y,x+1): t='K'
            elif not isd(y-1,x): t='j'
            elif CH[o[y,x]] in 'MLWw' and x<=40 and y<=34: t=CH[o[y,x]]
            else: t='i' if CH[o[y,x]] not in 'j' else 'j'
        else:
            t=CH[o[y,x]] if (edge and CH[o[y,x]] in 'MLW') else ('M' if edge else 'W')
        out[y,x]=C[t]
    return out
if __name__=='__main__':
    o=from_txt('r4.txt'); out=run(o)
    for y in range(26,57): print('%2d '%y+''.join('.' if v<0 else CH[v] for v in out[y,30:54]))
