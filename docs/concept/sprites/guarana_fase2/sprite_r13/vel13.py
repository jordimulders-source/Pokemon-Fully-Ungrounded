# voor_jordi_r13_8x.png (fase 1 | r13 | r12), afstand.png (fase 1 | r13 | r12 op 1x en 2x), closeups.png (per oog r12 | r13 op 12x)
import sys; sys.path.insert(0,'sprite_r13'); from PIL import Image, ImageDraw
from bouw13 import OGEN
def w(f):
    a=Image.open(f); a.info['transparency']=0; a=a.convert('RGBA'); B=Image.new('RGBA',a.size,(255,255,255,255)); B.alpha_composite(a); return B.convert('RGB')
F=[w('../guarana/af/guarana.png'),w('sprite_r13/guarana2_r13.png'),w('sprite_r12/guarana2_r12.png')]
T=Image.new('RGB',(3*512+32,512),'white')
for i,im in enumerate(F): T.paste(im.resize((512,512),0),(i*528,0))
T.save('sprite_r13/voor_jordi_r13_8x.png')
T=Image.new('RGB',(3*72+3*136+8,136),'white'); x=4
for s in (1,2):
    for im in F: T.paste(im.resize((64*s,64*s),0),(x,4)); x+=64*s+8
T.save('sprite_r13/afstand.png')
Z=12; rows=[]
for n,(x0,y0),Tp in OGEN:
    a0,b0,a1,b1=x0-3,y0-3,x0+len(Tp[0])+3,y0+len(Tp)+3
    a=F[2].crop((a0,b0,a1,b1)).resize(((a1-a0)*Z,(b1-b0)*Z),0); b=F[1].crop((a0,b0,a1,b1)).resize(((a1-a0)*Z,(b1-b0)*Z),0)
    r=Image.new('RGB',(a.width*2+20,a.height+16),'white'); ImageDraw.Draw(r).text((2,2),n+' (r12 | r13)',fill='black'); r.paste(a,(0,16)); r.paste(b,(a.width+20,16)); rows.append(r)
WW=max(r.width for r in rows); HH=max(r.height for r in rows); T=Image.new('RGB',(WW*2+20,((len(rows)+1)//2)*(HH+10)),'white')
for i,r in enumerate(rows): T.paste(r,((i%2)*(WW+20),(i//2)*(HH+10)))
T.save('sprite_r13/closeups.png')
