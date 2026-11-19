# vel.png: r10 | r9 | model | Archeops | Braviary (8x) + 1x/2x licht en donker; onderaan kop 12x r10 | model
import numpy as np, os; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def rgba(p):
    im=Image.open(p); a=np.asarray(im)[:64]; pal=np.array(im.getpalette()[:768]).reshape(-1,3)
    o=np.zeros(a.shape+(4,),'uint8'); o[...,:3]=pal[a]; o[...,3]=(a!=0)*255; return Image.fromarray(o,'RGBA')
s=2.8888889; x0=32; y0=8
f=lambda cx,cy:((x0+(cx-6)*s)*5.12-0.12,(y0+(cy-1)*s)*5.12-0.12)
M=Image.open('../../MODEL.png').convert('RGB'); a=f(0,0); b=f(64,64)
model=M.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1]))).resize((512,512),Image.LANCZOS).convert('RGBA')
rij=[(rgba('hoatzin.png'),'r10'),(rgba('../r9/hoatzin.png'),'r9'),(None,'model'),(rgba(G+'archeops/anim_front.png'),'Archeops'),(rgba(G+'braviary/anim_front.png'),'Braviary')]
vel=Image.new('RGB',(40+5*552,512+60+170+420),(225,225,225)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(rij):
    if im is None: vel.paste(model,(40+i*552,30))
    else:
        w=Image.new('RGBA',(512,512),(255,255,255,255)); w.alpha_composite(im.resize((512,512),Image.NEAREST)); vel.paste(w,(40+i*552,30))
    d.text((40+i*552,10),t+' 8x',fill=(0,0,0))
    if im is None: continue
    for j,bg in enumerate([(248,248,248),(40,40,48)]):
        w=Image.new('RGBA',(64,64),bg+(255,)); w.alpha_composite(im); vel.paste(w,(40+i*552+j*72,580))
        w2=Image.new('RGBA',(128,128),bg+(255,)); w2.alpha_composite(im.resize((128,128),Image.NEAREST)); vel.paste(w2,(40+160+i*552+j*140,580))
# kop 12x: x 3..33, y 1..29 (30x28 px -> 360x336)
K=12; bx=(3,1,33,29)
kop=Image.new('RGBA',(360,336),(255,255,255,255)); kop.alpha_composite(rij[0][0].crop(bx).resize((360,336),Image.NEAREST))
vel.paste(kop,(40,770)); d.text((40,755),'r10 kop 12x',fill=(0,0,0))
ma=f(bx[0],bx[1]); mb=f(bx[2],bx[3])
mk=M.crop((int(ma[0]),int(ma[1]),int(mb[0]),int(mb[1]))).resize((360,336),Image.LANCZOS)
vel.paste(mk,(420,770)); d.text((420,755),'model kop',fill=(0,0,0))
k9=Image.new('RGBA',(360,336),(255,255,255,255)); k9.alpha_composite(rij[1][0].crop(bx).resize((360,336),Image.NEAREST))
vel.paste(k9,(800,770)); d.text((800,755),'r9 kop 12x',fill=(0,0,0))
vel.save('vel.png'); print(vel.size)
