# lipmasker.py: lipmasker uit het model. Natieve pixel = liptint als hij in de lichtroze/zalm-cluster valt
# (helderheid 100-200, R >= 180, R-G >= 60); daarna sluiting (3x3 dilate + erode) zodat de dunne mondlijn binnen de band
# meetelt. Spritepixel (zelfde 4x4-fase) in het masker als >= 6 van zijn 16 natieve pixels in de gesloten band liggen.
# Uit: lipmasker.npy (64x64 bool) en lipmasker_overlay.png (masker als rode omtrek over r2 op 8x)
import numpy as np; from PIL import Image, ImageDraw
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); L=n@[0.299,0.587,0.114]; H,W=L.shape
def nat(x,y): return OY+4*(y-y0+ymin), OX+4*(x-x0+xmin)
ya,xa=nat(6,43); yb,xb=nat(23,53)
lip=np.zeros((H,W),bool)
R,G=n[...,0],n[...,1]
lip[ya:yb,xa:xb]=((L>=100)&(L<=200)&(R>=180)&(R-G>=60))[ya:yb,xa:xb]
def dil(b): p=np.pad(b,1); return np.max([p[dy:dy+H,dx:dx+W] for dy in range(3) for dx in range(3)],0)
def ero(b): p=np.pad(b,1,constant_values=True); return np.min([p[dy:dy+H,dx:dx+W] for dy in range(3) for dx in range(3)],0)
gl=ero(dil(lip))
s=Image.open('r2.png'); sa=np.asarray(s)
M=np.zeros((64,64),bool)
for y in range(43,53):
    for x in range(6,23):
        if not sa[y,x]: continue
        ny,nx=nat(x,y); M[y,x]=gl[ny:ny+4,nx:nx+4].sum()>=6
np.save('lipmasker.npy',M)
b=Image.new('RGBA',(64,64),(214,222,214,255)); b.alpha_composite(s.convert('RGBA'))
z=8; im=b.convert('RGB').resize((512,512),Image.NEAREST).crop((0,40*z,26*z,56*z)).resize((26*16,16*16),Image.NEAREST); d=ImageDraw.Draw(im); zz=16
for y in range(64):
    for x in range(64):
        if not M[y,x]: continue
        X,Y=(x)*zz,(y-40)*zz
        if not M[y-1,x]: d.line([(X,Y),(X+zz,Y)],fill=(0,255,255),width=2)
        if not M[y+1,x]: d.line([(X,Y+zz-1),(X+zz,Y+zz-1)],fill=(0,255,255),width=2)
        if not M[y,x-1]: d.line([(X,Y),(X,Y+zz)],fill=(0,255,255),width=2)
        if not M[y,x+1]: d.line([(X+zz-1,Y),(X+zz-1,Y+zz)],fill=(0,255,255),width=2)
im.save('lipmasker_overlay.png')
print('masker px',M.sum())
for y in range(42,54): print('%2d '%y+''.join(('M' if M[y,x] else '%x'%sa[y,x]) if sa[y,x] else '.' for x in range(6,23)), ' ',''.join('%x'%sa[y,x] if sa[y,x] else '.' for x in range(6,23)))
