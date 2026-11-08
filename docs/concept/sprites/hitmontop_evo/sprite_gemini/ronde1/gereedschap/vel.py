# vel.py sprite.png uit.png [variant.png] : vel met model (zelfde kader, 8x) | sprite 8x [| variant 8x], close-ups kop/handen/benen (12x)
# naast elkaar met het model, en 1x op licht en donker.
import sys,json,numpy as np; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde1/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
def model(mfile,x0,y0,x1,y1,z):
  mo=Image.open(G+mfile); bg=Image.new('RGBA',mo.size,(152,208,160,255)); bg.alpha_composite(mo)
  return bg.convert('RGB').crop((int(X0+x0*s),int(Y0+y0*s),int(X0+x1*s),int(Y0+y1*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def spr(f,x0,y0,x1,y1,z,bgc=(152,208,160)):
  p=Image.open(f).convert('RGBA'); b=Image.new('RGBA',p.size,bgc+(255,)); b.alpha_composite(p)
  return b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
sp=sys.argv[1]; var=sys.argv[3] if len(sys.argv)>3 else None
from PIL import ImageDraw
def label(im,t):
  o=Image.new('RGB',(im.width,im.height+16),'white'); o.paste(im,(0,16)); ImageDraw.Draw(o).text((4,2),t,fill=(0,0,0)); return o
rows=[]
top=[label(model(k['model'],0,0,64,64,8),'model (arm 1/3 korter, zelfde kader) 8x'),label(spr(sp,0,0,64,64,8),'capoeira.png 8x (arm 1/3 korter)')]
if var: top+=[label(spr(var,0,0,64,64,8),'capoeira_kwart.png 8x (arm 1/4 korter)')]
rows.append(top)
for (x0,y0,x1,y1,t) in [(6,25,28,51,'kop'),(26,40,40,63,'steunarm, koordband, polsband, hand'),(6,26,15,38,'vuist')]:
  rows.append([label(model(k['model'],x0,y0,x1,y1,12),'model '+t+' 12x'),label(spr(sp,x0,y0,x1,y1,12),'sprite '+t+' 12x')])
rows.append([label(model(k['model'],8,1,58,28,8),'model benen 8x'),label(spr(sp,8,1,58,28,8),'sprite benen 8x')])
small=Image.new('RGB',(64*2*2+64*2+60,64*2+20),(255,255,255))
for i,b in enumerate([(248,248,248),(40,40,48)]):
  small.paste(spr(sp,0,0,64,64,1,b),(10+i*74,10)); small.paste(spr(sp,0,0,64,64,2,b),(160+i*138,10))
rows.append([label(small,'1x en 2x op licht en donker')])
W=max(sum(im.width for im in r)+10*len(r) for r in rows); H=sum(max(im.height for im in r)+10 for r in rows)
o=Image.new('RGB',(W,H),'white'); y=0
for r in rows:
  x=0
  for im in r: o.paste(im,(x,y)); x+=im.width+10
  y+=max(im.height for im in r)+10
o.save(sys.argv[2])
