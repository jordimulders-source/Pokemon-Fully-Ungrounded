# Natief raster van ../gemini/model_kandidaat.png: pitch 10.24 (x,y), celgrens bij 9.77 (gemeten met pitch.py).
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../gemini/model_kandidaat.png').convert('RGB')).astype(int)
p=10.24; b=9.77
cs=np.arange(b-p+p/2,1024,p); cs=cs[cs>=2]
out=np.zeros((len(cs),len(cs),3),'uint8'); spread=np.zeros((len(cs),len(cs)))
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        blk=a[int(y-2):int(y+3),int(x-2):int(x+3)].reshape(-1,3)
        out[j,i]=np.median(blk,axis=0); spread[j,i]=blk.std(0).mean()
Image.fromarray(out).save('natief.png')
m=out.astype(int).min(2)<225; yy,xx=np.where(m)
print(out.shape,'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max(),'max spread',spread[m].max().round(1),'mean',spread[m].mean().round(2))
