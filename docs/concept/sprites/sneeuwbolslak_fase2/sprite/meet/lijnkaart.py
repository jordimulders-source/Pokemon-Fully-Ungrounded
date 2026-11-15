# Lijnkaart (methode poedelmot): elke donkere lijnpixel van het natieve model (81x58) op het 56-raster gezet.
# Uit: sprite/meet/lijnkaart.txt ('L' = modellijn valt in deze spritepixel) en lijnkaart_8x.png (r1 met modellijnen in rood).
import sys,numpy as np; from PIL import Image
n=np.asarray(Image.open('sprite/natief.png').convert('RGB')).astype(int)
fg=n.sum(2)<735; ys,xs=np.where(fg); y0,x0=ys.min(),xs.min(); n=n[y0:ys.max()+1,x0:xs.max()+1]
h0,w0=n.shape[:2]; k=56/w0; OX,OY=4,19
dark=n.sum(2)<260
L=np.zeros((64,64),bool)
for y,x in zip(*np.where(dark)):
    L[OY+int((y+0.5)*k),OX+int((x+0.5)*k)]=True
S=np.load('sprite/sil56_rond.npy'); L&=S
open('sprite/meet/lijnkaart.txt','w').write('\n'.join(''.join('L' if L[y,x] else ('o' if S[y,x] else '.') for x in range(64)) for y in range(64))+'\n')
R=sys.argv[1] if len(sys.argv)>1 else 'sprite/maker/r1.png'
im=np.array(Image.open(R).convert('RGBA')); bg=np.full((64,64,3),255,np.uint8); a=im[...,3:]>0
o=np.where(a,im[...,:3],bg).astype(np.uint8)
big=np.kron(o,np.ones((8,8,1),np.uint8)); m=np.kron(L,np.ones((8,8),bool))
inner=np.zeros_like(m); inner[2:-2,2:-2]=m[2:-2,2:-2]&m[:-4,2:-2]&m[4:,2:-2]&m[2:-2,:-4]&m[2:-2,4:]
big[m&~inner]=[230,0,0]
Image.fromarray(big).save('sprite/meet/lijnkaart_8x.png'); print('lijnpixels',int(L.sum()))
