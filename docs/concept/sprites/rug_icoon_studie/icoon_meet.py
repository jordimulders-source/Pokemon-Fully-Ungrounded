"""Icoon vs front (GBA, Gen 1-3): pose-overeenkomst en tekenstijl.
python3 icoon_meet.py uit.json"""
import os,sys,json,numpy as np
from PIL import Image
G='graphics/pokemon'
def rgbof(p,palfile=None):
    im=Image.open(p); ix=np.array(im)
    if palfile:
        L=open(palfile).read().split('\n'); P=np.array([[int(v) for v in L[3+k].split()[:3]] for k in range(16)])
    else:
        q=im.getpalette()[:48]; P=np.array(q).reshape(16,3)
    return ix,P
def mask_small(m,h,w):
    im=Image.fromarray((m*255).astype(np.uint8)).resize((w,h),Image.BOX); return np.array(im)>110
out=[]
for sp in sorted(os.listdir(G)):
    d=f'{G}/{sp}'
    if not os.path.exists(d+'/icon_gba.png') or not os.path.exists(d+'/anim_front_gba.png'): continue
    fi,FP=rgbof(d+'/anim_front_gba.png',d+'/normal_gba.pal'); fi=fi[:64]
    ii,IP=rgbof(d+'/icon_gba.png'); ii=ii[:32]
    fm=fi>0; im_=ii>0
    if not fm.any() or not im_.any(): continue
    ys,xs=np.nonzero(fm); fc=fm[ys.min():ys.max()+1,xs.min():xs.max()+1]
    ys2,xs2=np.nonzero(im_); ic=im_[ys2.min():ys2.max()+1,xs2.min():xs2.max()+1]
    h,w=ic.shape; s=mask_small(fc,h,w); sf=s[:,::-1]
    iou=lambda a,b:(a&b).sum()/max(1,(a|b).sum())
    r={'sp':sp,'iou':float(iou(s,ic)),'iou_flip':float(iou(sf,ic)),'fh':int(fc.shape[0]),'fw':int(fc.shape[1]),'ih':h,'iw':w,
       'aspect_f':fc.shape[1]/fc.shape[0],'aspect_i':w/h}
    # omlijning: randpixels van het icoon (buur transparant), helderheid boven- vs onderhelft
    pad=np.pad(im_,1); edge=im_&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    lum=IP[ii].mean(2)
    ey,ex=np.nonzero(edge); mid=(ys2.min()+ys2.max())/2
    r['edge_top']=float(lum[ey[ey<mid],ex[ey<mid]].mean()); r['edge_bot']=float(lum[ey[ey>=mid],ex[ey>=mid]].mean())
    r['edge_dark_frac']=float((lum[edge]<110).mean())
    r['ncol']=int(len(np.unique(ii))-1)
    # kopaandeel: bovenste 40% van de hoogte, oppervlak
    out.append(r)
json.dump(out,open(sys.argv[1],'w')); print(len(out))
