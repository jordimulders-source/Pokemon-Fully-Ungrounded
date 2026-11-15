# maak_vel.py (vanuit kleur_r8/): abra_r8_8x.png, abra_r8_curve_8x.png, vel.png, closeup.png
# vel: r8 8x | r8_curve 8x | r7 A 8x | model zelfde schaal | echte Abra 8x | 1x op licht/donker
# closeup: per onderdeel r7 | r8 | r8_curve | model (Gemini, 16 px per spritepixel verkleind), 12x, rode omtrek = r8_curve-silhouet
import os; import numpy as np; from PIL import Image, ImageDraw
S=os.environ.get('TMPDIR','/tmp')+'/'
def rgba(p,fr=False):
    im=Image.open(p)
    if fr: im=im.crop((0,0,64,64))
    if im.mode=='P': im.save(S+'_v8.png',transparency=0); im=Image.open(S+'_v8.png')
    return im.convert('RGBA')
def op(img,kl=(255,255,255,255)):
    b=Image.new('RGBA',img.size,kl); b.alpha_composite(img); return b.convert('RGB')
R8=rgba('abra_r8.png'); RC=rgba('abra_r8_curve.png'); R7=rgba('../kleur_r7/abra_r7_A.png')
ab=Image.open('../../../../../graphics/pokemon/abra/anim_front.png').crop((0,0,64,64)); ab.save(S+'_ab.png',transparency=0); AB=Image.open(S+'_ab.png').convert('RGBA')
x8=lambda im:op(im).resize((512,512),Image.NEAREST)
x8(R8).save('abra_r8_8x.png'); x8(RC).save('abra_r8_curve_8x.png')
G=Image.open('../referenties/gemini_gekozen.png').convert('RGB')
# spritepixel (x,y) = Gemini (16x, 16y-104)
mod=Image.new('RGB',(1024,1024),'white'); mod.paste(G.crop((0,0,1024,1024-0)),(0,104)); mod=mod.resize((512,512),Image.LANCZOS)
klein=Image.new('RGB',(512,512),(220,220,220)); dk=ImageDraw.Draw(klein)
dk.text((16,6),'1x:  r8      r8_curve    r7 A      Abra',fill=(0,0,0))
for r,kl in enumerate(((248,248,248,255),(40,40,48,255),(152,208,160,255))):
    for k,img in enumerate((R8,RC,R7,AB)): klein.paste(op(img,kl),(16+k*80,20+r*80))
dk.text((16,272),'2x: r8 licht | r8_curve licht | r8 donker',fill=(0,0,0))
for k,(img,kl) in enumerate(((R8,(248,248,248,255)),(RC,(248,248,248,255)),(R8,(40,40,48,255)))):
    klein.paste(op(img,kl).resize((128,128),Image.NEAREST),(16+k*164,290))
P=[(x8(R8),'r8 8x'),(x8(RC),'r8_curve 8x (variant)'),(x8(R7),'r7 A 8x'),(mod,'model (Gemini), zelfde schaal'),(x8(AB),'echte Abra 8x'),(klein,'1x/2x')]
v=Image.new('RGB',(3*532,2*560),'white'); d=ImageDraw.Draw(v)
for k,(x,t) in enumerate(P):
    X=(k%3)*532; Y=(k//3)*560; v.paste(x,(X,Y+40)); d.text((X+8,Y+12),t,fill=(0,0,0))
v.save('vel.png')
# ---- closeup
Z=12
def grid(c,nx,ny,col=(205,205,205)):
    dd=ImageDraw.Draw(c)
    for i in range(nx+1): dd.line([(i*Z,0),(i*Z,ny*Z)],fill=col)
    for j in range(ny+1): dd.line([(0,j*Z),(nx*Z,j*Z)],fill=col)
def omtrek(c,a,box,col=(255,0,0)):
    x0,y0,x1,y1=box; dd=ImageDraw.Draw(c)
    for y in range(y0,y1):
        for x in range(x0,x1):
            if not a[y,x]: continue
            X=(x-x0)*Z; Y=(y-y0)*Z
            if not a[y-1,x]: dd.line([(X,Y),(X+Z,Y)],fill=col,width=2)
            if y==63 or not a[y+1,x]: dd.line([(X,Y+Z),(X+Z,Y+Z)],fill=col,width=2)
            if not a[y,x-1]: dd.line([(X,Y),(X,Y+Z)],fill=col,width=2)
            if not a[y,x+1]: dd.line([(X+Z,Y),(X+Z,Y+Z)],fill=col,width=2)
DELEN=[('staart rechts',(44,45,58,64)),('lijf rechts',(36,27,48,48)),('linkerarm',(17,34,31,48)),('rechterarm',(33,33,45,48)),('kop links',(16,17,28,38))]
rows=[]
for nm,box in DELEN:
    x0,y0,x1,y1=box; nx,ny=x1-x0,y1-y0; ps=[]
    for im in (R7,R8,RC):
        c=op(im).crop(box).resize((nx*Z,ny*Z),Image.NEAREST); grid(c,nx,ny); ps.append(c)
    m=G.crop((16*x0,16*y0-104,16*x1,16*y1-104)).resize((nx*Z,ny*Z),Image.LANCZOS); grid(m,nx,ny,(215,215,215))
    omtrek(m,np.array(RC)[:,:,3]>0,box); ps.append(m); rows.append((nm,ps))
W=max(sum(p.width+10 for p in ps) for _,ps in rows)+10; H=sum(ps[0].height+34 for _,ps in rows)+10
o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o); y=6
for nm,ps in rows:
    d.text((10,y),nm+':   r7 A  |  r8  |  r8_curve (variant)  |  model (rode lijn = r8_curve-silhouet)',fill=(0,0,0)); x=10
    for p in ps: o.paste(p,(x,y+16)); x+=p.width+10
    y+=ps[0].height+34
o.save('closeup.png')
