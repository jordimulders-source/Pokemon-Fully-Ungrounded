# Vel r18: r18 | r17 | model 8x; koeienvanger 12x (r18, r18+lijnen, r17+lijnen, model+lijnen); kop 8x r18 | r17 | toonkaart | model; 1x/2x licht/donker.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from proj import *
from kv import V,NADEN,GROEVEN
from PIL import ImageDraw, ImageFont
P18=D+'sprite_r18/sprite.png'; P17=D+'sprite_r17/sprite.png'; P14=D+'sprite_r14/sprite.png'
def bg(im,col=(255,255,255)):
    im=im.convert('RGBA'); b=Image.new('RGBA',im.size,col+(255,)); b.alpha_composite(im); return b
MODEL=Image.fromarray(N.astype(np.uint8)).convert('RGBA')
def model_sprite_box(box,DY,Z):
    nx0,ny0=s2n(box[0],box[1],DY); nx1,ny1=s2n(box[2],box[3],DY)
    W=(box[2]-box[0])*Z; H=(box[3]-box[1])*Z
    # model bilineair-vrij: elke natieve pixel als blok, exact op spritecoördinaten
    out=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(out)
    for ny in range(int(np.floor(ny0)),int(np.ceil(ny1))):
        for nx in range(int(np.floor(nx0)),int(np.ceil(nx1))):
            if not(0<=nx<99 and 0<=ny<99): continue
            X0,Y0=n2s(nx,ny,DY); X1,Y1=n2s(nx+1,ny+1,DY)
            d.rectangle(((X0-box[0])*Z,(Y0-box[1])*Z,(X1-box[0])*Z-1,(Y1-box[1])*Z-1),fill=tuple(int(v) for v in N[ny,nx]))
    return out
def lijnen(im,box,Z,DY=-1):
    d=ImageDraw.Draw(im)
    for pl,col,w in [(V,(255,0,0),3)]+[(p,(255,0,0),3) for p in NADEN.values()]+[(p,(255,160,0),2) for p in GROEVEN.values()]:
        pts=[((n2s(nx+.5,ny+.5,DY)[0]-box[0])*Z,(n2s(nx+.5,ny+.5,DY)[1]-box[1])*Z) for nx,ny in pl]
        d.line(pts,fill=col,width=w)
    return im
def z(p,Z,box=None):
    im=bg(Image.open(p))
    if box: im=im.crop(box)
    return im.resize((im.size[0]*Z,im.size[1]*Z),Image.NEAREST)
def label(im,t):
    o=Image.new('RGBA',(im.size[0],im.size[1]+16),(255,255,255,255)); o.alpha_composite(im,(0,16))
    ImageDraw.Draw(o).text((2,2),t,fill=(0,0,0)); return o
def rij(ims,gap=10,col=(255,255,255)):
    W=sum(i.size[0] for i in ims)+gap*(len(ims)-1); H=max(i.size[1] for i in ims)
    o=Image.new('RGBA',(W,H),col+(255,)); x=0
    for i in ims: o.alpha_composite(i,(x,0)); x+=i.size[0]+gap
    return o
def kolom(ims,gap=14):
    W=max(i.size[0] for i in ims); H=sum(i.size[1] for i in ims)+gap*(len(ims)-1)
    o=Image.new('RGBA',(W,H),(255,255,255,255)); y=0
    for i in ims: o.alpha_composite(i,(0,y)); y+=i.size[1]+gap
    return o
# rij 1
m8=bg(Image.open(D+'model/model.webp')).resize((512,512),Image.LANCZOS)
r1=rij([label(z(P18,8),'r18 8x'),label(z(P17,8),'r17 8x'),label(m8,'model 8x')])
# rij 2: koeienvanger 12x
KB=(0,42,28,60); Z=12
r2=rij([label(z(P18,Z,KB),'r18 koeienvanger 12x'),label(lijnen(z(P18,Z,KB),KB,Z),'r18 + modellijnen (rood: V en naden, oranje: groeven)'),
        label(lijnen(z(P17,Z,KB),KB,Z),'r17 + modellijnen'),label(lijnen(model_sprite_box(KB,-1,Z),KB,Z),'model natief (geprojecteerd) + lijnen')])
# rij 3: kop 8x
HB=(0,17,32,46); Z=8
TOON=np.load(D+'sprite_r18/toon.npy')
tk=Image.new('RGBA',(64,64),(255,255,255,255)); px=tk.load()
grijs=[(70,70,70),(125,125,125),(180,180,180),(235,235,235)]
for y in range(64):
    for x in range(64):
        if TOON[y,x]>=0: px[x,y]=grijs[TOON[y,x]]+(255,)
tk=tk.crop(HB).resize(((HB[2]-HB[0])*Z,(HB[3]-HB[1])*Z),Image.NEAREST)
r3=rij([label(z(P18,Z,HB),'r18 kop 8x'),label(z(P17,Z,HB),'r17 kop 8x'),label(tk,'toonkaart (model 50% + bol 50%), 4 tonen'),label(model_sprite_box(HB,0,Z),'model natief (geprojecteerd)')])
# rij 4: 1x en 2x, licht en donker
def klein(col):
    ims=[]
    for p in (P18,P17,P14):
        im=bg(Image.open(p),col); ims+= [im.resize((128,128),Image.NEAREST),im]
    mm=bg(Image.open(D+'model/model.webp'),col)
    ims+=[mm.resize((128,128),Image.LANCZOS),mm.resize((64,64),Image.LANCZOS)]
    return rij(ims,10,col)
r4=label(kolom([klein((255,255,255)),klein((48,48,56))],6),'2x en 1x: r18, r17, r14, model (licht en donker)')
kolom([r1,r2,r3,r4]).convert('RGB').save(D+'sprite_r18/vel.png')
