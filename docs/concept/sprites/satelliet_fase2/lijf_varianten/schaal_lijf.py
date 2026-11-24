# Lijf (bol + antennes + oog) vergroten t.o.v. de panelen; panelen blijven pixel voor pixel model.png.
import sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from scipy import ndimage
from scipy.spatial import ConvexHull
im=Image.open('model.png').convert('RGB'); a=np.array(im).astype(int)
r,g,b=a[...,0],a[...,1],a[...,2]; L=a.mean(2)
cells=(L>45)&(L<130)&(b>r+25)&(b>g+25)
lab,n=ndimage.label(cells); cen=ndimage.center_of_mass(cells,lab,range(1,n+1)); sz=ndimage.sum(cells,lab,range(1,n+1))
grp={'L':[],'R':[]}
for i,(c,s) in enumerate(zip(cen,sz)):
  if s<1500: continue
  if c[1]<300: grp['L'].append(i+1)
  elif c[1]>520: grp['R'].append(i+1)
masks={}
for k,ids in grp.items():
  ys,xs=np.where(np.isin(lab,ids)); pts=np.c_[xs,ys]; h=ConvexHull(pts)
  m=Image.new('L',im.size,0); ImageDraw.Draw(m).polygon([tuple(map(int,pts[v])) for v in h.vertices],fill=255)
  masks[k]=m.filter(ImageFilter.MaxFilter(13))
white=(L>245)
fig=Image.fromarray(((~white)*255).astype('uint8'))
both=np.maximum(np.array(masks['L']),np.array(masks['R']))
bm0=(np.array(fig)>0)&(both==0)
lb,nb=ndimage.label(bm0); ss=ndimage.sum(bm0,lb,range(1,nb+1))
bm0=lb==(int(np.argmax(ss))+1)
body=Image.fromarray(bm0.astype('uint8')*255)
# lichaamsmidden = midden van het oog/koepel
cx,cy=380,470
out=[]
for f in [float(x) for x in sys.argv[1:]]:
  canvas=Image.new('RGB',im.size,'white')
  canvas.paste(im,(0,0),masks['L'])          # ver paneel achter
  n=int(1024*f); big=im.resize((n,n),Image.NEAREST); bm=body.resize((n,n),Image.NEAREST)
  ox,oy=int(cx-cx*f),int(cy-cy*f)
  canvas.paste(big,(ox,oy),bm)               # lijf
  canvas.paste(im,(0,0),masks['R'])          # nabij paneel voor
  canvas.save(f'lijf_varianten/lijf_{round(f*100)}.png'); out.append(canvas)
