# r19 stap 4: kuif opnieuw ingekleurd binnen de r17-vorm (alpha ongewijzigd), per pixel uit het model gemeten (meet.py).
# rand tegen de lucht -> lijn 1; bruin >=3/9 -> bruin: licht 7 / midden 6 / schaduw 2 naar de helderheid van de bruine modelcellen;
# mauve plukken -> 4 (licht, L>=100) / 3 / 2 (donker >=5/9 = scheiding tussen de plukken). Losse strengen links buiten de massa -> 6.
import numpy as np
from meet import cel
def nb4(a,x,y): return [a[y+dy,x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else 0 for dy,dx in ((0,1),(0,-1),(1,0),(-1,0))]
def kuif(out):
    Z=np.zeros((64,64),bool)
    for y in range(0,22):
        for x in range(0,30):
            if out[y,x] in (1,2,3,4,5,6,7) and not (x>=26 and y>=17): Z[y,x]=True
    base=out.copy(); log=[]
    bruin=[(x,y) for y,x in zip(*np.where(Z)) if cel(x,y) and cel(x,y)['bruin']>=3]
    Ls=np.array([cel(x,y)['Lbruin'] for x,y in bruin]); t7=np.quantile(Ls,0.62); t2=np.quantile(Ls,0.18)
    for y,x in zip(*np.where(Z)):
        c=cel(x,y); n=nb4(base,x,y); rand=0 in n
        buren=sum(v!=0 for v in n)
        if buren<=1 and x<=10: v=6                                # losse streng links
        elif rand: v=1
        elif c['bruin']>=3: v=7 if c['Lbruin']>=t7 else (2 if c['Lbruin']<t2 else 6)
        elif c['donker']>=5: v=2
        else: v=4 if c['Lmauve']>=100 else 3
        if out[y,x]!=v: log.append(('kuif',x,y,int(out[y,x]),v)); out[y,x]=v
    return out,log,Z
