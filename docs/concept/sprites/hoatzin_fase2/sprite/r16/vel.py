# vel.png: r16 | r15 | model (8x) + 1x/2x licht/donker; onderaan 12x nek, linker poot, linker (verre) vleugel: r16 | model
import numpy as np; from PIL import Image, ImageDraw
def rgba(p):
    im=Image.open(p); a=np.asarray(im)[:64]; pal=np.array(im.getpalette()[:768]).reshape(-1,3)
    o=np.zeros(a.shape+(4,),'uint8'); o[...,:3]=pal[a]; o[...,3]=(a!=0)*255; return Image.fromarray(o,'RGBA')
s=2.8888889; x0=32; y0=8
f=lambda cx,cy:((x0+(cx-6)*s)*5.12-0.12,(y0+(cy-1)*s)*5.12-0.12)
M=Image.open('../../MODEL.png').convert('RGB')
def mcrop(b,size):
    p=f(b[0],b[1]); q=f(b[2],b[3]); return M.crop((int(p[0]),int(p[1]),int(q[0]),int(q[1]))).resize(size,Image.LANCZOS)
r16=rgba('hoatzin.png'); r15=rgba('../r15/hoatzin.png')
vel=Image.new('RGB',(40+3*552,30+512+150+30+400),(225,225,225)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate([(r16,'r16'),(r15,'r15'),(None,'model')]):
    X=40+i*552; d.text((X,10),t+' 8x',fill=(0,0,0))
    if im is None: vel.paste(mcrop((0,0,64,64),(512,512)),(X,30)); continue
    w=Image.new('RGBA',(512,512),(255,255,255,255)); w.alpha_composite(im.resize((512,512),Image.NEAREST)); vel.paste(w,(X,30))
    for j,bg in enumerate([(248,248,248),(40,40,48)]):
        w=Image.new('RGBA',(64,64),bg+(255,)); w.alpha_composite(im); vel.paste(w,(X+j*72,560))
        w2=Image.new('RGBA',(128,128),bg+(255,)); w2.alpha_composite(im.resize((128,128),Image.NEAREST)); vel.paste(w2,(X+160+j*140,560))
Y=730; X=40
for nm,b in [('nek',(16,20,34,38)),('linker poot',(12,48,30,62)),('linker vleugel',(3,0,25,14))]:
    K=12; sz=((b[2]-b[0])*K,(b[3]-b[1])*K)
    w=Image.new('RGBA',sz,(255,255,255,255)); w.alpha_composite(r16.crop(b).resize(sz,Image.NEAREST))
    vel.paste(w,(X,Y)); vel.paste(mcrop(b,sz),(X+sz[0]+6,Y)); d.text((X,Y-15),nm+' 12x: r16 | model',fill=(0,0,0))
    X+=2*sz[0]+30
vel.save('vel.png'); print(vel.size)
