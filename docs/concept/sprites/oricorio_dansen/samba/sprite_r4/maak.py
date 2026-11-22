# Hele keten r4 (model gemini_r10): natief.py -> km.py -> reduce.py 2.9 0 0.97 -> plaats.py -> lijnen.py 1.6 0.3 -> build.py (= stap3.txt, kale
# reductie met modellijnen) -> hand_tooi.py -> hand_rest.py -> bladeren.py -> afwerk.py -> samba.png + telling per zone (log_r4.json)
import subprocess, json, numpy as np
for c in (['python3','hand_tooi.py'],['python3','hand_rest.py'],['python3','bladeren.py','hand2.txt','hand3.txt'],
          ['python3','afwerk.py','hand3.txt','samba.txt'],['python3','dump.py','terug','samba.txt','samba_r4.npy']): subprocess.run(c,check=True)
from render import maak as mk
o=np.load('samba_r4.npy'); mk(o).save('samba.png',transparency=0)
b=np.load('basis.npy')
Z={'tooi (rij 0-26, kol 12-47)':(0,27,12,48),'rechtervleugel (rij 13-40, kol 37-60)':(13,41,37,60),'kop (rij 25-33, kol 22-37)':(25,34,22,37),
   'lijf + rokje (rij 34-49, kol 24-39)':(34,50,24,40),'linkervleugel (rij 34-50, kol 0-24)':(34,51,0,24),'onderste rechterveren (rij 41-51, kol 38-52)':(41,52,38,52),'poten (rij 50-63)':(50,64,0,64)}
log={}
for k,(y0,y1,x0,x1) in Z.items():
    d=(o[y0:y1,x0:x1]!=b[y0:y1,x0:x1]); a=((o[y0:y1,x0:x1]>0)!=(b[y0:y1,x0:x1]>0))
    log[k]={'pixels_anders_dan_kale_reductie':int(d.sum()),'waarvan_dekking':int(a.sum()),'dekkend':int((o[y0:y1,x0:x1]>0).sum())}
ys,xs=np.where(o>0)
log['totaal']={'anders':int((o!=b).sum()),'dekking_anders':int(((o>0)!=(b>0)).sum()),'dekkend':int((o>0).sum()),
  'bbox':[int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max())],'breed_x_hoog':[int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)],
  'kleuren_incl_transparant':int(len(np.unique(o)))}
json.dump(log,open('log_r4.json','w'),indent=1,ensure_ascii=False); print(json.dumps(log,indent=1,ensure_ascii=False))
