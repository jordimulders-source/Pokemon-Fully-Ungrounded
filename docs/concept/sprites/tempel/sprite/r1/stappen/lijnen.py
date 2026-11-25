# lijnen.py: lijnen uit het model (black-hat), skelet, per spritepixel de skeletlengte
import numpy as np
from PIL import Image, ImageFilter
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
im=Image.open(M).convert('L'); L=np.asarray(im).astype(int)
def close(k): return np.asarray(im.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MinFilter(k))).astype(int)
bh21=close(21)-L; bh7=close(7)-L
fg=L<235
lines=(bh21>28)&fg
thin=(bh7>22)&fg
def zs(img):
    img=img.copy().astype(np.uint8)
    while True:
        ch=False
        for it in (0,1):
            P=np.pad(img,1)
            n=[P[:-2,1:-1],P[:-2,2:],P[1:-1,2:],P[2:,2:],P[2:,1:-1],P[2:,:-2],P[1:-1,:-2],P[:-2,:-2]]
            B=sum(n); A=sum(((n[i]==0)&(n[(i+1)%8]==1)).astype(int) for i in range(8))
            if it==0: c1=n[0]*n[2]*n[4]; c2=n[2]*n[4]*n[6]
            else: c1=n[0]*n[2]*n[6]; c2=n[0]*n[4]*n[6]
            d=(img==1)&(B>=2)&(B<=6)&(A==1)&(c1==0)&(c2==0)
            if d.any(): img[d]=0; ch=True
        if not ch: return img.astype(bool)
sk=zs(lines)
d=np.load('red.npz'); s=float(d['s']); top=int(d['top']); left=int(d['left'])
X0,Y0=46,57
skl=np.zeros((64,64)); thk=np.zeros((64,64)); bw=np.zeros((64,64))
ys,xs=np.where(sk)
for y,x in zip(ys,xs):
    by=int((y-Y0)/s); bx=int((x-X0)/s)
    if 0<=by<60 and 0<=bx<62:
        skl[top+by,left+bx]+=1
        if not thin[y,x]: thk[top+by,left+bx]+=1
np.savez('lijn.npz',skl=skl,thk=thk)
Image.fromarray((lines*255).astype('uint8')).save('lijnen_model.png')
o=np.stack([L]*3,-1).astype('uint8'); o[lines&thin]=[0,120,255]; o[lines&~thin]=[255,0,0]; o[sk]=[255,255,0]
Image.fromarray(o).save('lijnen_over_model.png')
print(lines.sum(),sk.sum())
li=Image.fromarray((lines*255).astype('uint8'))
op=np.asarray(li.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5)))>0
# dikte per skeletpixel: dichtbij geopende (dikke) lijn?
opd=np.asarray(Image.fromarray((op*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0
skS=np.zeros((64,64)); skT=np.zeros((64,64))
for y,x in zip(ys,xs):
    by=int((y-Y0)/s); bx=int((x-X0)/s)
    if 0<=by<60 and 0<=bx<62:
        if opd[y,x]: skS[top+by,left+bx]+=1
        else: skT[top+by,left+bx]+=1
np.savez('lijn.npz',skS=skS,skT=skT)
