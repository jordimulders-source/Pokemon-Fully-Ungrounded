import sys,numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
v8=Image.open(R+'icoon/maker/icon_v8.png'); V=np.array(v8)
G=open(sys.argv[1]).read().split('\n')
G=[g for g in G if g and g[0] in '0123456789' and ':' in g]
f1=np.zeros((32,32),np.uint8)
for g in G:
    y,s=g.split(':',1); y=int(y); s=s.strip()
    for x,c in enumerate(s):
        if c!='.': f1[y,x]=int(c,16)
# tail masks
def tm(rows):
    m=np.zeros((32,32),bool)
    for (a,b),x0 in rows:
        for y in range(a,b+1): m[y,x0:]=True
    return m
T1=tm([((9,15),21),((16,16),24),((17,19),25),((20,21),24),((22,23),25)])
T2=tm([((10,16),20),((17,17),24),((18,20),25),((21,22),24),((23,23),25)])
f1[T1]=V[:32][T1]
nt=f1.copy(); nt[T1]=0
# frame 2: body 1 px down except feet rows >= 27 ; drop row 26
f2=np.zeros_like(f1)
f2[1:24]=nt[0:23]; f2[24:]=nt[24:]
f2[T2]=V[32:][T2]
f2[(~T2)&T1]=0 if False else f2[(~T2)&T1]
out=np.vstack([f1,f2])
im=Image.fromarray(out,'P'); im.putpalette(v8.getpalette()); im.info['transparency']=0
im.save(sys.argv[2],transparency=0)
im.resize((256,512),Image.NEAREST).save(sys.argv[2].replace('.png','_8x.png'))
