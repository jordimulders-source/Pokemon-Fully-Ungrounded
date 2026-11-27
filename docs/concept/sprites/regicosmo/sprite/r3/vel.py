# vel.png: rij 1 r3 8x | r2 8x | model; rij 2: Saturnus 16x (r3 | r2 | natief model) naast de ijsplaneet 16x (r3);
# rij 3: 1x/2x op licht en donker + model 1x; rij 4: r3 8x naast Regiaqua af, Regirock, Registeel (gba).
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from PIL import Image; import gemeen as g, kaal as kl, vel_basis as vb
D=g.D
sp=vb.laad(os.path.join(D,'regicosmo_r3.png')); r2=vb.laad(os.path.join(D,'../r2/regicosmo_r2.png'))
mod=vb.modelvak().resize((512,512),Image.LANCZOS); BG=(255,255,255); G=16; Z=16
nat=Image.open(os.path.join(D,'natief.png')).convert('RGB')
def nmod(x0,y0,x1,y1):
    nx0=kl.X0+(x0-kl.OX)/kl.s; ny0=kl.Y0+(y0-kl.OY)/kl.s; nx1=kl.X0+(x1-kl.OX)/kl.s; ny1=kl.Y0+(y1-kl.OY)/kl.s
    return nat.resize((nat.width*8,nat.height*8),0).crop((int(nx0*8),int(ny0*8),int(nx1*8),int(ny1*8))).resize(((x1-x0)*Z,(y1-y0)*Z),0)
cut=lambda im,b:vb.op(im,BG).crop(b).resize(((b[2]-b[0])*Z,(b[3]-b[1])*Z),0)
SB=(46,22,64,38); IB=(0,22,12,38)
V=Image.new('RGB',(4*512+5*G,512+16*Z+200+512+5*G),(200,200,200))
for i,im in enumerate([vb.op(sp,BG).resize((512,512),0),vb.op(r2,BG).resize((512,512),0),mod]): V.paste(im,(G+i*(512+G),G))
y=512+2*G; x=G
for im in [cut(sp,SB),cut(r2,SB),nmod(*SB),cut(sp,IB)]: V.paste(im,(x,y)); x+=im.width+G
y+=16*Z+G; x=G
for bg in [(255,255,255),(232,240,208),(144,160,176),(40,40,56),(0,0,0)]:
    V.paste(vb.op(sp,bg),(x,y)); V.paste(vb.op(sp,bg).resize((128,128),0),(x,y+72)); x+=148
sm=mod.resize((64,64),Image.LANCZOS); V.paste(sm,(x,y)); V.paste(sm.resize((128,128),0),(x,y+72))
y+=200+G
ra=vb.op(vb.laad(os.path.join(D,'../../../regiaqua/af/regiaqua.png')),BG)
for i,im in enumerate([vb.op(sp,BG),ra,vb.gba('regirock',BG),vb.gba('registeel',BG)]): V.paste(im.resize((512,512),0),(G+i*(512+G),y))
V.save(os.path.join(D,'vel.png'))
