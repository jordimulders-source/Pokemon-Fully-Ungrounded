# Hulp: model-uitsnede met het spriteraster en coordinaten (spritepixels X0c..X1c, Y0c..Y1c) op Z x
import sys; from PIL import Image, ImageDraw; import numpy as np
info,Z,UIT=sys.argv[1],int(sys.argv[2]),sys.argv[3]; X0c,Y0c,X1c,Y1c=map(int,sys.argv[4:8]); MOD=sys.argv[8] if len(sys.argv)>8 else '../model/model.png'
geo=np.load(info)['geo']; S,OX,OY,bx0,by0=geo[:5]; ymin,xmin,Y0,X0,U=[int(v) for v in geo[5:]]
P=3.998; PH=3.25
mx=lambda X: PH+P*(bx0-S+OX+S*(X-X0+xmin)); my=lambda Y: PH+P*(by0-S+OY+S*(Y-Y0+ymin))
M=Image.open(MOD).convert('RGB')
B=M.crop((int(mx(X0c)),int(my(Y0c)),int(mx(X1c)),int(my(Y1c)))).resize(((X1c-X0c)*Z,(Y1c-Y0c)*Z),Image.NEAREST)
out=Image.new('RGB',(B.size[0]+30,B.size[1]+30),(255,255,255)); out.paste(B,(30,30)); d=ImageDraw.Draw(out)
for i in range(X1c-X0c+1):
    d.line([(30+i*Z,30),(30+i*Z,30+B.size[1])],fill=(0,0,255) if (X0c+i)%5==0 else (150,150,255))
    if (X0c+i)%5==0: d.text((32+i*Z,8),str(X0c+i),fill=(0,0,255))
for j in range(Y1c-Y0c+1):
    d.line([(30,30+j*Z),(30+B.size[0],30+j*Z)],fill=(0,0,255) if (Y0c+j)%5==0 else (150,150,255))
    if (Y0c+j)%5==0: d.text((2,32+j*Z),str(Y0c+j),fill=(0,0,255))
out.save(UIT)
