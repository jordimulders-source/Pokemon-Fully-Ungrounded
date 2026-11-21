# r6 punt 3: V-hals terug op de gemeten modelplek. Zone rij 19-27, kol 21-38 (oog/snavel erbuiten): vlakpixels opnieuw getint op de
# modelhelderheid per spritepixel: L<40 -> D4 (de V-lijn: kop tegen hals), 40-59 -> D2 (hals), >=60 -> D1 (kop). Zwart/silhouet onaangeroerd.
import numpy as np, json
o=np.load('na_franje.npy').copy(); f=o.copy(); L=np.load('model_L.npy')
_,O,D0,D1,D2,D3,D4=range(7)
log={}
for y in range(19,28):
    for x in range(21,39):
        if o[y,x] not in (D1,D2,D3,D4): continue
        if y<=22 and x<=30: 
            if not (y>=21 and (x<=24 or x>=30)): continue      # kop rond oog/snavel niet aanraken, behalve de V-armen
        v=D4 if L[y,x]<40 else (D2 if L[y,x]<60 else D1)
        if v!=o[y,x]: o[y,x]=v; log['V_hals_'+['','O','D0','D1','D2','D3','D4'][v]]=log.get('V_hals_'+['','O','D0','D1','D2','D3','D4'][v],0)+1
assert ((o>0)==(f>0)).all()
np.save('tango_r6.npy',o); log['px_veranderd']=int((o!=f).sum()); json.dump(log,open('log_hals.json','w'),indent=0); print(log)
s='.O01234ABCklmW'
for y in range(18,30): print('%2d '%y+''.join(s[v] for v in o[y,18:46]))
