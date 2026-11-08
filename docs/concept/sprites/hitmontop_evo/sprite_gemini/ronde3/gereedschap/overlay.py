# overlay.py sprite.png uit.png [x0 y0 x1 y1 zoom] : model met de omlijningspixels (index 1) van de sprite als magenta stippen
# en de silhouetrand van de sprite in rood (meting).
import sys,json,numpy as np; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
mo=Image.open(G+k['model']); bg=Image.new('RGBA',mo.size,(152,208,160,255)); bg.alpha_composite(mo); bg=bg.convert('RGB')
x0,y0,x1,y1,z=map(int,sys.argv[3:8]) if len(sys.argv)>3 else (0,0,64,64,10)
c=bg.crop((int(X0+x0*s),int(Y0+y0*s),int(X0+x1*s),int(Y0+y1*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
a=np.asarray(Image.open(sys.argv[1]))
d=ImageDraw.Draw(c)
for y in range(y0,y1):
  for x in range(x0,x1):
    if a[y,x]==1: cx,cy=(x-x0)*z+z//2,(y-y0)*z+z//2; d.rectangle([cx-2,cy-2,cx+2,cy+2],fill=(255,0,255))
    elif a[y,x]==0: pass
    elif any(a[y+dy,x+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<64 and 0<=x+dx<64):
      cx,cy=(x-x0)*z+z//2,(y-y0)*z+z//2; d.rectangle([cx-2,cy-2,cx+2,cy+2],outline=(255,0,0))
for x in range((x0+4)//5*5,x1,5): d.text(((x-x0)*z+2,2),str(x),fill=(0,0,255))
for y in range((y0+4)//5*5,y1,5): d.text((2,(y-y0)*z+2),str(y),fill=(0,0,255))
c.save(sys.argv[2])
