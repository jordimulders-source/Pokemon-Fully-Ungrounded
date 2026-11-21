# vel.png: r3 A | r3 B | r1 | model (8x); diffkaarten t.o.v. r1 (geel = herkleurd, magenta = silhouet gewijzigd); 1x op licht/donker
import numpy as np; from PIL import Image, ImageDraw
def rgba(f): return Image.open(f).convert('RGBA')
def op(im,bg,z): b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
A,B,R=rgba('samba_A.png'),rgba('samba_B.png'),rgba('../sprite_r1/samba.png')
M=Image.open('../model/gemini_r6.png').convert('RGB'); M=M.crop((300,40,740,500)); M=M.resize((512,int(512*M.height/M.width)))
def diff(X):
    x,r=np.array(X),np.array(R); ax,ar=x[...,3]>0,r[...,3]>0
    o=np.where(ar[...,None],(np.array(R.convert('L'))[...,None]*.35+165).astype('uint8').repeat(3,2),255).astype('uint8')
    o[ax&ar&(x[...,:3]!=r[...,:3]).any(-1)]=(240,200,0); o[ax!=ar]=(255,0,255)
    return Image.fromarray(o).resize((512,512),Image.NEAREST)
W=4*520+10; vel=Image.new('RGB',(W,1180),(255,255,255)); d=ImageDraw.Draw(vel)
for i,(t,im) in enumerate([('r3 A (geel waar het model geel heeft)',op(A,(255,255,255),8)),('r3 B (geel om en om)',op(B,(255,255,255),8)),('r1',op(R,(255,255,255),8)),('model gemini_r6',M)]):
    vel.paste(im,(5+i*520,25)); d.text((5+i*520,8),t,fill=(0,0,0))
for i,(t,X) in enumerate([('diff A vs r1',A),('diff B vs r1',B)]):
    vel.paste(diff(X),(5+i*520,570)); d.text((5+i*520,552),t+'  geel=herkleurd  magenta=silhouet',fill=(0,0,0))
x0=5+2*520; d.text((x0,552),'1x licht / donker: A, B, r1',fill=(0,0,0))
for j,bg in enumerate([(255,255,255),(40,40,48)]):
    for i,X in enumerate([A,B,R]):
        vel.paste(op(X,bg,2),(x0+i*140,580+j*140))
        vel.paste(op(X,bg,1),(x0+440+i*70,580+j*140))
vel.save('vel.png')
