# vel2.py SPRITE.png UIT.png VORIGE.png: sprite 8x | vorige 8x | model op schaal 8x | game-Altaria 8x / close-up kop 12x: sprite | model | game-Altaria-kop /
# 1x op wit, creme, donker, zwart + model 1x + game-Altaria 1x
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
GAME='../../../../../graphics/pokemon/altaria/anim_front.png'
def rgb_from(im,bg=(255,255,255)):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
sp=Image.open(sys.argv[1]); s=rgb_from(sp); vo=rgb_from(Image.open(sys.argv[3])); m=model_op_schaal(); g=rgb_from(Image.open(GAME))
M=Image.open(MODEL).convert('RGB')
def mcrop(x0,y0,x1,y1,z):
    fx=lambda u:PHX+0.5+PX*u
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    return M.crop((int(fx(u0)),int(fx(v0)),int(fx(u1)),int(fx(v1)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def raster(im,z):
    d=ImageDraw.Draw(im)
    for x in range(0,im.width,z): d.line([(x,0),(x,im.height)],fill=(225,225,225))
    for y in range(0,im.height,z): d.line([(0,y),(im.width,y)],fill=(225,225,225))
    return im
pan=[p.resize((512,512),Image.NEAREST) for p in (s,vo,m,g)]
z=12; x0,y0,x1,y1=20,8,46,30
kop=[raster(s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),z), mcrop(x0,y0,x1,y1,z),
     raster(g.crop((14,8,40,30)).resize((26*z,22*z),Image.NEAREST),z)]
W=4*520; H=520+kop[0].height+8+80
v=Image.new('RGB',(W,H),'white')
for i,p in enumerate(pan): v.paste(p,(i*520,0))
x=0
for p in kop: v.paste(p,(x,520)); x+=p.width+12
y=520+kop[0].height+8
for i,bg in enumerate([(255,255,255),(248,248,232),(40,48,56),(24,24,24)]): v.paste(rgb_from(sp,bg),(i*72,y))
v.paste(m,(4*72,y)); v.paste(g,(5*72,y))
v.save(sys.argv[2]); print(sys.argv[2],v.size)
