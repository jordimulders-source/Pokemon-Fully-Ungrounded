import numpy as np, shutil, os
from PIL import Image
S='/home/user/projectgrounded/docs/concept/sprites/'
class Sprite:
    def __init__(s, base):
        s.im=Image.open(S+base+'/anim_front.png'); s.old=np.array(s.im).copy(); s.a=s.old.copy(); s.base=base
    def set(s,f,x,y,v,exp=None):
        Y=y+64*f
        if exp is not None: assert s.old[Y,x]==exp,(f,x,y,s.old[Y,x],exp)
        s.a[Y,x]=v
    def both(s,x,y,v,dy2=0,exp=None):
        # frame1 at (x,y); frame2 at (x,y+dy2); asserts same old value in both
        assert s.old[y,x]==s.old[y+dy2+64,x],('f2 mismatch',x,y,s.old[y,x],s.old[y+dy2+64,x])
        s.set(0,x,y,v,exp); s.set(1,x,y+dy2,v,exp)
    def save(s,out):
        os.makedirs(S+out,exist_ok=True)
        im=Image.fromarray(s.a.astype(np.uint8),'P'); im.putpalette(s.im.getpalette())
        im.save(S+out+'/anim_front.png',transparency=0)
        shutil.copy(S+s.base+'/normal.pal',S+out+'/normal.pal')
        d=np.argwhere(s.a!=s.old)
        return d
    def openedges(s):
        # pixel next to transparent (4-neighbour) whose colour is not an outline index
        return None
def report(d):
    out=[]
    for f in (0,1):
        dd=d[(d[:,0]>=64*f)&(d[:,0]<64*(f+1))]
        if len(dd)==0: out.append('frame %d: 0 px'%(f+1)); continue
        ys=dd[:,0]-64*f; xs=dd[:,1]
        out.append('frame %d: %d px, box x%d-%d y%d-%d'%(f+1,len(dd),xs.min(),xs.max(),ys.min(),ys.max()))
    return out
def patch(s, x0, y0, rows, dy2=0, frames=(0,1)):
    """rows: strings; '?' keep, '.' transparent, hex digit = index"""
    for j,r in enumerate(rows):
        for i,ch in enumerate(r):
            if ch=='?': continue
            v=0 if ch=='.' else int(ch,16)
            for f in frames:
                s.set(f,x0+i,y0+j+(dy2 if f==1 else 0),v)
def openedges(a):
    """fill pixels (not outline idx) that touch transparency, per frame"""
    return None
