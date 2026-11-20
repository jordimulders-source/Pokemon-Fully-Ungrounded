# Model: r4-lijf + voorpoten van r3 (Jordi: "dit is je referentie voor de voorpoten, maar ook voor de grootte
# van de achterpoten") + achterpoten van r12 (telgang), per rij verbreed tot de breedte van de r3-achterpoten (±60 px).
from PIL import Image; import numpy as np
P=np.array(Image.open('poten/r4_poten_r12.png').convert('RGB')).astype(int)
R=np.array(Image.open('r3/r3_prompt_v3.png').convert('RGB')).astype(int)
O=P.copy(); white=lambda p: p.sum()>=700
# voorpoten: r3 vanaf y 765 (x 195-500)
O[815:,195:500]=255
for y in range(815,1024):
    for x in range(195,500):
        if not white(R[y,x]): O[y,x]=R[y,x]
# achterpoten verbreden
DOEL=60
for y in range(836,1024):
    row=P[y,500:960]; runs=[];s=None
    for i in range(len(row)):
        v=not white(row[i])
        if v and s is None: s=i
        if (not v or i==len(row)-1) and s is not None: runs.append((s+500,i+500)); s=None
    for x0,x1 in runs:
        w=x1-x0
        if w<4: continue
        f=max(1.0,DOEL/w); c=(x0+x1)/2; h=w*f/2
        seg=P[y,x0:x1].copy()
        O[y,x0:x1]=255
        for X in range(int(c-h),int(c+h)+1):
            src=int(round(c+(X-c)/f)); src=min(max(src,x0),x1-1)
            if 0<=X<1024: O[y,X]=P[y,src]
Image.fromarray(O.astype('uint8')).save('poten/model_v3.png')
Image.fromarray(O.astype('uint8')).resize((512,512)).save('poten/klein.png')
