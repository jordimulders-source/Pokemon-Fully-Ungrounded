# opruimen: per schots modus-filter op de modeltonen, losse pixels naar modelburen
import sys; sys.path.insert(0,'r7w'); sys.path.insert(0,'r6w')
import numpy as np, p6
from zones import flood, isin, I, CH, R
o=np.load(sys.argv[1]); out=sys.argv[2]
body=np.load('r7w/body2.npy'); outer=np.load('r7w/outer2.npy'); gas=np.load('r7w/gas.npy'); core=np.load('r7w/core.npy')
eye=isin(R,'erCg')
fill=body&~outer&~eye&isin(o,'WLMD')
TON=[I[c] for c in 'WLMD']
def modus(o,zone,it=2,keep_ties=True):
    for _ in range(it):
        n=o.copy()
        for j,i in zip(*np.where(zone)):
            c={}
            for dy in (-1,0,1):
              for dx in (-1,0,1):
                y,x=j+dy,i+dx
                if zone[y,x]: c[o[y,x]]=c.get(o[y,x],0)+1
            best=max(c.values())
            if c.get(o[j,i],0)<best and c.get(o[j,i],0)<=2: n[j,i]=max(c,key=c.get)
        o=n
    return o
o=modus(o,fill)
# losse pixels (geen 4-buur met dezelfde kleur) in gas en kern
for zone in (gas&~np.zeros_like(gas),core):
    for _ in range(2):
        n=o.copy()
        for j,i in zip(*np.where(zone)):
            nb=[o[j+dy,i+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if zone[j+dy,i+dx]]
            if nb and o[j,i] not in nb:
                n[j,i]=max(set(nb),key=nb.count)
        o=n
np.save(out+'.npy',o); p6.to_txt(o,out+'.txt')
