# v4: middelvinger met gladde randen (links en rechts monotoon) en een vloeiende aansluiting op de handpalm (geen inkeping rechts)
from PIL import Image
import numpy as np
a=np.asarray(Image.open('model/model_hand3_v3.png').convert('RGB')).copy()
P=7.3; I0=108
COL={'W':(255,255,255),'.':(255,255,255),'o':(13,12,18),'d':(85,83,102),'b':(170,167,181),'c':(139,136,156)}
L={40:19,41:18,42:17,43:17,44:16,45:15,46:15,47:14,48:13,49:13,50:12,51:11,52:11,53:11,54:11}
R={40:20,41:20,42:20,43:20,44:19,45:19,46:19,47:19,48:18,49:18,50:18,51:18,52:18,53:18,54:19}
START={40:11,41:11,42:11,43:11,44:11,45:11,46:11,47:11,48:11,49:11,50:11,51:11,52:11,53:11,54:11}
for r in range(39,55):
    s={}
    if r==39:
        for p in range(11,24): s[p]='.'
        s[19]='o'; s[20]='o'
    else:
        l,rr=L[r],R[r]
        for p in range(11,24): s[p]='.'
        for p in range(l,rr+1):
            if r<=41: ch='W'
            elif r>=51: ch='d' if p==rr else ('b' if p<=l+1 and r==51 else 'c')
            else: ch='b' if p<=l+(rr-l)//3 else 'c'
            s[p]=ch
        if r<=50: s[l-1]='o'
        s[rr+1]='o'
    for p,ch in s.items():
        i=I0+p; x0,y0,x1,y1=int(round(i*P)),int(round(r*P)),int(round((i+1)*P)),int(round((r+1)*P)); a[y0:y1,x0:x1]=COL[ch]
out=Image.fromarray(a); out.save('model/model_hand3_v4.png')
out.crop((700,230,1024,520)).resize((648,580),Image.NEAREST).save('model/hand_v4_closeup.png')
