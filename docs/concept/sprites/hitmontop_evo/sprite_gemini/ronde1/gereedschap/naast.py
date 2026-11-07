# naast.py sprite.png uit.png [x0 y0 x1 y1 zoom]: model (ingekort, zelfde kader) | sprite, met spritepixelrooster op beide
import sys,json; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde1/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
mo=Image.open(G+k['model']); bg=Image.new('RGBA',mo.size,(152,208,160,255)); bg.alpha_composite(mo); bg=bg.convert('RGB')
x0,y0,x1,y1,z=map(int,sys.argv[3:8]) if len(sys.argv)>3 else (0,0,64,64,8)
def grid(c,lijn):
  if not lijn: return c
  d=ImageDraw.Draw(c)
  for x in range(x0,x1+1): d.line([((x-x0)*z,0),((x-x0)*z,c.size[1])],fill=(255,0,0) if x%5==0 else (230,180,180))
  for y in range(y0,y1+1): d.line([(0,(y-y0)*z),(c.size[0],(y-y0)*z)],fill=(255,0,0) if y%5==0 else (230,180,180))
  for x in range((x0+4)//5*5,x1,5): d.text(((x-x0)*z+2,2),str(x),fill=(200,0,0))
  for y in range((y0+4)//5*5,y1,5): d.text((2,(y-y0)*z+2),str(y),fill=(200,0,0))
  return c
lijn=z>=10
m=grid(bg.crop((int(X0+x0*s),int(Y0+y0*s),int(X0+x1*s),int(Y0+y1*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS),lijn)
sp=Image.open(sys.argv[1]).convert('RGBA'); b=Image.new('RGBA',sp.size,(152,208,160,255)); b.alpha_composite(sp)
q=grid(b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),lijn)
o=Image.new('RGB',(m.width*2+8,m.height),'white'); o.paste(m,(0,0)); o.paste(q,(m.width+8,0)); o.save(sys.argv[2])
