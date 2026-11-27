# oogtabel.py: per oog wit-bbox (wit + pupil), pupil-bbox, offset pupilmidden t.o.v. witmidden, en of het oog ongeschonden in de sprite staat
import sys; sys.path.insert(0,'sprite_r9'); sys.path.insert(0,'sprite_r15'); import numpy as np; from PIL import Image; from hulp import N4
import bouw15 as B
o=np.array(Image.open('sprite_r15/guarana2_r15.png')).astype(int)
bb=lambda s:(min(x for x,y in s),min(y for x,y in s),max(x for x,y in s),max(y for x,y in s))
mid=lambda b:((b[0]+b[2])/2,(b[1]+b[3])/2)
print('| tros | oog | sjabloon | wit-bbox (x0,y0)-(x1,y1) | pupil-bbox | offset (dx,dy) | in sprite |')
print('|---|---|---|---|---|---|---|')
for n,(sp,sr,dx,dy) in B.INSTEL.items():
    vr=B.tros(n,sp,sr,dx,dy); B.bouw_tros(vr)
    for f in vr:
        if 'oog' not in f: continue
        d=f['oog']
        pup,wit=B.pupilplek(f['pup'],d)
        goed=sum(o[q[1],q[0]]==c for q,c in d.items()); 
        bw,bp=bb(wit),bb(pup); mw,mp=mid(bw),mid(bp)
        print('| %s | %s | %s | (%d,%d)-(%d,%d) | (%d,%d)-(%d,%d) | (%+.1f,%+.1f) | %d/%d px |'%(n,f['n'],f['pup'],*bw,*bp,mp[0]-mw[0],mp[1]-mw[1],goed,len(d)))
