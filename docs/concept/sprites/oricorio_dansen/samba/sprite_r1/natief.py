# Natief raster van gemini_r6 terughalen: pitch 1024/240 (gemeten met randsterkte, x en y), fase per as gemeten -> natief.png
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../model/gemini_r6.png').convert('RGB')).astype(float)
P=1024/240
def fase(g):
    pos=np.arange(len(g))+1.0; z=(g*np.exp(2j*np.pi*pos/P)).sum(); return (np.angle(z)/(2*np.pi)*P)%P
gx=np.abs(np.diff(a,axis=1)).sum(2).sum(0); gy=np.abs(np.diff(a,axis=0)).sum(2).sum(1)
fx,fy=fase(gx),fase(gy); print('fase x %.2f y %.2f'%(fx,fy))
cx=np.arange(fx+P/2,a.shape[1]-1,P); cy=np.arange(fy+P/2,a.shape[0]-1,P)
out=np.zeros((len(cy),len(cx),3),'uint8')
for j,y in enumerate(cy):
    for i,x in enumerate(cx):
        y0,y1=int(round(y-1)),int(round(y+1))+1; x0,x1=int(round(x-1)),int(round(x+1))+1
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png'); print(out.shape)
Image.fromarray(out).resize((out.shape[1]*4,out.shape[0]*4),Image.NEAREST).save('natief_4x.png')
