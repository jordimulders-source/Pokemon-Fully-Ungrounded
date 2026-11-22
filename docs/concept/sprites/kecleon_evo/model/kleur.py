from PIL import Image; import numpy as np, colorsys
from scipy import ndimage as nd
a=np.asarray(Image.open('combi_kop.png').convert('RGB')).astype(int)
H,W,_=a.shape
L=np.zeros((H,W)); Hh=np.zeros((H,W)); cl=np.empty((H,W),object)
for y in range(H):
  for x in range(W):
    r,g,b=a[y,x]/255; h,l,s=colorsys.rgb_to_hls(r,g,b); h*=360; L[y,x]=l; Hh[y,x]=h
    if min(a[y,x])>225: c='wit'
    elif l<0.22: c='zwart'
    elif 65<=h<=160: c='groen'
    elif (h>=330 or h<20) and l>0.62: c='roze'
    elif h<38 or h>=330: c='rood'
    else: c='geel'
    cl[y,x]=c
geel=(cl=='geel'); lab,_=nd.label(geel); buik=lab==lab[58,30]
ORA=[(120,45,25),(190,80,40),(232,120,52),(250,165,80)]
GEE=[(150,105,35),(215,165,50),(245,210,85),(255,238,150)]
ROZ=[(170,70,95),(225,125,140),(250,180,185)]
reg=np.full((H,W),'',object)
for y in range(H):
  for x in range(W):
    c=cl[y,x]
    if c in('wit','zwart'): reg[y,x]=c; continue
    kop = y<46 and x<44
    if buik[y,x]: reg[y,x]='g'
    elif c=='roze' and kop: reg[y,x]='p'
    elif c=='groen': reg[y,x]='o' if (x>=44 and x<68) else 'g'
    elif x>=68 and y>=46: reg[y,x]='g'          # staart
    elif c=='geel' and (kop or y>=80): reg[y,x]='g'
    else: reg[y,x]='o'
Ls=L.copy()
for k in 'o':
  m=reg==k; t=np.where(m,L,np.nan)
  sm=ndimage_med=nd.generic_filter(t,np.nanmedian,size=3,mode='constant',cval=np.nan)
  Ls[m]=sm[m]
out=np.full((H,W,3),255,'uint8')
for y in range(H):
  for x in range(W):
    k=reg[y,x]
    if k=='wit': continue
    if k=='zwart': out[y,x]=(24,16,16); continue
    l=Ls[y,x]
    ramp={'o':ORA,'g':GEE,'p':ROZ}[k]
    if k=='p': i=0 if l<0.5 else (1 if l<0.72 else 2)
    else: i=0 if l<0.36 else (1 if l<0.52 else (2 if l<0.68 else 3))
    out[y,x]=ramp[i]
Image.fromarray(out).save('model_v1.png')
Image.fromarray(out).resize((W*8,H*8),Image.NEAREST).save('model_v1_8x.png')
