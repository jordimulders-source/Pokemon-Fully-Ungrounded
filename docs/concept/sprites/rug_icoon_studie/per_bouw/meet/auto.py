import json,numpy as np,ld
from PIL import Image
from soorten import BOUW
def bb(m):
    ys,xs=np.nonzero(m); return ys.min(),ys.max(),xs.min(),xs.max()
def crop(m): y0,y1,x0,x1=bb(m); return m[y0:y1+1,x0:x1+1]
def small(m,h,w): return np.array(Image.fromarray((m*255).astype(np.uint8)).resize((w,h),Image.BOX))>110
def iou(a,b): return (a&b).sum()/max(1,(a|b).sum())
def bestiou(fm,im):
    # front verkleind met gelijke schaal (hoogte) en gecentreerd; beste verschuiving +-2
    fc=crop(fm); ic=crop(im); h=ic.shape[0]; S=h/fc.shape[0]; w=max(1,round(fc.shape[1]*S))
    s=small(fc,h,w); best=0
    H=h+8; W=max(w,ic.shape[1])+8
    for flip in (0,1):
        ss=s[:,::-1] if flip else s
        for dx in range(-3,4):
            A=np.zeros((H,W),bool); B=np.zeros((H,W),bool)
            ox=(W-w)//2+dx; A[4:4+h,ox:ox+w]=ss
            ox2=(W-ic.shape[1])//2; B[4:4+h,ox2:ox2+ic.shape[1]]=ic
            v=iou(A,B)
            if flip==0: best=max(best,v)
            else: bf=v if dx==-3 else max(bf,v)
    return best,bf
def lum(a): return a[...,:3].astype(float)@[.3,.59,.11]
def edge(m):
    p=np.pad(m,1); return m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
def band(m,frac=.4):
    y0,y1,_,_=bb(m); cut=y0+(y1-y0+1)*frac; ys=np.nonzero(m)[0]; return float((ys<cut).mean())
out=[]
for b,L in BOUW.items():
    for s in L:
        F=ld.front(s); fm=F[...,3]>0
        for kind,I in (('gba',ld.icon_gba(s)),('nieuw',ld.icon_new(s))):
            im=I[...,3]>0; fy0,fy1,fx0,fx1=bb(fm); iy0,iy1,ix0,ix1=bb(im)
            fh,fw,ih,iw=fy1-fy0+1,fx1-fx0+1,iy1-iy0+1,ix1-ix0+1
            v,vf=bestiou(fm,im); e=edge(im); Li=lum(I); ey,ex=np.nonzero(e); mid=(iy0+iy1)/2
            ncol=len({tuple(c) for c in I[im][:,:3]}); nf=len({tuple(c) for c in F[fm][:,:3]})
            out.append(dict(bouw=b,sp=s,icon=kind,fh=fh,fw=fw,ih=ih,iw=iw,S=ih/fh,Sw=iw/fw,asp_f=fw/fh,asp_i=iw/ih,
              iou=v,iou_flip=vf,band_f=band(fm),band_i=band(im),fill_f=fm.sum()/(fh*fw),fill_i=im.sum()/(ih*iw),
              area_rel=im.sum()/(fm.sum()*(ih/fh)**2),
              ncol_f=nf,ncol_i=ncol,edge_dark=float((Li[e]<110).mean()),edge_top=float(Li[ey[ey<mid],ex[ey<mid]].mean()),
              edge_bot=float(Li[ey[ey>=mid],ex[ey>=mid]].mean()),bottom=int(iy1),cx=(ix0+ix1)/2))
json.dump(out,open('auto.json','w'),indent=0,default=float)
import collections
for kind in ('gba','nieuw'):
  print('==',kind)
  for b in BOUW:
    R=[r for r in out if r['bouw']==b and r['icon']==kind]
    def q(k): a=np.array([r[k] for r in R]); return '%.2f(%.2f-%.2f)'%(np.median(a),*np.percentile(a,[25,75]))
    print(b,len(R),'S',q('S'),'Sw',q('Sw'),'asp f',q('asp_f'),'i',q('asp_i'),'iou',q('iou'),'flip',q('iou_flip'),'band f',q('band_f'),'i',q('band_i'),'area',q('area_rel'),'ncol',q('ncol_i'),'edge',q('edge_dark'),q('edge_top'),q('edge_bot'),'bot',q('bottom'),'cx',q('cx'))
print()
for r in out:
  if r['icon']=='gba': print('%-10s %-10s fh%2d fw%2d ih%2d iw%2d S%.2f Sw%.2f iou%.2f fl%.2f band %.2f>%.2f area%.2f nc%d/%d'%(r['bouw'],r['sp'],r['fh'],r['fw'],r['ih'],r['iw'],r['S'],r['Sw'],r['iou'],r['iou_flip'],r['band_f'],r['band_i'],r['area_rel'],r['ncol_i'],r['ncol_f']))
