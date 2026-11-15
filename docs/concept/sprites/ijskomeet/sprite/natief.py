# Natief raster van het Gemini-model terughalen: pitch 5.12 (FFT), fase via randsterkte.
import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB')).astype(float)
p=5.12
dx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0)  # rand tussen kolom i en i+1
dy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1)
def fase(d):
    best=None
    for ph in np.arange(0,p,0.08):
        pos=np.arange(ph,len(d),p); s=d[np.clip(np.round(pos).astype(int),0,len(d)-1)].sum()
        if best is None or s>best[0]: best=(s,ph)
    return best[1]
fx,fy=fase(dx),fase(dy); print('fase',fx,fy)
# cel-middens: rand ligt na kolom round(ph); midden = ph+0.5+p/2
cx=np.arange(fx+0.5+p/2-p, 1024, p); cx=cx[(cx>=1)&(cx<1023)]
cy=np.arange(fy+0.5+p/2-p, 1024, p); cy=cy[(cy>=1)&(cy<1023)]
out=np.zeros((len(cy),len(cx),3),'uint8')
for j,y in enumerate(cy):
    for i,x in enumerate(cx):
        y0,y1=int(round(y-1.5)),int(round(y+1.5)); x0,x1=int(round(x-1.5)),int(round(x+1.5))
        out[j,i]=np.median(a[y0:y1+1,x0:x1+1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png')
Image.fromarray(out).resize((out.shape[1]*4,out.shape[0]*4),Image.NEAREST).save('natief_x4.png')
np.save('natief_cx.npy',cx); np.save('natief_cy.npy',cy)
print(out.shape)
