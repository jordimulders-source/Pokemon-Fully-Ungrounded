# Natief pixelraster van het Gemini-model terughalen (pitch 5.12, celgrenzen op 0 gemeten met randsterkte) -> natief.png (200x200)
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../../gemini/r9_prompt_v6.png').convert('RGB')).astype(int)
p=5.12; ph=0.0
xs=np.arange(ph+p/2,1024,p); n=len(xs)
out=np.zeros((n,n,3),'uint8')
for j,y in enumerate(xs):
    for i,x in enumerate(xs):
        y0,y1=int(y-1),int(y+2); x0,x1=int(x-1),int(x+2)
        out[j,i]=np.median(a[max(0,y0):y1,max(0,x0):x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png'); print(n)
Image.fromarray(out).resize((n*5,n*5),0).save('_tmp/natief5x.png')
