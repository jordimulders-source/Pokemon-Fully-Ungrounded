# vel.py : r2 8x | r1 8x | model verkleind 8x ; daaronder 1x licht/donker en close-ups 12x (kop/oog, dijen, voeten) r2 | r1 | model
import numpy as np; from PIL import Image, ImageDraw
r2=Image.open('harpij_r2.png').convert('RGBA'); r1=Image.open('../sprite_r1/harpij_r1.png').convert('RGBA')
a=np.asarray(Image.open('../model/model_natief.png').convert('RGB')).astype(float)
o=np.load('model_idx.npy'); A=a[3:95,24:82]; M=(o[3:95,24:82]>0).astype(float)
def wm(n,N):
    m=np.zeros((N,n)); s=n/N
    for j in range(N):
        a0,a1=j*s,(j+1)*s
        for i in range(int(a0),min(n,int(np.ceil(a1)))): m[j,i]=max(0,min(a1,i+1)-max(a0,i))
    return m
Ry,Rx=wm(92,61),wm(58,38); S=Ry@M@Rx.T
cov=S/(Ry.sum(1)[:,None]*Rx.sum(1)[None]); avg=np.einsum('yi,ijc,xj->yxc',Ry,A*M[:,:,None],Rx)/np.maximum(S,1e-6)[:,:,None]
mm=np.zeros((64,64,4),'uint8'); mm[3:64,13:51,:3]=avg.clip(0,255).astype('uint8'); mm[3:64,13:51,3]=(cov>=0.5)*255
mod=Image.fromarray(mm,'RGBA')
def op(im,bg,s):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.size[0]*s,im.size[1]*s),Image.NEAREST)
G=16; BG=(232,232,232,255)
boxes=[('kop/oog',(15,8,37,30)),('dijen',(21,43,40,52)),('voeten',(16,50,42,64))]
hs=[ (b[3]-b[1])*12 for _,b in boxes]
V=Image.new('RGB',(3*512+4*G, 512+3*G+20+sum(hs)+len(hs)*(G+14)+80),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,im) in enumerate((('r2',r2),('r1',r1),('model verkleind x0,66',mod))):
    V.paste(op(im,BG,8),(G+i*(512+G),G+14)); d.text((G+i*(512+G),2),t+' (8x)',fill=(0,0,0))
y=512+G+30
for i,bg in enumerate(((248,248,248,255),(40,44,56,255))):
    V.paste(op(r2,bg,1),(G+i*80,y)); V.paste(op(mod,bg,1),(G+180+i*80,y))
d.text((G,y-12),'1x r2 licht/donker | model',fill=(0,0,0))
y+=80
for t,b in boxes:
    d.text((G,y),t+' 12x: r2 | r1 | model',fill=(0,0,0)); y+=14; x=G
    for im in (r2,r1,mod):
        c=op(im.crop(b),BG,12); V.paste(c,(x,y)); x+=c.size[0]+G
    y+=(b[3]-b[1])*12+G
V.save('vel.png'); print(V.size)
