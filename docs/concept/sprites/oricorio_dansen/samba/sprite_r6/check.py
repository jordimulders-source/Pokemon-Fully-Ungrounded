# check.py: technische controle r6 t.o.v. r5: kleuren, silhouetwijzigingen, diff per zone, losse vlakjes (<3 px), lichte rand
import numpy as np, json; from PIL import Image
from scipy import ndimage
a=np.array(Image.open('samba.png')); b=np.array(Image.open('r5_ref.png'))
H='.123456789abcdef'
Z={'tooi boven (rij 0-13)':(0,14,0,64),'gele tooibladen (rij 14-27, kol 14-44)':(14,28,14,44),'rechtervleugel (rij 13-40, kol 44-60)':(13,41,44,60),
   'kop (rij 25-33, kol 22-37)':(28,34,22,37),'lijf + banden (rij 34-49, kol 24-40)':(34,50,24,40),'linkervleugel (rij 34-50, kol 0-24)':(34,51,0,24),
   'onderste rechterveren (rij 41-51, kol 40-52)':(41,52,40,52),'poten (rij 50-63)':(50,64,0,64)}
log={}
for k,(y0,y1,x0,x1) in Z.items():
    d=a[y0:y1,x0:x1]!=b[y0:y1,x0:x1]; s=(a[y0:y1,x0:x1]>0)!=(b[y0:y1,x0:x1]>0)
    log[k]={'pixels_anders_dan_r5':int(d.sum()),'waarvan_silhouet':int(s.sum())}
S=(a>0)!=(b>0); ys,xs=np.where(S)
log['silhouet_totaal']={'erbij':int(((a>0)&(b==0)).sum()),'eraf':int(((a==0)&(b>0)).sum()),'pixels':[(int(y),int(x),'+' if a[y,x] else '-') for y,x in zip(ys,xs)]}
log['anders_totaal']=int((a!=b).sum())
log['kleuren_incl_transparant']=int(len(np.unique(a)))
# oog/snavel ongewijzigd (kop-uitsnede rij 26-33 kol 24-35)
log['oog_snavel_diff']=int((a[26:34,24:36]!=b[26:34,24:36]).sum())
klein=[]
for v in np.unique(a):
    if v in (0,1,14): continue
    lab,n=ndimage.label(a==v)
    for i in range(1,n+1):
        sz=int((lab==i).sum())
        if sz<3:
            yy,xx=np.where(lab==i); klein.append((H[v],sz,int(yy[0]),int(xx[0])))
log['losse_vlakjes_lt3']=klein
rand=[]
for y in range(64):
    for x in range(64):
        if a[y,x] in (2,3,6,7,9,11,12):
            if any(not(0<=y+dy<64 and 0<=x+dx<64) or a[y+dy,x+dx]==0 for dy,dx in ((0,1),(1,0),(0,-1),(-1,0))): rand.append((H[a[y,x]],y,x))
log['lichte_kleur_op_buitenrand']=rand
json.dump(log,open('log_r6.json','w'),indent=1,ensure_ascii=False)
for k,v in log.items():
    if k=='silhouet_totaal': print(k,v['erbij'],v['eraf'])
    else: print(k,v)
