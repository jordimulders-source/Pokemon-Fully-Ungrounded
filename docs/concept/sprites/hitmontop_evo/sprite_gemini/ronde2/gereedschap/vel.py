# vel.py r2.png r1.png uit.png : r2 | r1 | model (zelfde kader) op 8x; close-ups r2 | model op 12x (kop, steunarm, romp); 1x/2x licht en donker.
import sys,json; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde2/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
def model(x0,y0,x1,y1,z):
  mo=Image.open(G+k['model']).convert('RGBA'); bg=Image.new('RGBA',mo.size,(152,208,160,255)); bg.alpha_composite(mo)
  return bg.convert('RGB').crop((int(X0+x0*s),int(Y0+y0*s),int(X0+x1*s),int(Y0+y1*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def spr(f,x0,y0,x1,y1,z,bgc=(152,208,160)):
  p=Image.open(f).convert('RGBA'); b=Image.new('RGBA',p.size,bgc+(255,)); b.alpha_composite(p)
  return b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
def label(im,t):
  o=Image.new('RGB',(im.width,im.height+16),'white'); o.paste(im,(0,16)); ImageDraw.Draw(o).text((4,2),t,fill=(0,0,0)); return o
r2,r1=sys.argv[1],sys.argv[2]; rows=[]
rows.append([label(spr(r2,0,0,64,64,8),'ronde 2 (8x)'),label(spr(r1,0,0,64,64,8),'ronde 1 (8x)'),label(model(0,0,64,64,8),'model, arm 1/3 korter, zelfde kader (8x)')])
rows.append([label(spr(r2,5,29,28,51,12),'kop ronde 2 (12x)'),label(model(5,29,28,51,12),'kop model (12x)'),label(spr(r1,5,29,28,51,12),'kop ronde 1 (12x)')])
rows.append([label(spr(r2,18,25,38,47,12),'romp r2 (12x)'),label(model(18,25,38,47,12),'romp model (12x)'),label(spr(r2,26,40,38,63,12),'steunarm r2 (12x)'),label(model(26,40,38,63,12),'steunarm model (12x)')])
small=Image.new('RGB',(64*2*2+64*2+60,64*2+20),(255,255,255))
for i,b in enumerate([(248,248,248),(40,40,48)]):
  small.paste(spr(r2,0,0,64,64,1,b),(10+i*74,10)); small.paste(spr(r2,0,0,64,64,2,b),(160+i*138,10))
rows.append([label(small,'ronde 2 op 1x en 2x, licht en donker')])
W=max(sum(im.width for im in r)+10*len(r) for r in rows); H=sum(max(im.height for im in r)+10 for r in rows)
o=Image.new('RGB',(W,H),'white'); y=0
for r in rows:
  x=0
  for im in r: o.paste(im,(x,y)); x+=im.width+10
  y+=max(im.height for im in r)+10
o.save(sys.argv[3])
