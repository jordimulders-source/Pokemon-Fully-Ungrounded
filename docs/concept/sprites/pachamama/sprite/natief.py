# Haalt het eigen pixelraster van het Gemini-model terug (pitch 5.12 px, 200x200) -> natief.png
# (naar octillery_evo/sprite3/natief.py; pitch gemeten met randsterkte: 10.24/15.36 = veelvouden van 5.12)
import sys; from PIL import Image; import numpy as np
IN=sys.argv[1] if len(sys.argv)>1 else '../referenties/gemini_gekozen_r4c.png'; OUT=sys.argv[2] if len(sys.argv)>2 else 'natief.png'
a=np.asarray(Image.open(IN).convert('RGB')).astype(int)
g=np.abs(np.diff(a,axis=1)).sum(2).sum(0).astype(float)
best=max(((g[np.round(np.arange(ph,1022,5.12)).astype(int)].mean(),ph) for ph in np.arange(0,5.12,0.25)))
ph=best[1]; print('fase',ph)
p=5.12; xs=np.arange(ph+p/2,1024,p); ys=xs.copy()
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-1)),int(min(1024,y+2)); x0,x1=int(max(0,x-1)),int(min(1024,x+2))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT); print(out.shape)
