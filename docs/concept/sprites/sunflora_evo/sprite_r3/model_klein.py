# model_16 verkleind op exact het spriteraster (vlakgemiddelde per spritepixel), voor het vel.
import json, numpy as np; from PIL import Image
T=json.load(open('transform.json')); f=T['f']
a=np.asarray(Image.open('../gemini/model_16.png').convert('RGB')).astype(float)
mx=lambda sx: (4.1+4.267*(75+1.5*(sx-4)))*f+T['ox']; my=lambda sy: (4.4+4.267*(8+1.5*(sy-1)))*f+T['oy']
o=np.full((64,64,3),255,'uint8')
for j in range(64):
    for i in range(64):
        y0,y1,x0,x1=[int(round(v)) for v in (my(j),my(j+1),mx(i),mx(i+1))]
        y0,x0=max(y0,0),max(x0,0)
        if x1<=0 or y1<=0: continue
        b=a[y0:y1,x0:x1]
        if b.size: o[j,i]=b.reshape(-1,3).mean(0)
Image.fromarray(o).save('model16_64.png'); Image.fromarray(o).resize((512,512),Image.NEAREST).save('model16_64_8x.png')
