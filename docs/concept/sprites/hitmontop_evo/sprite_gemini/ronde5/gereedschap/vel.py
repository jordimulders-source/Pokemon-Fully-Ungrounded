# vel.py uit.png : ronde 5. rij 1: r5 | r5 armB | r3 | model 8x; rij 2: steunarm r5|armB|r3|model 12x; rij 3: kop r5|r3|model 12x;
# rij 4: 1x en 2x op licht en donker naast hitmontop en hitmonchan
import sys,json; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap/'
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/'
P='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
def model(x0,y0,x1,y1,z):
  mo=Image.open(G+k['model']).convert('RGBA'); bg=Image.new('RGBA',mo.size,(152,208,160,255)); bg.alpha_composite(mo)
  return bg.convert('RGB').crop((int(X0+x0*s),int(Y0+y0*s),int(X0+x1*s),int(Y0+y1*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def spr(f,x0,y0,x1,y1,z,bgc=(152,208,160)):
  p=Image.open(f).convert('RGBA').crop((0,0,64,64)); b=Image.new('RGBA',p.size,bgc+(255,))
  if f.startswith(P):  # echte sprite: index 0 transparant
    q=Image.open(f); q=q.crop((0,0,64,64)); m=Image.eval(q.convert('L'),lambda v:0); a=Image.new('L',(64,64),0)
    a.putdata([0 if v==0 else 255 for v in q.getdata()]); p.putalpha(a)
  b.alpha_composite(p)
  return b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
def label(im,t):
  o=Image.new('RGB',(im.width,im.height+16),'white'); o.paste(im,(0,16)); ImageDraw.Draw(o).text((4,2),t,fill=(0,0,0)); return o
r5,b5,r3=D+'ronde5/capoeira.png',D+'ronde5/capoeira_armB.png',D+'ronde3/capoeira.png'
rows=[[label(spr(r5,0,0,64,64,8),'r5 = capoeira.png 8x'),label(spr(b5,0,0,64,64,8),'r5 armB 8x'),label(spr(r3,0,0,64,64,8),'r3 8x'),label(model(0,0,64,64,8),'model 8x')]]
A=(22,36,40,64); rows.append([label(spr(f,*A,12),n) for f,n in ((r5,'steunarm r5 12x'),(b5,'armB 12x'),(r3,'r3 12x'))]+[label(model(*A,12),'model 12x')])
K=(4,26,28,52); rows.append([label(spr(f,*K,12),n) for f,n in ((r5,'kop r5 12x'),(r3,'kop r3 12x'))]+[label(model(*K,12),'kop model 12x')])
refs=[r5,b5,r3,P+'hitmontop/anim_front.png',P+'hitmonchan/anim_front.png']
small=Image.new('RGB',(2*len(refs)*200+20,64*2+20),(255,255,255)); x=10
for bg in [(248,248,248),(40,40,48)]:
  for f in refs:
    small.paste(spr(f,0,0,64,64,1,bg),(x,10)); small.paste(spr(f,0,0,64,64,2,bg),(x+68,10)); x+=200
rows.append([label(small,'1x en 2x licht en donker: r5 | armB | r3 | hitmontop | hitmonchan')])
W=max(sum(im.width for im in r)+10*len(r) for r in rows); H=sum(max(im.height for im in r)+10 for r in rows)
o=Image.new('RGB',(W,H),'white'); y=0
for r in rows:
  x=0
  for im in r: o.paste(im,(x,y)); x+=im.width+10
  y+=max(im.height for im in r)+10
o.save(sys.argv[1])
