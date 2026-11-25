# vel.png: kale reductie (modelkleuren) | rN | model verkleind (zelfde kader), op 8x ; 1x op licht en donker ;
# rN naast maatstaf-sprites en Stantler/Girafarig (_gba) op 1x en 3x.
import sys, json, numpy as np
from PIL import Image, ImageDraw
RN=sys.argv[1]; G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'; S='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/'
def rgba(f):
    im=Image.open(f)
    if im.mode=='P': im=im.crop((0,0,64,64)); im.info['transparency']=0
    return im.convert('RGBA').crop((0,0,64,64))
def gba(n):
    im=Image.open(G+n+'/anim_front_gba.png').crop((0,0,64,64))
    pal=[int(v) for l in open(G+n+'/normal_gba.pal').read().split('\n')[3:19] for v in l.split()]
    im.putpalette(pal); im.info['transparency']=0; return im.convert('RGBA')
sp=rgba(f'{RN}/impala_{RN}.png'); VORIG=sys.argv[2] if len(sys.argv)>2 else None
meta=json.load(open(f'{RN}/grid.json')); OX,OY=meta['OX'],meta['OY']; km=json.load(open('kaal_meta.json'))
kaal=Image.new('RGBA',(64,64)); k=Image.open('kaal.png').convert('RGBA'); kaal.paste(k,(OX,OY),k)
m0=Image.open('../referenties/model_r5.png').convert('RGB'); m=Image.new('RGB',(3072,3072),(255,255,255)); m.paste(m0,(1024,1024))
p=km['p']; bx0=km['x0']+1024-OX*p; by0=km['y0']+1024-OY*p
mod=m.crop((int(bx0),int(by0),int(bx0+64*p),int(by0+64*p))).resize((512,512),Image.LANCZOS)
PANELS=[sp]+([rgba(f'{VORIG}/impala_{VORIG}.png')] if VORIG else [])+[kaal]; NAMES=[RN]+([VORIG] if VORIG else [])+['kaal (modelkleuren)','model r5']
BG=(236,236,236,255); V=Image.new('RGBA',((len(PANELS)+1)*522+10,522+300),BG); d=ImageDraw.Draw(V)
for i,im in enumerate(PANELS):
    t=Image.new('RGBA',(64,64),(255,255,255,255)); t.paste(im,(0,0),im); V.paste(t.resize((512,512),Image.NEAREST),(10+i*522,10))
V.paste(mod,(10+len(PANELS)*522,10))
for i,s in enumerate(NAMES): d.text((14+i*522,12),s,fill=(200,0,0))
yy=532; xx=10
for bg in [(248,248,248,255),(40,40,48,255)]:
    t=Image.new('RGBA',(72,72),bg); t.paste(sp,(4,4),sp); V.paste(t,(xx,yy)); xx+=80
refs=[rgba(S+'skinguin/af/skinguin.png'),rgba(S+'dundragoon/af/dundragoon.png'),rgba(S+'viscacha/af/viscacha.png'),gba('stantler'),gba('girafarig')]
for r in refs:
    t=Image.new('RGBA',(72,72),(248,248,248,255)); t.paste(r,(4,4),r); V.paste(t,(xx,yy)); xx+=80
yy+=82; xx=10
for r in [sp]+refs[3:]+[gba('absol')]:
    t=Image.new('RGBA',(64,64),(248,248,248,255)); t.paste(r,(0,0),r); t=t.resize((192,192),Image.NEAREST); V.paste(t,(xx,yy)); xx+=200
V=V.crop((0,0,max(xx,V.width),yy+200))
# close-up kop + hoorns (sprite x OX..OX+32, y OY..OY+31) op 10x naast het model
cx0,cy0,cx1,cy1=OX-1,OY-1,OX+31,OY+31; Z=10
kop=Image.new('RGBA',((cx1-cx0),(cy1-cy0)),(255,255,255,255)); c=sp.crop((cx0,cy0,cx1,cy1)); kop.paste(c,(0,0),c); kop=kop.resize(((cx1-cx0)*Z,(cy1-cy0)*Z),Image.NEAREST)
bx=km['x0']+1024+(cx0-OX)*p; by=km['y0']+1024+(cy0-OY)*p
mk=m.crop((int(bx),int(by),int(bx+(cx1-cx0)*p),int(by+(cy1-cy0)*p))).resize(kop.size,Image.LANCZOS)
V2=Image.new('RGBA',(max(V.width,kop.width*2+30),V.height+kop.height+20),BG); V2.paste(V,(0,0)); V2.paste(kop,(10,V.height+10)); V2.paste(mk,(kop.width+20,V.height+10))
# raster 
d2=ImageDraw.Draw(V2)
for i in range(0,cx1-cx0+1,5): d2.line([(10+i*Z,V.height+10),(10+i*Z,V.height+10+kop.height)],fill=(220,220,220,255) if i%5 else (255,150,150,255))
V2.save(f'{RN}/vel.png'); print(V2.size)
