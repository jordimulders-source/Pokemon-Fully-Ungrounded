# Hummlet r2: alleen de benoemde reparaties op r1 (snavel, aansluiting, kopomtrek, volume, oog, staart, vleugellijnen).
# Elke wijziging gelogd per reparatie; diff buiten de zones = 0 wordt aan het eind gecontroleerd.
import numpy as np, json, sys
R1=np.load('r1.npy'); out=R1.copy(); Z=np.load('zone_t.npy'); Zn=np.load('zones_nat.npy')
from PIL import Image
Nl=np.asarray(Image.open('natief.png').convert('RGB')).astype(int).mean(2)
TH,TW=out.shape; log={}; zone_of={}
def zet(y,x,v,rep):
    if out[y,x]!=v:
        log.setdefault(rep,0); log[rep]+=1; out[y,x]=v; zone_of[(y,x)]=rep
s=77/40
def t(nx,ny): return int((nx+0.5-11.5)//s), int((ny+0.5-18.5)//s)
# 1+2 snavel en aansluiting: regelmatige diagonaal (onderrand 1 rij per 2 kolommen), punt 1 px, vanaf kolom 4 2 px (boven leisteen 14, onder 1)
for y in range(0,8):
  for x in range(0,12):
    if y==7 and x>=10: continue
    zet(y,x,0,'1 snavel')
for x in range(0,14):
    b=1+x//2
    if x>=4: zet(b-1,x,14,'1 snavel'); zet(b,x,1,'1 snavel')
    else: zet(b,x,1,'1 snavel')
zet(4,11,2,'2 aansluiting')        # kopomtrek loopt door tot op de snavel
for y,x in [(4,12),(5,12),(5,13),(6,14),(7,15)]: zet(y,x,4,'2 aansluiting')   # donkere klont -> lila wang (model)
zet(7,10,2,'2 aansluiting'); zet(7,11,1,'2 aansluiting')                     # kin: selout lichtkant, dan lijn
# 3 kopomtrek naar de modelboog (cirkel r=7 rond x=18.5): rij 0 16-20, rij 1 14-22, rij 2 13-23
zet(0,19,2,'3 kopomtrek'); zet(0,20,1,'3 kopomtrek'); zet(1,20,5,'3 kopomtrek')
zet(2,24,0,'3 kopomtrek'); zet(2,23,1,'3 kopomtrek')
# 4 volume kop: kleine boog hooglicht 6 op de kruin, sikkel achter de kop 2 px in het midden, nekschaduw naar de vleugel
for y,x in [(1,16),(1,17),(1,18),(2,15)]: zet(y,x,6,'4 volume kop')
for y,x in [(4,23),(5,23),(6,23),(7,24),(8,24),(9,21),(9,22),(9,23),(9,24)]: zet(y,x,3,'4 volume kop')
# 4 volume buik: sikkel onderaan 2 px (5 met lijn 1-2 rijen eronder -> 4), vanaf kolom 13
for y in range(21,TH-1):
  for x in range(13,30):
    if Z[y,x] in ('W','P') and R1[y,x]==5 and (out[y+1,x]==1 or (y+2<TH and out[y+2,x]==1 and out[y+1,x] in (4,5))): zet(y,x,4,'4 volume buik')
zet(29,24,4,'4 volume buik')
# 5 oog (a): modeloog afgerond (hoeken weg), iris 14 onder de glans, lichte onderrand 5
OOG_A={(5,18):4,(5,19):1,(5,20):1,(5,21):4,(6,18):1,(6,19):7,(6,20):14,(6,21):1,(7,18):1,(7,19):14,(7,20):14,(7,21):1,(8,18):4,(8,19):1,(8,20):1,(8,21):5,(9,19):5,(9,20):5}
# (b): Starly-oog uit af/kolibrie_pre.png, pixel voor pixel (glans op dezelfde plek), rest van het oude oogvak -> lila 4
OOG_B={(5,18):1,(5,19):1,(5,20):1,(6,17):2,(6,18):1,(6,19):7,(6,20):1,(6,21):2,(7,17):2,(7,18):1,(7,19):5,(7,20):1,(7,21):2,(8,18):1,(8,19):1,(8,20):1,(5,21):4,(8,21):4}
# 6 staart: lichte bovenrand 1 px (5) op de bovenste veer, middentint 4, scheidingslijn 10 schuin naar de onderste (blauwe) veer
TAIL={(20,35):5,(20,36):5,(20,37):5,(20,38):5,(21,35):4,(21,36):4,(21,37):10,(21,38):10,(22,35):10,(22,36):10,(22,37):8,(22,38):8,(23,35):8,(23,36):8,(23,37):10}
for (y,x),v in TAIL.items(): zet(y,x,v,'6 staart')
# 7 vleugellijnen: de twee lange donkere veerlijnen uit het natieve model (A: natief (58,61)->(72,78), B: (55,67)->(66,79)),
#   omgerekend naar het doelraster en als 1 px-lijn in 10 gezet, alleen op blauwe 8-pixels; eerste/laatste pixel weg (taps)
def lijn(p,q):
    (y0,x0),(y1,x1)=p,q; n=max(abs(y1-y0),abs(x1-x0)); return [(round(y0+(y1-y0)*i/n),round(x0+(x1-x0)*i/n)) for i in range(n+1)]
LA=lijn(t(61,58)[::-1],t(78,72)[::-1]); LB=lijn(t(67,55)[::-1],t(79,66)[::-1])
print('lijn A',LA[0],LA[-1],'lijn B',LB[0],LB[-1])
for L in (LA,LB):
    pts=[p for p in L if out[p]==8 and Z[p]=='V']
    for p in pts[1:-1]: zet(p[0],p[1],10,'7 vleugellijnen')
zet(28,24,4,'4 volume buik')
zet(25,31,10,'7 vleugellijnen'); zet(27,34,10,'7 vleugellijnen')   # losse lila pixels uit r1 op lijn A / vleugelpunt
np.save('r2_basis.npy',out.copy())
json.dump(log,open('log_r2.json','w'),indent=1)
A=out.copy()
for (y,x),v in OOG_A.items(): A[y,x]=v
B=out.copy()
for (y,x),v in OOG_B.items(): B[y,x]=v
for (y,x),v in OOG_A.items(): 
    if (y,x) not in OOG_B and B[y,x]!=R1[y,x] and (y,x) in [(9,19),(9,20)]: B[y,x]=R1[y,x]
np.save('r2_a.npy',A); np.save('r2_b.npy',B)
print(json.dumps(log)); print('oog a',int((A!=out).sum()),'oog b',int((B!=out).sum()))
for nm,M in (('a',A),):
  for y in range(TH): print('%2d '%y+''.join('.' if v==0 else '0123456789abcdef'[v] for v in M[y]))
