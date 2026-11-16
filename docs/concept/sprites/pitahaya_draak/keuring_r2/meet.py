import sys; sys.path.insert(0,'sprite_r1')
from PIL import Image; import numpy as np
from groepen import laad
a,lum,g=laad('sprite_r2/natief.png')
sp=Image.open('sprite_r2/pitahaya_r2.png'); S=np.array(sp); P=np.array(sp.getpalette()[:48]).reshape(16,3)
L=(P*[0.299,0.587,0.114]).sum(1)
def blok(x,y):
    r=3*(y+2); c=1+3*(x+1); return (slice(r,r+3),slice(c,c+3))
mean=np.zeros((64,64,3)); mlum=np.zeros((64,64)); mzw=np.zeros((64,64),int); mg=np.zeros((64,64),int)
for y in range(64):
  for x in range(64):
    sl=blok(x,y)
    if sl[0].stop>199 or sl[1].stop>199: continue
    gb=g[sl]; m=gb!=0
    if m.sum()==0: continue
    mean[y,x]=a[sl][m].mean(0); mlum[y,x]=lum[sl][m].mean(); mzw[y,x]=(gb==1).sum()
    vals,cn=np.unique(gb[m],return_counts=True); mg[y,x]=vals[cn.argmax()]
np.savez('keuring_r2/model_per_px.npz',mean=mean,mlum=mlum,mzw=mzw,mg=mg)
# image: model block mean at 8x beside sprite
im=Image.fromarray(mean.astype('uint8')); 
spr=sp.convert('RGB')
W=Image.new('RGB',(34*8*2+16,52*8),(200,200,200))
W.paste(spr.crop((14,5,48,57)).resize((34*8,52*8),Image.NEAREST),(0,0))
W.paste(im.crop((14,5,48,57)).resize((34*8,52*8),Image.NEAREST),(34*8+16,0))
W.save('keuring_r2/sprite_vs_blokgem.png')
print('groups', np.unique(g))
