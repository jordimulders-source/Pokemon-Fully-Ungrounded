# natief.py: haalt het eigen pixelraster van het r4-model terug. Pitch gemeten met randsterkte: 8,53 en 4,27 scoren
# bijna gelijk -> echte cel = 4,267 px (1024/240), fase x-rand 353,6, y-rand 64,1. -> natief.png (celmediaan 3x3)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../referenties/gemini_gekozen_r4.png').convert('RGB')).astype(int)
P=1024/240; BX=353.6; BY=64.1
x0=BX-P*int(BX/P); y0=BY-P*int(BY/P)
xs=np.arange(x0+P/2,1024-1,P); ys=np.arange(y0+P/2,559-1,P)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        Y,X=int(round(y)),int(round(x))
        out[j,i]=np.median(a[max(0,Y-1):Y+2,max(0,X-1):X+2].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png')
m=out.min(2)<215; yy,xx=np.where(m); print('natief',out.shape,'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max())
print('celrand x0 %.3f y0 %.3f'%(x0,y0))
