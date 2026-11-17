# Hulp: spritelijnen (index 1 rood, 2/6 blauw) als kaders over het model op Z x (zelfde uitsnede); controle of lijnen op modellijnen liggen.
import sys; from PIL import Image, ImageDraw; import numpy as np
sp,info,Z,UIT=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]
X0c,Y0c,X1c,Y1c=map(int,sys.argv[5:9])
o=np.asarray(Image.open(sp)).astype(int); geo=np.load(info)['geo']
S,OX,OY,bx0,by0=geo[:5]; ymin,xmin,Y0,X0,U=[int(v) for v in geo[5:]]
P=3.998; PH=3.25
mx=lambda X: PH+P*(bx0-S+OX+S*(X-X0+xmin)); my=lambda Y: PH+P*(by0-S+OY+S*(Y-Y0+ymin))
M=Image.open('../model/model.png').convert('RGB')
B=M.crop((int(mx(X0c)),int(my(Y0c)),int(mx(X1c)),int(my(Y1c)))).resize(((X1c-X0c)*Z,(Y1c-Y0c)*Z),Image.LANCZOS)
d=ImageDraw.Draw(B)
for y in range(Y0c,Y1c):
    for x in range(X0c,X1c):
        v=o[y,x]; c={1:(255,0,0),2:(0,0,255),6:(0,160,255)}.get(v)
        if c: d.rectangle([(x-X0c)*Z+2,(y-Y0c)*Z+2,(x-X0c+1)*Z-3,(y-Y0c+1)*Z-3],outline=c,width=2)
B.save(UIT)
