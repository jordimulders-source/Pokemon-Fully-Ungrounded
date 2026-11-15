# Controle: rode omtrek van het spritesilhouet over het model (zelfde schaal), 10x.
import sys,numpy as np; from PIL import Image
P,PH=5.12,4.1; s=165/46; top=22; left=9; k=P*s; z=10
ox=PH+P*(18-left*s); oy=PH+P*(37-top*s)
mod=Image.open('../../referenties/model_welp_gekozen.png').convert('RGB')
pad=Image.new('RGB',(1800,1800),(255,255,255)); pad.paste(mod,(400,400))
mc=np.asarray(pad.crop((int(ox)+400,int(oy)+400,int(ox+64*k)+400,int(oy+64*k)+400)).resize((640,640),Image.LANCZOS)).copy()
rows=[l.rstrip('\n') for l in open(sys.argv[1]) if l.strip()]
m=np.array([[c!='.' for c in r] for r in rows])
p=np.pad(m,1); edge=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
for y,x in zip(*np.where(edge)):
    mc[y*z:(y+1)*z,x*z]=[255,0,0]; mc[y*z:(y+1)*z,x*z+z-1]=[255,0,0]; mc[y*z,x*z:(x+1)*z]=[255,0,0]; mc[y*z+z-1,x*z:(x+1)*z]=[255,0,0]
Image.fromarray(mc).crop((60,200,580,640)).save(sys.argv[2])
