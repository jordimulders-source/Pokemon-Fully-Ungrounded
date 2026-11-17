# r2 punt 6: linkerrand van huls en kegel van de pijl als rechte modelrand. Per rij de plek waar de modeldekking 0,5 haalt
# (subpixel, uit blok_w_dg.npy), daar een rechte lijn door gefit (huls rij 46-54, kegel 54-62). Links van de lijn leeg,
# randpixel = donkermagenta 6 (lichtkant, zoals r1/model), nieuw gevulde pixels = vlakkleur van de rechterbuur.
import numpy as np
W=np.load('blok_w_dg.npy'); cov=1-W[...,0]; a=np.load('r2_gezicht.npy'); n=0
def rand(y,x0=20,x1=47):
    r=cov[y,x0:x1]
    for i in range(len(r)-1):
        if r[i]<0.5<=r[i+1]: return x0+i+(0.5-r[i])/(r[i+1]-r[i])   # kruising tussen pixelmiddens
    return None
for rows in (range(46,55),range(54,63)):
    ys=[y for y in rows if rand(y) is not None]; xs=[rand(y) for y in ys]
    k,c=np.polyfit(ys,xs,1); print('rijen',rows,'helling',round(k,3))
    for y in rows:
        e=int(np.ceil(k*y+c-0.5+1e-6))       # eerste pixel waarvan het midden rechts van de rand ligt
        for x in range(20,47):
            if a[y,x] in (10,11,12) : break
            if x<e and a[y,x]!=0: a[y,x]=0; n+=1
            elif x==e:
                if a[y,x]!=6 and not (y==62): a[y,x]=6; n+=1
                if y==62 and a[y,x]!=1: a[y,x]=1; n+=1
                break
# punt: alleen de onderste (zwarte) rij reikt tot de punt, zoals in het model de onderlijn voorbij de kegel uitsteekt
for (x,y,v) in ((25,60,0),(26,60,6),(25,61,0),(26,61,6)):
    if a[y,x]!=v: a[y,x]=v; n+=1
np.save('r2_pijl.npy',a); print('pijl: gewijzigd',n)
