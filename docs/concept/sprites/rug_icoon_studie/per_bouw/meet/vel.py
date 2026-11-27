import sys,numpy as np,ld
from PIL import Image,ImageDraw
from soorten import BOUW
import os; OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')+'/'
def crop(a):
    ys,xs=np.nonzero(a[...,3]); return a[ys.min():ys.max()+1,xs.min():xs.max()+1]
def small(a,h):
    c=crop(a); w=max(1,round(c.shape[1]*h/c.shape[0]))
    # premultiplied BOX, dan alfa drempel
    rgb=c[...,:3].astype(float)*(c[...,3:]>0); al=(c[...,3]>0).astype(float)
    R=np.stack([np.array(Image.fromarray(rgb[...,k]).resize((w,h),Image.BOX)) for k in range(3)],-1)
    A=np.array(Image.fromarray(al).resize((w,h),Image.BOX))
    o=np.zeros((h,w,4),np.uint8); m=A>0.45; o[m,:3]=(R[m]/A[m,None]).clip(0,255); o[m,3]=255; return o
Z=4; BG=(150,210,180)
for b,L in BOUW.items():
    rows=[]
    for s in L:
        F=crop(ld.front(s)); G=crop(ld.icon_gba(s)); N=crop(ld.icon_new(s)); V=small(ld.front(s),G.shape[0])
        cols=[('front',F),('front verkleind',V),('icoon Gen 3',G),('icoon nu (icon.png)',N)]
        W=sum(c.shape[1]*Z+16 for _,c in cols)+90; Hh=max(c.shape[0] for _,c in cols)*Z+18
        r=Image.new('RGB',(W,Hh),BG); d=ImageDraw.Draw(r); d.text((4,4),s,fill=(0,0,0)); x=90
        for nm,c in cols:
            im=Image.fromarray(c).resize((c.shape[1]*Z,c.shape[0]*Z),Image.NEAREST)
            r.paste(im,(x,Hh-c.shape[0]*Z-2),im); d.text((x,2),nm,fill=(60,60,60)); x+=c.shape[1]*Z+16
        rows.append(r)
    W=max(r.width for r in rows); o=Image.new('RGB',(W,sum(r.height+6 for r in rows)),(255,255,255)); y=0
    for r in rows: o.paste(r,(0,y)); y+=r.height+6
    o.save(OUT+b+'.png'); print(b,o.size)
