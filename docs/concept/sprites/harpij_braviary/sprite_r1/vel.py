# vel.py sprite.png uit.png : sprite 8x | model verkleind (vlakgemiddelde, zelfde plek) 8x | 1x en 2x op licht/donker | close-ups 12x kop/kuif en klauwen (sprite | model)
import sys, numpy as np; from PIL import Image, ImageDraw
sp=Image.open(sys.argv[1]).convert('RGBA')
a=np.asarray(Image.open('../model/model_natief.png').convert('RGB')).astype(float)
o=np.load('model_idx.npy'); A=a[3:95,24:82]; M=(o[3:95,24:82]>0).astype(float)
F=0.66; h,w=M.shape; H,W=61,38
def wm(n,N):
    m=np.zeros((N,n)); s=n/N
    for j in range(N):
        a0,a1=j*s,(j+1)*s
        for i in range(int(a0),min(n,int(np.ceil(a1)))): m[j,i]=max(0,min(a1,i+1)-max(a0,i))
    return m
Ry,Rx=wm(h,H),wm(w,W)
cov=(Ry@M@Rx.T)/(Ry.sum(1)[:,None]*Rx.sum(1)[None]); avg=np.einsum('yi,ijc,xj->yxc',Ry,A*M[:,:,None],Rx)/np.maximum(Ry@M@Rx.T,1e-6)[:,:,None]
mm=np.zeros((64,64,4),'uint8'); mm[3:64,13:51,:3]=avg.clip(0,255).astype('uint8'); mm[3:64,13:51,3]=(cov>=0.5)*255
mod=Image.fromarray(mm,'RGBA')
def op(im,bg,s):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.size[0]*s,im.size[1]*s),Image.NEAREST)
G=20; V=Image.new('RGB',(2*512+3*G+520,512+G*2+20+300),(255,255,255)); d=ImageDraw.Draw(V)
V.paste(op(sp,(232,232,232,255),8),(G,G+16)); V.paste(op(mod,(232,232,232,255),8),(2*G+512,G+16))
d.text((G,4),'sprite 8x',fill=(0,0,0)); d.text((2*G+512,4),'model verkleind (vlakgemiddelde, x0,66) 8x',fill=(0,0,0))
x=3*G+1024; d.text((x,4),'1x / 2x op licht en donker',fill=(0,0,0))
for i,bg in enumerate(((248,248,248,255),(40,44,56,255))):
    V.paste(op(sp,bg,1),(x+i*80,G+16)); V.paste(op(sp,bg,2),(x+i*140,G+100))
    V.paste(op(mod,bg,1),(x+i*80+0,G+250)); 
d.text((x,G+236),'model 1x',fill=(0,0,0))
# close-ups 12x
y0=512+2*G+20
def crop(im,box,s): return op(im.crop(box),(232,232,232,255),s)
kb=(13,3,42,27); kl=(15,49,42,64)
V.paste(crop(sp,kb,6),(G,y0)); V.paste(crop(mod,kb,6),(G+29*6+8,y0))
d.text((G,y0-14),'kop/kuif 6x: sprite | model',fill=(0,0,0))
V.paste(crop(sp,kl,6),(G+2*(29*6+8)+20,y0)); V.paste(crop(mod,kl,6),(G+3*(29*6+8)+20,y0))
d.text((G+2*(29*6+8)+20,y0-14),'klauwen 6x: sprite | model',fill=(0,0,0))
V.save(sys.argv[2]); print(V.size)
# losse close-ups op 12x
crop(sp,kb,12).save('closeup_kop_12x.png'); crop(sp,kl,12).save('closeup_klauw_12x.png')
