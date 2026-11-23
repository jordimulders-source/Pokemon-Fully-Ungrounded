# vel: eind | r6 (8x), lijf 12x met tintgrenzen-overlay, 1x licht/donker, 2x, diff-kaart, Gen 3 op dezelfde schaal
import os,numpy as np; from PIL import Image,ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def rgba(p,crop64=False):
    im=Image.open(p)
    if crop64: im=im.crop((0,0,64,64))
    a=np.array(im); rgb=im.convert('RGB'); m=Image.fromarray(((a!=0)*255).astype(np.uint8))
    out=rgb.convert('RGBA'); out.putalpha(m); return out,a
E,ea=rgba(os.path.join(H,'claydol_eind.png')); R,ra=rgba(os.path.join(H,'../r6/claydol_r10kop_r6.png'))
gens=[rgba(G+n+'/anim_front_gba.png',True)[0] for n in ('claydol','regirock','golem')]
W=1600; V=Image.new('RGBA',(W,1900),(255,255,255,255)); d=ImageDraw.Draw(V)
def put(im,x,y,z,bg=None):
    im=im.resize((im.width*z,im.height*z),Image.NEAREST)
    if bg: V.paste(Image.new('RGBA',im.size,bg),(x,y))
    V.alpha_composite(im,(x,y))
d.text((10,5),'eind (8x)',fill='black'); put(E,10,20,8)
d.text((540,5),'r6 (8x)',fill='black'); put(R,540,20,8)
# 1x en 2x op licht/donker
for i,bg in enumerate([(255,255,255,255),(40,40,48,255),(120,170,120,255)]):
    put(E,1070+i*80,20,1,bg); put(R,1070+i*80,100,1,bg)
d.text((1070,5),'1x eind / r6 (licht, donker, groen)',fill='black')
put(E,1070,200,2,(232,232,232,255)); put(R,1210,200,2,(232,232,232,255)); d.text((1070,185),'2x eind | r6',fill='black')
# lijf 12x met tintgrenzen
def grenzen(a,x0,y0,z,kleur):
    for y in range(39,62):
        for x in range(12,53):
            if a[y,x]==0: continue
            if x+1<64 and a[y,x+1]!=a[y,x] and a[y,x+1]!=0: d.line([(x0+(x+1-12)*z,y0+(y-39)*z),(x0+(x+1-12)*z,y0+(y-38)*z)],fill=kleur,width=2)
            if a[y+1,x]!=a[y,x] and a[y+1,x]!=0: d.line([(x0+(x-12)*z,y0+(y+1-39)*z),(x0+(x-11)*z,y0+(y+1-39)*z)],fill=kleur,width=2)
yb=560
for j,(im,a,n) in enumerate(((E,ea,'eind'),(R,ra,'r6'))):
    x0=10+j*520; d.text((x0,yb-15),'lijf 12x + tintgrenzen ('+n+')',fill='black')
    put(im.crop((12,39,53,62)),x0,yb,12); grenzen(a,x0,yb,12,(0,160,255,255))
# diff-kaart
diff=Image.new('RGBA',(64,64),(255,255,255,255)); dp=diff.load()
for y in range(64):
    for x in range(64):
        if ea[y,x]!=ra[y,x]: dp[x,y]=(220,0,0,255)
        elif ea[y,x]: dp[x,y]=(200,200,200,255)
d.text((1070,350),'diff eind vs r6 (rood)',fill='black'); put(diff,1070,365,4)
# Gen 3 op 8x
yg=860; d.text((10,yg-15),'eind | Gen 3 Claydol | Regirock | Golem (8x)',fill='black')
put(E,10,yg,6); 
for i,g in enumerate(gens): put(g,10+(i+1)*395,yg,6)
yg2=1260; d.text((10,yg2-15),'2x: eind, claydol, regirock, golem',fill='black')
for i,g in enumerate([E]+gens): put(g,10+i*140,yg2,2,(232,232,232,255))
V=V.crop((0,0,W,1400)); V.convert('RGB').save(os.path.join(H,'vel.png'))
