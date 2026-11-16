# raster.py SPRITE.png UIT.png x0 y0 x1 y1 : natief model met het spritepixelraster erover | sprite, zelfde schaal (meten, niet tekenen)
import sys,numpy as np; from PIL import Image, ImageDraw
sp=sys.argv[1]; info=np.load('kaal_info.npz')['geo']; OY,OX,ymin,xmin,y0,x0=info
X0,Y0,X1,Y1=map(int,sys.argv[3:7]); z=int(sys.argv[7]) if len(sys.argv)>7 else 12
n=Image.open('natief.png').convert('RGB')
def nat(x,y): return OX+4*(x-x0+xmin), OY+4*(y-y0+ymin)   # spritepixel -> natieve linkerbovenhoek
ax,ay=nat(X0,Y0); bx,by=nat(X1,Y1)
m=n.crop((ax,ay,bx,by)).resize(((bx-ax)*z//4*1,(by-ay)*z//4),Image.NEAREST)
d=ImageDraw.Draw(m)
for k in range(X1-X0+1): d.line([(k*z,0),(k*z,m.size[1])],fill=(0,160,255))
for k in range(Y1-Y0+1): d.line([(0,k*z),(m.size[0],k*z)],fill=(0,160,255))
s=Image.open(sp).convert('RGBA'); b=Image.new('RGBA',(64,64),(214,222,214,255)); b.alpha_composite(s)
s=b.convert('RGB').crop((X0,Y0,X1,Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST)
o=Image.new('RGB',(m.size[0]*2+10,m.size[1]),'white'); o.paste(m,(0,0)); o.paste(s,(m.size[0]+10,0)); 
d=ImageDraw.Draw(o)
for k in range(0,X1-X0,5): d.text((k*z+2,2),str(X0+k),fill='white')
for k in range(0,Y1-Y0,5): d.text((2,k*z+2),str(Y0+k),fill='white')
o.save(sys.argv[2])
