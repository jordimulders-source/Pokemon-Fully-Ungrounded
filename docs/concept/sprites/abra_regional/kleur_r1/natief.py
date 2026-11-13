# Haalt het eigen pixelraster van het Gemini-model terug -> natief.png
# Gemeten met pitch.py: pitch 8,00 px op beide assen, rastergrens na kolom/rij 6,75 (+8k).
# Elke natieve pixel = mediaan van het middelste 4x4-blok van zijn 8x8-cel.
import sys; from PIL import Image; import numpy as np
IN=sys.argv[1] if len(sys.argv)>1 else '../referenties/gemini_gekozen.png'; OUT=sys.argv[2] if len(sys.argv)>2 else 'natief.png'
P=8.0; PH=6.75+1   # eerste celgrens (pixelindex waar een nieuwe cel begint)
a=np.asarray(Image.open(IN).convert('RGB')).astype(int)
st=PH-P*np.floor(PH/P)
cx=np.arange(st+P/2,1024,P); cy=np.arange(st+P/2,1024,P)
out=np.zeros((len(cy),len(cx),3),'uint8')
for j,y in enumerate(cy):
    for i,x in enumerate(cx):
        y0,y1=int(round(y-2)),int(round(y+2)); x0,x1=int(round(x-2)),int(round(x+2))
        out[j,i]=np.median(a[max(0,y0):y1,max(0,x0):x1].reshape(-1,3),axis=0)
im=Image.fromarray(out); im.save(OUT)
g=np.asarray(im).min(axis=2); yy,xx=np.where(g<215)
print('natief',im.size,'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max(),'=> %dx%d'%(xx.max()-xx.min()+1,yy.max()-yy.min()+1))
