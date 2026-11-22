# vel.py SPRITE.png UIT.png [VAR1.png,VAR2.png] [kopregel]: sprite 8x | varianten 8x | model (1024) op dezelfde schaal
# geschrapt) / close-ups 12x (sprite | model): kop, hand met vinger, andere hand / 1x op wit, licht, donker naast Kricketune 1x
import sys; sys.path.insert(0,'gereedschap')
from PIL import Image, ImageDraw; import numpy as np; from gemeen import *; import schrap as S
def rgbp(path,bg=(255,255,255)):
    im=Image.open(path); o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
MOD=Image.open(MODEL).convert('RGB')
def modelcrop(x0,y0,x1,y1,size):
    # spritecoordinaten -> 1024-model (gelijke schaal 75/56 x 85/64 natief per spritepixel, pitch 10,24)
    px=lambda x:9.75+10.24*(U0+(x-X0)*75/56); py=lambda y:9.75+10.24*(V0+(y-Y0)*85/64)
    return MOD.crop((int(px(x0)),int(py(y0)),int(px(x1)),int(py(y1)))).resize(size,Image.LANCZOS)
def model_op_schaal(): return modelcrop(0,0,64,64,(64,64))
_a,_c,_L=klassen(); S.PRIO={11:4,5:4,4:4}; _s,_r,_k=S.schrap_merge(_c)
KR=[i for i in range(85) if i not in _r]; KK=[i for i in range(75) if i not in _k]
def natcrop(x0,y0,x1,y1,size):
    # precies dezelfde modelpixels als de spritepixels in het vak (natief raster, van eerste tot laatste behouden rij/kolom)
    u0=KK[max(0,x0-X0)]; u1=KK[min(len(KK)-1,x1-1-X0)]+1; v0=KR[max(0,y0-Y0)]; v1=KR[min(len(KR)-1,y1-1-Y0)]+1
    U=U0+u0; V=V0+v0; px=lambda u:int(9.75+10.24*u)
    return MOD.crop((px(U),px(V),px(U0+u1),px(V0+v1))).resize(size,Image.LANCZOS)
s=rgbp(sys.argv[1]); m=model_op_schaal()
pan=[s]+[rgbp(p) for p in sys.argv[3].split(',')] if len(sys.argv)>3 else [s]
zones=[('strik',24,20,40,30),('vest-onderrand',22,30,42,42),('buik',22,38,44,52),('antennes rechts',40,4,62,22)]
z=12; rows=[]
for n,x0,y0,x1,y1 in zones:
    A=s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); B=natcrop(x0,y0,x1,y1,A.size)
    r=Image.new('RGB',(A.width*2+8,A.height+16),'white'); r.paste(A,(0,16)); r.paste(B,(A.width+8,16))
    d=ImageDraw.Draw(r); d.text((2,2),n+' (sprite | model)',fill=(0,0,0))
    for off in (0,A.width+8):
        for x in range(0,A.width+1,z): d.line([(off+x,16),(off+x,16+A.height)],fill=(225,225,225))
        for y in range(0,A.height+1,z): d.line([(off,16+y),(off+A.width,16+y)],fill=(225,225,225))
    rows.append(r)
kt=Image.open('../../../../graphics/pokemon/kricketune/anim_front.png').convert('RGB').crop((0,0,64,64))
ktn=np.asarray(Image.open('../../../../graphics/pokemon/kricketune/anim_front.png'))[:64]
def ktbg(bg):
    i=np.asarray(kt).copy(); i[ktn==0]=bg; return Image.fromarray(i)
W=max((len(pan)+1)*520,rows[0].width+rows[1].width+16,rows[2].width+rows[3].width+16)
H=530+max(rows[0].height,rows[1].height)+8+max(rows[2].height,rows[3].height)+8+90
v=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(v)
for i,p in enumerate(pan): v.paste(p.resize((512,512),Image.NEAREST),(i*520,14))
v.paste(modelcrop(0,0,64,64,(512,512)),(len(pan)*520,14))
d.text((2,0),sys.argv[4] if len(sys.argv)>4 else 'sprite 8x | kaal 8x | model (1024) op dezelfde schaal',fill=(0,0,0))
y=532
for pr in (rows[0:2],rows[2:4]):
    x=0
    for r in pr: v.paste(r,(x,y)); x+=r.width+16
    y+=max(r.height for r in pr)+8
for i,bg in enumerate([(255,255,255),(232,232,216),(40,48,56)]):
    v.paste(rgbp(sys.argv[1],bg),(i*140,y+8)); v.paste(ktbg(bg),(i*140+68,y+8))
v.paste(m,(3*140,y+8)); d.text((2,y+76),'1x: sprite | Kricketune op wit, licht, donker; model op schaal',fill=(0,0,0))
v.save(sys.argv[2]); print(sys.argv[2],v.size)
