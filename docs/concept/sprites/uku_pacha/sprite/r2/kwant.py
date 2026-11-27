# Uku Pacha r2 stap 1: natief raster (100x100) kwantiseren naar vaste modeltinten.
# Uitvoer: nat_idx.npy (per natieve cel een klasse), nat_pal.npy, kwant_8x.png (met legenda).
import numpy as np; from PIL import Image, ImageDraw
N=np.asarray(Image.open('../../model/r2_natief.png').convert('RGB')).astype(float)
wit=N.min(2)>235
bg=np.zeros_like(wit); st=[(0,0)]
while st:
    y,x=st.pop()
    if 0<=y<100 and 0<=x<100 and wit[y,x] and not bg[y,x]:
        bg[y,x]=True; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
np.save('nat_bg.npy',bg)
fg=N[~bg]
# k-means
K=16; rng=np.random.default_rng(1)
C=fg[rng.choice(len(fg),K,replace=False)]
for it in range(60):
    d=((fg[:,None]-C[None])**2).sum(-1); a=d.argmin(1)
    C=np.array([fg[a==k].mean(0) if (a==k).any() else C[k] for k in range(K)])
order=np.argsort(C.sum(1)); C=C[order]
d=((N[...,None,:]-C[None,None])**2).sum(-1); idx=d.argmin(-1); idx[bg]=-1
np.save('nat_idx.npy',idx); np.save('nat_pal.npy',C)
for k,c in enumerate(C): print(k,c.round(),(idx==k).sum())
im=Image.new('RGB',(800+200,800),'white'); px=im.load()
for y in range(100):
  for x in range(100):
    c=(255,255,255) if idx[y,x]<0 else tuple(int(v) for v in C[idx[y,x]])
    for dy in range(8):
      for dx in range(8): px[x*8+dx,y*8+dy]=c
dr=ImageDraw.Draw(im)
for k,c in enumerate(C):
    dr.rectangle([810,10+k*40,850,40+k*40],fill=tuple(int(v) for v in c)); dr.text((860,20+k*40),str(k),fill='black')
im.save('kwant_8x.png')
