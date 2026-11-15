# Stap 5 (bovenlaag, Jordi 15 nov: "wat meer belijning en spiralen ... de huidige wat groter maakt en het lichaam wat meer bedekt").
# Niets nieuw getekend: bestaande spiralen uit de sprite zelf als asset hergebruiken.
#  A  heupspiraal (in de reductie een vlek): vervangen door de schouderspiraal (cremeboog + lila ring + binnenkrul),
#     gespiegeld, bruin binnenin een tint donkerder omdat de heup in de schaduw ligt -> groter en leesbaar.
#  B  kleine cremekrul onder de schouder (x22-25,y32-34) als lila krul op borst en opgeheven poot -> lichaam meer bedekt.
import numpy as np, sys
a=np.load('welp_r2_zonder_extra.npy'); base=a.copy()
K,d,S,M,L,P,Q,R,g_,W,C,T,G=range(1,14)
BROWN={S,M,L}
log={}
# A: schouderspiraal-asset x20-28,y20-30 (alleen creme/lila/binnenkrul, geen omliggend bruin)
src=base[20:31,20:29].copy()
srcm=np.isin(src,[C,P,Q,R])
# binnenkrul en binnenvlak (binnen de lila ring) ook meenemen
inner=np.zeros_like(srcm); inner[3:9,2:6]=True     # x22-25,y23-28
srcm|=inner
src=src[:,::-1]; srcm=srcm[:,::-1]                 # gespiegeld
DARKER={L:M,M:S,S:d}
y0,x0=28,30                                        # doel x30-38, y28-38
ch=0
for j in range(src.shape[0]):
    for i in range(src.shape[1]):
        if not srcm[j,i]: continue
        y,x=y0+j,x0+i
        if a[y,x] in (0,K): continue               # buitenlijn en zwarte lijnen blijven
        v=src[j,i]; v=DARKER.get(v,v)
        if a[y,x]!=v: a[y,x]=v; ch+=1
log['heupspiraal']=ch
# oude lila streep/vlek op de heup buiten de nieuwe spiraal -> heupbruin (de spiraal neemt zijn plek in)
ch=0
for y in range(28,39):
    for x in range(29,42):
        inside=(0<=y-y0<src.shape[0]) and (0<=x-x0<src.shape[1]) and srcm[y-y0,x-x0]
        if not inside and a[y,x] in (P,Q,R,C) and base[y,x]==a[y,x]: a[y,x]=S; ch+=1
log['heup_oud_weg']=ch
# B: krul (uit x23-25,y32-34 van de sprite): c c . / c d . / c c c  -> lila q met donkere kern
hook=[(0,0),(1,0),(0,1),(0,2),(1,2),(2,2)]; core=(1,1)
def put(x0,y0,col,kern,name):
    ch=0
    for dx,dy in hook:
        if a[y0+dy,x0+dx]!=col: a[y0+dy,x0+dx]=col; ch+=1
    x,y=x0+core[0],y0+core[1]
    if a[y,x]!=kern: a[y,x]=kern; ch+=1
    log[name]=ch
put(15,23,Q,S,'krul_borst')
put(3,24,Q,S,'krul_poot')
np.save('welp_r2.npy',a)
print(log,'totaal t.o.v. zonder_extra',(a!=base).sum())
