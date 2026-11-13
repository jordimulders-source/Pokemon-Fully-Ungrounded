# Onderlaag: natief Gemini-raster (hybride_v1) -> <=15 kleuren, seeds per kleurgroep, k-means. Geen tekenwerk.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('sprite/hybride_v1.png').convert('RGB')).astype(float)
fg=np.load('sprite/fg_mask.npy')
seeds=np.array([(16,16,22),(96,128,144),(144,176,190),(178,198,214),(208,224,232),
 (218,232,238),(236,242,246),(250,251,252),(112,54,62),(160,92,96),(205,184,150),(170,150,130),(115,118,130)],float)
X=a[fg]
for it in range(10):
    d=((X[:,None,:]-seeds[None])**2).sum(2); lab=d.argmin(1)
    for k in range(len(seeds)):
        if (lab==k).any(): seeds[k]=X[lab==k].mean(0)
out=np.zeros((64,64),np.uint8); out[fg]=lab+1
P=[(152,208,160)]+[tuple(int(v) for v in c) for c in seeds]
im=Image.new('P',(64,64)); im.putpalette(sum(P,())+(0,)*(768-3*len(P))); im.putdata(out.reshape(-1).tolist())
im.save('sprite/onderlaag.png',transparency=0)
for k,c in enumerate(P): print(k,c,int((out==k).sum()))
rgb=np.array(P,np.uint8)[out]; rgb[~fg]=255
v=Image.new('RGB',(1040,512),'white')
v.paste(Image.fromarray(a.astype(np.uint8)).resize((512,512),Image.NEAREST),(0,0)); v.paste(Image.fromarray(rgb).resize((512,512),Image.NEAREST),(528,0)); v.save('sprite/onderlaag_vel.png')
# Losse misindelingen (anti-aliasrestjes) naar de blauwgrijze lijntint 2
o=np.array(Image.open('sprite/onderlaag.png'))
for (x,y) in [(15,28),(10,29),(56,12),(57,13)]: o[y,x]=2
# Bol-binnenkant: vullen vanaf het midden, gestopt door omlijning (1,2) en voetstuk (9,10)
from collections import deque
g=np.zeros_like(o,bool); q=deque([(15,45)]); g[15,45]=1
while q:
    y,x=q.popleft()
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<64 and 0<=xx<64 and not g[yy,xx] and o[yy,xx] not in (0,1,2,9,10): g[yy,xx]=1; q.append((yy,xx))
np.save('sprite/bol_mask.npy',g)
im2=Image.new('P',(64,64)); im2.putpalette(sum(P,())+(0,)*(768-3*len(P))); im2.putdata(o.reshape(-1).tolist()); im2.save('sprite/onderlaag.png',transparency=0)
print('bol px',g.sum(), 'kleuren in bol',sorted(set(o[g].tolist())))
