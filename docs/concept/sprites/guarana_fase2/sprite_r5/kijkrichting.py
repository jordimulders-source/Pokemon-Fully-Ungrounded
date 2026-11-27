# r5: kijkrichting per oog gemeten in het natieve model: oogwit-component (klasse 4) + donkere cellen binnen het oog (pupil);
# offset = pupilzwaartepunt t.o.v. het midden van het oog (wit + pupil), genormeerd op de halve breedte/hoogte.
import numpy as np
from gemeen2 import *
from klassen2 import klassen
a,c,L=klassen(NATIEF); H,W=c.shape
def label(m):
    lab=np.zeros(m.shape,int);k=0
    for y,x in zip(*np.where(m)):
        if lab[y,x]: continue
        k+=1; st=[(y,x)]; lab[y,x]=k
        while st:
            cy,cx=st.pop()
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=cy+dy,cx+dx
                    if 0<=yy<H and 0<=xx<W and m[yy,xx] and not lab[yy,xx]: lab[yy,xx]=k; st.append((yy,xx))
    return lab,k
EL,ne=label(c==4)
OGEN_MODEL=[]
for e in range(1,ne+1):
    ys,xs=np.where(EL==e)
    if len(ys)<8: continue
    y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
    # pupil: donkere cellen (L<60) binnen de bbox die links en rechts (op de rij) oogwit hebben of boven en onder
    py=[];px=[]
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if L[y,x]<60 and not EL[y,x]:
                row=EL[y,x0:x1+1]==e; col=EL[y0:y1+1,x]==e
                if (row[:x-x0].any() and row[x-x0+1:].any()) or (col[:y-y0].any() and col[y-y0+1:].any()): py.append(y); px.append(x)
    if not py: continue
    ay=np.r_[ys,py]; ax=np.r_[xs,px]
    cx,cy=(ax.min()+ax.max())/2,(ay.min()+ay.max())/2
    dx=(np.mean(px)-cx)/max(1,(ax.max()-ax.min())/2); dy=(np.mean(py)-cy)/max(1,(ay.max()-ay.min())/2)
    X,Y=naar_sprite(cx+.5,cy+.5)
    OGEN_MODEL.append(dict(X=X,Y=Y,dx=dx,dy=dy,n=len(ys)))
if __name__=='__main__':
    for o in OGEN_MODEL: print('sprite (%.1f,%.1f) n=%d  dx %+.2f dy %+.2f'%(o['X'],o['Y'],o['n'],o['dx'],o['dy']))
