# Stap 6 (Gen 3-eis, SPRITE_KERN "Belijning"): buitenlijn aan de lichtkant (transparant erboven of links ervan, niet
# eronder/rechts) wordt gekleurde selout: donkerste modeltint van het vlak erachter (roest #433425, staal #36332b).
import numpy as np
o=np.load('grens.npy'); n=0; out=o.copy()
for y,x in zip(*np.where(o==1)):
    up=o[y-1,x]==0; lf=o[y,x-1]==0; dn=o[y+1,x]==0; rt=o[y,x+1]==0
    if not (up or lf) or dn or rt: continue
    inner=[o[y+dy,x+dx] for dy,dx in ((1,0),(0,1),(1,1)) if o[y+dy,x+dx]>1]
    if not inner: continue
    v=max(set(inner),key=inner.count)
    if 2<=v<=6: out[y,x]=2; n+=1
    elif 7<=v<=10: out[y,x]=7; n+=1
print('selout-pixels',n); np.save('sprite.npy',out)
