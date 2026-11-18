# Hulp: sprite-uitsnede op Z x naast dezelfde modeluitsnede (zelfde schaal) en met het spriteraster eroverheen.
# Gebruik: python3 vergelijk.py sprite.png x0 y0 x1 y1 Z uit.png
import sys; from PIL import Image, ImageDraw; import numpy as np
sp=sys.argv[1]; x0,y0,x1,y1,Z=map(int,sys.argv[2:7]); UIT=sys.argv[7]
info=np.load(sp[:-4]+'_info.npz') if len(sys.argv)<9 else np.load(sys.argv[8])
S,OX,OY,bx0,by0,ymin,xmin,Y0,X0,U=info['geo']
im=Image.open(sp); im.save('/tmp/_v.png',transparency=0); s=Image.open('/tmp/_v.png').convert('RGBA')
bg=Image.new('RGBA',s.size,(255,255,255,255)); bg.alpha_composite(s)
A=bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
M=Image.open('../model/model.png').convert('RGB')
# spritepixel X -> natieve x = bx0-S+OX+S*(X-X0+xmin); model = natief*3.998+3.25
P=3.998; PH=3.25
def mx(X): return PH+P*(bx0-S+OX+S*(X-X0+xmin))
def my(Y): return PH+P*(by0-S+OY+S*(Y-Y0+ymin))
B=M.crop((int(mx(x0)),int(my(y0)),int(mx(x1)),int(my(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
C=B.copy(); d=ImageDraw.Draw(C)
for i in range(x1-x0+1): d.line([(i*Z,0),(i*Z,C.size[1])],fill=(0,0,255))
for j in range(y1-y0+1): d.line([(0,j*Z),(C.size[0],j*Z)],fill=(0,0,255))
out=Image.new('RGB',(A.size[0]*3+20,A.size[1]),(128,128,128)); out.paste(A.convert('RGB'),(0,0)); out.paste(B,(A.size[0]+10,0)); out.paste(C,(2*A.size[0]+20,0)); out.save(UIT)
