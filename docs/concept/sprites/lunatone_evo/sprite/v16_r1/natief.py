# Natief Gemini-raster (16 px, fase 15) terughalen: per cel mediaan van het midden (10x10).
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../referenties/model_v16.png').convert('RGB')).astype(float)
N=np.zeros((64,64,3)); bgc=np.zeros((64,64),bool); spread=np.zeros((64,64))
for j in range(64):
  for i in range(64):
    y0=16*j-1+3; x0=16*i-1+3
    b=a[max(y0,0):y0+10, max(x0,0):x0+10].reshape(-1,3)
    N[j,i]=np.median(b,0); spread[j,i]=b.std(0).mean()
    bgc[j,i]=N[j,i].min()>225
np.save('natief.npy',N); np.save('natief_bg.npy',bgc)
ys,xs=np.where(~bgc); print('bbox',xs.min(),xs.max(),ys.min(),ys.max(),'spread>20:',(spread>20).sum())
im=Image.fromarray(N.astype('uint8')); im.save('natief.png'); im.resize((512,512),Image.NEAREST).save('natief_8x.png')
