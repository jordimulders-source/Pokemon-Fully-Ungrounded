import re,os
from PIL import Image
R='/home/user/projectgrounded/'
G=R+'graphics/pokemon/'
def dex():
    d={}
    for l in open(R+'include/constants/species.h'):
        m=re.match(r'\s*SPECIES_(\w+) = (\d+),',l)
        if m and int(m.group(2))<=1025 and int(m.group(2))>0:
            d[int(m.group(2))]=m.group(1).lower()
    return d
def path(name,gba=True):
    for cand in [name, name.replace('_','/',1), name.split('_')[0], name.replace('_','')]:
        p=_path(cand,gba)
        if p: return p
def _path(name,gba=True):
    for f in (['anim_front_gba.png'] if gba else [])+['anim_front.png','front.png']:
        p=G+name+'/'+f
        if os.path.exists(p): return p
    return None
def load(name,gba=True,p=None):
    p=p or path(name,gba)
    if not p: return None
    im=Image.open(p)
    if im.mode=='P':
        a=im.convert('RGBA'); px=a.load(); idx=im.load()
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                if idx[x,y]==0: px[x,y]=(0,0,0,0)
        im=a
    else: im=im.convert('RGBA')
    return im.crop((0,0,64,64))
def metrics(im):
    px=im.load(); pts=[(x,y) for y in range(64) for x in range(64) if px[x,y][3]]
    if not pts: return None
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    w,h=x1-x0+1,y1-y0+1; A=len(pts)
    cx=sum(xs)/A; cy=sum(ys)/A
    # dark fraction of outline
    top=sum(1 for x,y in pts if y<y0+h/3)/A
    # facing: mass left of bbox mid in top third (head side)
    tp=[x for x,y in pts if y<y0+h*0.4]
    head=(sum(tp)/len(tp)-(x0+x1)/2)/w if tp else 0
    return dict(x0=x0,x1=x1,y0=y0,y1=y1,w=w,h=h,A=A,fill=A/(w*h),cx=(cx-(x0+x1)/2)/w,cy=(cy-y0)/h,top=top,head=head)
