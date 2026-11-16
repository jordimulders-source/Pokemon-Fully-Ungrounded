# Vel r10: r10 | r9 | model 8x; close-ups 12x (koeienvanger extra groot 16x, schoorsteen, linkerkant kop); 1x/2x licht/donker.
import sys; from PIL import Image, ImageDraw
D='sprite_r10/'; OUT=sys.argv[1] if len(sys.argv)>1 else D+'vel.png'
def op(f,bg=(255,255,255)):
    im=Image.open(f).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
m=Image.open('model/model.webp').convert('RGB'); K=13.77
def mod(x0,y0,x1,y1,Z): # model op hetzelfde spriteraster
    X=102+x0*K; Y=71+(y0-2)*K
    return m.crop((int(X),int(Y),int(X+(x1-x0)*K),int(Y+(y1-y0)*K))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def spr(f,box,Z): return op(f).crop(box).resize(((box[2]-box[0])*Z,(box[3]-box[1])*Z),Image.NEAREST)
def raster(im,Z):
    d=ImageDraw.Draw(im)
    for i in range(0,im.size[0],Z): d.line([(i,0),(i,im.size[1])],fill=(215,215,215))
    for j in range(0,im.size[1],Z): d.line([(0,j),(im.size[0],j)],fill=(215,215,215))
    return im
rows=[]
rows.append(('r10 | r9 | model, 8x',[spr(D+'sprite.png',(0,0,64,64),8),spr('sprite_r9/sprite.png',(0,0,64,64),8),mod(0,0,64,64,8)]))
for t,b,Z in [('KOEIENVANGER 16x (x0-25, y42-61): r10 | r9 | model',(0,42,25,61),16),
              ('schoorsteen 12x (x9-26, y12-24)',(9,12,26,24),12),('linkerkant kop 12x (x0-14, y18-50)',(0,18,14,50),12)]:
    rows.append((t,[raster(spr(D+'sprite.png',b,Z),Z),raster(spr('sprite_r9/sprite.png',b,Z),Z),raster(mod(*b,Z),Z)]))
W=max(sum(i.size[0]+16 for i in r) for _,r in rows)+20; H=sum(max(i.size[1] for i in r)+30 for _,r in rows)+180
V=Image.new('RGB',(W,H),(235,235,235)); d=ImageDraw.Draw(V); y=6
for t,r in rows:
    d.text((10,y),t,fill=(0,0,0)); x=10
    for i in r: V.paste(i,(x,y+16)); x+=i.size[0]+16
    y+=max(i.size[1] for i in r)+30
x=10; d.text((10,y),'1x / 2x op licht en donker: r10 | r9',fill=(0,0,0))
for f in [D+'sprite.png','sprite_r9/sprite.png']:
    for bg in [(255,255,255),(48,48,64)]:
        s=op(f,bg); V.paste(s,(x,y+16)); V.paste(s.resize((128,128),Image.NEAREST),(x+70,y+16)); x+=220
V.save(OUT); print(V.size)
