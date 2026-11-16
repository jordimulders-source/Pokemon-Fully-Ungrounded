# Vel r11: koeienvanger 16x r11 | r10 | model; hele sprite 8x r11 | model; 1x/2x licht/donker r11 | r10.
import sys; from PIL import Image, ImageDraw
OUT=sys.argv[1] if len(sys.argv)>1 else 'sprite_r11/vel.png'
def op(f,bg=(255,255,255)):
    im=Image.open(f).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
m=Image.open('model/model.webp').convert('RGB'); K=13.77
def mod(x0,y0,x1,y1,Z):
    X=102+x0*K; Y=71+(y0-2)*K
    return m.crop((int(X),int(Y),int(X+(x1-x0)*K),int(Y+(y1-y0)*K))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def spr(f,box,Z): return op(f).crop(box).resize(((box[2]-box[0])*Z,(box[3]-box[1])*Z),Image.NEAREST)
def raster(im,Z):
    d=ImageDraw.Draw(im)
    for i in range(0,im.size[0],Z): d.line([(i,0),(i,im.size[1])],fill=(215,215,215))
    for j in range(0,im.size[1],Z): d.line([(0,j),(im.size[0],j)],fill=(215,215,215))
    return im
b=(0,42,26,62)
rows=[('koeienvanger 16x (x0-25, y42-61): r11 | r10 | model',[raster(spr('sprite_r11/sprite.png',b,16),16),raster(spr('sprite_r10/sprite.png',b,16),16),raster(mod(*b,16),16)]),
      ('hele sprite 8x: r11 | model',[spr('sprite_r11/sprite.png',(0,0,64,64),8),mod(0,0,64,64,8)])]
W=max(sum(i.size[0]+16 for i in r) for _,r in rows)+20; H=sum(max(i.size[1] for i in r)+30 for _,r in rows)+180
V=Image.new('RGB',(W,H),(235,235,235)); d=ImageDraw.Draw(V); y=6
for t,r in rows:
    d.text((10,y),t,fill=(0,0,0)); x=10
    for i in r: V.paste(i,(x,y+16)); x+=i.size[0]+16
    y+=max(i.size[1] for i in r)+30
x=10; d.text((10,y),'1x / 2x op licht en donker: r11 | r10 | model',fill=(0,0,0))
mm=mod(0,0,64,64,2).resize((64,64),Image.BOX)
for f in ['sprite_r11/sprite.png','sprite_r10/sprite.png',None]:
    for bg in [(255,255,255),(48,48,64)]:
        s=op(f,bg) if f else mm
        V.paste(s,(x,y+16)); V.paste(s.resize((128,128),Image.NEAREST),(x+70,y+16)); x+=210
        if not f: break
V.save(OUT); print(V.size)
