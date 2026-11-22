# vel2.py SPRITE.png UIT.png VORIGE.png [NATIEF.png PAD]: (model = natief raster, standaard gereedschap/natief.png; kop x1,3-model: model_kop/natief_kop13.png 3) sprite 8x | vorige 8x | model op schaal 8x | game-Altaria 8x / close-up kop 12x: sprite | model | game-Altaria-kop /
# 1x op wit, creme, donker, zwart + model 1x + game-Altaria 1x
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
GAME='../../../../../graphics/pokemon/altaria/anim_front.png'
def rgb_from(im,bg=(255,255,255)):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
sp=Image.open(sys.argv[1]); s=rgb_from(sp); vo=rgb_from(Image.open(sys.argv[3])); g=rgb_from(Image.open(GAME))
NAT=sys.argv[4] if len(sys.argv)>4 else NATIEF; PADN=int(sys.argv[5]) if len(sys.argv)>5 else 0
n=np.asarray(Image.open(NAT).convert('RGB')).astype(float); n=np.concatenate([np.full((PADN,n.shape[1],3),255.),n])
mm=np.full((64,64,3),255.)
for Y in range(64):
    for X in range(64):
        u=U0+3*(X-X0); v=V0+PADN+3*(Y-Y0)
        if 0<=u<n.shape[1]-2 and 0<=v<n.shape[0]-2: mm[Y,X]=n[v:v+3,u:u+3].reshape(-1,3).mean(0)
m=Image.fromarray(mm.astype('uint8'))
def mcrop(x0,y0,x1,y1,z):   # natief raster, elke natieve pixel z/3 groot (het model zelf, niet verkleind)
    u0=U0+3*(x0-X0); v0=V0+PADN+3*(y0-Y0)
    return Image.fromarray(n[v0:v0+3*(y1-y0),u0:u0+3*(x1-x0)].astype('uint8')).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
def raster(im,z):
    d=ImageDraw.Draw(im)
    for x in range(0,im.width,z): d.line([(x,0),(x,im.height)],fill=(225,225,225))
    for y in range(0,im.height,z): d.line([(0,y),(im.width,y)],fill=(225,225,225))
    return im
pan=[p.resize((512,512),Image.NEAREST) for p in (s,vo,m,g)]
z=12; x0,y0,x1,y1=18,4,52,28
kop=[raster(s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),z), mcrop(x0,y0,x1,y1,z),
     raster(g.crop((14,8,40,30)).resize((26*z,22*z),Image.NEAREST),z)]
W=max(4*520,3*(34*12+12)); H=520+kop[0].height+8+80
v=Image.new('RGB',(W,H),'white')
for i,p in enumerate(pan): v.paste(p,(i*520,0))
x=0
for p in kop: v.paste(p,(x,520)); x+=p.width+12
y=520+kop[0].height+8
for i,bg in enumerate([(255,255,255),(248,248,232),(40,48,56),(24,24,24)]): v.paste(rgb_from(sp,bg),(i*72,y))
v.paste(m,(4*72,y)); v.paste(g,(5*72,y))
v.save(sys.argv[2]); print(sys.argv[2],v.size)
