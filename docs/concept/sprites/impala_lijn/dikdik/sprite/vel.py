# vel.png: sprite 8x | model verkleind (zelfde kader) 8x ; kop 12x naast model-kop ; 1x licht/donker ; naast Eevee/Vulpix _gba 1x en 4x
import sys, json, numpy as np
from PIL import Image, ImageDraw
RN=sys.argv[1]; G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
sp=Image.open(f'{RN}/dikdik_{RN}.png').convert('RGBA')
meta=json.load(open(f'{RN}/grid.json')); OX,OY=meta['OX'],meta['OY']; W=len(meta['grid'][0]); H=len(meta['grid'])
m0=Image.open('../referenties/model_r3b.png').convert('RGB'); m=Image.new('RGB',(2048,2048),(255,255,255)); m.paste(m0,(512,512)); a=np.asarray(m0).astype(int); fg=a.min(2)<225
ys,xs=np.nonzero(fg); x0,y0,y1=xs.min()+512,ys.min()+512,ys.max()+1+512; p=(y1-y0)/H
def mcrop(sx0,sy0,sx1,sy1,Z):  # spritecoordinaten (64-kader) -> modeluitsnede op schaal Z
    bx0=x0+(sx0-OX)*p; by0=y0+(sy0-OY)*p
    return m.crop((int(bx0),int(by0),int(bx0+(sx1-sx0)*p),int(by0+(sy1-sy0)*p))).resize(((sx1-sx0)*Z,(sy1-sy0)*Z),Image.LANCZOS)
def gba(n):
    im=Image.open(G+n+'/anim_front_gba.png'); pal=Image.open(G+n+'/anim_front_gba.png')
    im=im.crop((0,0,64,64)); im.info['transparency']=0; return im.convert('RGBA')
BG=(236,236,236,255); V=Image.new("RGBA",(1150,512+30+300+30+260),BG); d=ImageDraw.Draw(V)
V.paste(sp.resize((512,512),Image.NEAREST),(10,10),sp.resize((512,512),Image.NEAREST))
V.paste(mcrop(0,0,64,64,8),(10+512+20,10))
# kop 12x: kader x OX..OX+28, y OY..OY+26 (spritecoord)
kx0,ky0,kx1,ky1=OX-1,OY+8,OX+24,OY+33
kop=sp.crop((kx0,ky0,kx1,ky1)).resize(((kx1-kx0)*12,(ky1-ky0)*12),Image.NEAREST)
yy=10+512+20; V.paste(kop,(10,yy),kop); V.paste(mcrop(kx0,ky0,kx1,ky1,12),(10+kop.width+20,yy))
yy+=kop.height+20; xx=10
for bg in [(248,248,248,255),(40,40,48,255)]:
    t=Image.new('RGBA',(72,72),bg); t.paste(sp,(4,4),sp); V.paste(t,(xx,yy)); xx+=80
for n in ['eevee','vulpix']:
    r=gba(n); t=Image.new('RGBA',(72,72),(248,248,248,255)); t.paste(r,(4,4),r); V.paste(t,(xx,yy)); xx+=80
xx+=10
for im in [sp,gba('eevee'),gba('vulpix')]:
    t=Image.new('RGBA',(64,64),(248,248,248,255)); t.paste(im,(0,0),im); t=t.resize((256,256),Image.NEAREST); 
    if xx+256>V.width: break
    V.paste(t,(xx,yy)); xx+=262
V=V.crop((0,0,V.width,yy+262))
V.save(f'{RN}/vel.png'); print(V.size)
