"""Gedeelde lader: front frame 1 (64x64) en icoon frame 1 (32x32) van de in-game set, als RGBA-array.
python3 laad.py soort [f|i]  -> tekstraster (lichtheid: @ zeer donker, # donker, % , +, =, - licht, : wit; . = leeg)"""
import os,re,sys,numpy as np
from PIL import Image
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../../..'))
def pal(p):
    L=open(p).read().split('\n'); n=int(L[2]); return [tuple(int(v) for v in L[3+k].split()[:3]) for k in range(n)]+[(0,0,0)]*(16-n)
_IPI=None
def ipi(sp):
    global _IPI
    if _IPI is None:
        _IPI={}; d=ROOT+'/src/data/pokemon/species_info/'
        for fn in os.listdir(d):
            for mm in re.finditer(r'\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},',open(d+fn).read(),re.S):
                v=re.search(r'iconPalIndex = (?:P_GBA_STYLE_SPECIES_ICONS \? \d : )?(\d)',mm.group(2))
                if v: _IPI[mm.group(1).lower()]=int(v.group(1))
    return _IPI.get(sp,0)
def rgba(ix,P):
    o=np.zeros(ix.shape+(4,),np.uint8)
    for k in range(1,16): o[ix==k]=P[k]+(255,)
    return o
def front(sp,path=None,palp=None):
    D=ROOT+'/graphics/pokemon/'+sp
    if path is None: path=D+'/anim_front.png' if os.path.exists(D+'/anim_front.png') else D+'/front.png'
    im=Image.open(path)
    if palp is None and im.mode=='P' and not os.path.exists(D+'/normal.pal'):
        q=im.getpalette()[:48]; P=[tuple(q[3*k:3*k+3]) for k in range(16)]
    else: P=pal(palp or D+'/normal.pal')
    return rgba(np.array(im)[:64,:64],P)
def icoon(sp,path=None):
    D=ROOT+'/graphics/pokemon/'+sp; im=Image.open(path or D+'/icon.png')
    return rgba(np.array(im)[:32,:32],pal(ROOT+'/graphics/pokemon/icon_palettes/pal%d.pal'%ipi(sp)))
def raster(a):
    L=a[...,:3].astype(float)@[.3,.59,.11]; ch='@#%+=-:'
    ys,xs=np.nonzero(a[...,3]); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    out=['    '+''.join(str(x//10%10) if x%10==0 else ' ' for x in range(x0,x1+1)),'    '+''.join(str(x%10) for x in range(x0,x1+1))]
    for y in range(y0,y1+1):
        out.append('%3d '%y+''.join('.' if a[y,x,3]==0 else ch[min(6,int(L[y,x]/37))] for x in range(x0,x1+1)))
    return '\n'.join(out)
if __name__=='__main__':
    sp=sys.argv[1]; w=sys.argv[2] if len(sys.argv)>2 else 'fi'
    if 'f' in w: print(raster(front(sp)))
    if 'i' in w: print(raster(icoon(sp)))
def hexraster(sp,wat='i'):
    from PIL import Image as I
    D=ROOT+'/graphics/pokemon/'+sp
    if wat=='i': ix=np.array(I.open(D+'/icon.png'))[:32,:32]
    else:
        p=D+'/anim_front.png' if os.path.exists(D+'/anim_front.png') else D+'/front.png'; ix=np.array(I.open(p))[:64,:64]
    ys,xs=np.nonzero(ix); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    out=['    '+''.join(str(x//10%10) if x%10==0 else ' ' for x in range(x0,x1+1)),'    '+''.join(str(x%10) for x in range(x0,x1+1))]
    for y in range(y0,y1+1): out.append('%3d '%y+''.join('.' if ix[y,x]==0 else '%x'%ix[y,x] for x in range(x0,x1+1)))
    return '\n'.join(out)
