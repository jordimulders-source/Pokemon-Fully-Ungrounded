# Alleen om de spritegrootte te kiezen: natief raster van Gemini r1 terughalen, dan kale reductie op drie hoogtes (geen sprite).
import numpy as np
from PIL import Image, ImageDraw
src=Image.open('gemini/r1.png').convert('RGB'); a=np.array(src).astype(int); g=a.sum(-1)
def fase(d,p):
    z=(d*np.exp(2j*np.pi*np.arange(len(d))/p)).sum(); return (-np.angle(z)/(2*np.pi)*p)%p
p=6.83
ox=fase(np.abs(np.diff(g,axis=1)).sum(0),p)+.5; oy=fase(np.abs(np.diff(g,axis=0)).sum(1),p)+.5
xs=np.arange(ox+p/2,1024,p).astype(int); ys=np.arange(oy+p/2,1024,p).astype(int)
nat=a[np.ix_(ys,xs)]; Image.fromarray(nat.astype('uint8')).save('maat/natief.png')
n=Image.fromarray(nat.astype('uint8')); bg=nat.min(-1)>235
yy,xx=np.where(~bg); crop=n.crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1)); W,H=crop.size
ca=np.array(crop); fg=ca[ca.min(-1)<=235]
pal=Image.fromarray(fg.reshape(1,-1,3).astype('uint8')).quantize(15,method=Image.MEDIANCUT)
cols=[]
for h in (52,58,63):
    w=round(W*h/H)
    q=crop.resize((w,h),Image.BOX).quantize(palette=pal,dither=Image.NONE).convert('RGB')
    m=np.array(crop.convert('L').point(lambda v:255 if v<235 else 0).resize((w,h),Image.BOX))>110
    qa=np.array(q); qa[~m]=255
    t=Image.new('RGB',(64,64),'white'); t.paste(Image.fromarray(qa.astype('uint8')),((64-w)//2,64-h)); cols.append((w,h,t))
S=6; vel=Image.new('RGB',(64*S*3+40+ 64*3,64*S+30),'white'); d=ImageDraw.Draw(vel)
for i,(w,h,t) in enumerate(cols):
    vel.paste(t.resize((64*S,64*S),Image.NEAREST),(i*(64*S+20),30)); d.text((i*(64*S+20)+4,8),f'{w}x{h} px (64x64-kader)',fill='black')
    vel.paste(t,(3*(64*S+20)+ 0, 30+i*70))
vel.save('maat/maten.png'); print(n.size,W,H,[(w,h) for w,h,_ in cols])
