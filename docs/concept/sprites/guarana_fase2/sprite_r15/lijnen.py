# lijnen.py: binnenlijnen in links/midden (zwart en lijnrood binnen de tros, buiten de ogen) r14 vs r15, en hoe heel vrucht G (linksonder) is
import sys; sys.path.insert(0,'sprite_r9'); sys.path.insert(0,'sprite_r15'); sys.path.insert(0,'sprite_r14')
import numpy as np; from PIL import Image; from hulp import N4; import bouw14 as A, bouw15 as B
for tag,mod,img in (('r14',A,'sprite_r14/guarana2_r14.png'),('r15',B,'sprite_r15/guarana2_r15.png')):
    o=np.array(Image.open(img)).astype(int)
    for n in 'LM':
        vr=mod.tros(n,*mod.INSTEL[n]); m=set().union(*[f['F'] for f in vr])
        ogen={(x,y) for (x,y) in m if any(0<=y+a<64 and 0<=x+b<64 and o[y+a,x+b]==10 for a in (-1,0,1) for b in (-1,0,1))}
        binnen=[(x,y) for (x,y) in m if all((x+b,y+a) in m for a,b in N4) and (x,y) not in ogen]
        k=sum(o[y,x]==1 for x,y in binnen); l=sum(o[y,x]==2 for x,y in binnen)
        dik=sum(o[y,x] in (1,2) and o[y,x+1] in (1,2) and o[y+1,x] in (1,2) and o[y+1,x+1] in (1,2) for x,y in binnen)
        print(tag,n,'binnen de tros, niet bij een oog: zwart',k,'lijnrood',l,'2x2-lijnklonten',dik)
    G=[f for f in mod.tros('L',*mod.INSTEL['L']) if f['n']=='G'][0]
    print(tag,'vrucht G zichtbaar (rood):',sum(1 for q in G['F'] if o[q[1],q[0]] in (2,3,4,5)),'/',len(G['F']))
