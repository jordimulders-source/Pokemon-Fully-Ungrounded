# vel: sprite 8x | model verkleind tot dezelfde maat 8x ; kop/bek 12x naast model ; 1x op licht en donker
import sys,numpy as np; from PIL import Image, ImageDraw
F=sys.argv[1] if len(sys.argv)>1 else 'pitahaya2_r1.png'; UIT=sys.argv[2] if len(sys.argv)>2 else 'vel.png'
im=Image.open(F); im.save('_t.png',transparency=0); sp=Image.open('_t.png').convert('RGBA')
o=np.asarray(im); ys,xs=np.where(o>0); bx=(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
mod=Image.open('../model/model.png').convert('RGB'); M=np.asarray(mod).astype(int); my,mx=np.where(M.sum(2)<735)
mb=(mx.min(),my.min(),mx.max()+1,my.max()+1)
def op(bgc,img):
    b=Image.new('RGBA',img.size,bgc+(255,)); b.alpha_composite(img); return b.convert('RGB')
W=64*8; out=Image.new('RGB',(2*W+30,W+20+300+20+80),(235,235,240)); d=ImageDraw.Draw(out)
out.paste(op((215,215,225),sp.resize((W,W),Image.NEAREST)),(0,0))
mk=mod.crop(mb).resize((bx[2]-bx[0],bx[3]-bx[1]),Image.LANCZOS)
can=Image.new('RGB',(64,64),(255,255,255)); can.paste(mk,(bx[0],bx[1]))
out.paste(can.resize((W,W),Image.NEAREST),(W+30,0))
# kop/bek close-up: sprite x 2-24, y 33-56 op 12x; model zelfde uitsnede
kb=(2,33,26,57); S=12
out.paste(op((215,215,225),sp.crop(kb).resize((24*S,24*S),Image.NEAREST)).resize((300,300),Image.NEAREST),(0,W+20))
sx=(mb[2]-mb[0])/(bx[2]-bx[0]); sy=(mb[3]-mb[1])/(bx[3]-bx[1])
mc=mod.crop((int(mb[0]+(kb[0]-bx[0])*sx),int(mb[1]+(kb[1]-bx[1])*sy),int(mb[0]+(kb[2]-bx[0])*sx),int(mb[1]+(kb[3]-bx[1])*sy))).resize((300,300),Image.LANCZOS)
out.paste(mc,(310,W+20))
for k,c in enumerate([(248,248,248),(40,40,48)]):
    out.paste(op(c,sp),(650+k*80,W+20)); out.paste(op(c,sp.resize((128,128),Image.NEAREST)),(650+k*140,W+110))
out.save(UIT)
