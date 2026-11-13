# v3: middelvinger als rechte, taps toelopende vinger (as schuin omhoog), op model_hand3_v2
from PIL import Image
import numpy as np
im=Image.open('model/model_hand3_v2.png').convert('RGB'); a=np.asarray(im).copy()
P=7.3; I0=108
COL={'W':(255,255,255),'.':(255,255,255),'o':(13,12,18),'d':(85,83,102),'b':(170,167,181),'c':(139,136,156),'w':(225,224,232)}
rows={}
for r in range(40,51):
    c=19.5-0.5*(r-40); hw=0.7+0.2*(r-40)
    L=int(round(c-hw)); R=int(round(c+hw))
    s=['.']*23
    for p in range(L,R+1):
        if r<=41: ch='W'
        else: ch='b' if p<=L+(R-L)//3 else 'c'
        s[p]=ch
    s[L-1]='o'; s[R+1]='o'
    rows[r]=''.join(s)
rows[39]='.'*19+'ooo'+'.'
rows[38]='.'*23
for r in sorted(rows): print(r,rows[r])
for r,row in rows.items():
    for p,ch in enumerate(row):
        if p<9: continue
        i=I0+p; x0,y0,x1,y1=int(round(i*P)),int(round(r*P)),int(round((i+1)*P)),int(round((r+1)*P)); a[y0:y1,x0:x1]=COL[ch]
    a[int(round(r*P)):int(round((r+1)*P)), int(round((I0+23)*P)):]=(255,255,255)
out=Image.fromarray(a); out.save('model/model_hand3_v3.png')
out.crop((700,230,1024,520)).resize((648,580),Image.NEAREST).save('model/hand_v3_closeup.png')
