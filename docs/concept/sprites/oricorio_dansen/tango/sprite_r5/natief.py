# Natief (micro)raster van gemini_r7 terughalen: pitch 4,2667 (=1024/240) in x en y, randfase x 3,74 / y 3,78 (gemeten met randsterkte, zie log).
# Gemini-kunstpixels zijn ±2 microcellen (8,53 px) maar randen vallen op elke microgrens; daarom het microraster als natief.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../model/gemini_r7.png').convert('RGB')).astype(int)
P=1024/240; FX,FY=3.74,3.78
cx=np.arange(FX+P/2,a.shape[1],P); cy=np.arange(FY+P/2,a.shape[0],P)
out=np.zeros((len(cy),len(cx),3),'uint8')
for j,y in enumerate(cy):
    for i,x in enumerate(cx):
        y0,y1=int(round(y-1)),int(round(y+2)); x0,x1=int(round(x-1)),int(round(x+2))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png'); print(out.shape)
