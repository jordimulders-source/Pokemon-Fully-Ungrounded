# zoom: sprite-uitsnede 14x met coordinaten | model zelfde uitsnede  (python3 r1/zoom.py x0 y0 x1 y1 [map] [uit])
import sys; sys.path.insert(0,'r1'); from pal import *
from PIL import ImageDraw
x0,y0,x1,y1=map(int,sys.argv[1:5]); f=sys.argv[5] if len(sys.argv)>5 else 'r1'; uit=sys.argv[6] if len(sys.argv)>6 else '/tmp/claude-0/zoom.png'
g=np.array(Image.open(f+'/anim_front.png'))[:64].astype(int)
M=Image.open('referenties/gemini_gekozen_r3.png').convert('RGB'); s=14
a=naar_img(g[y0:y1,x0:x1],s,(255,255,255)).convert('RGB')
m=M.crop((15+x0*16,15+(y0-2)*16,15+x1*16,15+(y1-2)*16)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
V=Image.new('RGB',(a.width*2+30,a.height+14),(200,200,200)); V.paste(a,(0,14)); V.paste(m,(a.width+30,14)); d=ImageDraw.Draw(V)
for i in range(x1-x0):
    d.text((i*s+2,1),str((x0+i)%10),fill=(200,0,0)); d.text((a.width+30+i*s+2,1),str((x0+i)%10),fill=(200,0,0))
for j in range(y1-y0): d.text((a.width+4,14+j*s+1),str(y0+j),fill=(0,120,0))
V.save(uit)
