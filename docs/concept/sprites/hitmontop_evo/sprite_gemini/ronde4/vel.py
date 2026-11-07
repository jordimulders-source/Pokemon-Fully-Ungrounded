# vel.py uit.png [dl] : ronde 4. r4 | r4 glansmidden | r3 | model op 8x; torso op 12x; 1x/2x licht en donker. dl = detailvel (voeten/arm)
import sys,json; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap/'
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
def model(x0,y0,x1,y1,z):
  mo=Image.open(G+k['model']).convert('RGBA'); bg=Image.new('RGBA',mo.size,(152,208,160,255)); bg.alpha_composite(mo)
  return bg.convert('RGB').crop((int(X0+x0*s),int(Y0+y0*s),int(X0+x1*s),int(Y0+y1*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def spr(f,x0,y0,x1,y1,z,bgc=(152,208,160)):
  p=Image.open(f).convert('RGBA').crop((0,0,64,64)); b=Image.new('RGBA',p.size,bgc+(255,)); b.alpha_composite(p)
  return b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
def label(im,t):
  o=Image.new('RGB',(im.width,im.height+16),'white'); o.paste(im,(0,16)); ImageDraw.Draw(o).text((4,2),t,fill=(0,0,0)); return o
r4,gm,r3=D+'ronde4/capoeira.png',D+'ronde4/capoeira_glansmidden.png',D+'ronde3/capoeira.png'
rows=[[label(spr(r4,0,0,64,64,8),'r4 = capoeira.png 8x'),label(spr(gm,0,0,64,64,8),'r4 glansmidden 8x'),label(spr(r3,0,0,64,64,8),'r3 (torso c) 8x'),label(model(0,0,64,64,8),'model 8x')]]
if len(sys.argv)>2:
  rows=[[label(spr(f,6,1,58,26,8),n) for f,n in ((r4,'benen/voeten r4 8x'),(r3,'r3 8x'))],[label(spr(f,24,40,38,56,12),n) for f,n in ((r4,'steunarm r4 12x'),(r3,'r3 12x'))]]
else:
  rows.append([label(spr(f,17,24,39,43,12),n) for f,n in ((r4,'torso r4 12x'),(gm,'torso glansmidden 12x'),(r3,'torso r3 12x'))]+[label(model(17,24,39,43,12),'torso model 12x')])
  small=Image.new('RGB',(3*(64*2+64+30)*2,64*2+20),(255,255,255)); x=10
  for bg in [(248,248,248),(40,40,48)]:
    for f in (r4,gm,r3):
      small.paste(spr(f,0,0,64,64,1,bg),(x,10)); small.paste(spr(f,0,0,64,64,2,bg),(x+70,10)); x+=210
  rows.append([label(small,'1x en 2x, licht en donker: r4 | glansmidden | r3 (twee keer: licht, donker)')])
W=max(sum(im.width for im in r)+10*len(r) for r in rows); H=sum(max(im.height for im in r)+10 for r in rows)
o=Image.new('RGB',(W,H),'white'); y=0
for r in rows:
  x=0
  for im in r: o.paste(im,(x,y)); x+=im.width+10
  y+=max(im.height for im in r)+10
o.save(sys.argv[1])
