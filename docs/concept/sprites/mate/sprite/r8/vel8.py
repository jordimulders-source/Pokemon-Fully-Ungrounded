# vel ronde 8: r8 | r7 | model (8x, zelfde schaal); close-ups 12x van hoorns en linkerarm: r8 | r7 | model; 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mate/sprite/'
def rgba(f):
    im=Image.open(f); a=np.asarray(im); p=np.array(im.getpalette()[:768]).reshape(-1,3)
    r=np.zeros((64,64,4),'uint8'); r[...,:3]=p[a]; r[...,3]=(a>0)*255; return Image.fromarray(r)
def op(img,bg): b=Image.new('RGBA',img.size,bg); b.alpha_composite(img); return b.convert('RGB')
o=np.load(D+'r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
def tm(sx,sy): return ((NX0+(sx-fx+ox0)*s)*10.24-1.0,(NY0+(sy-top+oy0)*s)*10.24-1.0)
M=Image.open(D+'../referenties/model.png').convert('RGB'); big=Image.new('RGB',(3000,3000),'white'); big.paste(M,(1000,1000))
def mcrop(x0,y0,x1,y1,S):
    (a0,b0),(a1,b1)=tm(x0,y0),tm(x1,y1); return big.crop((int(a0)+1000,int(b0)+1000,int(a1)+1000,int(b1)+1000)).resize(((x1-x0)*S,(y1-y0)*S),Image.LANCZOS)
wit=(255,255,255,255); r8=rgba(D+'r8/mate.png'); r7=rgba(D+'r7/mate.png')
def grid(im,x0,y0,S):
    d=ImageDraw.Draw(im)
    for i in range(0,im.size[0]//S+1):
        if (x0+i)%5==0: d.line([i*S,0,i*S,im.size[1]],fill=(255,0,0))
    for j in range(0,im.size[1]//S+1):
        if (y0+j)%5==0: d.line([0,j*S,im.size[0],j*S],fill=(255,0,0))
    return im
S=8; zones=[('linkerhoorn',(14,19,26,33)),('rechterhoorn',(37,19,49,35)),('linkerarm',(9,37,21,55))]; Z=12
rows=[]
for nm,(x0,y0,x1,y1) in zones:
    w,h=(x1-x0)*Z,(y1-y0)*Z
    ims=[grid(op(r8,wit).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),x0,y0,Z),grid(op(r7,wit).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),x0,y0,Z),grid(mcrop(x0,y0,x1,y1,Z),x0,y0,Z)]
    rows.append((nm,ims))
Wd=3*(64*S+10)+150; Hd=64*S+40+sum(r[1][0].size[1]+30 for r in rows)
v=Image.new('RGB',(max(Wd,3*(rows[2][1][0].size[0]+10)+10),Hd),(235,235,235)); d=ImageDraw.Draw(v)
for k,(im,t) in enumerate(((op(r8,wit).resize((512,512),Image.NEAREST),'r8'),(op(r7,wit).resize((512,512),Image.NEAREST),'r7'),(mcrop(0,0,64,64,S),'model (zelfde schaal)'))):
    v.paste(im,(k*(64*S+10),24)); d.text((k*(64*S+10)+4,6),t,fill='black')
x=3*(64*S+10)
for j,bg in enumerate((wit,(40,40,48,255))):
    v.paste(op(r8,bg),(x,24+j*70)); v.paste(op(r7,bg),(x+70,24+j*70))
d.text((x,170),'1x: r8 | r7',fill='black')
y=64*S+40
for nm,ims in rows:
    d.text((4,y),nm+' 12x: r8 | r7 | model',fill='black')
    for k,im in enumerate(ims): v.paste(im,(k*(im.size[0]+10),y+16))
    y+=ims[0].size[1]+30
v.save(D+'r8/vel.png'); op(r8,wit).resize((512,512),Image.NEAREST).save(D+'r8/mate_8x.png')
