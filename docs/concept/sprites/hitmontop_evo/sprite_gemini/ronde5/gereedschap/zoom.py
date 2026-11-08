# zoom.py uit.png x0 y0 x1 y1 z bron... : bron = raster.txt / .png / 'model' / 'modelorig'; rooster + coordinaten
import sys,json; from PIL import Image, ImageDraw
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap')
from palet import PAL,CH
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
out,x0,y0,x1,y1,z=sys.argv[1],*map(int,sys.argv[2:7])
def model(f):
  mo=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',mo.size,(152,208,160,255)); bg.alpha_composite(mo)
  return bg.convert('RGB').crop((int(X0+x0*s),int(Y0+y0*s),int(X0+x1*s),int(Y0+y1*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def spr(f):
  if f.endswith('.txt'):
    R=[l.rstrip('\n').ljust(64,'.') for l in open(f)][:64]; im=Image.new('RGB',(64,64))
    for y in range(64):
      for x in range(64): im.putpixel((x,y),PAL[CH.index(R[y][x])])
  else:
    p=Image.open(f).convert('RGBA'); im=Image.new('RGBA',p.size,(152,208,160,255)); im.alpha_composite(p); im=im.convert('RGB')
  return im.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
ims=[]
for f in sys.argv[7:]:
  im=model(G+k['model']) if f=='model' else model('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/referenties/gemini_gekozen_capoeira.png') if f=='modelorig' else spr(f)
  d=ImageDraw.Draw(im)
  for i in range(x1-x0+1): d.line([(i*z,0),(i*z,im.height)],fill=(255,0,0) if (x0+i)%5==0 else (120,120,120),width=1)
  for j in range(y1-y0+1): d.line([(0,j*z),(im.width,j*z)],fill=(255,0,0) if (y0+j)%5==0 else (120,120,120),width=1)
  o=Image.new('RGB',(im.width+30,im.height+30),'white'); o.paste(im,(30,30)); d=ImageDraw.Draw(o)
  for i in range(x1-x0):
    if (x0+i)%2==0: d.text((30+i*z+2,4+ (i%4)*0),str(x0+i),fill=(0,0,0))
  for j in range(y1-y0): d.text((2,30+j*z+2),str(y0+j),fill=(0,0,0))
  ims.append(o)
W=sum(i.width+10 for i in ims); H=max(i.height for i in ims); o=Image.new('RGB',(W,H),'white'); x=0
for i in ims: o.paste(i,(x,0)); x+=i.width+10
o.save(out)
