# maak.py r10 (vanaf r9): alleen 3 herkeurpunten, silhouet gelijk aan r9
import numpy as np, json
from render import schrijf
a=np.load('../sprite_r9/samba_r9.npy'); r9=a.copy()
E={'1_lijnhoek_veer':[(43,14,1,5),(44,14,1,5),(43,15,1,5)],
   '2_middelste_tooiveer':[(29,14,8,6),(29,15,8,6)],
   '3_band_links':[(15,45,7,8),(19,45,7,8),(20,45,7,8),(20,43,8,7)]}
log={}
for k,l in E.items():
    for x,y,o,n in l: assert a[y,x]==o,(k,x,y,a[y,x]); a[y,x]=n
    log[k]=len(l)
assert ((a>0)!=(r9>0)).sum()==0
log['alpha_diff']=0; log['totaal']=int((a!=r9).sum())
np.save('samba_r10.npy',a); schrijf(a,'samba.png'); json.dump(log,open('log_r10.json','w'),indent=1); print(log)
