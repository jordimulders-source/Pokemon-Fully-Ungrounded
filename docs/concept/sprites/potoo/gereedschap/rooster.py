# rooster.py x0 y0 x1 y1 zoom uit.png [ronde]: model-uitsnede met spritepixelrooster (rood elke 5) en, met ronde, de sprite ernaast.
import sys,json; from PIL import Image, ImageDraw
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
k=json.load(open(P+'gereedschap/kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
im=Image.open(P+'model/model_lijf_30.png'); bg=Image.new('RGBA',im.size,(64,160,64,255)); bg.alpha_composite(im); bg=bg.convert('RGB')
x0,y0,x1,y1,z=map(int,sys.argv[1:6])
def grid(c):
  d=ImageDraw.Draw(c)
  for x in range(x0,x1+1): d.line([((x-x0)*z,0),((x-x0)*z,c.size[1])],fill=(255,0,0) if x%5==0 else (255,170,170))
  for y in range(y0,y1+1): d.line([(0,(y-y0)*z),(c.size[0],(y-y0)*z)],fill=(255,0,0) if y%5==0 else (255,170,170))
  for x in range(x0,x1):
    if x%5==0: d.text(((x-x0)*z+2,2),str(x),fill=(255,0,0))
  for y in range(y0,y1):
    if y%5==0: d.text((2,(y-y0)*z+2),str(y),fill=(255,0,0))
  return c
c=grid(bg.crop((int(X0+x0*s),int(Y0+y0*s),int(X0+x1*s),int(Y0+y1*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS))
if len(sys.argv)>7:
  sp=Image.open(P+sys.argv[7]+'/potoo.png').convert('RGBA'); b=Image.new('RGBA',sp.size,(64,160,64,255)); b.alpha_composite(sp)
  q=grid(b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST))
  o=Image.new('RGB',(c.width*2+8,c.height),'white'); o.paste(c,(0,0)); o.paste(q,(c.width+8,0)); c=o
c.save(sys.argv[6])
