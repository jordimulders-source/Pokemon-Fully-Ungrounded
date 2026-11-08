# vel.py uit.png : ronde 3. Rij 1: r3 c/a/b | r2 B | model op 8x. Ogen r3 | Hitmontop | model op 12x. Torso a/b/c | model op 12x. Benen r3 | model 8x. 1x/2x.
import sys,json; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap/'
D=G+'../'; k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
def model(x0,y0,x1,y1,z):
  mo=Image.open(G+k['model']).convert('RGBA'); bg=Image.new('RGBA',mo.size,(152,208,160,255)); bg.alpha_composite(mo)
  return bg.convert('RGB').crop((int(X0+x0*s),int(Y0+y0*s),int(X0+x1*s),int(Y0+y1*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def spr(f,x0,y0,x1,y1,z,bgc=(152,208,160)):
  p=Image.open(f).convert('RGBA').crop((0,0,64,64)); b=Image.new('RGBA',p.size,bgc+(255,)); b.alpha_composite(p)
  return b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
def label(im,t):
  o=Image.new('RGB',(im.width,im.height+16),'white'); o.paste(im,(0,16)); ImageDraw.Draw(o).text((4,2),t,fill=(0,0,0)); return o
c,a,b=D+'capoeira_torso_c.png',D+'capoeira_torso_a.png',D+'capoeira_torso_b.png'; r2=D+'../ronde2/capoeira_B.png'
HT='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/hitmontop/anim_front.png'
rows=[[label(spr(c,0,0,64,64,8),'r3 = capoeira.png (torso c) 8x'),label(spr(a,0,0,64,64,8),'r3 torso a 8x'),label(spr(b,0,0,64,64,8),'r3 torso b 8x'),label(spr(r2,0,0,64,64,8),'r2 benen B 8x'),label(model(0,0,64,64,8),'model 8x')]]
rows.append([label(spr(c,11,33,27,50,12),'ogen r3 12x'),label(spr(HT,18,36,40,48,12),'Hitmontop (anim_front) 12x'),label(model(11,33,27,50,12),'ogen model 12x')])
rows.append([label(spr(a,17,24,39,43,12),'torso a 12x'),label(spr(b,17,24,39,43,12),'torso b 12x'),label(spr(c,17,24,39,43,12),'torso c 12x'),label(model(17,24,39,43,12),'torso model 12x')])
rows.append([label(spr(c,8,1,56,28,8),'benen r3 8x'),label(model(8,1,56,28,8),'benen model 8x')])
small=Image.new('RGB',(64*2*2+64*2+60,64*2+20),(255,255,255))
for i,bg in enumerate([(248,248,248),(40,40,48)]):
  small.paste(spr(c,0,0,64,64,1,bg),(10+i*74,10)); small.paste(spr(c,0,0,64,64,2,bg),(160+i*138,10))
rows.append([label(small,'r3 (torso c) op 1x en 2x, licht en donker')])
W=max(sum(im.width for im in r)+10*len(r) for r in rows); H=sum(max(im.height for im in r)+10 for r in rows)
o=Image.new('RGB',(W,H),'white'); y=0
for r in rows:
  x=0
  for im in r: o.paste(im,(x,y)); x+=im.width+10
  y+=max(im.height for im in r)+10
o.save(sys.argv[1])
