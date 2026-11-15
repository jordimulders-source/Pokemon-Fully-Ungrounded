# maak_vel.py (vanuit kleur_r9/): abra_r9_8x.png, abra_r9_curve_8x.png, vel.png, schouder.png
import os; import numpy as np; from PIL import Image, ImageDraw
S=os.environ.get('TMPDIR','/tmp')+'/'
def rgba(p,fr=False):
    im=Image.open(p)
    if fr: im=im.crop((0,0,64,64))
    if im.mode=='P': im.save(S+'_v9.png',transparency=0); im=Image.open(S+'_v9.png')
    return im.convert('RGBA')
def op(img,kl=(255,255,255,255)):
    b=Image.new('RGBA',img.size,kl); b.alpha_composite(img); return b.convert('RGB')
R9=rgba('abra_r9.png'); RC=rgba('abra_r9_curve.png'); R8=rgba('../kleur_r8/abra_r8.png'); R8C=rgba('../kleur_r8/abra_r8_curve.png')
AB=rgba('../../../../../graphics/pokemon/abra/anim_front.png',True)
x8=lambda im:op(im).resize((512,512),Image.NEAREST)
x8(R9).save('abra_r9_8x.png'); x8(RC).save('abra_r9_curve_8x.png')
G=Image.open('../referenties/gemini_gekozen.png').convert('RGB')
mod=Image.new('RGB',(1024,1024),'white'); mod.paste(G,(0,104)); mod=mod.resize((512,512),Image.LANCZOS)  # spritepixel (x,y) = Gemini (16x,16y-104)
klein=Image.new('RGB',(512,512),(220,220,220)); dk=ImageDraw.Draw(klein)
dk.text((16,6),'1x:  r9      r9_curve    r8       Abra',fill=(0,0,0))
for r,kl in enumerate(((248,248,248,255),(40,40,48,255),(152,208,160,255))):
    for k,img in enumerate((R9,RC,R8,AB)): klein.paste(op(img,kl),(16+k*80,20+r*80))
dk.text((16,272),'2x: r9 licht | r9_curve licht | r9 donker',fill=(0,0,0))
for k,(img,kl) in enumerate(((R9,(248,248,248,255)),(RC,(248,248,248,255)),(R9,(40,40,48,255)))):
    klein.paste(op(img,kl).resize((128,128),Image.NEAREST),(16+k*164,290))
P=[(x8(R9),'r9 8x'),(x8(RC),'r9_curve 8x (variant)'),(x8(R8),'r8 8x'),(mod,'model (Gemini), zelfde schaal'),(x8(AB),'echte Abra 8x'),(klein,'1x/2x licht/donker/groen')]
v=Image.new('RGB',(3*532,2*560),'white'); d=ImageDraw.Draw(v)
for k,(x,t) in enumerate(P):
    X=(k%3)*532; Y=(k//3)*560; v.paste(x,(X,Y+40)); d.text((X+8,Y+12),t,fill=(0,0,0))
v.save('vel.png')
# ---- schouder: r8 | r9 | model, 12x, rijen r8/r9 en r8_curve/r9_curve; rode lijn op het model = r9-silhouet
Z=12; box=(32,18,50,42); x0,y0,x1,y1=box; nx,ny=x1-x0,y1-y0
def grid(c,col=(205,205,205)):
    dd=ImageDraw.Draw(c)
    for i in range(nx+1): dd.line([(i*Z,0),(i*Z,ny*Z)],fill=(150,150,255) if (x0+i)%5==0 else col)
    for j in range(ny+1): dd.line([(0,j*Z),(nx*Z,j*Z)],fill=(150,150,255) if (y0+j)%5==0 else col)
def omtrek(c,a,col=(255,0,0)):
    dd=ImageDraw.Draw(c)
    for y in range(y0,y1):
        for x in range(x0,x1):
            if not a[y,x]: continue
            X=(x-x0)*Z; Y=(y-y0)*Z
            if not a[y-1,x]: dd.line([(X,Y),(X+Z,Y)],fill=col,width=2)
            if not a[y+1,x]: dd.line([(X,Y+Z),(X+Z,Y+Z)],fill=col,width=2)
            if not a[y,x-1]: dd.line([(X,Y),(X,Y+Z)],fill=col,width=2)
            if not a[y,x+1]: dd.line([(X+Z,Y),(X+Z,Y+Z)],fill=col,width=2)
def mark(c,a,b):  # gewijzigde pixels geel omkaderd
    dd=ImageDraw.Draw(c)
    for y,x in np.argwhere(np.any(np.array(a)!=np.array(b),axis=2)[y0:y1,x0:x1]): dd.rectangle([x*Z+1,y*Z+1,x*Z+Z-2,y*Z+Z-2],outline=(255,200,0),width=2)
rows=[]
for nm,A,B in (('r8 | r9 | model',R8,R9),('r8_curve | r9_curve | model',R8C,RC)):
    ps=[]
    for im in (A,B):
        c=op(im).crop(box).resize((nx*Z,ny*Z),Image.NEAREST); grid(c); ps.append(c)
    mark(ps[1],A,B)
    m=G.crop((16*x0,16*y0-104,16*x1,16*y1-104)).resize((nx*Z,ny*Z),Image.LANCZOS); grid(m,(215,215,215))
    omtrek(m,np.array(B)[:,:,3]>0); ps.append(m); rows.append((nm,ps))
W=sum(p.width+10 for p in rows[0][1])+10; H=sum(ps[0].height+30 for _,ps in rows)+10
o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o); y=6
for nm,ps in rows:
    d.text((10,y),nm+'   (12x, x 32-49, y 18-41; blauwe lijn elke 5 px; geel = gewijzigd; rood = r9-silhouet)',fill=(0,0,0)); x=10
    for p in ps: o.paste(p,(x,y+14)); x+=p.width+10
    y+=ps[0].height+30
o.save('schouder.png')
