# Kale reductie van het model naar 64x64 (niets getekend).
# Per spritepixel (blok van S modelpixels): dekking = aandeel niet-wit; zwart wint bij >= ZW aandeel
# (dunne barsten/omlijning blijven, ijskomeet-les); anders gemiddelde van de niet-zwarte pixels
# -> dichtstbijzijnde paletkleur (iris alleen binnen de oogschijf).
# Uit: kaal.npy (indices), kaal.png, zones.npy
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../referenties/model.png').convert('RGB')).astype(float)
r,g,b=a[...,0],a[...,1],a[...,2]; lum=a.mean(2)
H=1024; Y,X=np.mgrid[0:H,0:H]
bg=a.min(2)>235
blk=(lum<40)&~bg
EC=(525,505); eyed=np.hypot(X-EC[0],Y-EC[1])<112
iris=(r>150)&(r-g>100)&eyed
PAL=np.array([
 (0,0,0),        #0 transparant
 (24,16,16),     #1 zwart (omlijning/barst/pupil)
 (72,28,32),     #2 steen 5 diepste / selout
 (104,40,36),    #3 steen 4
 (136,52,44),    #4 steen 3
 (172,72,58),    #5 steen 2 (midden)
 (204,108,92),   #6 steen 1
 (228,148,128),  #7 hooglicht
 (160,20,24),    #8 iris donker
 (216,44,40),    #9 iris
 (248,112,96),   #10 iris licht
],float)
STEEN=[2,3,4,5,6,7]; IRIS=[8,9,10]
S=13.0; X0=63-(64*S-808)/2; Y0=194-(64*S-697)/2
def near(c,ids): return ids[int(np.argmin([((PAL[i]-c)**2).sum() for i in ids]))]
out=np.zeros((64,64),int); zone=np.zeros((64,64),int)
ZW=0.34
for j in range(64):
  for i in range(64):
    ys=slice(int(round(Y0+j*S)),int(round(Y0+(j+1)*S))); xs=slice(int(round(X0+i*S)),int(round(X0+(i+1)*S)))
    if ys.start<0 or xs.start<0 or ys.stop>H or xs.stop>H: continue
    B=bg[ys,xs]; fig=1-B.mean()
    if fig<0.5: continue
    F=~B
    if blk[ys,xs][F].mean()>=ZW: out[j,i]=1; continue
    I=iris[ys,xs]
    if I.sum()>=0.4*F.sum(): out[j,i]=near(a[ys,xs][I].mean(0),IRIS); continue
    m=F&~blk[ys,xs]&~I
    out[j,i]=near(a[ys,xs][m].mean(0),STEEN)
np.save('kaal.npy',out)
def save(o,fn,sc=1):
  im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL.ravel()]; im.putpalette(p+[0]*(768-len(p)))
  if sc>1: im=im.resize((64*sc,64*sc),Image.NEAREST)
  im.save(fn,transparency=0)
save(out,'kaal.png'); save(out,'kaal_8x.png',8)
ys,xs=np.where(out>0); print('bbox',xs.min(),xs.max(),ys.min(),ys.max())
