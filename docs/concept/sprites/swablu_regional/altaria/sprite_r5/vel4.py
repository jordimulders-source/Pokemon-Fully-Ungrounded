# vel4.py (r5): r5 | r4 | model op schaal | game-Altaria (8x) / close-up rechtervleugel 16x: r5 | natief model / linkervleugel 16x: r5 | natief model /
# 1x op wit, creme, donker, zwart + model + game.  python3 sprite_r5/vel4.py   (vanuit altaria/)
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import U0,V0,X0,Y0
GAME='../../../../../graphics/pokemon/altaria/anim_front.png'; PADN=3
def rgb_from(im,bg=(255,255,255)):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
sp=Image.open('sprite_r5/altaria_r5.png'); s=rgb_from(sp); vo=rgb_from(Image.open('sprite_r4/altaria_r4.png')); g=rgb_from(Image.open(GAME))
n=np.asarray(Image.open('model_kop/natief_kop15_dy10.png').convert('RGB')).astype(float); n=np.concatenate([np.full((PADN,n.shape[1],3),255.),n])
mm=np.full((64,64,3),255.)
for Y in range(64):
    for X in range(64):
        u=U0+3*(X-X0); v=V0+PADN+3*(Y-Y0)
        if 0<=u<n.shape[1]-2 and 0<=v<n.shape[0]-2: mm[Y,X]=n[v:v+3,u:u+3].reshape(-1,3).mean(0)
m=Image.fromarray(mm.astype('uint8'))
def raster(im,z):
    d=ImageDraw.Draw(im)
    for x in range(0,im.width,z): d.line([(x,0),(x,im.height)],fill=(225,225,225))
    for y in range(0,im.height,z): d.line([(0,y),(im.width,y)],fill=(225,225,225))
    return im
def paar(x0,y0,x1,y1,z=16):
    a=raster(s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),z)
    u0=U0+3*(x0-X0); v0=V0+PADN+3*(y0-Y0)
    b=Image.fromarray(n[v0:v0+3*(y1-y0),u0:u0+3*(x1-x0)].astype('uint8')).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
    return a,b
k=paar(37,13,63,35); w=paar(2,13,24,34)   # r5: rechtervleugel en linkervleugel 16x naast het natieve model
W=4*520; H=520+k[0].height+8+w[0].height+8+80
v=Image.new('RGB',(W,H),'white')
for i,p in enumerate((s,vo,m,g)): v.paste(p.resize((512,512),Image.NEAREST),(i*520,0))
y=520; v.paste(k[0],(0,y)); v.paste(k[1],(k[0].width+12,y)); y+=k[0].height+8
v.paste(w[0],(0,y)); v.paste(w[1],(w[0].width+12,y)); y+=w[0].height+8
for i,bg in enumerate([(255,255,255),(248,248,232),(40,48,56),(24,24,24)]): v.paste(rgb_from(sp,bg),(i*72,y))
v.paste(m,(4*72,y)); v.paste(g,(5*72,y))
v.save('sprite_r5/vel.png'); print('sprite_r5/vel.png',v.size)
