# stralen.py: lichte straallijnen in het model vinden. Natieve pixel = straal als hij >= 22 helderder is dan de
# mediaan van zijn 7x7-omgeving (alleen vispixels). Per spritepixel: aantal straalpixels in het 4x4-blok.
import numpy as np; from PIL import Image
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); L=n@[0.299,0.587,0.114]; H,W=L.shape
vis=n.min(2)<215
med=np.zeros_like(L)
for y in range(H):
    for x in range(W):
        if not vis[y,x]: continue
        b=L[max(0,y-3):y+4,max(0,x-3):x+4]; v=vis[max(0,y-3):y+4,max(0,x-3):x+4]; med[y,x]=np.median(b[v])
st=vis&(L-med>=22)
def telling(s):
    t=np.zeros((64,64),int)
    for y in range(64):
        for x in range(64):
            if not s[y,x]: continue
            ny=OY+4*(y-y0+ymin); nx=OX+4*(x-x0+xmin)
            if 0<=ny<H-3 and 0<=nx<W-3: t[y,x]=st[ny:ny+4,nx:nx+4].sum()
    return t
if __name__=='__main__':
    s=np.asarray(Image.open('r1.png')); t=telling(s); np.save('stralen.npy',t)
    for y in range(24,56): print('%2d '%y+''.join(('%x'%min(15,t[y,x])) if s[y,x] else '.' for x in range(6,60)))
