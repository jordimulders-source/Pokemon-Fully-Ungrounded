# r2 punt 1: kap = berg. Per kappixel (creme/sneeuwtinten 5,6,10,13 boven de schouders, buiten het gezicht) opnieuw gemeten
# op het model: koel (blauw > rood) = sneeuw (licht -> 10 wit, anders 6 blauwgrijs), warm = kap (licht -> 5 creme, anders 13).
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
a=np.asarray(Image.open('../natief_g1.png').convert('RGB')).astype(float); L=lum(a)
MY,MX=np.load('basis_map.npy'); o=np.load(sys.argv[1]); z=np.load('gezzone.npy'); oud=o.copy(); log={}
for y in range(8,27):
  for x in range(64):
    if o[y,x] not in (5,6,10,13) or z[y,x]: continue
    b=(slice(MY+3*y,MY+3*y+3),slice(MX+3*x,MX+3*x+3)); px=a[b].reshape(-1,3); l=L[b].ravel(); px=px[l>=120]; l=l[l>=120]
    if len(px)<3: continue
    koel=(px[:,2]>px[:,0]+3).mean()
    if koel>=0.5: v=10 if np.median(l[px[:,2]>px[:,0]+3])>=232 else 6
    else: v=5 if np.median(l)>=215 else 13
    if v!=o[y,x]: log[(o[y,x],v)]=log.get((o[y,x],v),0)+1; o[y,x]=v
# r2 punt 2: sneeuwtopjes op armen en mantelpieken: cel met >= 4 sneeuwpixels in het model -> sneeuw (wit/blauwgrijs gemeten)
bg=np.load('basis_bg.npy'); sn=(a.min(2)>=200)&(a[...,2]>=a[...,0]-3)&~bg
for y in range(27,64):
  for x in range(64):
    if o[y,x] in (0,1) or z[y,x]: continue
    b=(slice(MY+3*y,MY+3*y+3),slice(MX+3*x,MX+3*x+3))
    if sn[b].sum()>=4:
      v=10 if np.median(L[b][sn[b]])>=232 else 6
      if v!=o[y,x]: log[('sneeuwtop',int(o[y,x]),v)]=log.get(('sneeuwtop',int(o[y,x]),v),0)+1; o[y,x]=v
np.save(sys.argv[2],o); print(log,(o!=oud).sum())
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48)); im.save(sys.argv[2].replace('.npy','.png'),transparency=0)
