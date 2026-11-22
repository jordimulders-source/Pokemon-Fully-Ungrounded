# Rechterkant rond maken zonder tekenen (Jordi akkoord, 23 nov):
# cirkel gepast op de bestaande omtrek boven (incl. rechtsboven), links (boven/onder de neus) en onder (niet neus, niet puin):
# c=(36.41,30.46), R=22.17. Nieuwe rechterrand per rij E[y] = laatste pixel waarvan het midden binnen R+0.1 valt
# (nooit smaller dan het model). Per rij wordt de bestaande schaduwband (vanaf het ankerpunt op straal r0 = binnenkant
# van de sikkel) horizontaal uitgerekt tot E[y]: zelfde tinten, barsten lopen mee. Rijen 16-41 (daarboven rond, daaronder puin).
import numpy as np; from scipy import ndimage; import tool
q=np.load('q.npy'); f=q>0
lab,n=ndimage.label(f); s=np.bincount(lab.ravel()); s[0]=0; main=lab==np.argmax(s)
cx,cy,R=36.412,30.457,22.174; r0=10.0
o=q.copy(); zone=np.zeros((64,64),bool); E={}
for y in range(16,42):
    dy=y+0.5-cy
    oldE=np.where(main[y])[0].max()
    e=int(np.floor(cx+np.sqrt((R+0.1)**2-dy*dy)-0.5))
    puin=f&~main
    while e>oldE and puin[y-1:y+2,oldE:e+2].any(): e-=1   # 1 px afstand tot los puin
    e=max(e,oldE); E[y]=(oldE,e)
    if e==oldE: continue
    xa=int(round(cx+np.sqrt(max(r0*r0-dy*dy,0))))
    for x in range(xa,e+1):
        xs=int(round(xa+(x-xa)*(oldE-xa)/(e-xa)))
        o[y,x]=q[y,xs]; zone[y,x]=True
np.save('rond.npy',o); np.save('rond_zone.npy',zone)
print('rand per rij (oud->nieuw):',{y:v for y,v in E.items() if v[0]!=v[1]})
print('zone px',zone.sum(),'gewijzigd t.o.v. model',(o!=q).sum(),'nieuw silhouet',((o>0)&~(q>0)).sum())
